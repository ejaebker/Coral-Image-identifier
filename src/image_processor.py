import os
import imagehash
import cv2
import numpy as np
from PIL import Image
from pathlib import Path
from tqdm import tqdm

# Config
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
IMG_SIZE = (224, 224)

# CLAHE Configuration
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

def apply_clahe(img_pil):
    """
    Applies CLAHE (Contrast Limited Adaptive Histogram Equalization) to an image.
    Operates in the LAB color space to enhance lightness without distorting color.
    """
    img_np = np.array(img_pil)
    lab = cv2.cvtColor(img_np, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    l_enhanced = clahe.apply(l)
    lab_enhanced = cv2.merge((l_enhanced, a, b))
    img_rgb = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2RGB)
    return Image.fromarray(img_rgb)

def process_images():
    """
    Main pipeline with progress bars: Clean -> Deduplicate -> Enhance (CLAHE) -> Resize -> Standardize.
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    classes = [d for d in os.listdir(RAW_DIR) if os.path.isdir(os.path.join(RAW_DIR, d))]
    
    seen_hashes = set()
    total_processed = 0
    total_duplicates = 0
    total_failed = 0

    # Calculate total files for the master progress bar
    total_files = 0
    for class_name in classes:
        total_files += len(os.listdir(os.path.join(RAW_DIR, class_name)))

    print(f"Starting Image Processing Pipeline...")
    print(f"Enhancements: Perceptual Deduplication + LAB-space CLAHE")
    
    # Master progress bar for all images
    with tqdm(total=total_files, desc="Total Processing Progress", unit="img") as pbar:
        for class_name in classes:
            source_class_dir = os.path.join(RAW_DIR, class_name)
            target_class_dir = os.path.join(PROCESSED_DIR, class_name)
            os.makedirs(target_class_dir, exist_ok=True)
            
            files = os.listdir(source_class_dir)
            pbar.set_postfix({"class": class_name})
            
            for filename in files:
                source_path = os.path.join(source_class_dir, filename)
                
                try:
                    with Image.open(source_path) as img:
                        img = img.convert('RGB')
                        
                        # 2. PERCEPTUAL DEDUPLICATION
                        h = str(imagehash.phash(img))
                        if h in seen_hashes:
                            total_duplicates += 1
                            pbar.update(1)
                            continue
                        seen_hashes.add(h)
                        
                        # 3. CLAHE ENHANCEMENT
                        img = apply_clahe(img)
                        
                        # 4. RESIZE & STANDARDIZE
                        img = img.resize(IMG_SIZE, Image.Resampling.LANCZOS)
                        
                        target_filename = Path(filename).with_suffix('.jpg')
                        target_path = os.path.join(target_class_dir, target_filename)
                        
                        # 5. SAVE
                        img.save(target_path, 'JPEG', quality=95)
                        total_processed += 1
                        
                except Exception:
                    total_failed += 1
                
                pbar.update(1)
                
    print(f"\nProcessing Complete!")
    print(f"Total unique images enhanced & saved: {total_processed}")
    print(f"Total duplicates removed: {total_duplicates}")
    print(f"Total failed/broken: {total_failed}")

if __name__ == "__main__":
    process_images()
