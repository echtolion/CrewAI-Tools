from langchain.tools import BaseTool
import os
import fnmatch

class FileSearchTool(BaseTool):
    name = "File Search Tool"
    description = "Searches for files matching a specific pattern within a directory."
    
    def search_files(self, directory, pattern):
        matches = []
        for root, dirs, files in os.walk(directory):
            for filename in fnmatch.filter(files, pattern):
                matches.append(os.path.join(root, filename))
        return matches

    def run(self, directory, pattern):
        """Executes the file search within the specified directory."""
        return self.search_files(directory, pattern)
