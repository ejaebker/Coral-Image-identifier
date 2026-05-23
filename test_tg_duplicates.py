import requests
import re

def extract_urls(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    r = requests.get(url, headers=headers, timeout=15)
    
    pattern = 'data-src' + chr(61) + chr(34) + '(https://tidalgardens' + chr(46) + 'com/media/catalog/product/.*?' + chr(46) + 'jpg)'
    urls = list(set(re.findall(pattern, r.text)))
    if not urls:
        pattern = 'data-original' + chr(61) + chr(34) + '(https://tidalgardens' + chr(46) + 'com/media/catalog/product/.*?' + chr(46) + 'jpg)'
        urls = list(set(re.findall(pattern, r.text)))
        
    return urls

def test():
    urls = {
        "acropora": "https://www.tidalgardens.com/corals/sps.html?cat=20",
        "zoanthid": "https://www.tidalgardens.com/corals/zoanthids.html",
        "montipora": "https://www.tidalgardens.com/corals/sps.html?cat=21"
    }
    
    results = {}
    for name, url in urls.items():
        extracted = extract_urls(url)
        results[name] = set(extracted)
        print(f"{name}: {len(extracted)} images")
        
    print("Intersection acropora & zoanthid:", len(results["acropora"].intersection(results["zoanthid"])))
    print("Intersection acropora & montipora:", len(results["acropora"].intersection(results["montipora"])))
    print("Intersection zoanthid & montipora:", len(results["zoanthid"].intersection(results["montipora"])))

if __name__ == '__main__':
    test()
