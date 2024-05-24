from crawler.web_crawler import WebCrawler
from classifier.page_classifier import PageClassifier
import os

def save_to_file(file_path, page_type, url):
    with open(file_path, 'a') as f:
        f.write(f"{url}, {page_type}\n")
    print(f"Saved: {page_type},{url}")  # Debug statement

if __name__ == "__main__":
    base_url = "https://prose.com/"
    print(1)
    crawler = WebCrawler(base_url, max_pages=10)  # Limit to 10 pages for debugging
    print(2)
    
    output_file = "classified_pages.csv"
    
    # Check if the file exists, if not create it and add headers
    if not os.path.exists(output_file):
        with open(output_file, 'w') as f:
            f.write("Page Type,URL\n")
    
    all_urls = crawler.crawl()
    print(3)
    classifier = PageClassifier()
    print(4)

    for url in all_urls:
        html = crawler.fetch_page(url)
        print(f"Fetching page: {url}")
        if html:
            print(f"Classifying page: {url}")
            page_type = classifier.classify(url, html)
            save_to_file(output_file, page_type, url)
    
    print(f"Classified pages saved to {output_file}")
