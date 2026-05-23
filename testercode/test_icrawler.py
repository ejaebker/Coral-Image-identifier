from icrawler.builtin import BingImageCrawler
import os

def test_icrawler_bing():
    save_dir = 'test_icrawler_bing'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    bing_crawler = BingImageCrawler(storage={'root_dir': save_dir})
    bing_crawler.crawl(keyword='acropora', max_num=5)
    
    files = os.listdir(save_dir)
    print(f"Downloaded {len(files)} images: {files}")

if __name__ == "__main__":
    test_icrawler_bing()
