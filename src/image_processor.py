import os
import imagehash
import cv2
import numpy as np
from PIL import Image
from pathlib import Path

# Config
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
IMG_SIZE = (224, 224)

# CLAHE Configuration
# clipLimit: Threshold for contrast limiting. 2.0 is a good standard.
# tileGridSize: Size of grid for histogram equalization. (8,8) is standard.
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

def apply_clahe(img_pil):
    """
    Applies CLAHE (Contrast Limited Adaptive Histogram Equalization) to an image.
    Operates in the LAB color space to enhance lightness without distorting color.
    """
    # Convert PIL to OpenCv (Numpy array)
    img_np = np.array(img_pil)
    
    # Convert RGB to LAB
    lab = cv2.cvtColor(img_np, cv2.COLOR_RGB2LAB)
    
    # Split channels
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to the L-channel (Lightness)
    l_enhanced = clahe.apply(l)
    
    # Merge back
    lab_enhanced = cv2.merge((l_enhanced, a, b))
    
    # Convert back to RGB
    img_rgb = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2RGB)
    
    return Image.fromarray(img_rgb)

def process_images():
    """
    Main pipeline: Clean -> Deduplicate -> Enhance (CLAHE) -> Resize -> Standardize.
    """
    # Ensure processed directory exists
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    # Get all class subdirectories from data/raw
    classes = [d for d in os.listdir(RAW_DIR) if os.path.isdir(os.path.join(RAW_DIR, d))]
    
    seen_hashes = set()
    total_processed = 0
    total_duplicates = 0
    total_failed = 0

    print(f"Starting Image Processing Pipeline...")
    print(f"Enhancements: Perceptual Deduplication + LAB-space CLAHE")
    print(f"Source: {RAW_DIR} | Destination: {PROCESSED_DIR}")
    
    for class_name in classes:
        source_class_dir = os.path.join(RAW_DIR, class_name)
        target_class_dir = os.path.join(PROCESSED_DIR, class_name)
        os.makedirs(target_class_dir, exist_ok=True)
        
        # Get all files in the class directory
        files = os.listdir(source_class_dir)
        print(f"\nProcessing class: {class_name} ({len(files)} files)")
        
        for filename in files:
            source_path = os.path.join(source_class_dir, filename)
            
            try:
                # 1. OPEN & CLEAN
                # Attempts to open file; if corrupted, skips to except block
                with Image.open(source_path) as img:
                    img = img.convert('RGB')
                    
                    # 2. PERCEPTUAL DEDUPLICATION
                    # Checks visual structure to avoid redundant data cross-class
                    h = str(imagehash.phash(img))
                    if h in seen_hashes:
                        total_duplicates += 1
                        continue
                    seen_hashes.add(h)
                    
                    # 3. CLAHE ENHANCEMENT
                    # Normalizes lighting and pops coral features
                    img = apply_clahe(img)
                    
                    # 4. RESIZE & STANDARDIZE
                    # Standardizes resolution for the CNN model
                    img = img.resize(IMG_SIZE, Image.Resampling.LANCZOS)
                    
                    # Create target filename
                    target_filename = Path(filename).with_suffix('.jpg')
                    target_path = os.path.join(target_class_dir, target_filename)
                    
                    # 5. SAVE
                    img.save(target_path, 'JPEG', quality=95)
                    total_processed += 1
                    
            except Exception as e:
                print(f"  [ERROR] Failed to process {filename}: {e}")
                total_failed += 1
                
    print(f"\nProcessing Complete!")
    print(f"Total unique images enhanced & saved: {total_processed}")
    print(f"Total duplicates removed: {total_duplicates}")
    print(f"Total failed/broken: {total_failed}")

if __name__ == "__main__":
    process_images()
