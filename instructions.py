from config import RESOURCES_DIR


def get_agent_instructions(name: str) -> str:
    file_path = f"{RESOURCES_DIR}/instructions/{name}.md"
    with open(file_path, mode="r") as f:
        return f.read()
