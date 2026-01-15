"""
Configuration settings for Instagram Automation
Support pour contenu arabe (RTL)
"""

from pathlib import Path

# === PATHS ===
BASE_DIR = Path(__file__).parent
TEMPLATE_PATH = BASE_DIR.parent / "templates" / "template.png"
QUOTES_CSV_PATH = BASE_DIR.parent / "data" / "quotes.csv"
OUTPUT_DIR = BASE_DIR.parent / "output"
FONTS_DIR = BASE_DIR.parent / "fonts"

# === FONTS (Arabe) ===
FONT_QUOTE = FONTS_DIR / "Amiri-Bold.ttf"       # Police arabe pour citations
FONT_DATE = FONTS_DIR / "Amiri-Bold.ttf"     # Police arabe pour date

# === TEXT POSITIONING ===
TEXT_CONFIG = {
    "quote": {
        "position": (540, 480),      # Centre de l'image
        "font_size": 56,             # Un peu plus petit pour l'arabe
        "color": "#141313",
        "max_width": 35,             # Caractères par ligne
        "line_spacing": 20,          # Plus d'espace pour l'arabe
        "rtl": True,                  # Right-to-Left pour l'arabe
        "shadow_color": None,
        "shadow_offset": 0,
    },
    "date": {
        "position": (540, 200),      # Centre-bas (changé pour RTL)
        "font_size": 60,
        "color": "#169485",
        "rtl": True
    }
}

# === INSTAGRAM ===
HASHTAGS = """
#تنمية_ذاتية #تطوير_الذات #اقتباسات #حكم
#تحفيز #إيجابية #نجاح #تفاؤل
#اقتباسات_عربية #حكمة_اليوم
"""

# === IMAGE SETTINGS ===
IMAGE_QUALITY = 95
IMAGE_FORMAT = "PNG"