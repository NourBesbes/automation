"""
Generates Instagram images with Arabic text (RTL support)
Optimisé pour le public tunisien - VERSION CORRIGÉE
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import date
from pathlib import Path
import sys
import textwrap

# Support RTL arabe - OBLIGATOIRE
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    print("✅ Support arabe activé")
except ImportError as e:
    raise ImportError(f"Installez: pip install arabic-reshaper python-bidi\nErreur: {e}")

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
        
        # Charger les polices
        print("🔤 Chargement des polices...")
        print(f"   Quote font: {FONT_QUOTE}")
        print(f"   Date font: {FONT_DATE}")
        
        self.font_quote = ImageFont.truetype(str(FONT_QUOTE), self.quote_config["font_size"])
        self.font_date = ImageFont.truetype(str(FONT_DATE), self.date_config["font_size"])
        print("✅ Polices chargées")
    
    def _reshape_arabic(self, text: str) -> str:
        """
        Reshape le texte arabe pour affichage correct
        Cette fonction doit être appelée sur le texte FINAL avant dessin
        """
        # Configuration du reshaper pour meilleure compatibilité
        configuration = {
            'delete_harakat': False,
            'support_ligatures': True,
            'RIAL SIGN': True,
        }
        
        reshaped = arabic_reshaper.reshape(text, configuration)
        bidi_text = get_display(reshaped)
        return bidi_text
    
    def _wrap_text_arabic(self, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list:
        """
        Découpe le texte en lignes qui tiennent dans max_width pixels
        Retourne les lignes NON reshapées (on reshape après)
        """
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            # Teste si le mot tient sur la ligne actuelle
            test_line = ' '.join(current_line + [word])
            
            # Pour mesurer, on doit reshaper temporairement
            test_reshaped = self._reshape_arabic(test_line)
            bbox = font.getbbox(test_reshaped)
            line_width = bbox[2] - bbox[0]
            
            if line_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def generate(self, quote_text: str, quote_date: date, 
                 output_filename: str = None) -> Path:
        """
        Génère l'image avec citation arabe et date
        """
        print(f"📝 Texte original: {quote_text[:50]}...")
        
        # Charger template
        img = Image.open(self.template_path).copy()
        draw = ImageDraw.Draw(img)
        
        # Calculer la largeur max pour le texte (80% de l'image)
        img_width = img.size[0]
        max_text_width = int(img_width * 0.85)
        
        # Dessiner la citation
        self._draw_quote(draw, quote_text, max_text_width)
        
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
    
    def _draw_quote(self, draw: ImageDraw.ImageDraw, text: str, max_width: int):
        """Dessine la citation arabe centrée"""
        config = self.quote_config
        
        # Découper en lignes (texte original, pas reshapé)
        lines = self._wrap_text_arabic(text, self.font_quote, max_width)
        print(f"   Nombre de lignes: {len(lines)}")
        
        # Calculer hauteur totale
        line_height = config["font_size"] + config["line_spacing"]
        total_height = len(lines) * line_height
        
        # Position Y de départ (centré verticalement)
        start_y = config["position"][1] - (total_height // 2)
        
        for i, line in enumerate(lines):
            # RESHAPER la ligne complète maintenant
            display_line = self._reshape_arabic(line)
            print(f"   Ligne {i+1}: '{line[:40]}...'")
            
            # Calculer position X (centré horizontalement)
            bbox = self.font_quote.getbbox(display_line)
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
    
    def _draw_date(self, draw: ImageDraw.ImageDraw, quote_date: date):
        """Dessine la date en style tunisien"""
        config = self.date_config
        
        # Mois tunisiens
        tunisian_months = {
            1: "جانفي", 2: "فيفري", 3: "مارس", 4: "أفريل",
            5: "ماي", 6: "جوان", 7: "جويلية", 8: "أوت",
            9: "سبتمبر", 10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر"
        }
        
        # Jours arabes
        arabic_days = {
            0: "الإثنين", 1: "الثلاثاء", 2: "الأربعاء", 3: "الخميس",
            4: "الجمعة", 5: "السبت", 6: "الأحد"
        }
        
        # Construire la date (chiffres normaux pour style tunisien)
        day_name = arabic_days[quote_date.weekday()]
        day_num = quote_date.day
        month_name = tunisian_months[quote_date.month]
        year = quote_date.year
        
        date_text = f"{day_name} {day_num} {month_name} {year}"
        print(f"📅 Date originale: {date_text}")
        
        # Reshaper la date
        display_date = self._reshape_arabic(date_text)
        print(f"📅 Date reshapée: {display_date}")
        
        # Centrer la date
        bbox = self.font_date.getbbox(display_date)
        text_width = bbox[2] - bbox[0]
        x = config["position"][0] - (text_width // 2)
        y = config["position"][1]
        
        # Dessiner avec ombre
        draw.text((x + 2, y + 2), display_date, font=self.font_date, fill="#000000")
        draw.text((x, y), display_date, font=self.font_date, fill=config["color"])


# === TEST ===
if __name__ == "__main__":
    generator = ImageGenerator()
    
    test_quote = "خمس عبارات يحب الزوج سمعها من زوجته: أنت وسيم، بوجودك بحياتي أنا أكثر سعادة"
    
    generator.generate(
        quote_text=test_quote,
        quote_date=date(2026, 1, 19)
    )
    print("✅ Test terminé!")
