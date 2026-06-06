import os
import shutil
import matplotlib.pyplot as plt
from PIL import Image

# Configuration
PROCESSED_DIR = "data/processed"
TRASH_DIR = "data/trash"

def clean_dataset():
    """
    Lightweight UI to manually prune the dataset.
    Controls:
    - 'k' or Right Arrow: Keep image (Skip to next)
    - 'd' or Delete: Delete image (Move to trash)
    - 'q' or Escape: Quit the cleaner
    """
    print("\n" + "="*50)
    print("CORAL DATASET CLEANER")
    print("="*50)
    print("Controls: [K]eep | [D]elete | [Q]uit")
    print("="*50)

    # Gather all images
    all_images = []
    for root, dirs, files in os.walk(PROCESSED_DIR):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                all_images.append(os.path.join(root, file))

    if not all_images:
        print("No images found in data/processed!")
        return

    total = len(all_images)
    current_idx = 0

    plt.ion() # Turn on interactive mode
    fig, ax = plt.subplots(figsize=(8, 8))

    def on_key(event):
        nonlocal current_idx
        
        if event.key == 'q' or event.key == 'escape':
            plt.close()
            current_idx = total # Signal exit
            return

        if event.key == 'k' or event.key == 'right':
            print(f"[{current_idx+1}/{total}] Kept: {os.path.basename(all_images[current_idx])}")
            current_idx += 1
            plt.close()

        elif event.key == 'd' or event.key == 'delete' or event.key == 'backspace':
            img_path = all_images[current_idx]
            rel_path = os.path.relpath(img_path, PROCESSED_DIR)
            trash_path = os.path.join(TRASH_DIR, rel_path)
            
            # Ensure trash subfolder exists
            os.makedirs(os.path.dirname(trash_path), exist_ok=True)
            
            # Move file
            shutil.move(img_path, trash_path)
            print(f"[{current_idx+1}/{total}] DELETED: {os.path.basename(img_path)}")
            
            current_idx += 1
            plt.close()

    while current_idx < total:
        img_path = all_images[current_idx]
        try:
            img = Image.open(img_path)
            ax.clear()
            ax.imshow(img)
            ax.set_title(f"Image {current_idx+1}/{total}\n{os.path.basename(img_path)}")
            ax.axis('off')
            
            # Connect the key event and wait
            cid = fig.canvas.mpl_connect('key_press_event', on_key)
            plt.show(block=True)
            fig.canvas.mpl_disconnect(cid)
            
        except Exception as e:
            print(f"Error opening {img_path}: {e}")
            current_idx += 1

    print("\n" + "="*50)
    print("CLEANING SESSION FINISHED")
    print("="*50)

if __name__ == "__main__":
    clean_dataset()
