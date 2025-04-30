import streamlit as st
import logging
import concurrent.futures
# Import start_crawl instead of crawl
import json # Import the json module for exception handling
from utils.crawler import start_crawl 
from utils.parser import extract_text_from_url
from utils.extractor import extract_modules

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

st.title("🤖 Module Extraction AI Agent")

# Use text_area for multiple URLs, one per line
url_input_area = st.text_area("Enter documentation URLs (one per line):", height=100)

if st.button("Extract Modules"):
    # Split the input into a list of URLs, stripping whitespace and removing empty lines
    start_urls = [url.strip() for url in url_input_area.splitlines() if url.strip()]

    if start_urls:
        logging.info(f"Extract Modules button clicked with URLs: {start_urls}")
        all_pages_to_parse = set() # Use a set to automatically handle duplicates across crawls
        texts = []

        try:
            # Crawl each starting URL
            with st.spinner(f"Crawling starting from {len(start_urls)} URLs (max 50 pages per start URL)..."):
                for base_url in start_urls:
                    logging.info(f"Starting crawl for URL: {base_url} with max 50 pages.")
                    # Use start_crawl to get the list of pages for the current base_url
                    # The max_pages limit is handled within start_crawl (default is 50)
                    pages_found = start_crawl(base_url)
                    all_pages_to_parse.update(pages_found) # Add found pages to the set
                    logging.info(f"Finished crawl for {base_url}. Found {len(pages_found)} unique pages.")

            # Convert the set of unique pages back to a list for parsing
            unique_pages_list = list(all_pages_to_parse)
            logging.info(f"Total unique pages found across all starting URLs: {len(unique_pages_list)}")

            # Check if any pages were found before attempting to parse
            if not unique_pages_list:
                logging.warning(f"No pages found or accessible starting from the provided URLs.")
                st.warning(f"Could not find any pages to parse starting from the provided URL.")
            else:
                # Correctly indented block starts here
                with st.spinner(f"Parsing {len(unique_pages_list)} unique pages concurrently..."), concurrent.futures.ThreadPoolExecutor() as executor:
                    logging.info(f"Starting concurrent parsing of {len(unique_pages_list)} pages.")
                    # Submit parsing tasks
                    future_to_url = {executor.submit(extract_text_from_url, page): page for page in unique_pages_list}

                    # Collect results as they complete
                for future in concurrent.futures.as_completed(future_to_url):
                    page_url = future_to_url[future]
                    try:
                        text = future.result()
                        texts.append(text)
                        logging.info(f"Successfully parsed page: {page_url}")
                    except Exception as exc:
                        logging.error(f"Page {page_url} generated an exception during parsing: {exc}")

                    all_text = "\n".join(texts)
                    logging.info("Concurrent parsing completed.")

                # This block should only execute if parsing happened (i.e., pages were found)
                with st.spinner("Extracting modules..."):
                    logging.info(f"Starting module extraction from combined text (length: {len(all_text)}).")
                    result = extract_modules(all_text) # This might return None now

                if result is not None:
                    logging.info("Module extraction completed successfully with valid JSON.")
                    # Add try-except block for robust JSON parsing (as a final safety net)
                    try:
                        st.json(result)
                    except json.JSONDecodeError as json_err:
                        # This block might be less likely to be hit now, but kept for safety
                        logging.error(f"Failed to parse JSON response even after validation in extractor. Error: {json_err}")
                        logging.error(f"String content that failed parsing: '{result}'")
                        st.error(f"Failed to display the result. The AI returned data that could not be parsed as JSON.")
                        st.text_area("Raw AI Response (for debugging):", result, height=200) # Show the raw string
                else:
                    logging.warning("Module extraction failed because the AI did not return valid JSON.")
                    st.warning("The AI could not extract modules from the content of the provided URL. The content might be unsuitable, or the AI failed to generate the expected structure.")
        except Exception as e:
            logging.error(f"An error occurred during processing: {e}", exc_info=True)
            st.error(f"An error occurred: {e}")
    else:
        logging.warning("Extract Modules button clicked, but no URLs were provided.")
        st.warning("Please enter at least one URL.")
