import requests
from crewai import Agent
from langchain.tools import tool

class DictionaryTools:

    @tool("Fetch Word Definition")
    def fetch_word_definition(self, word):
        """Fetches the definition of a given word from the dictionary API."""
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {"error": "Word not found or API error."}
