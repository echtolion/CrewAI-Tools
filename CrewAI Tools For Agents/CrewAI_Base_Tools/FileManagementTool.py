from langchain.tools import BaseTool
import shutil
import os

class FileManagementTool(BaseTool):
    name = "File Management Tool"
    description = "Performs common file operations such as copy, move, delete, and rename."

    def copy_file(self, src, dest):
        shutil.copy(src, dest)
        return f"File copied from {src} to {dest}."

    def move_file(self, src, dest):
        shutil.move(src, dest)
        return f"File moved from {src} to {dest}."

    def delete_file(self, path):
        os.remove(path)
        return f"File {path} has been deleted."

    def rename_file(self, src, new_name):
        os.rename(src, new_name)
        return f"File {src} has been renamed to {new_name}."

    def run(self, operation, **kwargs):
        if operation == 'copy':
            return self.copy_file(kwargs['src'], kwargs['dest'])
        elif operation == 'move':
            return self.move_file(kwargs['src'], kwargs['dest'])
        elif operation == 'delete':
            return self.delete_file(kwargs['path'])
        elif operation == 'rename':
            return self.rename_file(kwargs['src'], kwargs['new_name'])
        else:
            return "Unsupported operation."
