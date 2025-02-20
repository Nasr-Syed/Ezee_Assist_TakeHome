# Ezee Assist Take Home Assignment - Site wide web scraper
# By Nasr Syed
import os

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Define the base URL
main_url = "https://mineolasearchpartners.com"
image_folder = r"C:\Users\nasrs\Documents\Projects\Ezee\images"
visited_links = set()  # To track visited URLs. Set data type is used to make sure there are unique links.
visited_images = set()


# Function to scrape page and parse through recursively.
def download(image_link):
    filename = os.path.join(image_folder, os.path.basename(image_link))
    try:
        response = requests.get(image_link)
        if response.status_code == 200:
            with open('name', 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {image_link}")
        else:
            print(f"Failed to download {image_link}")
    except Exception as e:
        print(f"Failed to download url {image_link}")

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

        # Extract text
        page_text = soup.get_text(separator=" ", strip=True)
        print("Printing page content...")
        print(page_text, "\n")
        # Write text to .txt file

        # Extract images
        page_images = soup.find_all("img", src=True)
        for img in page_images:
            image_link = urljoin(main_url, img["src"])
            if urlparse(image_link).netloc == urlparse(main_url).netloc:
                download(image_link)  # Recursively visit to extract all links from site.


        # Recursively finding URL links inside main URL
        all_urls = soup.find_all("a", href=True)
        for link in all_urls:
            full_link = urljoin(main_url, link["href"])  # Combining sub-links with main link to acquire URL
            # Ensure parsing is done under URL domain
            if urlparse(full_link).netloc == urlparse(main_url).netloc:
                scrape_page(full_link)  # Recursively visit to extract all links from site.
    except Exception as e:
        print(f"Error scraping {url}: {e}")


# Start the scraper
scrape_page(main_url)

# Generating Summary file
print("\nTotal pages scraped:", len(visited_links))
print("Total images scraped:", len(visited_images))
print("Pages visited:", visited_links)
