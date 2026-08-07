"""
Thie module containst the config value, both constants and environmental.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

def _get_env(name: str) -> str:
    """
    Reads the given name from the environment. If it doesn't exist an error will be thrown.

    Parameters:
        name: The name of the environment variable to read.

    Returns:
        The environment variable value.
    """
    value = os.getenv(name)

    if not value:
        raise Exception(f"{name} environment variable is not set.")

    return value

GOOGLE_MAPS_KEY = _get_env("GOOGLE_MAPS_KEY")

PROJECT_ID = _get_env("PROJECT_ID")

LOCATION = _get_env("LOCATION")

STAGING_BUCKET = _get_env("STAGING_BUCKET")

GEMINI_MODEL = "gemini-2.5-flash"

RESOURCES_DIR = Path(__file__).resolve().parent / "resources"
