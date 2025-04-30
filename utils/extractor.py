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

model = genai.GenerativeModel("gemini-2.5-pro-preview-03-25")

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
    Analyze the provided documentation text and identify the distinct main features, components, or conceptual areas.
    For each distinct area identified, treat it as a main module. Extract its description and any relevant sub-components or sub-topics as submodules with their descriptions.

    IMPORTANT: You must extract AT LEAST 10 main modules (if possible) and a TOTAL of AT LEAST 20 submodules (across all modules) for the given documentation text. If the text is too short, extract as many as possible, but always aim for these minimums. Do not merge unrelated concepts. If you need to, break down larger modules into more granular submodules to reach the minimum count.

    Return the result as a JSON list, where each element in the list represents a main module and follows this format:
    [
      {{
        "module": "Example Module Name 1",
        "Description": "Brief description of what Example Module 1 covers.",
        "Submodules": {{
          "Sub Feature A": "Description of sub feature A.",
          "Sub Feature B": "Description of sub feature B."
        }}
      }},
      {{
        "module": "Example Module Name 2",
        "Description": "Brief description of Example Module 2.",
        "Submodules": {{
          "Related Concept X": "Description of concept X.",
          "Related Concept Y": "Description of concept Y."
        }}
      }}
      # ... at least 10 module objects, each with submodules, and at least 20 submodules in total
    ]

    If only one main module is truly appropriate for the entire text, return a list containing just that single module object. Do not list unrelated concepts as submodules under a single overarching topic unless they genuinely belong there. Strive to identify genuinely distinct top-level modules based on the text structure and content. If the text is too short, extract as many as possible.

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
