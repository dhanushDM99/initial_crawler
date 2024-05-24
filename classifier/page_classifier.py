from bs4 import BeautifulSoup
import re

class PageClassifier:
    def __init__(self):
        pass

    def classify(self, url, html):
        if self.is_product_url(url):
            return "Product Page"
        elif self.is_collection_url(url):
            return "Collection Page"
        elif self.is_misc_url(url):
            return "Misc Page"
        else:
            if self.is_product_page(html):
                return "Product Page"
            elif self.is_collection_page(html):
                return "Collection Page"
            elif self.is_misc_page(html):
                return "Misc Page"
            else:
                return "Unknown"

    def is_product_url(self, url):
        return "product" in url or re.search(r'/product/', url)

    def is_collection_url(self, url):
        return "collection" in url or re.search(r'/collections?/', url)

    def is_misc_url(self, url):
        misc_keywords = ["about", "contact", "blog", "privacy"]
        return any(keyword in url for keyword in misc_keywords)

    def is_product_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        if soup.find(text=re.compile(r"Add to Cart|Buy Now")) or soup.find(text=re.compile(r"\$\d+")):
            return True
        product_indicators = ['product', 'price', 'quantity', 'availability']
        for indicator in product_indicators:
            if soup.find(attrs={"class": re.compile(indicator, re.IGNORECASE)}) or soup.find(attrs={"id": re.compile(indicator, re.IGNORECASE)}):
                return True
        return False

    def is_collection_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        product_links = soup.find_all('a', href=re.compile(r'/product/'))
        if len(product_links) > 2:
            return True
        collection_indicators = ['collection', 'category', 'products']
        for indicator in collection_indicators:
            if soup.find(attrs={"class": re.compile(indicator, re.IGNORECASE)}) or soup.find(attrs={"id": re.compile(indicator, re.IGNORECASE)}):
                return True
        return False

    def is_misc_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        misc_keywords = ["about", "contact", "blog", "privacy"]
        if any(keyword in soup.get_text().lower() for keyword in misc_keywords):
            return True
        return False
