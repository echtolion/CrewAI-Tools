# Important Notes:
# - The .env file must be correctly configured with your Scrape-It API key variable named SCRAPE-IT_API_KEY.
# - Ensure you have an Excel file named keywords.xlsx in the correct path, formatted with a "Keywords" header in A1 and keywords listed below.
# - Necessary Python packages must be installed: openpyxl, beautifulsoup4. Note that http.client is part of the standard library.
import http.client
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import openpyxl
from urllib.parse import quote

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv('SCRAPE-IT_API_KEY')



def search_google(query):
    conn = http.client.HTTPSConnection("api.scrape-it.cloud")
    headers = {'x-api-key': API_KEY}
    # Encode the query to make it URL-safe
    encoded_query = quote(query)
    params = f"/scrape/google/serp?q={encoded_query}&num=5&deviceType=desktop"
    
    conn.request("GET", params, headers=headers)
    res = conn.getresponse()
    data = res.read()
    results = json.loads(data.decode("utf-8"))
    
    if results['requestMetadata']['status'] == 'ok':
        urls = [result['link'] for result in results['organicResults'][:5]]
        return urls
    else:
        print(f"Error during Google search: {results.get('message', 'Unknown error')}")
        return []



def scrape_content(url):
    conn = http.client.HTTPSConnection("api.scrape-it.cloud")
    payload = json.dumps({"url": url})
    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
    }
    
    conn.request("POST", "/scrape", payload, headers)
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data.decode("utf-8"))
    
    if result['status'] == 'ok':
        return result['scrapingResult']['content']
    else:
        print(f"Error scraping {url}: {result.get('message', 'Unknown error')}")
        return None

def parse_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.title.text if soup.title else 'No title'
    headers = [header.text for header in soup.find_all(['h1', 'h2', 'h3'])]
    paragraphs = [p.text for p in soup.find_all('p')]
    
    return {
        'title': title,
        'headers': headers,
        'paragraphs': paragraphs,
    }

def read_keywords_from_excel(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    keywords = [sheet[f'A{i}'].value for i in range(2, sheet.max_row + 1) if sheet[f'A{i}'].value is not None]
    return keywords

def get_checkpoint():
    try:
        with open('checkpoint.txt', 'r') as f:
            last_keyword = f.read().strip()
        return last_keyword
    except FileNotFoundError:
        return ""

def update_checkpoint(keyword):
    with open('checkpoint.txt', 'w') as f:
        f.write(keyword)

def append_to_json(data):
    try:
        with open('scraped_data.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []
    
    existing_data.append(data)
    
    with open('scraped_data.json', 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

        
def main():
    file_path = 'keywords.xlsx'  # Path to your Excel file
    keywords = read_keywords_from_excel(file_path)
    last_processed_keyword = get_checkpoint()
    
    start_processing = False if last_processed_keyword else True
    
    for keyword in keywords:
        if not start_processing:
            if keyword == last_processed_keyword:
                start_processing = True
            continue
        
        print(f"Processing keyword: {keyword}")
        urls = search_google(keyword)
        
        all_data = []
        for url in urls:
            html_content = scrape_content(url)
            if html_content:
                parsed_data = parse_html_content(html_content)
                all_data.append(parsed_data)
        
        append_to_json({keyword: all_data})
        update_checkpoint(keyword)

if __name__ == "__main__":
    main()
