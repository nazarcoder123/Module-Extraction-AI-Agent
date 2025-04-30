import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging # Add logging

# Configure logging for this module if not already configured globally
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Added max_pages parameter with a default limit
def crawl(url, visited=None, max_pages=50): 
    if visited is None:
        visited = set()

    # Stop if max_pages limit is reached or URL already visited or invalid domain
    if len(visited) >= max_pages or url in visited or urlparse(url).netloc == '':
        return []

    logging.info(f"Crawling: {url} (Visited: {len(visited)}/{max_pages})")
    visited.add(url)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    # Initialize links for the current level only if the URL was successfully processed
    links = [url] 

    # Recursively crawl links found on the page, respecting the max_pages limit
    for link in soup.find_all('a', href=True):
        if len(visited) >= max_pages:
            logging.info(f"Max pages ({max_pages}) reached. Stopping crawl.")
            break # Stop iterating through links if limit is hit

        full_url = urljoin(url, link['href'])
        # Ensure we stay on the same domain and haven't visited the link
        if urlparse(full_url).netloc == urlparse(url).netloc and full_url not in visited:
            # Pass visited set and max_pages limit down
            links.extend(crawl(full_url, visited, max_pages)) 

    # Return unique links found starting from this URL (and its children within limits)
    # This recursive function now primarily focuses on populating the 'visited' set.
    # The return value isn't strictly needed by the caller if using start_crawl.
    return [] # Return empty list as the main collection happens via the 'visited' set.

# --- Helper function for the initial call ---
def start_crawl(start_url, max_pages=50):
    """
    Initializes the crawl process and returns the set of visited URLs.
    """
    visited_links = set()
    # The crawl function modifies visited_links in place
    crawl(start_url, visited=visited_links, max_pages=max_pages) 
    logging.info(f"Crawl finished. Total unique pages visited: {len(visited_links)}")
    return list(visited_links) # Return the collected unique links
