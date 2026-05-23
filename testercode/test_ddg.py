from duckduckgo_search import DDGS
import os
import requests

def test_ddg_images():
    save_dir = 'test_ddg_images'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    with DDGS() as ddgs:
        keywords = 'acropora coral'
        ddgs_images = ddgs.images(keywords, max_results=5)
        
        for i, img in enumerate(ddgs_images):
            print(f"Image {i+1}: {img['image']}")
            try:
                r = requests.get(img['image'], timeout=10)
                with open(os.path.join(save_dir, f"{i}.jpg"), 'wb') as f:
                    f.write(r.content)
            except Exception as e:
                print(f"Failed to download {img['image']}: {e}")

    files = os.listdir(save_dir)
    print(f"Downloaded {len(files)} images: {files}")

if __name__ == "__main__":
    test_ddg_images()
