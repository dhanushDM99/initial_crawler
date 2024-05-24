from crawler.web_crawler import WebCrawler
from classifier.page_classifier import PageClassifier
import os
import pandas as pd

def save_to_spreadsheet(base_url, url_data, classified_data):
    # Create file names
    safe_base_url = base_url.replace('https://', '').replace('http://', '').replace('/', '_')
    unclassified_file_name = f"{safe_base_url}_unclassified.csv"
    classified_file_name = f"{safe_base_url}_classified.csv"
    
    # Save unclassified data
    if url_data:
        unclassified_df = pd.DataFrame(url_data, columns=['Base URL', 'Scraped URL'])
        unclassified_df.to_csv(unclassified_file_name, index=False, mode='a', header=not os.path.exists(unclassified_file_name))
        print(f"Saved unclassified data to {unclassified_file_name}")
    
    # Save classified data
    if classified_data:
        classified_df = pd.DataFrame(classified_data, columns=['Base URL', 'Scraped URL', 'URL Class'])
        classified_df.to_csv(classified_file_name, index=False, mode='a', header=not os.path.exists(classified_file_name))
        print(f"Saved classified data to {classified_file_name}")

if __name__ == "__main__":
    base_urls = [
        # "https://simplisafe.com/",
        "https://prose.com/",
        # "https://www.palmangels.com/en-us/",
        # "https://www.hellyhansen.com/en_global/"
    ]

    for base_url in base_urls:
        print(f"Starting crawl for base URL: {base_url}")
        crawler = WebCrawler(base_url)  # Limit to 10 pages for debugging
        all_urls = crawler.crawl()
        classifier = PageClassifier()

        for url in all_urls:
            print(f"Processing URL: {url}")  # Debug statement
            try:
                html = crawler.fetch_page(url)
                print(f"Fetched page: {url}")  # Debug statement
                url_data = [[base_url, url]]
                save_to_spreadsheet(base_url, url_data, [])
                if html:
                    print(f"Classifying page: {url}")  # Debug statement
                    page_type = classifier.classify(url, html)
                    if not page_type:
                        page_type = "Unknown"
                    classified_data = [[base_url, url, page_type]]
                    save_to_spreadsheet(base_url, [], classified_data)
            except Exception as e:
                print(f"Failed to process {url}: {e}")

    print("Crawling and classification completed for all base URLs.")






# from crawler.web_crawler import WebCrawler
# from classifier.page_classifier import PageClassifier
# import os
# import pandas as pd

# def save_to_spreadsheet(base_url, url_data, classified_data):
#     # Create file names
#     safe_base_url = base_url.replace('https://', '').replace('http://', '').replace('/', '_')
#     unclassified_file_name = f"{safe_base_url}_unclassified.csv"
#     classified_file_name = f"{safe_base_url}_classified.csv"
    
#     # Save unclassified data
#     if url_data:
#         unclassified_df = pd.DataFrame(url_data, columns=['Base URL', 'Scraped URL'])
#         unclassified_df.to_csv(unclassified_file_name, index=False, mode='a', header=not os.path.exists(unclassified_file_name))
#         print(f"Saved unclassified data to {unclassified_file_name}")
    
#     # Save classified data
#     if classified_data:
#         classified_df = pd.DataFrame(classified_data, columns=['Base URL', 'Scraped URL', 'URL Class'])
#         classified_df.to_csv(classified_file_name, index=False, mode='a', header=not os.path.exists(classified_file_name))
#         print(f"Saved classified data to {classified_file_name}")

# if __name__ == "__main__":
#     base_urls = [
#         # "https://simplisafe.com/",
#         "https://prose.com/",
#         # "https://www.palmangels.com/en-us/",
#         # "https://www.hellyhansen.com/en_global/"
#     ]

#     for base_url in base_urls:
#         print(f"Starting crawl for base URL: {base_url}")
#         crawler = WebCrawler(base_url, max_pages=10)  # Limit to 10 pages for debugging
#         all_urls = crawler.crawl()
#         classifier = PageClassifier()

#         for url in all_urls:
#             print(f"Processing URL: {url}")  # Debug statement
#             try:
#                 html = crawler.fetch_page(url)
#                 print(f"Fetched page: {url}")  # Debug statement
#                 url_data = [[base_url, url]]
#                 save_to_spreadsheet(base_url, url_data, [])
#                 if html:
#                     print(f"Classifying page: {url}")  # Debug statement
#                     page_type = classifier.classify(url, html)
#                     if not page_type:
#                         page_type = "Unknown"
#                     classified_data = [[base_url, url, page_type]]
#                     save_to_spreadsheet(base_url, [], classified_data)
#             except Exception as e:
#                 print(f"Failed to process {url}: {e}")

#     print("Crawling and classification completed for all base URLs.")
