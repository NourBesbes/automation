"""
Generates Instagram images with Arabic text (RTL support)
Optimisé pour le public tunisien - VERSION FINALE
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import date
from pathlib import Path
import sys

# Support RTL arabe
try:
    import arabic_reshaper
    # On n'utilise PAS bidi avec Pillow!
    print("✅ Support arabe activé")
except ImportError as e:
    raise ImportError(f"Installez: pip install arabic-reshaper\nErreur: {e}")

sys.path.append(str(Path(__file__).parent.parent))
from config import (
    TEMPLATE_PATH, FONT_QUOTE, FONT_DATE, 
    OUTPUT_DIR, TEXT_CONFIG, IMAGE_QUALITY, FONTS_DIR
)


class ImageGenerator:
    def __init__(self, template_path: Path = TEMPLATE_PATH):
        self.template_path = template_path
        self.quote_config = TEXT_CONFIG["quote"]
        self.date_config = TEXT_CONFIG["date"]
        
        print("🔤 Chargement des polices...")
        self.font_quote = ImageFont.truetype(str(FONT_QUOTE), self.quote_config["font_size"])
        self.font_date = ImageFont.truetype(str(FONT_DATE), self.date_config["font_size"])
        print("✅ Polices chargées")
    
    def _reshape_arabic(self, text: str) -> str:
        """
        Reshape le texte arabe - SANS bidi pour Pillow
        Pillow gère déjà le RTL en interne
        """
        # Seulement reshaper pour connecter les lettres
        reshaped = arabic_reshaper.reshape(text)
        # NE PAS utiliser get_display() - Pillow gère le RTL
        return reshaped
    
    def _wrap_text_simple(self, text: str, max_chars: int = 45) -> list:
        """
        Découpe le texte en lignes par nombre de caractères
        Plus simple et plus fiable pour l'arabe
        """
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_len = len(word)
            if current_length + word_len + 1 <= max_chars:
                current_line.append(word)
                current_length += word_len + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_len
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def generate(self, quote_text: str, quote_date: date, 
                 output_filename: str = None) -> Path:
        """
        Génère l'image avec citation arabe et date
        """
        print(f"📝 Texte original: {quote_text[:50]}...")
        
        img = Image.open(self.template_path).copy()
        draw = ImageDraw.Draw(img)
        
        # Dessiner la citation
        self._draw_quote(draw, quote_text)
        
        # Dessiner la date
        self._draw_date(draw, quote_date)
        
        # Sauvegarder
        if output_filename is None:
            output_filename = f"post_{quote_date.strftime('%Y%m%d')}.png"
        
        output_path = OUTPUT_DIR / output_filename
        OUTPUT_DIR.mkdir(exist_ok=True)
        
        img.save(output_path, quality=IMAGE_QUALITY)
        print(f"🖼️  Image générée: {output_path}")
        
        return output_path
    
    def _draw_quote(self, draw: ImageDraw.ImageDraw, text: str):
        """Dessine la citation arabe centrée"""
        config = self.quote_config
        
        # Découper en lignes
        lines = self._wrap_text_simple(text, max_chars=40)
        print(f"   Nombre de lignes: {len(lines)}")
        
        line_height = config["font_size"] + config["line_spacing"]
        total_height = len(lines) * line_height
        start_y = config["position"][1] - (total_height // 2)
        
        for i, line in enumerate(lines):
            # Reshaper SEULEMENT (pas de bidi)
            display_line = self._reshape_arabic(line)
            print(f"   Ligne {i+1}: '{line[:35]}...'")
            
            # Centrer
            bbox = self.font_quote.getbbox(display_line)
            line_width = bbox[2] - bbox[0]
            x = config["position"][0] - (line_width // 2)
            y = start_y + (i * line_height)
            
            # Ombre
            draw.text(
                (x + config["shadow_offset"], y + config["shadow_offset"]),
                display_line,
                font=self.font_quote,
                fill=config["shadow_color"]
            )
            
            # Texte
            draw.text(
                (x, y),
                display_line,
                font=self.font_quote,
                fill=config["color"]
            )
    
    def _draw_date(self, draw: ImageDraw.ImageDraw, quote_date: date):
        """Dessine la date en style tunisien"""
        config = self.date_config
        
        tunisian_months = {
            1: "جانفي", 2: "فيفري", 3: "مارس", 4: "أفريل",
            5: "ماي", 6: "جوان", 7: "جويلية", 8: "أوت",
            9: "سبتمبر", 10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر"
        }
        
        arabic_days = {
            0: "الإثنين", 1: "الثلاثاء", 2: "الأربعاء", 3: "الخميس",
            4: "الجمعة", 5: "السبت", 6: "الأحد"
        }
        
        day_name = arabic_days[quote_date.weekday()]
        date_text = f"{day_name} {quote_date.day} {tunisian_months[quote_date.month]} {quote_date.year}"
        print(f"📅 Date: {date_text}")
        
        display_date = self._reshape_arabic(date_text)
        
        bbox = self.font_date.getbbox(display_date)
        text_width = bbox[2] - bbox[0]
        x = config["position"][0] - (text_width // 2)
        y = config["position"][1]
        
        draw.text((x + 2, y + 2), display_date, font=self.font_date, fill="#000000")
        draw.text((x, y), display_date, font=self.font_date, fill=config["color"])


if __name__ == "__main__":
    generator = ImageGenerator()
    test_quote = "خمس عبارات يحب الزوج سمعها من زوجته أنت وسيم بوجودك بحياتي"
    generator.generate(quote_text=test_quote, quote_date=date(2026, 1, 19))
