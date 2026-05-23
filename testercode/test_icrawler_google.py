from icrawler.builtin import GoogleImageCrawler
import os

def test_icrawler_google():
    save_dir = 'test_icrawler_google'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    google_crawler = GoogleImageCrawler(storage={'root_dir': save_dir})
    google_crawler.crawl(keyword='acropora coral', max_num=5)
    
    files = os.listdir(save_dir)
    print(f"Downloaded {len(files)} images: {files}")

if __name__ == "__main__":
    test_icrawler_google()
