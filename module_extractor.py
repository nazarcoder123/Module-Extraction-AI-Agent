import argparse
from utils.crawler import start_crawl
from utils.parser import extract_text_from_url
from utils.extractor import extract_modules

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--urls', nargs='+', required=True, help='List of documentation URLs')
    args = parser.parse_args()

    all_text = ""
    for base_url in args.urls:
        print(f"Crawling {base_url}...")
        pages = start_crawl(base_url)
        for page in pages:
            print(f"Parsing {page}...")
            text = extract_text_from_url(page)
            all_text += text + "\n"

    print("\nExtracting modules and submodules...\n")
    result = extract_modules(all_text)
    print(result)