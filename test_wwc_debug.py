import requests
import re
import time

def test_wwc():
    base_url = "https://worldwidecorals.com"
    collection_name = "acropora"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = f"{base_url}/collections/{collection_name}?page=1"
    r = requests.get(url, headers=headers, timeout=15)
    
    pattern = r"cdn(?:\\/|/)shop(?:\\/|/)files(?:\\/|/)([^\",]+(?:jpg|jpeg|png))"
    filenames = list(set(re.findall(pattern, r.text, re.IGNORECASE)))
    print("Found filenames:", len(filenames))
    if filenames:
        urls = [f"{base_url}/cdn/shop/files/{f}" for f in filenames if not any(x in f.lower() for x in ['menu', 'logo', 'icon', 'badge'])]
        print("Valid URLs:", len(urls))
        if urls:
            try:
                img_data = requests.get(urls[0], timeout=10)
                print("First URL:", urls[0])
                print("Status code:", img_data.status_code)
            except Exception as e:
                print("Error fetching:", e)

if __name__ == '__main__':
    test_wwc()
