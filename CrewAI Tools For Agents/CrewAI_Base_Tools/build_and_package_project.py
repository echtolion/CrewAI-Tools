from crewai.tools import BaseTool
import subprocess

class BuildAndPackageProject(BaseTool):
    name = "build_and_package_project"
    description = "Builds and packages the project for distribution."

    def run(self, project_path: str) -> str:
        try:
            subprocess.run(["poetry", "build"], cwd=project_path, check=True)
            return "Project built and packaged successfully."
        except subprocess.CalledProcessError as e:
            return f"Error building and packaging project: {e}"
