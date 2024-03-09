import pandas as pd
import json
import os
from datetime import datetime
from typing import Type
from pydantic import BaseModel, Field

class SEOStrategyInput(BaseModel):
    """Inputs required for the SEO Strategy Analyzer Tool."""
    source_directory: str = Field(description="The directory containing Excel files with keyword data.")
    output_base_directory: str = Field(description="The base directory for saving analysis results in JSON format.")
    analysis_date_range: str = Field(description="Date range for the analysis, in YYYY-MM-DD format (e.g., '2023-01-01 to 2023-12-31').")

class SEOStrategyAnalyzer(BaseTool):
    name: str = "SEO Strategy Analyzer"
    description: str = ("Analyzes keyword trends, competition levels, and changes over time using keyword data "
                        "to provide insights for optimizing SEO strategies.")
    args_schema: Type[BaseModel] = SEOStrategyInput

    def analyze_keywords(self, df: pd.DataFrame) -> pd.DataFrame:
        """Analyzes keywords based on search volume, trend changes, competition, and intent."""
        # Convert percent change strings to floats for calculation
        df['Three month change'] = df['Three month change'].str.rstrip('%').astype('float') / 100.0
        df['YoY change'] = df['YoY change'].str.rstrip('%').astype('float') / 100.0

        # Keyword Popularity Analysis
        df['Popularity Rank'] = df['Avg. monthly searches'].rank(ascending=False)
        
        # Trend Analysis
        df['Trend Score'] = df.apply(lambda x: (x['Three month change'] + x['YoY change']) / 2, axis=1)
        
        # Competition Analysis
        df['Competition Level'] = df['Competition (indexed value)'].apply(lambda x: 'Low' if x < 25 else ('Medium' if x < 50 else 'High'))
        
        # Bid Range Analysis
        df['Bid Range'] = df.apply(lambda x: f"${x['Top of page bid (low range)']} - ${x['Top of page bid (high range)']}", axis=1)
        
        # Intent and Focus Strategy
        df['Intent-Focus Match'] = df.apply(lambda x: 'Match' if (x['Search Intent'] == 'Informational' and x['Focus'] == 'Blog Page') or (x['Search Intent'] == 'Transactional' and x['Focus'] == 'Website Service Page') else 'Mismatch', axis=1)
        
        return df

    def _run(self, source_directory: str, output_base_directory: str, analysis_date_range: str) -> str:
        start_date, end_date = map(lambda x: datetime.strptime(x.strip(), '%Y-%m-%d'), analysis_date_range.split('to'))
        
        os.makedirs(output_base_directory, exist_ok=True)

        for file_name in os.listdir(source_directory):
            if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
                file_path = os.path.join(source_directory, file_name)
                try:
                    df = pd.read_excel(file_path)
                    # The date filter is removed since the example data does not include a 'Date' column
                    seo_analysis = self.analyze_keywords(df)
                    output_dir = os.path.join(output_base_directory, os.path.splitext(file_name)[0] + "_SEO_Analysis")
                    os.makedirs(output_dir, exist_ok=True)
                    seo_analysis.to_json(os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_SEO_Analysis.json"), orient='records', indent=4)
                except Exception as e:
                    print(f"Error processing file {file_name}: {e}")

        return f"SEO strategy analysis completed. Results saved in {output_base_directory}."

    async def _arun(self, *args, **kwargs):
        """Async version of the run method, if needed."""
        raise NotImplementedError("Async operation not supported for SEO Strategy Analyzer.")
