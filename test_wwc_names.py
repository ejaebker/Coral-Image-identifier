import requests
import re
import json

def debug_wwc_images():
    base_url = "https://worldwidecorals.com"
    r = requests.get(f"{base_url}/collections/zoanthids?page=1", timeout=15)
    pattern = r"cdn(?:\\/|/)shop(?:\\/|/)files(?:\\/|/)([^\",]+(?:jpg|jpeg|png))"
    filenames = list(set(re.findall(pattern, r.text, re.IGNORECASE)))
    
    print("Sample filenames:")
    for f in filenames[:20]:
        print(f)

if __name__ == '__main__':
    debug_wwc_images()
