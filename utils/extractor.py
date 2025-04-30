# --- utils/extractor.py ---
import google.generativeai as genai
import os
import logging
import json # Import json for potential future use or validation
import re # Import the regex module

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load your API key from environment variable or hardcode (not recommended)
genai.configure(api_key="AIzaSyDn567Ef8OtU7dUr_oE5KTVsjGxPB2xkpY")

model = genai.GenerativeModel("gemini-2.0-flash-lite")

def clean_json_response(text):
    """Removes Markdown code block fences and leading/trailing whitespace."""
    logging.debug(f"Raw response text before cleaning: '{text}'")
    # Regex to find ```json ... ``` or ``` ... ```
    match = re.search(r"```(json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if match:
        # Extract the content inside the fences
        cleaned_text = match.group(2).strip()
        logging.debug(f"Cleaned response text after removing fences: '{cleaned_text}'")
        return cleaned_text
    cleaned_text = text.strip() # Return stripped original text if no fences found
    logging.debug(f"Cleaned response text (no fences found): '{cleaned_text}'")
    return cleaned_text

def extract_modules(text):
    prompt = f"""
    Extract main modules and submodules from the given documentation text.
    Return the result in the following JSON format:
    {{
        "module": "Module_1",
        "Description": "Description of Module_1",
        "Submodules": {{
            "submodule_1": "Description of submodule_1",
            "submodule_2": "Description of submodule_2"
        }}
    }}
    Documentation Text:
    {text}
    """
    logging.info("Starting module extraction.")
    try:
        response = model.generate_content(prompt)
        cleaned_response = clean_json_response(response.text)

        # Attempt to parse the JSON to ensure it's valid before returning
        try:
            json.loads(cleaned_response) # Try parsing
            logging.info("Module extraction successful and response is valid JSON.")
            return cleaned_response # Return the valid JSON string
        except json.JSONDecodeError as e:
            logging.error(f"Model returned a response that is not valid JSON after cleaning. Error: {e}")
            logging.error(f"Non-JSON response content: '{cleaned_response}'")
            return None # Indicate failure to produce valid JSON
    except Exception as e:
        logging.error(f"Error during module extraction: {e}")
        raise  # Re-raise the exception after logging
