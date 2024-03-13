from crewai.tools import BaseTool
import subprocess

class DeployOrPublishProject(BaseTool):
    name = "deploy_or_publish_project"
    description = "Deploys the project or publishes it to a package repository."

    def run(self, project_path: str, repository: str = None) -> str:
        try:
            command = ["poetry", "publish"]
            if repository:
                command += ["--repository", repository]
            subprocess.run(command, cwd=project_path, check=True)
            return "Project deployed/published successfully."
        except subprocess.CalledProcessError as e:
            return f"Error deploying/publishing project: {e}"
