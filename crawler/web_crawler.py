from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

class WebCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_urls = set()
        self.to_visit_urls = [base_url]
        # self.max_pages = max_pages
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    def fetch_page(self, url):
        try:
            print(f"Fetching page: {url}")  # Debug statement
            self.driver.get(url)
            time.sleep(5)  # Allow time for the page to load
            page_source = self.driver.page_source
            print(f"Fetched {len(page_source)} characters from {url}")  # Debug statement
            return page_source
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            return None
    
    def get_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(self.base_url, href)
            if self.is_valid_url(full_url):
                links.add(full_url)
        return links
    
    def is_valid_url(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc.endswith(urlparse(self.base_url).netloc)
    
    def crawl(self):
        page_count = 0
        while self.to_visit_urls:
            url = self.to_visit_urls.pop(0)
            if url not in self.visited_urls:
                self.visited_urls.add(url)
                print(f"Crawling: {url}")  # Debug statement
                html = self.fetch_page(url)
                if html:
                    links = self.get_links(html)
                    self.to_visit_urls.extend(links)
                    page_count += 1
                    print(f"Visited pages: {page_count}")  # Debug statement
        self.driver.quit()
        return self.visited_urls
