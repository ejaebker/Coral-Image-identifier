import requests
from bs4 import BeautifulSoup

def test_wwc_bs4():
    url = "https://worldwidecorals.com/collections/zoanthids?page=1"
    r = requests.get(url, timeout=15)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Select images that are inside the main collection grid
    # Shopify usually puts products in a grid or list under main
    main_content = soup.find('main')
    if main_content:
        # Avoid 'Recently Viewed' or 'Recommendations' which are often at the bottom or outside the main product list
        # But sometimes they are in main. Let's look for standard product card classes.
        images = main_content.select('.grid-view-item img, .product-card img, .card img, .collection img')
        urls = []
        for img in images:
            src = img.get('src') or img.get('data-src') or ''
            src = src.split('?')[0]
            if src.endswith('.jpg') or src.endswith('.png'):
                urls.append(src)
        print("Found valid grid images:", len(set(urls)))
    else:
        print("No main content found")

if __name__ == '__main__':
    test_wwc_bs4()
