import io
import os
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from src.core.processor import apply_clahe

app = FastAPI(title="Coral Image Identifier API")

# --- CONFIGURATION ---
MODEL_PATH = "models/coral_model_best.keras"
CLASS_NAMES = ["acropora", "frogspawn", "montipora", "zoanthid"]
IMG_SIZE = (224, 224)

# Enable CORS for future frontend integration (e.g., React Flow)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variable
model = None

@app.on_event("startup")
async def load_model():
    global model
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Please train the model first.")
    
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
