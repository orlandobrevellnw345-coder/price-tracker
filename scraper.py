

























import requests
from bs4 import BeautifulSoup
import re

def get_product_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try common price selectors (customize per site)
        price_tags = soup.find_all(string=re.compile(r'[\$€£₹¥]\d+'))
        if not price_tags:
            # Amazon-specific examples (these selectors change often)
            price = soup.find('span', {'class': 'a-price-whole'}) or \
                    soup.find('span', id='priceblock_ourprice') or \
                    soup.find('span', {'class': 'aok-offscreen'})
            if price:
                price_text = price.get_text()
            else:
                price_text = None
        else:
            price_text = price_tags[0]
        
        if price_text:
            # Extract numeric price
            price_num = re.sub(r'[^\d.,]', '', str(price_text))
            price_num = float(price_num.replace(',', ''))
            return round(price_num, 2)
        
        return None
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def get_product_title(url):
    # Similar logic to extract title (add your own selectors)
    headers = {"User-Agent": "Mozilla/5.0 ..."}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').get_text() if soup.find('title') else "Unknown Product"
        return title.strip()[:100]  # Limit length
    except:
        return "Unknown Product"
