from langchain.tools import BaseTool
import pyperclip

class ClipboardManagerTool(BaseTool):
    name = "Clipboard Manager Tool"
    description = "Manages clipboard operations, allowing text to be copied to and retrieved from the clipboard."

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        return "Text copied to clipboard."

    def get_from_clipboard(self):
        return pyperclip.paste()

    def run(self, operation, text=None):
        if operation == 'copy' and text is not None:
            return self.copy_to_clipboard(text)
        elif operation == 'get':
            return self.get_from_clipboard()
        else:
            return "Invalid operation or missing text for copy operation."
