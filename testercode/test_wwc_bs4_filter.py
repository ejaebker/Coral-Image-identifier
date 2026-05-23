import requests
from bs4 import BeautifulSoup

def test_wwc_bs4():
    url = "https://worldwidecorals.com/collections/zoanthids?page=1"
    r = requests.get(url, timeout=15)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # We want to get the title of the product to verify it matches our target class
    # and then get its image.
    cards = soup.select('.card, .product-card, .grid-view-item')
    print("Found cards:", len(cards))
    
    valid_urls = []
    for card in cards:
        # Check if the title has our keyword (e.g. 'zoanthid' or 'zoa' or 'paly')
        text = card.get_text().lower()
        if 'zoa' in text or 'paly' in text:
            imgs = card.select('img')
            for img in imgs:
                src = img.get('src') or img.get('data-src') or ''
                src = src.split('?')[0]
                if src.endswith('.jpg') or src.endswith('.png'):
                    valid_urls.append(src)
    print("Valid matched images:", len(set(valid_urls)))

if __name__ == '__main__':
    test_wwc_bs4()
