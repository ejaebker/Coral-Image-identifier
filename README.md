# Coral Image Identifier

A computer vision system that identifies coral species from photographs.

## 🌊 Overview
This project uses **TensorFlow** and **Keras** to build a deep learning model capable of analyzing images of coral and returning their specific classification (e.g., Acropora, Montipora, Zoanthids).

## 🛠️ Tech Stack
- **Deep Learning:** TensorFlow / Keras
- **Image Processing:** OpenCV, Pillow, ImageHash, NumPy
- **Data Collection:** BeautifulSoup, icrawler (Bing & Targeted Retailers)

## 📁 Project Structure
- `src/image_crawler.py`: Scrapes images from search engines and retailer websites.
- `src/image_processor.py`: Standardizes, deduplicates, and enhances raw data.
- `src/ML-backend.py`: Defines and trains the CNN model.
- `data/raw/`: Original scraped images.
- `data/processed/`: Cleaned, enhanced, and standardized images ready for training.

## ⚙️ Data Pipeline
The project features a robust data processing pipeline to handle the challenges of reef photography:
- **Perceptual Deduplication**: Removes visually identical images cross-class.
- **CLAHE Enhancement**: Normalizes lighting and enhances textures in LAB color space.
- **Standardization**: All images are resized to 224x224 RGB JPEGs.

For more details, see [PIPELINE.md](./PIPELINE.md) and the [Architecture Diagram](./DIAGRAM.md).

## 🚀 Getting Started
1. **Crawl Data**:
   ```bash
   python src/image_crawler.py
   ```
2. **Process Images**:
   ```bash
   python src/image_processor.py
   ```
3. **Train Model**:
   ```bash
   python src/ML-backend.py
   ```

## ✅ Current Status
- **Pipeline Complete**: Full automated scraping and processing pipeline is operational.
- **Dataset**: ~780 unique, enhanced images processed across 3 classes.
- **Model**: Basic CNN implemented and training on processed data.
- **Testing**: Unified `pytest` suite for crawlers and processors.

## 🧪 Running Tests
To run the automated test suite, ensure you have the dependencies installed and run:
```bash
pytest tests/
```
If you are using a specific environment (e.g., `tf_env`), ensure it is activated or use:
```bash
conda run -n tf_env pytest tests/
```

## 🗺️ Roadmap
- [x] Automated Image Crawling
- [x] Robust Image Processing (Deduplication & CLAHE)
- [ ] Model Optimization & Transfer Learning (MobileNetV2/ResNet)
- [ ] Export Model for Web/Mobile deployment
- [ ] Expand dataset to 10+ common reef coral classes
