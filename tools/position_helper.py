# tools/position_helper.py
"""
Run this to find the right coordinates for your template
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_position_guide(template_path: str, output_path: str = "position_guide.png"):
    """Creates a visual grid to help position text"""
    
    img = Image.open(template_path)
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Draw grid every 100 pixels
    for x in range(0, width, 100):
        # Vertical lines
        color = "red" if x % 500 == 0 else "gray"
        draw.line([(x, 0), (x, height)], fill=color, width=1)
        draw.text((x + 5, 10), str(x), fill="red")
    
    for y in range(0, height, 100):
        # Horizontal lines
        color = "red" if y % 500 == 0 else "gray"
        draw.line([(0, y), (width, y)], fill=color, width=1)
        draw.text((10, y + 5), str(y), fill="red")
    
    # Mark center
    center_x, center_y = width // 2, height // 2
    draw.ellipse(
        [center_x - 15, center_y - 15, center_x + 15, center_y + 15], 
        fill="blue"
    )
    draw.text(
        (center_x + 20, center_y), 
        f"CENTER\n({center_x}, {center_y})", 
        fill="blue"
    )
    
    # Suggested positions
    suggestions = {
        "Quote (center)": (center_x, center_y - 50),
        "Date (bottom-right)": (width - 130, height - 100),
        "Date (bottom-left)": (130, height - 100),
    }
    
    for label, pos in suggestions.items():
        draw.ellipse(
            [pos[0] - 8, pos[1] - 8, pos[0] + 8, pos[1] + 8],
            fill="green"
        )
        draw.text((pos[0] + 15, pos[1] - 10), label, fill="green")
    
    img.save(output_path)
    
    print(f"""
╔══════════════════════════════════════════════════════╗
║            📐 POSITION GUIDE GENERATED               ║
╠══════════════════════════════════════════════════════╣
║  Image size: {width} x {height}
║  Center: ({center_x}, {center_y})
║  
║  Suggested positions:
║  • Quote text: ({center_x}, {center_y - 50})
║  • Date (bottom-right): ({width - 130}, {height - 100})
║  
║  Guide saved to: {output_path}
║  
║  → Open the image and adjust config.py accordingly
╚══════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        template = sys.argv[1]
    else:
        template = "templates/template.png"
    
    create_position_guide(template)