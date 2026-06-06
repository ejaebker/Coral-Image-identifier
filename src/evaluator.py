import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf

def evaluate_model(model, history, val_ds, class_names):
    """
    Performs comprehensive evaluation of the trained model.
    """
    print("\n" + "="*50)
    print("STARTING MODEL EVALUATION")
    print("="*50)

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
    plt.show()

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

    # 3. Print Classification Report
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=class_names))

    # 4. Plot Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.show()

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
    plt.show()

    print("\n" + "="*50)
    print("EVALUATION COMPLETE")
    print("="*50)
