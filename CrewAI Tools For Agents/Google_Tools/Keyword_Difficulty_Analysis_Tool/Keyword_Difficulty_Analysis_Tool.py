import pandas as pd
import json
import os
from typing import Type
from pydantic import BaseModel, Field

class KeywordDifficultyInput(BaseModel):
    """Inputs for the Keyword Difficulty Analysis Tool."""
    source_directory: str = Field(description="Directory containing Excel files with keyword data.")
    output_base_directory: str = Field(description="Base directory for saving keyword difficulty reports.")

class KeywordDifficultyAnalyzer(BaseTool):
    name: str = "Keyword Difficulty Analyzer"
    description: str = ("Assesses the difficulty of ranking for specific keywords based on comprehensive metrics including competition levels, search volumes, trend changes, bid range, and search intent.")
    args_schema: Type[BaseModel] = KeywordDifficultyInput

    def calculate_difficulty_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculates and ranks keyword difficulty with advanced logic."""
        # Pre-process percentage strings to float
        df['Three month change'] = df['Three month change'].str.rstrip('%').astype(float) / 100
        df['YoY change'] = df['YoY change'].str.rstrip('%').astype(float) / 100

        # Normalize search volume and competition index
        df['Normalized Search Volume'] = df['Avg. monthly searches'] / df['Avg. monthly searches'].max()
        df['Normalized Competition Index'] = df['Competition (indexed value)'] / 100
        
        # Account for trend changes
        df['Trend Score'] = (df['Three month change'] + df['YoY change']) / 2
        
        # Factor in the bid range
        df['Bid Range Score'] = (df['Top of page bid (high range)'] - df['Top of page bid (low range)']) / df['Top of page bid (high range)'].max()
        
        # Assign weights to each component based on perceived impact
        weights = {
            'search_volume': 0.4,
            'competition_index': 0.3,
            'trend_score': 0.1,
            'bid_range': 0.2,
        }
        
        # Calculate the difficulty score
        df['Difficulty Score'] = (
            df['Normalized Search Volume'] * weights['search_volume'] +
            df['Normalized Competition Index'] * weights['competition_index'] +
            df['Trend Score'] * weights['trend_score'] +
            df['Bid Range Score'] * weights['bid_range']
        )
        
        # Convert Search Intent into a numerical score, prioritizing transactional and commercial intents
        intent_score = {'Informational': 0.5, 'Navigational': 0.75, 'Transactional': 1, 'Commercial': 1}
        df['Search Intent Score'] = df['Search Intent'].map(intent_score)
        df['Total Difficulty Score'] = df['Difficulty Score'] * df['Search Intent Score']
        
        # Rank keywords based on the total difficulty score
        df['Difficulty Rank'] = df['Total Difficulty Score'].rank(method='max', ascending=False)
        
        return df.sort_values('Difficulty Rank', ascending=True)

    def _run(self, source_directory: str, output_base_directory: str) -> str:
        os.makedirs(output_base_directory, exist_ok=True)

        for file_name in os.listdir(source_directory):
            if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
                file_path = os.path.join(source_directory, file_name)
                df = pd.read_excel(file_path)
                difficulty_analysis = self.calculate_difficulty_scores(df)
                output_dir = os.path.join(output_base_directory, os.path.splitext(file_name)[0] + "_Keyword_Difficulty")
                os.makedirs(output_dir, exist_ok=True)
                with open(os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_Keyword_Difficulty.json"), 'w') as f:
                    json.dump(difficulty_analysis.to_dict(orient='records'), f, indent=4)

        return f"Keyword difficulty analysis completed. Reports saved in {output_base_directory}."

    async def _arun(self, *args, **kwargs):
        """Async version of the run method, if needed."""
        raise NotImplementedError("Async operation not supported for Keyword Difficulty Analyzer.")
