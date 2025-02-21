# Ezee Assist Take Home Assignment - Site wide web scraper
# By Nasr Syed
import json
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Define the base URL
main_url = "https://mineolasearchpartners.com"
text_folder = r"C:\Users\nasrs\Documents\Projects\Ezee\text"
image_folder = r"C:\Users\nasrs\Documents\Projects\Ezee\images"
visited_links = set()  # To track visited URLs. Set data type is used to make sure there are unique links.
total_visited_images = set()
summary_data = {}  # Store summary info


# Function to scrape page and parse through recursively.
def download(image_link):
    if image_link in total_visited_images:
        return
    filename = os.path.basename(urlparse(image_link).path)
    filepath = os.path.join(image_folder, filename)
    try:
        response = requests.get(image_link, stream=True)
        print(filename)
        print(response.status_code)
        if response.status_code == 200:
            with open(filepath, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {filepath}")
            total_visited_images.add(image_link)  # Track downloaded images
        else:
            print(f"Response code is: {response.status_code}")
            print(f"Failed to download {image_link}")
    except Exception as e:
        print(f"Failed to download url {image_link}")

def clean(url):
    return url.replace("https://", "").replace("http://", "").replace("/", "_").replace("?", "_")

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
        filename = os.path.join(text_folder, clean(url) +".txt")
        page_text = soup.get_text(separator=" ", strip=True)
        print("Printing page content...")
        print(page_text, "\n")
        # Write text to .txt file
        with open(filename, "w") as file:
            file.write(page_text)
            print(f"Wrote text to file: {filename}")


        # Extract images
        page_images = soup.find_all("img", src=True)
        for img in page_images:
            image_link = urljoin(main_url, img["src"])
            download(image_link)

        # Recursively finding URL links inside main URL
        all_urls = soup.find_all("a", href=True)
        sublist = []
        for link in all_urls:
            full_link = urljoin(main_url, link["href"])  # Combining sub-links with main link to acquire URL
            # Recursively visit to extract all links from site.
            if urlparse(full_link).netloc == urlparse(main_url).netloc:
                sublist.append(full_link)

        # Save summary data
        summary_data[url] = {
            "num_images": len(page_images),
            "referenced_urls": sublist
        }
        # Recurse through internal links
        for item in sublist:
            scrape_page(item)

    except Exception as e:
        print(f"Error scraping {url}: {e}")


# Start the scraper
scrape_page(main_url)

# Save summary data as JSON
with open("summary.json", "w") as f:
    json.dump(summary_data, f, indent=4)

# Summary
print("\nTotal pages scraped:", len(visited_links))
print("Pages visited:", visited_links)
print("\nList of Total image URLs accessed:", total_visited_images)
print("Summary added to: summary.json")
