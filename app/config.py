import os
from pathlib import Path

from dotenv import load_dotenv


# Project directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Load .env
load_dotenv(PROJECT_DIR / ".env")


# Application folders
APP_DIR = PROJECT_DIR / "app"

STATIC_DIR = PROJECT_DIR / "static"

PANELS_DIR = STATIC_DIR / "panels"

EXPORTS_DIR = STATIC_DIR / "exports"

TEMPLATES_DIR = PROJECT_DIR / "templates"


# Create folders if they do not exist
PANELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

EXPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

TEMPLATES_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# Gemini configuration
GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
)

GEMINI_FLASH_MODEL = os.getenv(
    "GEMINI_FLASH_MODEL",
    "gemini-3.1-flash-lite"
)


# Hugging Face configuration
HF_TOKEN = os.getenv(
    "HF_TOKEN",
    ""
)

HF_IMAGE_MODEL = os.getenv(
    "HF_IMAGE_MODEL",
    "black-forest-labs/FLUX.1-schnell"
)


# Comic configuration
PANEL_COUNT = 5