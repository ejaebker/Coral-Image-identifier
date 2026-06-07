import os
import time
import json
import requests
import concurrent.futures
from bs4 import BeautifulSoup
from tqdm import tqdm

# --- ROBUST SEARCH ENGINE SCRAPER ---
from icrawler.builtin import BingImageCrawler
from icrawler import ImageDownloader

class CustomBingDownloader(ImageDownloader):
    # naming convention for not overwritting
    def get_filename(self, task, default_ext):
        query_slug = getattr(self, 'query_slug', 'image')
        timestamp = int(time.time() * 1000)
        idx = self.fetched_num + 1
        return f"scraped_bing_{query_slug}_{timestamp}_{idx}.{default_ext}"

class SearchEngineScraper:
    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir

    def scrape(self, coral_classes, images_per_keyword):
        # Progress bar for the overall class/query list
        total_queries = sum(len(queries) for queries in coral_classes.values())
        pbar = tqdm(total=total_queries, desc="Bing Scraping Progress", unit="query")

        for class_name, keys in coral_classes.items():
            class_target_dir = os.path.join(self.dataset_dir, class_name)
            os.makedirs(class_target_dir, exist_ok=True)
            class_total = 0

            for query in keys:
                query_slug = query.replace(' ', '_').lower()
                
                crawler = BingImageCrawler(
                    downloader_cls=CustomBingDownloader,
                    storage={'root_dir': class_target_dir}, 
                    log_level=50
                )
                
                crawler.downloader.query_slug = query_slug
                crawler.crawl(keyword=query, max_num=images_per_keyword)
                
                downloaded = crawler.downloader.fetched_num
                class_total += downloaded
                pbar.update(1)
            
            pbar.write(f"Completed Bing class '{class_name}': {class_total} images downloaded.")
            
        pbar.close()

# Website scrapper
class RetailerScraper:
    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape_wwc(self, collection_name, target_class):
        """Specific logic for World Wide Corals (Shopify)."""
        self._generic_shopify_scrape("https://worldwidecorals.com", collection_name, target_class, "wwc")

    def scrape_tidal_gardens(self, target_url, target_class):
        """Specific logic for Tidal Gardens (Magento) using direct category URLs."""
        print(f"\n--- Scraping Tidal Gardens: {target_class} ---")
        target_dir = os.path.join(self.dataset_dir, target_class)
        os.makedirs(target_dir, exist_ok=True)

        page = 1
        total_downloaded = 0
        seen_urls = set()

        while True:
            # Handle pagination
            if "?" in target_url:
                url = f"{target_url}&p={page}"
            else:
                url = f"{target_url}?p={page}"

            try:
                r = requests.get(url, headers=self.headers, timeout=15)
                if r.status_code != 200: break

                soup = BeautifulSoup(r.text, 'html.parser')
                urls = []

                # Find all product cards
                for item in soup.select('.product-item'):
                    img = item.select_one('.product-image-photo')
                    if img:
                        src = img.get('data-src') or img.get('data-original') or img.get('src')
                        if src and 'media/catalog/product' in src:
                            urls.append(src)

                if not urls: break
                
                new_urls = [u for u in urls if u not in seen_urls]
                if not new_urls: break
                    
                seen_urls.update(new_urls)
                total_downloaded += self._download_list(new_urls, target_dir, f"tg_{target_class}")

                if 'pages-item-next' not in r.text:
                    break
                page += 1

            except Exception as e:
                print(f"Tidal Gardens failed on page {page}: {e}")
                break
        
        print(f"Finished Tidal Gardens {target_class}. Downloaded {total_downloaded} images.")

    def _generic_shopify_scrape(self, base_url, collection_name, target_class, prefix):
        target_dir = os.path.join(self.dataset_dir, target_class)
        os.makedirs(target_dir, exist_ok=True)
        page = 1
        total = 0
        print(f"\n--- Scraping {prefix.upper()}: {collection_name} ---")
        while True:
            url = f"{base_url}/collections/{collection_name}/products.json?page={page}"
            try:
                r = requests.get(url, timeout=15)
                if r.status_code != 200: break
                
                data = r.json()
                products = data.get('products', [])
                if not products: break
                
                urls = []
                for product in products:
                    for img in product.get('images', []):
                        src = img.get('src')
                        if src:
                            urls.append(src)
                
                total += self._download_list(urls, target_dir, f"{prefix}_{collection_name}")
                page += 1
            except Exception as e:
                print(f"Error on {prefix.upper()}: {e}")
                break
        print(f"Finished {prefix.upper()} {collection_name}. Downloaded {total} images.")

    def _download_single_image(self, url, target_dir, prefix, index):
        """Worker function for concurrent downloads."""
        try:
            # Strip size parameters
            clean_url = url.split('?')[0]
            timestamp = int(time.time() * 1000)
            save_name = f"scraped_{prefix}_{timestamp}_{index}.jpg"
            save_path = os.path.join(target_dir, save_name)
            
            img_data = requests.get(clean_url, timeout=10).content
            with open(save_path, 'wb') as f:
                f.write(img_data)
            return 1
        except:
            return 0

    def _download_list(self, urls, target_dir, prefix):
        """Concurrent download using ThreadPoolExecutor with Progress Bar."""
        success_count = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Submit tasks and wrap in tqdm
            futures = [executor.submit(self._download_single_image, url, target_dir, prefix, i) for i, url in enumerate(urls)]
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(urls), desc=f"Downloading {prefix}", leave=False):
                success_count += future.result()
        return success_count

def run_crawler():
    # Load Configuration
    with open("config.json", "r") as f:
        config = json.load(f)

    TARGET_DIR = config.get("target_dir", "data/raw")
    IMAGES_PER_KEY = config.get("images_per_keyword", 25)
    CORAL_CLASSES = config.get("coral_classes", {})
    RETAILERS = config.get("retailers", {})

    # Determine which classes actually need scraping
    active_coral_classes = {}
    for class_name, queries in CORAL_CLASSES.items():
        class_dir = os.path.join(TARGET_DIR, class_name)
        if os.path.exists(class_dir) and len(os.listdir(class_dir)) > 0:
            print(f"  [SKIP] Class '{class_name}' already has data in {TARGET_DIR}. Skipping Bing scrape.")
        else:
            active_coral_classes[class_name] = queries

    # 1. RUN BROAD SEARCH (BING) - Only for active classes
    if active_coral_classes:
        search_scraper = SearchEngineScraper(TARGET_DIR)
        search_scraper.scrape(active_coral_classes, IMAGES_PER_KEY)
    else:
        print("\n[INFO] All coral classes already have Bing data. No new scraping needed.")

    # 2. RUN TARGETED RETAILER SCRAPE
    scraper = RetailerScraper(TARGET_DIR)
    
    # World Wide Corals (WWC)
    for entry in RETAILERS.get("wwc", []):
        target_class = entry["target_class"]
        class_dir = os.path.join(TARGET_DIR, target_class)
        # We check if retailer files (prefixed with 'wwc') already exist to avoid duplicates
        if os.path.exists(class_dir) and any(f.startswith("scraped_wwc") for f in os.listdir(class_dir)):
            print(f"  [SKIP] WWC data already exists for '{target_class}'.")
            continue
        scraper.scrape_wwc(entry["collection"], target_class)
    
    # Tidal Gardens
    for entry in RETAILERS.get("tidal_gardens", []):
        target_class = entry["target_class"]
        class_dir = os.path.join(TARGET_DIR, target_class)
        # Check for 'tg' prefix
        if os.path.exists(class_dir) and any(f.startswith("scraped_tg") for f in os.listdir(class_dir)):
            print(f"  [SKIP] Tidal Gardens data already exists for '{target_class}'.")
            continue
        scraper.scrape_tidal_gardens(entry["url"], target_class)

    print("\nCrawl Complete. Data organized in data/raw/")
    
    # Final summary per class
    print("\n--- Final Dataset Summary ---")
    for class_name in CORAL_CLASSES.keys():
        class_dir = os.path.join(TARGET_DIR, class_name)
        if os.path.exists(class_dir):
            count = len([f for f in os.listdir(class_dir) if os.path.isfile(os.path.join(class_dir, f))])
            print(f"Class '{class_name}': {count} total images")
        else:
            print(f"Class '{class_name}': 0 images (directory not created)")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    run_crawler()
