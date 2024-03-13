from crewai.tools import BaseTool
import subprocess

class ManageVirtualEnvironment(BaseTool):
    name = "manage_virtual_environment"
    description = "Creates or deletes a Python virtual environment within the project."

    def run(self, project_path: str, action: str) -> str:
        venv_path = os.path.join(project_path, 'venv')
        try:
            if action == 'create':
                subprocess.run(["python", "-m", "venv", venv_path], check=True)
                return "Virtual environment created."
            elif action == 'remove':
                subprocess.run(["rm", "-rf", venv_path], check=True)
                return "Virtual environment removed."
            else:
                return "Invalid action. Use 'create' or 'remove'."
        except subprocess.CalledProcessError as e:
            return f"Error managing virtual environment: {e}"
