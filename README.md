# Coral Image Identifier

A computer vision system that identifies coral species from photographs.

## 🌊 Overview
This project uses **TensorFlow** and **Keras** to build a deep learning model capable of analyzing images of coral and returning their specific classification (e.g., Acropora, Montipora, Zoanthids).

## 🛠️ Tech Stack
- **API Framework:** FastAPI, Uvicorn
- **Deep Learning:** TensorFlow / Keras, Keras-Tuner
- **Image Processing:** OpenCV, Pillow, ImageHash, NumPy
- **Analysis & Stats:** Scikit-Learn, Seaborn, Matplotlib
- **Data Collection:** BeautifulSoup, icrawler (Bing & Targeted Retailers)

## 📁 Project Structure
- `src/api/server.py`: FastAPI inference server with Swagger documentation.
- `src/core/processor.py`: Standardizes, deduplicates, and enhances raw data (CLAHE).
- `src/data/crawler.py`: Scrapes images from search engines and retailer websites.
- `src/data/cleaner.py`: UI for manual dataset pruning (Keep/Delete).
- `src/data/balancer.py`: Eliminates class bias via random undersampling.
- `src/training/train.py`: Optimized training with Hyperparameter Tuning and Export.
- `src/training/evaluator.py`: Modular evaluation suite (Confusion Matrix, Sample Grid).

## ⚙️ Data Pipeline
The project features a robust data processing pipeline:
- **Perceptual Deduplication**: Global cross-class duplicate removal.
- **CLAHE Enhancement**: Normalizes lighting in LAB color space.
- **Manual Pruning**: Final human-in-the-loop quality check.
- **Balancing**: Ensures equal representation across all coral classes.

## 🚀 Getting Started

### 1. Environment Setup
```bash
conda activate tf_env
pip install -r requirements.txt
```

### 2. Run the Inference API (Fastest way to test)
```bash
python src/api/server.py
```
*   **Test it**: Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser to use the interactive dashboard.

### 3. Full Data Pipeline (For retraining)
1. **Crawl & Process**:
   ```bash
   python src/data/crawler.py
   python src/core/processor.py
   ```
2. **Clean & Balance**:
   ```bash
   python src/data/cleaner.py  # Use 'k' to keep, 'd' to delete
   python src/data/balancer.py
   ```
3. **Train & Evaluate**:
   ```bash
   python src/training/train.py
   ```

## ✅ Current Status
- **V3.0 In Progress**: Modular Architecture and Inference API implemented.
- **Model**: Transfer Learning (MobileNetV2) with automated TFLite/Keras export.
- **API**: FastAPI server with CORS support and automated preprocessing.

## Roadmap
- [x] Automated Image Crawling
- [x] Robust Image Processing (Deduplication & CLAHE)
- [x] Model Optimization & Transfer Learning (MobileNetV2)
- [x] Dataset Balancing & Manual Pruning Tools
- [x] Automated Hyperparameter Tuning (Keras-Tuner)
- [x] Export Model for Web/Mobile deployment (.tflite)
- [x] Modular Project Refactor (V3.0)
- [x] FastAPI Inference Server (V3.0)
- [ ] Expand dataset to 10+ common reef coral classes
- [ ] Active Learning Feedback Loop
