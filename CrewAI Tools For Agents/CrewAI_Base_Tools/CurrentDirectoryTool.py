from langchain.tools import BaseTool
import os

class CurrentDirectoryTool(BaseTool):
    name = "Current Directory Finder"
    description = "Finds and returns the current working directory."

    def run(self):
        """Returns the current working directory."""
        return os.getcwd()
