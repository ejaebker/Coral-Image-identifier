import io
import os
import sys
import json
import numpy as np

# --- PATH FIX FOR DIRECT EXECUTION ---
# This allows running the script directly from the api folder or the root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import tensorflow as tf
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from src.core.processor import apply_clahe

app = FastAPI(title="Coral Image Identifier API")

# --- CONFIGURATION ---
MODEL_PATH = "models/coral_model_best.keras"
CLASSES_PATH = "models/classes.json"
CONFIG_PATH = "config.json"
IMG_SIZE = (224, 224)

# Global variables
model = None
CLASS_NAMES = []

def get_class_names():
    """Dynamically determines class names from available metadata or config."""
    # 1. Try loading from training artifact (Best way)
    if os.path.exists(CLASSES_PATH):
        with open(CLASSES_PATH, "r") as f:
            return json.load(f)
    
    # 2. Fallback to config.json
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
            return sorted(config.get("coral_classes", {}).keys())
    
    # 3. Last resort default
    return ["acropora", "frogspawn", "montipora", "zoanthid"]

# Enable CORS for future frontend integration (e.g., React Flow)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    global model, CLASS_NAMES
    
    # Load class names
    CLASS_NAMES = get_class_names()
    print(f"Loaded {len(CLASS_NAMES)} classes: {CLASS_NAMES}")
    
    # Load model
    if not os.path.exists(MODEL_PATH):
        print(f"WARNING: Model not found at {MODEL_PATH}. Prediction endpoint will fail.")
        return
    
    print(f"Loading model from {MODEL_PATH}...")
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully.")

@app.get("/")
async def root():
    return {"message": "Coral Image Identifier API is running", "classes": CLASS_NAMES}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File uploaded is not an image.")

    try:
        # 1. Read and open image
        contents = await file.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")

        # 2. Preprocess (matching training pipeline)
        # Apply CLAHE
        img = apply_clahe(img)
        
        # Resize
        img = img.resize(IMG_SIZE, Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Add batch dimension (1, 224, 224, 3)
        img_array = np.expand_dims(img_array, axis=0)

        # 3. Inference
        if model is None:
            raise HTTPException(status_code=500, detail="Model is not loaded.")
        
        predictions = model.predict(img_array)
        
        # Since the model ends with a Dense layer (logits), we apply softmax manually for confidence
        # or check if from_logits was used in the loss.
        # Based on ML-backend.py: loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        # So we apply softmax to get probabilities.
        probabilities = tf.nn.softmax(predictions[0]).numpy()
        
        predicted_class_idx = np.argmax(probabilities)
        confidence = float(probabilities[predicted_class_idx])
        predicted_class = CLASS_NAMES[predicted_class_idx]

        return {
            "filename": file.filename,
            "prediction": predicted_class,
            "confidence": round(confidence, 4),
            "all_scores": {CLASS_NAMES[i]: round(float(probabilities[i]), 4) for i in range(len(CLASS_NAMES))}
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
