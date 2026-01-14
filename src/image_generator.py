"""
Generates Instagram images with dynamic text and date
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import date
from pathlib import Path
import textwrap
import sys

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
        
        # Load fonts
        self.font_quote = ImageFont.truetype(
            str(FONT_QUOTE), 
            self.quote_config["font_size"]
        )
        self.font_date = ImageFont.truetype(
            str(FONT_DATE), 
            self.date_config["font_size"]
        )
    
    def generate(self, quote_text: str, quote_date: date, 
                 output_filename: str = None) -> Path:
        """
        Generate image with quote and date
        
        Args:
            quote_text: The quote to display
            quote_date: Date to display on image
            output_filename: Optional custom filename
        
        Returns:
            Path to generated image
        """
        # Load template
        img = Image.open(self.template_path).copy()
        draw = ImageDraw.Draw(img)
        
        # Draw quote text
        self._draw_quote(draw, quote_text)
        
        # Draw date
        self._draw_date(draw, quote_date)
        
        # Save image
        if output_filename is None:
            output_filename = f"post_{quote_date.strftime('%Y%m%d')}.png"
        
        output_path = OUTPUT_DIR / output_filename
        OUTPUT_DIR.mkdir(exist_ok=True)
        
        img.save(output_path, quality=IMAGE_QUALITY)
        print(f"🖼️  Generated image: {output_path}")
        
        return output_path
    
    def _draw_quote(self, draw: ImageDraw, text: str):
        """Draw centered, multi-line quote with shadow"""
        config = self.quote_config
        
        # Wrap text into lines
        lines = textwrap.wrap(text, width=config["max_width"])
        
        # Calculate dimensions
        line_height = config["font_size"] + config["line_spacing"]
        total_height = len(lines) * line_height
        
        # Starting Y (vertically centered)
        start_y = config["position"][1] - (total_height // 2)
        
        for i, line in enumerate(lines):
            # Calculate X (horizontally centered)
            bbox = draw.textbbox((0, 0), line, font=self.font_quote)
            line_width = bbox[2] - bbox[0]
            x = config["position"][0] - (line_width // 2)
            y = start_y + (i * line_height)
            
            # Draw shadow
            shadow_offset = config["shadow_offset"]
            draw.text(
                (x + shadow_offset, y + shadow_offset),
                line,
                font=self.font_quote,
                fill=config["shadow_color"]
            )
            
            # Draw main text
            draw.text(
                (x, y),
                line,
                font=self.font_quote,
                fill=config["color"]
            )
    
    def _draw_date(self, draw: ImageDraw, quote_date: date):
        """Draw date in bottom area"""
        config = self.date_config
        
        # Format date
        date_text = quote_date.strftime(config["format"])
        
        # Draw with right alignment
        draw.text(
            config["position"],
            date_text,
            font=self.font_date,
            fill=config["color"],
            anchor="rm"  # Right-middle anchor
        )


# === QUICK TEST ===
if __name__ == "__main__":
    from datetime import date
    
    generator = ImageGenerator()
    generator.generate(
        quote_text="Data is the new oil, but insight is the refinery.",
        quote_date=date.today()
    )
    print("✅ Test image generated!")