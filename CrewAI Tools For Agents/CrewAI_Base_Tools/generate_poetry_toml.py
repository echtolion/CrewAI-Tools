import toml
from crewai import Agent
from langchain.tools import tool

class PoetryTOMLTool:
    @tool("generate_poetry_toml")
    def generate_poetry_toml(self, project_details: dict, toml_file_path: str = "pyproject.toml") -> str:
        """
        Generates a pyproject.toml file for Poetry based on the provided project details.
        The project_details argument should be a dictionary with keys and values
        corresponding to the TOML structure of a pyproject.toml file.
        """
        try:
            # Convert the project details dictionary to TOML format
            toml_content = toml.dumps(project_details)
            
            # Write the TOML content to a file
            with open(toml_file_path, 'w') as toml_file:
                toml_file.write(toml_content)
            
            return f"pyproject.toml file successfully created at {toml_file_path}."
        except Exception as e:
            return f"An error occurred while creating the pyproject.toml file: {str(e)}"

# Example usage within a CrewAI agent setup
# Assuming `generate_poetry_toml` method is invoked by an agent with appropriate project details
