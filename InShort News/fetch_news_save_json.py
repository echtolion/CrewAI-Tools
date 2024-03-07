import requests
import os
import json
from datetime import datetime

# Function to fetch news articles by category from Inshorts News API
def fetch_news_by_category(category):
    url = f'https://inshortsapi.vercel.app/news?category={category}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print(f"Failed to retrieve news for category: {category}")
        return []

# Function to save news articles to a JSON file in a category-named directory
def save_news_to_json(news_articles, category):
    today = datetime.now().strftime("%Y-%m-%d")
    file_name = f'{category}_{today}.json'

    # Define the path for the new directory and JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    category_dir = os.path.join(current_dir, category)
    os.makedirs(category_dir, exist_ok=True)  # Create the category directory if it doesn't exist

    file_path = os.path.join(category_dir, file_name)
    
    # Save the news articles to the JSON file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(news_articles, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(news_articles)} articles for category: {category} in {file_name}")

def main():
    categories = [
        "all", "national", "business", "sports", "world", 
        "politics", "technology", "startup", "entertainment", 
        "miscellaneous", "hatke", "science", "automobile"
    ]

    for category in categories:
        print(f"Fetching news for category: {category}")
        news_articles = fetch_news_by_category(category)
        if news_articles:
            save_news_to_json(news_articles, category)

if __name__ == '__main__':
    main()
