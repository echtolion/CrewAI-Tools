import requests
import os
import json

# Function to fetch news articles by category from Inshorts News API
def fetch_news_by_category(category):
    url = f'https://inshortsapi.vercel.app/news?category={category}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print(f"Failed to retrieve news for category: {category}")
        return []

# Function to save news articles to a JSON file
def save_news_to_json(news_articles, category):
    # Define the path for the JSON file. Adjust the directory as needed.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, f'{category}_news.json')
    
    # Save the news articles to the JSON file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(news_articles, f, ensure_ascii=False, indent=4)

def main():
    categories = ['business', 'world', 'technology', 'politics', 'science']

    for category in categories:
        print(f"Fetching news for category: {category}")
        news_articles = fetch_news_by_category(category)
        if news_articles:
            save_news_to_json(news_articles, category)
            print(f"Saved {len(news_articles)} articles for category: {category} to JSON file.")

if __name__ == '__main__':
    main()
