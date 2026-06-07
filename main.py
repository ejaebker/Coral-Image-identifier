import os
import sys

# --- PATH FIX ---
# Ensures that imports from the src directory work correctly
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.data.crawler import run_crawler
from src.core.processor import process_images
from src.data.cleaner import clean_dataset
from src.data.balancer import balance_dataset
from src.training.train import run_training

def main():
    print("\n" + "="*60)
    print("🚀 CORAL IDENTIFIER: FULL END-TO-END PIPELINE")
    print("="*60)

    # 1. CRAWLING
    print("\n[STEP 1/5] Starting Data Acquisition...")
    run_crawler()

    # 2. PROCESSING
    print("\n[STEP 2/5] Starting Image Processing (Enhance & Resize)...")
    process_images()

    # 3. MANUAL CLEANING
    print("\n[STEP 3/5] Starting Manual Pruning...")
    print("       A window will open. Use [K] to keep and [D] to delete.")
    print("       Close the window or press [Q] when finished.")
    clean_dataset()

    # 4. BALANCING
    print("\n[STEP 4/5] Starting Dataset Balancing...")
    balance_dataset()

    # 5. TRAINING
    print("\n" + "-"*40)
    print("📝 DATA PREPARATION COMPLETE.")
    input("👉 Press [ENTER] to start Model Training & Hyperparameter Tuning (or Ctrl+C to stop)...")
    
    print("\n[STEP 5/5] Starting Training...")
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
