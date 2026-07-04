import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
import os

def evaluate_model(model, history, val_ds, class_names, output_dir="models/evaluation"):
    """
    Performs comprehensive evaluation of the trained model and saves results to output_dir.
    """
    print("\n" + "="*50)
    print(f"STARTING MODEL EVALUATION (Saving to {output_dir})")
    print("="*50)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # 1. Plot Training History (Accuracy and Loss)
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs_range = range(len(acc))

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.tight_layout()
    
    history_path = os.path.join(output_dir, "training_history.png")
    plt.savefig(history_path)
    print(f"Saved training history plot to {history_path}")
    plt.close()

    # 2. Extract True Labels and Predictions
    print("\nGenerating predictions for validation set...")
    y_true = []
    y_pred = []
    
    # We'll also keep some images for the sample grid
    sample_images = []
    sample_labels = []
    sample_preds = []

    for images, labels in val_ds:
        preds = model.predict(images, verbose=0)
        y_true.extend(labels.numpy())
        y_pred.extend(np.argmax(preds, axis=1))
        
        # Capture first batch for visual sample
        if len(sample_images) == 0:
            sample_images = images.numpy()
            sample_labels = labels.numpy()
            sample_preds = np.argmax(preds, axis=1)

    # 3. Print and Save Classification Report
    report = classification_report(y_true, y_pred, target_names=class_names)
    print("\nClassification Report:")
    print(report)
    
    report_path = os.path.join(output_dir, "classification_report.txt")
    with open(report_path, "w") as f:
        f.write(report)
    print(f"Saved classification report to {report_path}")

    # 4. Plot Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    
    cm_path = os.path.join(output_dir, "confusion_matrix.png")
    plt.savefig(cm_path)
    print(f"Saved confusion matrix plot to {cm_path}")
    plt.close()

    # 5. Plot Sample Predictions Grid (3x3)
    plt.figure(figsize=(10, 10))
    for i in range(min(9, len(sample_images))):
        plt.subplot(3, 3, i + 1)
        # Standardize image for display (dataset provides 0-255)
        img = sample_images[i].astype("uint8")
        
        plt.imshow(img)
        
        actual_name = class_names[sample_labels[i]]
        pred_name = class_names[sample_preds[i]]
        
        color = 'green' if sample_labels[i] == sample_preds[i] else 'red'
        plt.title(f"Act: {actual_name}\nPred: {pred_name}", color=color, fontsize=10)
        plt.axis("off")
    
    plt.suptitle("Sample Predictions (Validation Set)", fontsize=16)
    plt.tight_layout()
    
    samples_path = os.path.join(output_dir, "sample_predictions.png")
    plt.savefig(samples_path)
    print(f"Saved sample predictions plot to {samples_path}")
    plt.close()

    print("\n" + "="*50)
    print("EVALUATION COMPLETE")
    print("="*50)

if __name__ == "__main__":
    import sys
    # Path setup for direct script execution
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    from src.training.train import load_data

    model_path = "models/coral_model_best.keras"
    eval_dir = "models/evaluation"

    if not os.path.exists(model_path):
        print(f"Error: Trained model not found at '{model_path}'. Please run training first.")
        sys.exit(1)

    print(f"Loading model from {model_path}...")
    model = tf.keras.models.load_model(model_path)

    print("Loading dataset...")
    _, validate_ds, class_names, num_classes, _ = load_data()

    # Create a mock history object
    class MockHistory:
        def __init__(self):
            self.history = {
                'accuracy': [0.78],
                'val_accuracy': [0.78],
                'loss': [0.5],
                'val_loss': [0.5]
            }

    history = MockHistory()
    evaluate_model(model, history, validate_ds, class_names, output_dir=eval_dir)
