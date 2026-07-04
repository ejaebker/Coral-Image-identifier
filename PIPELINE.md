# Coral Image Processing Pipeline

This document details the architecture and logic of the image processing pipeline used to prepare scraped coral data for machine learning.

## 🚀 Overview
The pipeline transforms raw, heterogeneous web-scraped images into a standardized, high-quality dataset optimized for Convolutional Neural Networks (CNNs). It is located in `src/core/processor.py`.

---

## 🛠️ Pipeline Stages

### 1. Integrity Validation
*   **Action**: Attempts to load the file using the Pillow (PIL) library.
*   **Purpose**: Filters out corrupted files, partial downloads, or unsupported formats.
*   **Result**: Only valid image files proceed.

### 2. Perceptual Deduplication (Cross-Class)
*   **Action**: Generates a 64-bit perceptual hash (pHash) using the `imagehash` library.
*   **Purpose**: Identifies visually identical images even if they have different filenames, resolutions, or compression levels.
*   **Scope**: Deduplication is **Global**. If an image exists in 'acropora' and is found again in 'zoanthid', the second instance is discarded to prevent data leakage and label confusion.

### 3. LAB-Space CLAHE Enhancement
*   **Action**: 
    1. Converts image from RGB to LAB color space.
    2. Applies Contrast Limited Adaptive Histogram Equalization (CLAHE) to the **L (Lightness)** channel.
    3. Merges channels back and converts to RGB.
*   **Purpose**: Normalizes lighting and enhances textural details. This is critical for reef photography, which often suffers from heavy blue-spectrum lighting and uneven exposure. It "pops" the coral features without distorting the actual species' colors.

### 4. Geometric Standardization
*   **Action**: Resizes images to exactly **224x224 pixels** using **LANCZOS** resampling.
*   **Purpose**: Standardizes the input dimensions for the TensorFlow model, ensuring consistent tensor shapes and high-quality downsampling.

### 5. Format Standardization
*   **Action**: Converts all images to RGB and saves them as high-quality JPEGs.
*   **Purpose**: Removes alpha channels (transparency) and ensures a uniform file format for the training data generator.

### 6. Manual Pruning (Human-in-the-loop)
*   **Action**: User utilizes `src/data/cleaner.py` to manually verify scraped images.
*   **Purpose**: Removes "noise" from web-scraping (e.g., equipment, non-target species) that automated filters might miss.

### 7. Class Weighting (Mathematical Balancing)
*   **Action**: `src/training/train.py` calculates distribution weights for each class using `sklearn`.
*   **Purpose**: Instead of deleting images to balance the dataset, we "penalize" the model more for misclassifying minority classes. This allows the model to learn from the **entire** dataset without bias.

### 8. Hyperparameter Tuning
*   **Action**: `src/training/train.py` uses **Keras Tuner** (Hyperband) to optimize the learning rate and dropout rate for the EfficientNetV2 dense classification head.
*   **Purpose**: Scientifically determines the best initial classification head configuration for the dataset.

### 9. Two-Stage Fine-Tuning
*   **Action**: Unfreezes the top convolutional layers of the **EfficientNetV2-B0** base model (from layer index 200 to 270) and trains with a very low learning rate (`1e-5`) for another 10 epochs.
*   **Purpose**: Specializes the high-level convolutional feature detectors on fine coral skeleton structures and polyp patterns instead of general ImageNet features.

### 10. Comprehensive Evaluation
*   **Action**: `src/training/evaluator.py` generates metrics after training.
*   **Result**: Produces a Confusion Matrix, Classification Report (Precision/Recall), and a visual grid of sample predictions to verify model reliability.

---

## 📂 Data Flow
*   **Input**: `data/raw/<class_name>/`
*   **Intermediate**: `data/processed/<class_name>/`
*   **Final Training Set**: `data/processed/` (with mathematical weighting)

## ⚙️ Configuration
*   **Base Network**: EfficientNetV2-B0 (with built-in normalization, no rescaling layer needed)
*   **Image Size**: 224x224
*   **CLAHE Clip Limit**: 2.0
*   **CLAHE Tile Grid**: 8x8
*   **Export Quality**: 95% JPEG
*   **Optimizers**: Adam (Initial: Tuned, Fine-Tuning: 1e-5)
