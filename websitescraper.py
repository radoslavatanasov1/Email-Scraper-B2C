import requests

def google_search(keyword, location, pages, api_key):
    search_results = set()  # Use a set to avoid duplicate URLs
    for page in range(1, pages + 1):
        params = {
            "engine": "google",
            "q": keyword,
            "location": location,  # Correct location format from Location Finder
            "google_domain": "google.com",
            "gl": "us",  # Geographic location of the search, 'us' for United States
            "hl": "en",  # Language of the search
            "start": (page - 1) * 10,  # Google pagination starts at 0
            "api_key": api_key,
        }

        # Request to SerpApi
        response = requests.get("https://serpapi.com/search.json", params=params)
        
        # Check if the response was successful
        if response.status_code == 200:
            data = response.json()

            # Extract URLs from search results
            if "organic_results" in data:
                for result in data["organic_results"]:
                    link = result.get("link")
                    if link:
                        search_results.add(link)
            else:
                print(f"[!] No 'organic_results' found on page {page}")
        else:
            print(f"[!] Error fetching page {page}: {response.status_code}, {response.text}")
        
        print(f"[+] Fetched page {page}...")

    return search_results

if __name__ == "__main__":
    # Hard-coded API key
    api_key = "TESTTESTSETTESTTESTTEST"

    # User inputs
    keyword = input("[+] Enter the keyword to search: ")
    # Use the canonical name from the location finder script
    location = input("[+] Enter the correct location format (canonical name from location finder): ")
    pages = int(input("[+] Enter the number of Google pages to scrape (1-10): "))

    if pages < 1 or pages > 10:
        print("[-] Please enter a number between 1 and 10 for the pages.")
    else:
        # Scrape the search results
        urls = google_search(keyword, location, pages, api_key)

        # Save the URLs to a text file
        with open("scraped_urls.txt", "w") as file:
            for url in sorted(urls):
                file.write(url + "\n")

        print(f"\n[+] Found {len(urls)} unique URLs.")
        print("[+] URLs saved to 'scraped_urls.txt'.")
