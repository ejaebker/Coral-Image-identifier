# Coral Image Identifier

A computer vision system that identifies coral species from photographs.

## 🌊 Overview
This project uses **TensorFlow** and **Keras** to build a deep learning model capable of analyzing images of coral and returning their specific classification (e.g., Acropora, Montipora, Zoanthids).

## 🛠️ Tech Stack
- **Deep Learning:** TensorFlow / Keras, Keras-Tuner
- **Image Processing:** OpenCV, Pillow, ImageHash, NumPy
- **Analysis & Stats:** Scikit-Learn, Seaborn, Matplotlib
- **Data Collection:** BeautifulSoup, icrawler (Bing & Targeted Retailers)

## 📁 Project Structure
- `src/image_crawler.py`: Scrapes images from search engines and retailer websites.
- `src/image_processor.py`: Standardizes, deduplicates, and enhances raw data.
- `src/cleaner.py`: Lightweight UI for manual dataset pruning (Keep/Delete).
- `src/balancer.py`: Eliminates class bias via random undersampling.
- `src/evaluator.py`: Modular evaluation suite (Confusion Matrix, Sample Grid).
- `src/ML-backend.py`: Optimized training with Hyperparameter Tuning and Export.

## ⚙️ Data Pipeline
The project features a robust data processing pipeline:
- **Perceptual Deduplication**: Global cross-class duplicate removal.
- **CLAHE Enhancement**: Normalizes lighting in LAB color space.
- **Manual Pruning**: Final human-in-the-loop quality check (`cleaner.py`).
- **Balancing**: Ensures equal representation across all coral classes (`balancer.py`).

## 🚀 Getting Started
1. **Crawl & Process**:
   ```bash
   python src/image_crawler.py
   python src/image_processor.py
   ```
2. **Clean & Balance (V2.0)**:
   ```bash
   python src/cleaner.py  # Use 'k' to keep, 'd' to delete
   python src/balancer.py
   ```
3. **Train & Export**:
   ```bash
   python src/ML-backend.py
   ```

## ✅ Current Status
- **V2.0 Complete**: Integrated Hyperparameter Tuning, Manual Cleaning, and Dataset Balancing.
- **Model**: Transfer Learning (MobileNetV2) with automated TFLite/Keras export.
- **Evaluation**: Comprehensive suite including Confusion Matrices and Prediction Grids.

## Roadmap
- [x] Automated Image Crawling
- [x] Robust Image Processing (Deduplication & CLAHE)
- [x] Model Optimization & Transfer Learning (MobileNetV2)
- [x] Dataset Balancing & Manual Pruning Tools
- [x] Automated Hyperparameter Tuning (Keras-Tuner)
- [x] Export Model for Web/Mobile deployment (.tflite)
- [ ] Expand dataset to 10+ common reef coral classes

