import os
import time
import requests
from bs4 import BeautifulSoup

# --- ROBUST SEARCH ENGINE SCRAPER ---
from icrawler.builtin import BingImageCrawler
from icrawler import ImageDownloader

class CustomBingDownloader(ImageDownloader):
    #naming convention for not overwritting
    def get_filename(self, task, default_ext):
        # We'll use the query_slug and count from the task or instance
        query_slug = getattr(self, 'query_slug', 'image')
        timestamp = int(time.time() * 1000)
        idx = self.fetched_num + 1
        return f"scraped_bing_{query_slug}_{timestamp}_{idx}.{default_ext}"

class SearchEngineScraper:
    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir

    def scrape(self, coral_classes, images_per_keyword):

        for class_name, keys in coral_classes.items():
            class_target_dir = os.path.join(self.dataset_dir, class_name) #creates path if it does not exist
            os.makedirs(class_target_dir, exist_ok=True) #creates folder if it doesnt exist

            for query in keys: #for the query in the list of them
                query_slug = query.replace(' ', '_').lower() #for the filename
                print(f"\n--- Scraping Bing for {class_name} using query: {query} ---")
                
                # We use a custom downloader to control the filename and not overwrite images
                crawler = BingImageCrawler(
                    downloader_cls=CustomBingDownloader,
                    storage={'root_dir': class_target_dir}, 
                    log_level=50
                )
                
                # Set the query_slug on the downloader instance so get_filename can use it
                crawler.downloader.query_slug = query_slug

                crawler.crawl(keyword=query, max_num=images_per_keyword)
                
                # Report total for this specific query run
                downloaded = crawler.downloader.fetched_num
                print(f"Finished Bing crawl for {query}. Downloaded {downloaded} images.")

#Website scrapper
class RetailerScraper:
    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape_wwc(self, collection_name, target_class):
        """Specific logic for World Wide Corals (Shopify)."""
        print(f"\n--- Scraping WWC: {collection_name} (Saving to {target_class}) ---")
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

            print(f"Fetching Tidal Gardens page {page}...")
            try:
                r = requests.get(url, headers=self.headers, timeout=15)
                if r.status_code != 200: break

                soup = BeautifulSoup(r.text, 'html.parser')
                urls = []

                # Find all product cards
                for item in soup.select('.product-item'):
                    # Extract the image for this specific valid coral
                    img = item.select_one('.product-image-photo')
                    if img:
                        src = img.get('data-src') or img.get('data-original') or img.get('src')
                        if src and 'media/catalog/product' in src:
                            urls.append(src)

                if not urls: break # No valid images found on this page
                
                # Check for infinite loop / repeating pages
                new_urls = [u for u in urls if u not in seen_urls]
                if not new_urls:
                    print("No new images found on this page. Ending pagination.")
                    break
                    
                seen_urls.update(new_urls)

                total_downloaded += self._download_list(new_urls, target_dir, f"tg_{target_class}")

                # Check if there is a 'Next' page link
                if 'pages-item-next' not in r.text:
                    break
                page += 1

            except Exception as e:
                print(f"Tidal Gardens failed on page {page}: {e}")
                break
        
        print(f"Finished. Downloaded {total_downloaded} images for {target_class} from Tidal Gardens.")

    def _generic_shopify_scrape(self, base_url, collection_name, target_class, prefix):
        target_dir = os.path.join(self.dataset_dir, target_class)
        os.makedirs(target_dir, exist_ok=True)
        page = 1
        total = 0
        while True:
            # Use Shopify's built-in JSON endpoint for perfect accuracy
            url = f"{base_url}/collections/{collection_name}/products.json?page={page}"
            print(f"Fetching {prefix.upper()} page {page}...")
            try:
                r = requests.get(url, timeout=15)
                if r.status_code != 200: break
                
                data = r.json()
                products = data.get('products', [])
                
                if not products: 
                    break # Reached the end of the collection
                
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
        print(f"Finished. Downloaded {total} images from {prefix.upper()}.")

    def _download_list(self, urls, target_dir, prefix):
        count = 0
        for url in urls:
            try:
                # Strip size parameters
                clean_url = url.split('?')[0]
                timestamp = int(time.time() * 1000)
                save_name = f"scraped_{prefix}_{timestamp}_{count}.jpg"
                save_path = os.path.join(target_dir, save_name)
                
                img_data = requests.get(clean_url, timeout=10).content
                with open(save_path, 'wb') as f:
                    f.write(img_data)
                count += 1
            except: continue
        return count

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    TARGET_DIR = "data/raw"
    IMAGES_PER_KEY = 25
    
    CORAL_CLASSES = {
        'acropora': [
            'acropora colony', 
            'acropora frag reef tank', 
            'sps acropora coral'
        ],
        'zoanthid': [
            'zoanthid coral frag', 
            'zoa colony reef aquarium', 
            'zoanthid rock reef aquarium'
        ],
        'montipora': [
            'montipora capricornis', 
            'plating montipora colony', 
            'plating montipora frag'
        ]
    }

    # 1. RUN BROAD SEARCH (BING)
    search_scraper = SearchEngineScraper(TARGET_DIR)
    search_scraper.scrape(CORAL_CLASSES, IMAGES_PER_KEY)

    # 2. RUN TARGETED RETAILER SCRAPE
    scraper = RetailerScraper(TARGET_DIR)
    
    # World Wide Corals (Shopify)
    scraper.scrape_wwc("acropora", "acropora")
    scraper.scrape_wwc("zoanthids", "zoanthid")
    scraper.scrape_wwc("montipora", "montipora")
    
    # Tidal Gardens (Magento)
    scraper.scrape_tidal_gardens("https://tidalgardens.com/corals/sps/staghorn-corals-acropora.html", "acropora")
    scraper.scrape_tidal_gardens("https://tidalgardens.com/corals/zoanthids.html", "zoanthid")
    scraper.scrape_tidal_gardens("https://tidalgardens.com/corals/sps/velvet-corals-montipora.html", "montipora")

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
