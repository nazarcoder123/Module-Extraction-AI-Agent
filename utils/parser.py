from bs4 import BeautifulSoup
import requests

def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        for tag in ['nav', 'header', 'footer', 'script', 'style']:
            for t in soup.find_all(tag):
                t.decompose()

        texts = [p.get_text(separator=' ', strip=True) for p in soup.find_all(['h1', 'h2', 'h3', 'p', 'li'])]
        return '\n'.join([t for t in texts if len(t) > 30])
    except:
        return ''