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
# Changed from text_area to text_input for a single URL
url_input = st.text_input("Enter the help documentation URL:")

if st.button("Extract Modules"):
    # Check if url_input is not empty
    if url_input:
        base_url = url_input.strip() # Use the input directly
        logging.info(f"Extract Modules button clicked with URL: {base_url}")
        # Removed all_pages_to_parse initialization here
        texts = []
        try:
            with st.spinner("Crawling (max 50 pages)..."): # Updated spinner text
                logging.info(f"Starting crawl for URL: {base_url} with max 50 pages.")
                # Use start_crawl to get the list of pages directly
                # The max_pages limit is handled within start_crawl (default is 50)
                all_pages_to_parse = start_crawl(base_url) 
                # Logging of found pages is now inside start_crawl

            # Check if any pages were found before attempting to parse
            if not all_pages_to_parse:
                logging.warning(f"No pages found or accessible starting from {base_url}.")
                st.warning(f"Could not find any pages to parse starting from the provided URL.")
            else:
                # Correctly indented block starts here
                with st.spinner(f"Parsing {len(all_pages_to_parse)} pages concurrently..."), concurrent.futures.ThreadPoolExecutor() as executor: # Updated spinner text
                    logging.info(f"Starting concurrent parsing of {len(all_pages_to_parse)} pages.")
                    # Submit parsing tasks
                    future_to_url = {executor.submit(extract_text_from_url, page): page for page in all_pages_to_parse}
                    
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
