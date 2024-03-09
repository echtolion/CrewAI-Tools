import subprocess
from langchain.tools import BaseTool

class CondaEnvCreationTool(BaseTool):
    name = "Conda Environment Creation Tool"
    description = "Creates a new Conda environment with a specified name and Python version."

    def create_conda_env(self, env_name, python_version="3.8"):
        command = ["conda", "create", "--name", env_name, f"python={python_version}", "--yes"]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return f"Environment '{env_name}' with Python {python_version} created successfully."
        else:
            return f"Failed to create environment '{env_name}'. Error: {result.stderr}"

    def run(self, env_name, python_version="3.8"):
        """Executes the environment creation with dynamic Python version selection."""
        return self.create_conda_env(env_name, python_version)
