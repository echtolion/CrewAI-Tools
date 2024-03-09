from langchain.tools import BaseTool

class VoiceOfConsumerTool(BaseTool):
    name = "Voice of Consumer Analysis"
    description = "Analyzes product or service reviews in JSON to detect consumer sentiments and categories."

    def __init__(self, api_key, model="VoC-Retail"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.meaningcloud.com/deep-categorization-1.0"

    def parse_json_reviews(self, json_input):
        # Extract review texts from the JSON input
        # This is a placeholder; implementation depends on JSON structure
        return [review['text'] for review in json_input]

    def analyze_reviews(self, texts):
        headers = {"content-type": "application/x-www-form-urlencoded"}
        payload = {
            "key": self.api_key,
            "txt": "\n".join(texts),
            "model": self.model
        }
        response = requests.post(self.api_url, data=payload, headers=headers)
        return response.json()

    def run(self, json_input):
        texts = self.parse_json_reviews(json_input)
        analysis_results = self.analyze_reviews(texts)
        # Process analysis_results to format as needed
        return analysis_results
