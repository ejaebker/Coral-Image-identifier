# Coral Image Identifier

A computer vision system that identifies coral species from photographs.

## Overview
This project uses **TensorFlow** and **Keras** to build a deep learning model capable of analyzing images of coral and returning their specific classification (e.g., Acropora, Frogspawn, Zoanthids).

## Tech Stack
- **Backend:** TensorFlow / Keras
- **Language:** Python
- **Image Processing:** PIL (Pillow), NumPy

## Current Status
- **Initial Backend:** A basic Convolutional Neural Network (CNN) has been implemented in `src/ML-backend.py` using TensorFlow.
- **Dataset:** Approximately 580 images have been scraped across three classes: Acropora, Montipora, and Zoanthids.
- **Issue Identified:** Discovered that some scraped images are corrupted or in incompatible formats, causing training to fail during the first epoch.

## Planned Improvements
- **Dataset Cleaning:** Implement a script to validate image integrity and remove corrupted files before training.
- **Model Persistence:** Add logic to save the trained model (e.g., `.h5` or SavedModel format) for deployment.
- **Environment Management:** Create a `requirements.txt` or `environment.yml` to formalize the `tf_env` dependency.
- **Error Handling:** Enhance the data loading pipeline to gracefully handle or skip invalid image files.
