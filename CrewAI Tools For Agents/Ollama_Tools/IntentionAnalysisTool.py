import requests
import os
from langchain.tools import BaseTool

class IntentionAnalysisTool(BaseTool):
    name = "Intention Analysis"
    description = "Analyzes the intention behind text inputs using specified intention analysis models."
    
    available_models = {
        "default_model": "A general model for broad intention analysis.",
        "customer_inquiry": "Specialized in analyzing customer inquiries for intent.",
        "feedback_analysis": "Focused on discerning the intention behind customer feedback.",
        # Add additional models and their descriptions here
    }

    def __init__(self):
        self.api_url = "http://localhost:11434/api/generate"  # Use the appropriate URL for Ollama API
        self.api_key = os.getenv('OLLAMA_API_KEY')  # Ensure OLLAMA_API_KEY is in your environment variables
        if not self.api_key:
            raise ValueError("Ollama API key not found in environment variables.")

    def generate_prompt(self, text, model_version="default_model"):
        model_description = self.available_models.get(model_version, "A general model for intention analysis.")
        return f"{model_version} ({model_description}): Analyze the intention behind the following text: {text}"

    def analyze_intention(self, text, model_version="default_model"):
        prompt = self.generate_prompt(text, model_version)
        payload = {
            "model": model_version,  # Specify the model version here
            "prompt": prompt,
            "stream": False,  # Set to False to get a single response object
            "format": "json"
        }
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.post(self.api_url, json=payload, headers=headers)
        return response.json()

    def run(self, text, model_version="default_model"):
        """Allows dynamic model version selection for intention analysis."""
        if model_version not in self.available_models:
            return {"error": "Selected model version is not available."}
        return self.analyze_intention(text, model_version)
