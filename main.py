import os
import sys

# --- PATH FIX ---
# Ensures that imports from the src directory work correctly
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.data.crawler import run_crawler
from src.core.processor import process_images
from src.data.balancer import balance_dataset
from src.training.train import run_training

def main():
    print("\n" + "="*60)
    print("🚀 CORAL IDENTIFIER: FULL END-TO-END PIPELINE")
    print("="*60)

    # 1. CRAWLING
    print("\n[STEP 1/4] Starting Data Acquisition...")
    run_crawler()

    # 2. PROCESSING
    print("\n[STEP 2/4] Starting Image Processing (Enhance & Resize)...")
    process_images()

    # NOTE: Manual cleaning (src/data/cleaner.py) is skipped here 
    # because it requires user interaction.
    print("\n[SKIP] Manual Cleaning step requires user interaction.")
    print("       If you want to prune data, run: python src/data/cleaner.py")

    # 3. BALANCING
    print("\n[STEP 3/4] Starting Dataset Balancing...")
    balance_dataset()

    # 4. TRAINING
    print("\n[STEP 4/4] Starting Model Training & Hyperparameter Tuning...")
    run_training()

    print("\n" + "="*60)
    print("🎉 PIPELINE EXECUTION COMPLETE!")
    print("   - Model saved to: models/coral_model_best.keras")
    print("   - TFLite exported: models/coral_model.tflite")
    print("   - API Classes: models/classes.json")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Pipeline interrupted by user. Exiting safely.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n[❌] Pipeline failed with error: {e}")
        sys.exit(1)
