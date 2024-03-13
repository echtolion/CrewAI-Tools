import os
import requests
import json
import pandas as pd
from tqdm import tqdm

# Define the URL for the Ollama REST API
ollama_url = "http://localhost:11434/api/generate"

# Define the directory containing the CSV files
directory = "Google_Keywords_Cleaned/SEO/Data"

# Function to fill out search intent and focus using LLM
def fill_out_intent_and_focus(prompt):
    data = {
        "model": "llama2",
        "prompt": prompt
    }
    response = requests.post(ollama_url, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()["completion"]
    else:
        return None

# Loop through each CSV file in the directory
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".csv"):
            file_path = os.path.join(root, file)
            output_json_path = os.path.splitext(file_path)[0] + "_results.json"
            
            # Read the CSV file
            df = pd.read_csv(file_path)
            
            # Create a list to store results
            results = []
            
            # Iterate over each row
            for index, row in tqdm(df.iterrows(), total=len(df), desc=f"Processing {file}"):
                prompt = "Search intent: " + str(row["Keyword"]) + ". Focus: "
                filled_response = fill_out_intent_and_focus(prompt)
                
                if filled_response is not None:
                    # Extract filled out search intent and focus
                    filled_intent_focus = filled_response.split("Focus:")[1].strip()
                    search_intent = filled_intent_focus.split("\n")[0].strip()
                    focus = filled_intent_focus.split("\n")[1].strip()
                    
                    # Append the result to the list
                    results.append({"Search Intent": search_intent, "Focus": focus})
                    
            # Save the results as a JSON file in the same folder
            with open(output_json_path, "w") as json_file:
                json.dump(results, json_file, indent=4)
