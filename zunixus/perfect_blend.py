#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

# Load the original backup
img = Image.open('cover_backup.png')
width, height = img.size

# Copy actual background pixels from clean area (x=1000-1700 is clean, no logo)
# to the text area (x=1800-3500)
pixels = img.load()

text_area_x_start = 1800
text_area_x_end = 3500
text_area_y_start = 150
text_area_y_end = 950

# For each row, sample background from a clean horizontal slice
# and paint it across the text area
for y in range(text_area_y_start, min(text_area_y_end, height)):
    # Sample from clean area at x=100 (far left, clean background)
    for x in range(text_area_x_start, min(text_area_x_end, width)):
        # Get color from clean area at same y position
        source_x = 100
        bg_color = img.getpixel((source_x, y))[:3]
        pixels[x, y] = bg_color

# Load fonts
font_paths = [
    '/usr/share/fonts/TTF/DejaVuSans-BoldOblique.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf',
]

title_font = None
subtitle_font = None

for path in font_paths:
    try:
        title_font = ImageFont.truetype(path, 220)
        # Try to find regular oblique for subtitle
        subtitle_path = path.replace('BoldOblique', 'Oblique')
        try:
            subtitle_font = ImageFont.truetype(subtitle_path, 70)
        except:
            subtitle_font = ImageFont.truetype(path, 70)
        break
    except:
        continue

if not title_font:
    # Fallback to bold
    for path in ['/usr/share/fonts/TTF/DejaVuSans-Bold.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']:
        try:
            title_font = ImageFont.truetype(path, 220)
            subtitle_font = ImageFont.truetype(path.replace('Bold', ''), 70)
            break
        except:
            continue

# Draw new text
draw = ImageDraw.Draw(img)
if title_font:
    draw.text((2000, 280), "Zunixus", fill='white', font=title_font)
    draw.text((2000, 530), "Zahid, u, and us", fill='white', font=subtitle_font)
else:
    print("Warning: Could not load fonts, using default")

# Save
img.save('cover.png')
print("Cover updated with perfect blend!")
