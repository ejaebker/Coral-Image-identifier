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
# Python Environment (Backend)
pip install -r requirements.txt

# Node Environment (Frontend)
cd frontend
npm install
```

### 2. Start the Application (Complete Stack)
To run the full "CoralID" platform, you need to start both the inference engine and the dashboard.

**Terminal 1: FastAPI Inference Server**
```bash
python src/api/server.py
```

**Terminal 2: React Editorial Dashboard**
```bash
cd frontend
npm run dev
```

### 3. Usage
- **Web UI**: Open [http://localhost:5173/](http://localhost:5173/) to identify specimens.
- **API Docs**: Visit [http://localhost:8000/docs](http://localhost:8000/docs) for technical telemetry.

---

## 🌐 Web Dashboard (CoralID)
The **CoralID** dashboard (v4.0) is a high-fidelity "Scientific Editorial" interface designed for biological research.

### ✨ Key Features
- **Neural Ingestor**: An advanced HUD-style upload zone with technical telemetry and real-time scan-line visualization.
- **Research Archives**: Automatic local persistence of taxonomic runs. Every identification is saved to your browser's history with confidence scores and timestamps.
- **Validation Pipeline**: A static infographic visualizing the 4-stage neural validation process (Preprocessing, Extraction, Analysis, Result).
- **Editorial Foundations**: Designed with **OKLCH colors**, **fluid typography** (Manrope/Inter/JetBrains Mono), and a tactile **editorial grain** texture.

---

## ✅ Current Status
- **V5.0 Released**: Fine-tuned EfficientNetV2-B0 model integrated, achieving **81% validation accuracy** (up from 69% on MobileNetV2).
- **Data Ingestion**: Integrated open iNaturalist observations API to download scientific community-verified coral specimens.
- **Model**: Two-stage training pipeline (Stage 1 classification head warmup + Stage 2 top-layer fine-tuning).
- **API & UI**: FastAPI inference server with live reload, serving predictions to the Vite dashboard.

## Roadmap
- [x] Automated Image Crawling
- [x] Robust Image Processing (Deduplication & CLAHE)
- [x] Model Optimization & Transfer Learning (EfficientNetV2-B0)
- [x] Dataset Balancing & Manual Pruning Tools
- [x] Automated Hyperparameter Tuning (Keras-Tuner)
- [x] Export Model for Web/Mobile deployment (.tflite)
- [x] Modular Project Refactor (V3.0)
- [x] FastAPI Inference Server (V3.0)
- [x] Scientific Editorial Dashboard (V4.0)
- [x] Local Storage Research Archives (V4.0)
- [x] Integrate iNaturalist API for research-grade observations (V5.0)
- [x] Two-Stage Backbone Fine-Tuning (V5.0)
- [ ] Expand dataset to 20+ common reef coral classes
- [ ] Active Learning Feedback Loop (User-corrected labels)
- [ ] PRAW Reddit API Scraper activation (Requires client credentials)

## 📡 Future Data Acquisition
To improve model accuracy and taxonomic breadth, we are shifting focus towards high-quality, verified data sources. This includes hobbyist-driven data (Reddit), citizen science (iNaturalist), and professional photography (Flickr). Detailed implementation specs can be found in `proposed_changes.txt`.
