import streamlit as st
import logging
import concurrent.futures
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
        try:
            for base_url in start_urls:
                st.subheader(f"Results for: {base_url}")
                with st.spinner(f"Crawling {base_url} (max 50 pages)..."):
                    pages_found = start_crawl(base_url)
                    logging.info(f"Finished crawl for {base_url}. Found {len(pages_found)} pages.")

                if not pages_found:
                    logging.warning(f"No pages found or accessible for {base_url}.")
                    st.warning(f"Could not find any pages to parse for: {base_url}")
                    continue

                texts = []
                with st.spinner(f"Parsing {len(pages_found)} pages for {base_url}..."):
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future_to_url = {executor.submit(extract_text_from_url, page): page for page in pages_found}
                        for future in concurrent.futures.as_completed(future_to_url):
                            page_url = future_to_url[future]
                            try:
                                text = future.result()
                                texts.append(text)
                                logging.info(f"Successfully parsed page: {page_url}")
                            except Exception as exc:
                                logging.error(f"Page {page_url} generated an exception during parsing: {exc}")
                all_text = "\n".join(texts)
                logging.info(f"Parsing completed for {base_url}.")

                with st.spinner(f"Extracting modules for {base_url}..."):
                    logging.info(f"Starting module extraction from combined text (length: {len(all_text)}) for {base_url}.")
                    result = extract_modules(all_text)

                if result is not None:
                    logging.info(f"Module extraction completed successfully for {base_url}.")
                    try:
                        st.json(result)
                    except json.JSONDecodeError as json_err:
                        logging.error(f"Failed to parse JSON response for {base_url}. Error: {json_err}")
                        st.error(f"Failed to display the result for {base_url}. The AI returned data that could not be parsed as JSON.")
                        st.text_area(f"Raw AI Response for {base_url} (for debugging):", result, height=200)
                else:
                    logging.warning(f"Module extraction failed for {base_url}.")
                    st.warning(f"The AI could not extract modules from the content of {base_url}. The content might be unsuitable, or the AI failed to generate the expected structure.")
        except Exception as e:
            logging.error(f"An error occurred during processing: {e}", exc_info=True)
            st.error(f"An error occurred: {e}")
    else:
        logging.warning("Extract Modules button clicked, but no URLs were provided.")
        st.warning("Please enter at least one URL.")
