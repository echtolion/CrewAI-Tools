import pandas as pd
import json
import os
from typing import Type
from pydantic import BaseModel, Field

class PPCCampaignInput(BaseModel):
    """Inputs for the PPC Campaign Planner Tool."""
    source_directory: str = Field(description="Directory containing Excel files with keyword and bid data.")
    output_base_directory: str = Field(description="Base directory for saving PPC campaign plans.")

class PPCCampaignPlanner(BaseTool):
    name: str = "PPC Campaign Planner"
    description: str = ("Estimates the cost and effectiveness of PPC campaigns targeting specific keywords using bid range data.")
    args_schema: Type[BaseModel] = PPCCampaignInput

    def generate_campaign_plans(self, df: pd.DataFrame) -> list:
        """Generates PPC campaign plans from the DataFrame."""
        campaign_plans = []
        for _, row in df.iterrows():
            average_bid = (row['Top of page bid (low range)'] + row['Top of page bid (high range)']) / 2
            plan = {
                'Keyword': row['Keyword'],
                'Estimated Cost': average_bid,
                'Potential Reach': row['Avg. monthly searches'],
                'Competition Level': row['Competition'],
            }
            campaign_plans.append(plan)
        return campaign_plans

    def _run(self, source_directory: str, output_base_directory: str) -> str:
        os.makedirs(output_base_directory, exist_ok=True)

        for file_name in os.listdir(source_directory):
            if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
                file_path = os.path.join(source_directory, file_name)
                df = pd.read_excel(file_path)
                campaign_plans = self.generate_campaign_plans(df)
                output_dir = os.path.join(output_base_directory, os.path.splitext(file_name)[0] + "_PPC_Campaigns")
                os.makedirs(output_dir, exist_ok=True)
                with open(os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_PPC_Campaigns.json"), 'w') as f:
                    json.dump(campaign_plans, f, indent=4)

        return f"PPC campaign planning completed. Plans saved in {output_base_directory}."

    async def _arun(self, *args, **kwargs):
        """Async version of the run method, if needed."""
        raise NotImplementedError("Async operation not supported for PPC Campaign Planner.")
