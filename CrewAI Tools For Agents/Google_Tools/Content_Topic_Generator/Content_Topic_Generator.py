import pandas as pd
import json
import os
from typing import Type
from pydantic import BaseModel, Field

class ContentTopicInput(BaseModel):
    """Inputs for the Content Topic Generator Tool."""
    source_directory: str = Field(description="Directory containing Excel files with keyword data.")
    output_base_directory: str = Field(description="Base directory for saving generated content ideas.")

class ContentTopicGenerator(BaseTool):
    name: str = "Content Topic Generator"
    description: str = ("Generates content ideas based on keyword popularity, search intent, and user focus derived from the keyword data.")
    args_schema: Type[BaseModel] = ContentTopicInput

    def generate_content_ideas(self, df: pd.DataFrame) -> list:
        """Generates content ideas from the DataFrame."""
        content_ideas = []
        for _, row in df.iterrows():
            idea = {
                'Keyword': row['Keyword'],
                'Content Idea': f"How to {row['Keyword']} for {row['Focus']}",
                'Popularity': row['Avg. monthly searches'],
                'Search Intent': row['Search Intent'],
                'Focus': row['Focus']
            }
            content_ideas.append(idea)
        return content_ideas

    def _run(self, source_directory: str, output_base_directory: str) -> str:
        os.makedirs(output_base_directory, exist_ok=True)

        for file_name in os.listdir(source_directory):
            if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
                file_path = os.path.join(source_directory, file_name)
                df = pd.read_excel(file_path)
                content_ideas = self.generate_content_ideas(df)
                output_dir = os.path.join(output_base_directory, os.path.splitext(file_name)[0] + "_Content_Ideas")
                os.makedirs(output_dir, exist_ok=True)
                with open(os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_Content_Ideas.json"), 'w') as f:
                    json.dump(content_ideas, f, indent=4)

        return f"Content topic generation completed. Ideas saved in {output_base_directory}."

    async def _arun(self, *args, **kwargs):
        """Async version of the run method, if needed."""
        raise NotImplementedError("Async operation not supported for Content Topic Generator.")
