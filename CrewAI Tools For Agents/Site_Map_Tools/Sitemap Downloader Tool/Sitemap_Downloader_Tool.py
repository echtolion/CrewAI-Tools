import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree
from pathlib import Path

def extract_and_save_sitemaps(excel_path, output_dir):
    df = pd.read_excel(excel_path)
    urls = df['URL'].tolist()  # Assuming URLs are under the 'URL' column
    
    for url in urls:
        domain = url.split("//")[-1].split("/")[0]
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Create XML root
        root = etree.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        
        # Find all links (modify this according to the actual page structure)
        for link in soup.find_all('a'):  # Example: finding all <a> tags, adjust based on actual needs
            href = link.get('href')
            if href:
                url_element = etree.SubElement(root, 'url')
                loc = etree.SubElement(url_element, 'loc')
                loc.text = href
        
        # Save XML
        domain_dir = Path(output_dir) / domain
        domain_dir.mkdir(parents=True, exist_ok=True)
        xml_path = domain_dir / 'sitemap.xml'
        
        with open(xml_path, 'wb') as f:
            f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
        print(f'Sitemap saved to: {xml_path}')

# Usage
excel_path = 'path/to/your/excel.xlsx'  # Path to the Excel file
output_dir = 'path/to/save/sitemaps'  # Directory to save sitemaps
extract_and_save_sitemaps(excel_path, output_dir)
