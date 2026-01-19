"""
Generates Instagram images with Arabic text (RTL support)
Optimisé pour le public tunisien
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import date
from pathlib import Path
import sys

# Pour le support RTL arabe - OBLIGATOIRE
try:
    from arabic_reshaper import reshape
    from bidi.algorithm import get_display
    ARABIC_SUPPORT = True
    print("✅ Support arabe activé (arabic-reshaper + python-bidi)")
except ImportError as e:
    ARABIC_SUPPORT = False
    print(f"❌ ERREUR: Librairies arabes manquantes!")
    print(f"   Installez: pip install arabic-reshaper python-bidi")
    print(f"   Erreur: {e}")
    # ARRÊTER si pas de support arabe
    raise ImportError("arabic-reshaper et python-bidi sont OBLIGATOIRES pour le texte arabe!")

sys.path.append(str(Path(__file__).parent.parent))
from config import (
    TEMPLATE_PATH, FONT_QUOTE, FONT_DATE, 
    OUTPUT_DIR, TEXT_CONFIG, IMAGE_QUALITY
)


class ImageGenerator:
    def __init__(self, template_path: Path = TEMPLATE_PATH):
        self.template_path = template_path
        self.quote_config = TEXT_CONFIG["quote"]
        self.date_config = TEXT_CONFIG["date"]
        
        # Charger les polices
        self.font_quote = ImageFont.truetype(
            str(FONT_QUOTE), 
            self.quote_config["font_size"]
        )
        self.font_date = ImageFont.truetype(
            str(FONT_DATE), 
            self.date_config["font_size"]
        )
    
    def _prepare_arabic_text(self, text: str) -> str:
        """
        Prépare le texte arabe pour l'affichage correct (RTL)
        OBLIGATOIRE pour affichage correct
        """
        # Reshape pour connecter les lettres arabes
        reshaped_text = reshape(text)
        # Bidi pour l'ordre RTL
        bidi_text = get_display(reshaped_text)
        return bidi_text
    
    def _wrap_arabic_text(self, text: str, max_width: int) -> list:
        """
        Découpe le texte arabe en lignes
        """
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word)
            if current_length + word_length + 1 <= max_width:
                current_line.append(word)
                current_length += word_length + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def generate(self, quote_text: str, quote_date: date, 
                 output_filename: str = None) -> Path:
        """
        Generate image with Arabic quote and date
        """
        print(f"📝 Texte original: {quote_text[:50]}...")
        
        # Charger template
        img = Image.open(self.template_path).copy()
        draw = ImageDraw.Draw(img)
        
        # Dessiner la citation arabe
        self._draw_arabic_quote(draw, quote_text)
        
        # Dessiner la date (style tunisien)
        self._draw_tunisian_date(draw, quote_date)
        
        # Sauvegarder
        if output_filename is None:
            output_filename = f"post_{quote_date.strftime('%Y%m%d')}.png"
        
        output_path = OUTPUT_DIR / output_filename
        OUTPUT_DIR.mkdir(exist_ok=True)
        
        img.save(output_path, quality=IMAGE_QUALITY)
        print(f"🖼️  Image générée: {output_path}")
        
        return output_path
    
    def _draw_arabic_quote(self, draw: ImageDraw, text: str):
        """Dessine la citation arabe centrée"""
        config = self.quote_config
        
        # Découper en lignes
        lines = self._wrap_arabic_text(text, config["max_width"])
        
        # Calculer dimensions
        line_height = config["font_size"] + config["line_spacing"]
        total_height = len(lines) * line_height
        
        # Position Y de départ (centré verticalement)
        start_y = config["position"][1] - (total_height // 2)
        
        for i, line in enumerate(lines):
            # Préparer le texte arabe - OBLIGATOIRE
            display_line = self._prepare_arabic_text(line)
            print(f"   Ligne {i+1}: {line[:30]}... → {display_line[:30]}...")
            
            # Calculer position X (centré horizontalement)
            bbox = draw.textbbox((0, 0), display_line, font=self.font_quote)
            line_width = bbox[2] - bbox[0]
            x = config["position"][0] - (line_width // 2)
            y = start_y + (i * line_height)
            
            # Dessiner l'ombre
            shadow_offset = config["shadow_offset"]
            draw.text(
                (x + shadow_offset, y + shadow_offset),
                display_line,
                font=self.font_quote,
                fill=config["shadow_color"]
            )
            
            # Dessiner le texte principal
            draw.text(
                (x, y),
                display_line,
                font=self.font_quote,
                fill=config["color"]
            )
    
    def _draw_tunisian_date(self, draw: ImageDraw, quote_date: date):
        """
        Dessine la date en style tunisien
        Chiffres normaux (1, 2, 3...) + mois en arabe tunisien
        """
        config = self.date_config
        
        # Mois en arabe TUNISIEN
        tunisian_months = {
            1: "جانفي", 2: "فيفري", 3: "مارس", 4: "أفريل",
            5: "ماي", 6: "جوان", 7: "جويلية", 8: "أوت",
            9: "سبتمبر", 10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر"
        }
        
        # Jours en arabe
        arabic_days = {
            0: "الإثنين", 1: "الثلاثاء", 2: "الأربعاء", 3: "الخميس",
            4: "الجمعة", 5: "السبت", 6: "الأحد"
        }
        
        # Construire la date
        day_name = arabic_days[quote_date.weekday()]
        day_num = quote_date.day
        month_name = tunisian_months[quote_date.month]
        year = quote_date.year
        
        date_text = f"{day_name} {day_num} {month_name} {year}"
        
        # Préparer pour affichage RTL
        display_date = self._prepare_arabic_text(date_text)
        print(f"📅 Date: {date_text} → {display_date}")
        
        # Centrer la date
        bbox = draw.textbbox((0, 0), display_date, font=self.font_date)
        text_width = bbox[2] - bbox[0]
        x = config["position"][0] - (text_width // 2)
        y = config["position"][1]
        
        # Dessiner avec ombre
        draw.text((x + 2, y + 2), display_date, font=self.font_date, fill="#000000")
        draw.text((x, y), display_date, font=self.font_date, fill=config["color"])


# === TEST ===
if __name__ == "__main__":
    generator = ImageGenerator()
    
    test_quote = "ان حسن ظني بربي يجعل الامور دائما تسير لمصلحتي"
    
    generator.generate(
        quote_text=test_quote,
        quote_date=date(2026, 1, 16)
    )
    print("✅ Test image générée!")
