from langchain.tools import BaseTool
import subprocess

class ShellCommandTool(BaseTool):
    name = "Shell Command Execution Tool"
    description = "Executes predefined safe shell commands."

    def __init__(self):
        self.allowed_commands = {
            "create_conda_env": "conda create --name {env_name} python={python_version} --yes",
            "verify_conda": "conda info",
            "update_conda": "conda update conda",
            "install_package": "conda install {package_name}",
            "list_envs": "conda env list",
            "list_packages": "conda list",
            "create_env_clone": "conda create --clone {source_env_name} --name {new_env_name}",
            "list_revisions": "conda list --revisions",
            "restore_env_revision": "conda install --revision {revision_number}",
            "save_env_details": "conda list --explicit > {filename}",
            "delete_env": "conda env remove --name {env_name}",
            "install_jupyter": "conda install jupyter",
            "update_package": "conda update {package_name}",
            "install_from_channel": "conda install --channel {channel_name} {package_name}",
            "remove_packages": "conda remove --name {env_name} {package_names}",
            # Placeholder for pip install; consider security implications
            "pip_install": "pip install {package_name}"
        }

    def run_command(self, command_key, **kwargs):
        if command_key not in self.allowed_commands:
            return "Command not allowed."
        
        command = self.allowed_commands[command_key].format(**kwargs)
        
        try:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            return result.stdout or "Command executed successfully."
        except subprocess.CalledProcessError as e:
            return f"Command failed: {e.stderr}"

    def run(self, command_key, **kwargs):
        return self.run_command(command_key, **kwargs)
