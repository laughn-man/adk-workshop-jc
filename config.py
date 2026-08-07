import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_KEY", "")

if not GOOGLE_MAPS_KEY:
    raise Exception("GOOGLE_MAPS_KEY environment variable is not set.")

GEMINI_MODEL = "gemini-flash-latest"

RESOURCES_DIR = Path(__file__).resolve().parent / "resources"
