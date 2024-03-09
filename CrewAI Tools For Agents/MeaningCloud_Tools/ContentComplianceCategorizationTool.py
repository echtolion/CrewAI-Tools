from langchain.tools import BaseTool
import requests

class ContentComplianceCategorizationTool(BaseTool):
    def __init__(self):
        self.api_key = os.getenv('Meaning_Cloud_API_KEY')
        self.api_url = "https://api.meaningcloud.com/deep-categorization-1.0"
        if not self.api_key:
            raise ValueError("Meaning Cloud API key not found in environment variables.")
    
    def analyze_content(self, content, model="IAB_2.0_en"):
        """Dynamically analyzes the provided content using the specified IAB 2.0 model version."""
        headers = {"content-type": "application/x-www-form-urlencoded"}
        payload = {
            "key": self.api_key,
            "txt": content,
            "model": model
        }
        response = requests.post(self.api_url, data=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "API request failed", "status_code": response.status_code}

    def run(self, content, model_version="IAB_2.0"):
        """Agent specifies model_version dynamically for the content analysis."""
        # Mapping agent input to specific MeaningCloud model codes
        model_mapping = {
            "IAB_2.0": "IAB_2.0_en",
            "IAB_2.0_Tier_3": "IAB_2.0_Tier_3_en",
            "IAB_2.0_Tier_4": "IAB_2.0_Tier_4_en"
        }
        model = model_mapping.get(model_version, "IAB_2.0_en")  # Default to IAB_2.0 if unspecified
        return self.analyze_content(content, model=model)

