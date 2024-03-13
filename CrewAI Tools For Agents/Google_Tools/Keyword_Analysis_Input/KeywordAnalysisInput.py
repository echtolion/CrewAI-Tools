import os
import pandas as pd
import json

from langchain.tools import BaseTool
from typing import List, Dict

class KeywordAnalysisInput(BaseModel):
    """Inputs required for the Keyword Analysis Tool."""
    source_directory: str = Field(description="The directory containing Excel files with keyword data.")
    output_base_directory: str = Field(description="The base directory for saving analysis results in JSON format.")

class KeywordAnalysisTool(BaseTool):
    name: str = "Keyword Analysis Tool"
    description: str = ("Automates keyword research by reading data from Excel files, identifying high-volume, low-competition keywords, "
                        "and saving the analysis in JSON format. Results are organized in directories named after the original Excel files.")
    args_schema: Type[BaseModel] = KeywordAnalysisInput

    def process_excel_file(self, file_path: str) -> List[Dict]:
        """Process an individual Excel file to extract high-volume, low-competition keywords."""
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)
        # Example analysis: Filter keywords based on criteria (this step will vary based on the actual data structure)
        filtered_keywords = df[(df['Search Volume'] > 1000) & (df['Competition Index'] < 0.5)]
        return filtered_keywords.to_dict(orient='records')

    def _run(self, source_directory: str, output_base_directory: str) -> str:
        """The main logic for the Keyword Analysis Tool."""
        # Ensure output base directory exists
        os.makedirs(output_base_directory, exist_ok=True)

        # Iterate over each Excel file in the source directory
        for file_name in os.listdir(source_directory):
            if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
                file_path = os.path.join(source_directory, file_name)
                try:
                    # Process the Excel file
                    keywords_analysis = self.process_excel_file(file_path)
                    # Save the analysis results
                    output_dir = os.path.join(output_base_directory, os.path.splitext(file_name)[0])
                    os.makedirs(output_dir, exist_ok=True)
                    with open(os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.json"), 'w') as f:
                        json.dump(keywords_analysis, f, indent=4)
                except Exception as e:
                    # Handle potential errors, e.g., unreadable files
                    print(f"Error processing file {file_name}: {e}")

        return f"Keyword analysis completed. Results saved in {output_base_directory}."

    async def _arun(self, *args, **kwargs):
        """Async version of the run method, if needed."""
        raise NotImplementedError("Async operation not supported for Keyword Analysis Tool.")
