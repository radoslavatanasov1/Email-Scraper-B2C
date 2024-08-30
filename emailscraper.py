import requests
import urllib.parse
from collections import deque
from bs4 import BeautifulSoup
import re
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# List of user agents to rotate through
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Mobile/15E148 Safari/604.1'
]

# Function to extract emails from a URL with error skipping
def extract_emails_from_url(url):
    try:
        # Select a random user-agent from the list
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',  # Mimic coming from a search engine
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        response = requests.get(url, headers=headers, timeout=10, verify=True)  # Keep SSL verification for security
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Find email addresses in the page content
        new_emails = set(re.findall(r"[a-zA-Z0-9.\-+_{}]+@[a-zA-Z0-9.\-+_]+\.[a-zA-Z]{2,}", response.text))
        return new_emails, response.text

    except requests.exceptions.RequestException as e:
        # Log the error and skip to the next URL
        print(f"[!] Skipping {url} due to error: {e}")
        return set(), ""

# Function to find and normalize URLs from the page
def extract_links_from_page(base_url, path, html_content, scraped_urls):
    soup = BeautifulSoup(html_content, features="lxml")
    found_urls = deque()

    for anchor in soup.find_all("a"):
        link = anchor.attrs.get('href', '')
        if link.startswith('/'):
            link = base_url + link
        elif not link.startswith('http'):
            link = urllib.parse.urljoin(path, link)

        # Normalize and avoid re-processing URLs
        link = urllib.parse.urlparse(link)._replace(fragment='').geturl()  # Remove fragments
        if link not in scraped_urls:
            found_urls.append(link)

    return found_urls

# Function to handle scraping with threading
def scrape_emails_with_threading(urls, max_count=50, delay=1, max_workers=5):
    scraped_urls = set()
    emails = set()
    count = 0
    urls_to_scrape = deque(urls)

    def scrape_url(url):
        nonlocal count
        count += 1
        scraped_urls.add(url)

        # Parse base URL and path
        parts = urllib.parse.urlsplit(url)
        base_url = f"{parts.scheme}://{parts.netloc}"
        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        print(f"[{count}] Processing {url}")
        new_emails, html_content = extract_emails_from_url(url)
        emails.update(new_emails)

        # Extract and queue new links
        found_urls = extract_links_from_page(base_url, path, html_content, scraped_urls)
        urls_to_scrape.extend(found_urls)

        time.sleep(delay)  # Respectful delay between requests

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(scrape_url, urls_to_scrape.popleft()) for _ in range(min(max_count, len(urls_to_scrape)))]
        for future in as_completed(futures):
            future.result()  # Handle exceptions if needed

    return emails

# Main entry point
if __name__ == "__main__":
    # Load URLs from urls.txt file
    try:
        with open('urls.txt', 'r') as file:
            initial_urls = [line.strip() for line in file if line.strip()]  # Read and strip URLs, ignoring empty lines
    except FileNotFoundError:
        print("[-] Error: 'urls.txt' file not found.")
        exit(1)

    max_pages = int(input('[+] Enter Maximum Pages To Scrape: '))
    scrape_delay = float(input('[+] Enter Delay Between Requests (seconds): '))
    max_threads = int(input('[+] Enter the number of threads to use: '))

    try:
        # Start the email scraping process with threading
        found_emails = scrape_emails_with_threading(initial_urls, max_count=max_pages, delay=scrape_delay, max_workers=max_threads)

        # Save the found emails to a file
        with open("emails.txt", "w") as file:
            for email in sorted(found_emails):
                file.write(email + "\n")

        print(f"\n[+] Found {len(found_emails)} emails.")
        print("[+] Emails saved to 'emails.txt'.")

    except KeyboardInterrupt:
        print('[-] Scraping interrupted by user!')
