import os
import shutil
import random

# Configuration
SOURCE_DIR = "data/processed"
TARGET_DIR = "data/balanced"

def balance_dataset():
    """
    Balances the dataset by undersampling majority classes.
    Creates a new directory 'data/balanced' with an equal number of images per class.
    """
    print("\n" + "="*50)
    print("DATASET BALANCER")
    print("="*50)

    # 1. Analyze distribution
    classes = [d for d in os.listdir(SOURCE_DIR) if os.path.isdir(os.path.join(SOURCE_DIR, d))]
    class_counts = {}
    class_files = {}

    for cls in classes:
        files = [f for f in os.listdir(os.path.join(SOURCE_DIR, cls)) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        class_counts[cls] = len(files)
        class_files[cls] = files
        print(f"Class '{cls}': {len(files)} images")

    if not class_counts:
        print("No classes found!")
        return

    # 2. Determine target count (minimum count)
    min_count = min(class_counts.values())
    print(f"\nTarget count (based on minimum): {min_count}")

    # 3. Create target directory
    if os.path.exists(TARGET_DIR):
        print(f"Removing existing '{TARGET_DIR}'...")
        shutil.rmtree(TARGET_DIR)
    os.makedirs(TARGET_DIR)

    # 4. Perform balancing (undersampling)
    print("\nBalancing classes...")
    for cls, files in class_files.items():
        os.makedirs(os.path.join(TARGET_DIR, cls))
        
        # Randomly select 'min_count' files
        selected_files = random.sample(files, min_count)
        
        for file in selected_files:
            src_path = os.path.join(SOURCE_DIR, cls, file)
            dst_path = os.path.join(TARGET_DIR, cls, file)
            shutil.copy2(src_path, dst_path)
            
        print(f"  - {cls}: Copied {min_count} images.")

    print("\n" + "="*50)
    print(f"BALANCING COMPLETE. New dataset in '{TARGET_DIR}'")
    print("="*50)

if __name__ == "__main__":
    balance_dataset()
