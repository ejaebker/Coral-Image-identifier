import requests
import re

def test():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    r1 = requests.get('https://worldwidecorals.com/collections/acropora')
    r2 = requests.get('https://worldwidecorals.com/collections/acropora', headers=headers)
    r3 = requests.get('https://worldwidecorals.com/collections/acropora?page=1')
    p = r"cdn(?:\\/|/)shop(?:\\/|/)files(?:\\/|/)([^\",]+(?:jpg|jpeg|png))"
    print('Without headers:', len(re.findall(p, r1.text, re.IGNORECASE)))
    print('With headers:', len(re.findall(p, r2.text, re.IGNORECASE)))
    print('With page=1:', len(re.findall(p, r3.text, re.IGNORECASE)))

if __name__ == '__main__':
    test()
