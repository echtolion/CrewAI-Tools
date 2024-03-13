import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import json
import os
from urllib.request import urlopen

class SitemapContentFreshnessAnalyzer:
    def __init__(self, sitemap_url, output_directory):
        self.sitemap_url = sitemap_url
        self.output_directory = output_directory

    def parse_sitemap(self):
        """Parse the sitemap XML to extract URLs and their lastmod dates."""
        response = urlopen(self.sitemap_url)
        tree = ET.parse(response)
        root = tree.getroot()

        urls = []
        for url in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
            loc = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
            lastmod = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod").text
            urls.append({'loc': loc, 'lastmod': lastmod})
        return urls

    def analyze_freshness(self, urls):
        """Categorize content by freshness."""
        today = datetime.today()
        report = {'Very Fresh': 0, 'Moderately Fresh': 0, 'Stale': 0}

        for url in urls:
            lastmod_date = datetime.strptime(url['lastmod'], "%Y-%m-%dT%H:%M:%S%z")
            age = (today - lastmod_date).days

            if age <= 30:
                report['Very Fresh'] += 1
            elif 30 < age <= 90:
                report['Moderately Fresh'] += 1
            else:
                report['Stale'] += 1
        
        return report

    def generate_report(self):
        """Generate a report detailing the content freshness distribution."""
        urls = self.parse_sitemap()
        freshness_report = self.analyze_freshness(urls)

        # Ensure the output directory exists
        os.makedirs(self.output_directory, exist_ok=True)
        report_path = os.path.join(self.output_directory, 'content_freshness_report.json')

        with open(report_path, 'w') as f:
            json.dump(freshness_report, f, indent=4)

        print(f"Content freshness report saved to {report_path}")

# Example usage
sitemap_url = 'YOUR_SITEMAP_URL_HERE'
output_directory = 'YOUR_OUTPUT_DIRECTORY_HERE'
analyzer = SitemapContentFreshnessAnalyzer(sitemap_url, output_directory)
analyzer.generate_report()
