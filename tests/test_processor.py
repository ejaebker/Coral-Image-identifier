import pytest
import os
import sys
import numpy as np
from PIL import Image

# --- PATH FIX ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.core.processor import apply_clahe, process_images
import src.core.processor as ip

def test_apply_clahe():
    # Create a random RGB image
    img_data = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    img = Image.fromarray(img_data)
    
    enhanced_img = apply_clahe(img)
    
    assert isinstance(enhanced_img, Image.Image)
    assert enhanced_img.size == (100, 100)
    assert enhanced_img.mode == 'RGB'

def test_process_images(tmp_path, monkeypatch):
    # Setup mock directories
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"
    raw_dir.mkdir()
    
    class_dir = raw_dir / "acropora"
    class_dir.mkdir()
    
    # Create a dummy image
    img_data = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
    img = Image.fromarray(img_data)
    img.save(class_dir / "test.png")
    
    # Mock global variables in src.image_processor
    monkeypatch.setattr(ip, "RAW_DIR", str(raw_dir))
    monkeypatch.setattr(ip, "PROCESSED_DIR", str(processed_dir))
    
    process_images()
    
    # Check if processed image exists
    expected_path = processed_dir / "acropora" / "test.jpg"
    assert expected_path.exists()
    
    # Check if resized correctly
    with Image.open(expected_path) as processed_img:
        assert processed_img.size == (224, 224)
        assert processed_img.format == 'JPEG'

def test_deduplication(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"
    raw_dir.mkdir()
    
    class_dir = raw_dir / "acropora"
    class_dir.mkdir()
    
    # Create two identical images
    img_data = np.zeros((224, 224, 3), dtype=np.uint8)
    img = Image.fromarray(img_data)
    img.save(class_dir / "img1.png")
    img.save(class_dir / "img2.png")
    
    monkeypatch.setattr(ip, "RAW_DIR", str(raw_dir))
    monkeypatch.setattr(ip, "PROCESSED_DIR", str(processed_dir))
    
    process_images()
    
    # Only one should be processed due to deduplication
    processed_files = os.listdir(processed_dir / "acropora")
    assert len(processed_files) == 1
