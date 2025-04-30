# Documentation Module Extractor

This Streamlit application crawls a given starting URL, extracts text content from the found pages, and uses the Google Gemini API to identify and structure the documentation modules or sections present in the text.

## Features

*   Accepts a starting URL for documentation.
*   Crawls linked pages within the same domain (basic implementation).
*   Parses HTML content to extract relevant text.
*   Leverages Google Gemini to analyze the text and extract a structured list of documentation modules in JSON format.
*   Displays the extracted modules in a user-friendly format.
*   Includes error handling for web requests, content parsing, and AI response validation.
*   Provides Docker support for easy containerization and deployment.

## Prerequisites

*   Python 3.8+
*   Pip (Python package installer)
*   Google Gemini API Key
*   Docker (Optional, for containerized deployment)

## Setup and Local Installation

1.  **Clone the repository (or download the files):**
    ```bash
    # If using git
    # git clone https://github.com/nazarcoder123/Module-Extraction-AI-Agent.git
    # cd <your-repo-directory>/s
    ```
    Ensure you are in the directory containing `app.py`, `requirements.txt`, and the `utils` folder (e.g., `e:/Gemini-Fine-Tuning/s/`).

2.  **Create and activate a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set your Google Gemini API Key:**
    The application currently expects the API key to be hardcoded in `utils/extractor.py`.
    *   Open `e:/Gemini-Fine-Tuning/s/utils/extractor.py`.
    *   Replace `"AIzaSyDn567Ef8OtU7dUr_oE5KTVsjGxPB2xkpY"` with your actual API key.
    *   **Note:** For better security, consider using environment variables or a configuration file to manage your API key instead of hardcoding it.

## Running Locally

Once the setup is complete, run the Streamlit application:

```bash
streamlit run app.py
```

Open your web browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).

## Running with Docker

1.  **Build the Docker image:**
    Make sure Docker Desktop (or Docker Engine) is running. Navigate to the directory containing the `Dockerfile` (`e:/Gemini-Fine-Tuning/s/`) and run:
    ```bash
    docker build -t module-extractor-app .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -p 8501:8501 module-extractor-app
    ```
    *   Ensure your API key is set within the `utils/extractor.py` file *before* building the image, or modify the Dockerfile/code to accept the key via environment variables (recommended for production).

3.  **Access the application:**
    Open your web browser and navigate to `http://localhost:8501`.

## Project Structure

```
.
├── app.py             # Main Streamlit application file
├── requirements.txt   # Python dependencies
├── Dockerfile         # Docker configuration
├── README.md          # This file contain the steps to run the application.
└── utils/             # Directory for helper modules
    ├── crawler.py     # Handles web crawling
    ├── parser.py      # Extracts text from HTML
    └── extractor.py   # Interacts with Gemini API
```
*   `app.py`: The main Streamlit application file.
*   `requirements.txt`: Lists Python dependencies.
*   `Dockerfile`: Defines the Docker container build process.
*   `README.md`: This file contain the steps to run the application.
*   `utils/`: Directory containing helper modules:
    *   `crawler.py`: Handles crawling web pages starting from a given URL.
    *   `parser.py`: Extracts text content from HTML.
    *   `extractor.py`: Interacts with the Google Gemini API to extract modules and cleans the response.

## Notes & Limitations

*   The web crawler (`crawler.py`) is basic and might not handle all website structures, JavaScript-rendered content, or complex navigation effectively.
*   The effectiveness of module extraction depends heavily on the quality of the input text and the Gemini model's ability to understand the specific prompt and content.
*   Error handling is included, but edge cases might still exist. Check the logs for detailed error information.
*   API Key Management: Hardcoding the API key is not recommended for production environments. Consider using environment variables.
