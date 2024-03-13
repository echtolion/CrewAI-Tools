import os
import subprocess
from crewai import Agent
from langchain.tools import tool

@tool("initialize_project_directory")
def initialize_project_directory(project_name: str, base_path: str = ".") -> str:
    """
    Initializes a Python project directory with essential structures and a virtual environment.
    """
    try:
        project_path = os.path.join(base_path, project_name)
        os.makedirs(os.path.join(project_path, 'src'), exist_ok=True)
        os.makedirs(os.path.join(project_path, 'tests'), exist_ok=True)
        
        # Create virtual environment
        subprocess.run(["python", "-m", "venv", os.path.join(project_path, 'venv')], check=True)
        
        return f"Project '{project_name}' initialized at '{project_path}'."
    except Exception as e:
        return f"Error initializing project: {e}"
