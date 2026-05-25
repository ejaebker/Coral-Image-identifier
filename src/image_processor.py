import os
import imagehash
from PIL import Image
from pathlib import Path

# Config
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
IMG_SIZE = (224, 224)

def process_images():
    # Ensure processed directory exists
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    # Get all class subdirectories from data/raw
    classes = [d for d in os.listdir(RAW_DIR) if os.path.isdir(os.path.join(RAW_DIR, d))]
    
    seen_hashes = set()
    total_processed = 0
    total_duplicates = 0
    total_failed = 0

    print(f"Starting image processing with duplicate detection...")
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
                # Open and check for duplicates using perceptual hash
                with Image.open(source_path) as img:
                    # Generate hash before any transformations
                    # We use phash (perceptual hash) which is robust to resizing/compression
                    h = str(imagehash.phash(img))
                    
                    if h in seen_hashes:
                        total_duplicates += 1
                        continue
                    
                    seen_hashes.add(h)
                    
                    # Convert to RGB and resize
                    img = img.convert('RGB')
                    img = img.resize(IMG_SIZE, Image.Resampling.LANCZOS)
                    
                    # Create a consistent target filename (convert to .jpg)
                    target_filename = Path(filename).with_suffix('.jpg')
                    target_path = os.path.join(target_class_dir, target_filename)
                    
                    # Save as high-quality JPEG
                    img.save(target_path, 'JPEG', quality=95)
                    total_processed += 1
                    
            except Exception as e:
                print(f"  [ERROR] Failed to process {filename}: {e}")
                total_failed += 1
                
    print(f"\nProcessing Complete!")
    print(f"Total unique images processed: {total_processed}")
    print(f"Total duplicates skipped: {total_duplicates}")
    print(f"Total failed/skipped: {total_failed}")

if __name__ == "__main__":
    process_images()
