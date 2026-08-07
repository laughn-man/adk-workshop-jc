"""
This module contains logic for retrieving agent instructions.
"""

from config import RESOURCES_DIR

def get_agent_instructions(name: str) -> str:
    """
    Retrives the agent instructions for the given name. The name must must an Markdown file without the extension. The markdown file
    must be located in the resources/instructions folder.

    Parameters:
        name: The name of the markdown file to retrieve without the extension.

    Returns:
        The contents of the file.
    """
    file_path = f"{RESOURCES_DIR}/instructions/{name}.md"
    with open(file_path, mode="r") as f:
        return f.read()
