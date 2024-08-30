
# Email Scraper and Filtering Tools

Welcome to the Email Scraper and Filtering Tools repository! This project includes a set of Python scripts designed to help you scrape, filter, and manage emails from various sources. The tools include functionalities for extracting emails from websites, filtering out unwanted emails, and finding location formats for targeted searches.
## https://serpapi.com from here you can get API KEY

## Tools Overview

1. **Location Finder** - Find the correct location formats using SerpApi.
2. **Website Scraper** - Scrape URLs from Google search results based on keywords and location.
3. **Email Scraper** - Extract emails from URLs with threading and error handling.
4. **Email Filter** - Filter out duplicate emails, those ending with `.gov`, image file extensions, and programming-related extensions.

---

## 1. Location Finder

**Script:** `location_finder.py`

Use this tool to find the correct location formats that can be used in Google search queries with SerpApi.

### How to Use:

1. **Run the Script:**
   ```bash
   python location_finder.py
   ```
2. **Input the Location Query:**
   - When prompted, enter a location query, e.g., "New York".
3. **Review Possible Locations:**
   - The script will display possible locations, including IDs, names, and canonical names.

---

## 2. Website Scraper

**Script:** `websitescraper.py`

This tool scrapes URLs from Google search results based on the keyword and location inputs.

### How to Use:

1. **Run the Script:**
   ```bash
   python websitescraper.py
   ```
2. **Input Details:**
   - Enter the keyword to search (e.g., "Law firms").
   - Enter the correct location format (as found from the Location Finder).
   - Enter the number of Google pages to scrape (1-10).
3. **Output:**
   - The script will fetch and save URLs in `scraped_urls.txt`.

---

## 3. Email Scraper

**Script:** `emailscraper.py`

Extract emails from the URLs using threading for efficient scraping. This script also skips URLs that cause repeated errors.

### How to Use:

1. **Prepare `urls.txt`:**
   - Ensure `urls.txt` contains URLs you want to scrape, each on a new line.
2. **Run the Script:**
   ```bash
   python emailscraper.py
   ```
3. **Input Details:**
   - Enter the maximum number of pages to scrape.
   - Enter the delay between requests (in seconds).
   - Enter the number of threads to use (e.g., 5).
4. **Output:**
   - The script will save the found emails to `emails.txt`.

---

## 4. Email Filter

**Script:** `filteremails.py`

Filters out duplicate emails, emails ending with `.gov`, image file extensions, and programming or sensitive file extensions.

### How to Use:

1. **Prepare `total.txt`:**
   - Ensure `total.txt` exists and contains the emails to filter, each on a new line.
2. **Run the Script:**
   ```bash
   python filteremails.py
   ```
3. **Output:**
   - The script will save the filtered emails to `filtered_emails.txt`.

---

## Requirements

Ensure you have Python installed along with the necessary libraries:

- `requests`
- `beautifulsoup4`
- `lxml`

Install the dependencies using pip:

```bash
pip install requests beautifulsoup4 lxml
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
## BUY ME A COOKIE <3
Here is the link > [BuyMeACookie](https://web3buymecookie.vercel.app/) (WITH CRYPTO ONLY)

---


Happy scraping and filtering! 🚀
