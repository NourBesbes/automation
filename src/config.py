"""
Configuration settings for Instagram Automation
Adjust these values based on your template design
"""

from pathlib import Path

# === PATHS ===
BASE_DIR = Path(__file__).parent.parent
TEMPLATE_PATH = BASE_DIR / "templates" / "template.png"
QUOTES_CSV_PATH = BASE_DIR / "data" / "quotes.csv"
OUTPUT_DIR = BASE_DIR / "output"
FONTS_DIR = BASE_DIR / "fonts"

# === FONTS ===
FONT_QUOTE = FONTS_DIR / "Montserrat-Bold.ttf"
FONT_DATE = FONTS_DIR / "Montserrat-Medium.ttf"

# === TEXT POSITIONING ===
# Adjust these based on your template (use position_helper.py)
TEXT_CONFIG = {
    "quote": {
        "position": (540, 450),      # Center point (x, y)
        "font_size": 48,
        "color": "#FFFFFF",          # White
        "shadow_color": "#000000",   # Black
        "shadow_offset": 3,
        "max_width": 30,             # Characters per line
        "line_spacing": 15
    },
    "date": {
        "position": (640, 220),       # Top center
        "font_size": 40,
        "color": "#FFD700",          # Gold
        "format": "%B %d, %Y"        # June 13, 2025
    }
}

# === INSTAGRAM ===
HASHTAGS = """
#DataScience #MachineLearning #AI #Python 
#DataAnalytics #Tech #Innovation #LearnToCode
#ArtificialIntelligence #BigData
"""

# === IMAGE SETTINGS ===
IMAGE_QUALITY = 95
IMAGE_FORMAT = "PNG"