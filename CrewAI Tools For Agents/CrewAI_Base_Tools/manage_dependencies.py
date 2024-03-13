from crewai.tools import BaseTool
import subprocess

class ManageDependencies(BaseTool):
    name = "manage_dependencies"
    description = "Manages project dependencies using Poetry."

    def run(self, project_path: str, action: str, dependency: str) -> str:
        try:
            command = ["poetry", action, dependency]
            subprocess.run(command, cwd=project_path, check=True)
            return f"Dependency '{dependency}' {action}ed successfully."
        except subprocess.CalledProcessError as e:
            return f"Error managing dependency: {e}"
