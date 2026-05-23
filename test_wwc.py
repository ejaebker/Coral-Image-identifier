import requests
import re

def test():
    r = requests.get('https://worldwidecorals.com/collections/acropora')
    text = r.text
    
    # Try different patterns
    p1 = r"cdn\\/shop\\/files\\/([^\",]+\.jpg)"
    p2 = r"cdn/shop/files/([^\",]+\.jpg)"
    p3 = r"cdn.*?shop.*?files.*?([^\",]+\.jpg)"
    p4 = r"cdn(?:\\/|/)shop(?:\\/|/)files(?:\\/|/)([^\",]+(?:jpg|jpeg|png))"
    
    print("P1:", len(re.findall(p1, text)))
    print("P2:", len(re.findall(p2, text)))
    print("P3:", len(re.findall(p3, text)))
    print("P4 (case insensitive):", len(re.findall(p4, text, re.IGNORECASE)))
    
    matches = set(re.findall(p4, text, re.IGNORECASE))
    print("Sample matches:", list(matches)[:3])

if __name__ == '__main__':
    test()
