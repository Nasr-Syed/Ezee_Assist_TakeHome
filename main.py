# Ezee Assist Take Home Assignment - Site wide web scraper
# By Nasr Syed

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Define the base URL
main_url = "https://mineolasearchpartners.com"
visited_links = set()  # To track visited URLs. Set data type is used to make sure there are unique links.
visited_images = set()


# Function to scrape page and parse through recursively.
def scrape_page(url):
    if url in visited_links:
        return  # Avoid revisiting the same page

    print(f"Scraping: {url}")  # Logging progress
    visited_links.add(url)  # Mark this URL as visited

    try:
        response = requests.get(url)
        content = response.text
        if response.status_code != 200:
            print(f"Failed to retrieve {url}")
            return
        soup = BeautifulSoup(content, "html.parser")

        # Extract text (first 500 characters for preview)
        page_text = soup.get_text(separator=" ", strip=True)
        print("Printing page content...")
        print(page_text, "\n")
        # Write text to .txt file

        # Recursively finding URL links inside main URL
        all_urls = soup.find_all("a", href=True)
        for link in all_urls:
            full_link = urljoin(main_url, link["href"])  # Combining sublinks with main link to consolidate and acquire URL

            # Ensure it's an internal link
            if urlparse(full_link).netloc == urlparse(main_url).netloc:
                scrape_page(full_link)  # Recursively visit to extract all links from site, only for the domain mineolasearchpartners.com.
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        



# Start the scraper
scrape_page(main_url)

# Generating Summary file
print("\nTotal pages scraped:", len(visited_links))
print("Total images scraped:", len(visited_images))
print("Pages visited:", visited_links)
