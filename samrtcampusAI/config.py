import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
ASSETS_DIR = BASE_DIR / "assets"
CSS_DIR = ASSETS_DIR / "css"
IMAGES_DIR = ASSETS_DIR / "images"
PAGES_DIR = BASE_DIR / "pages"
UTILS_DIR = BASE_DIR / "utils"

# Ensure directories exist
for directory in [DATABASE_DIR, ASSETS_DIR, CSS_DIR, IMAGES_DIR, PAGES_DIR, UTILS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Configuration keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY", ""))
SECRET_KEY = os.getenv("SECRET_KEY", "smartcampusai_default_secret_key_98765")
SESSION_KEY = os.getenv("SESSION_KEY", "smartcampusai")

# App meta
APP_NAME = "SmartCampusAI"
APP_SUBTITLE = "AI Powered Smart Campus Management Platform"
APP_ICON = "⚡"
PRIMARY_COLOR = "#6366F1"  # Modern Indigo
SECONDARY_COLOR = "#EC4899" # Modern Pink
DARK_BG = "#0B0F19"
LIGHT_BG = "#F9FAFB"
