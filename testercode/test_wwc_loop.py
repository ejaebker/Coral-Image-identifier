import requests
import re

def test_wwc_pagination():
    base_url = "https://worldwidecorals.com"
    collection_name = "zoanthids"
    
    for page in [1, 2, 3, 100]:
        url = f"{base_url}/collections/{collection_name}?page={page}"
        r = requests.get(url, timeout=15)
        pattern = r"cdn(?:\\/|/)shop(?:\\/|/)files(?:\\/|/)([^\",]+(?:jpg|jpeg|png))"
        filenames = list(set(re.findall(pattern, r.text, re.IGNORECASE)))
        print(f"Page {page} images:", len(filenames))
        print(f"Page {page} 'pagination__next' in HTML:", 'pagination__next' in r.text)

if __name__ == '__main__':
    test_wwc_pagination()
