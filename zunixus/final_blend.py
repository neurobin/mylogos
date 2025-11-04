#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

# Load the original backup
img = Image.open('cover_backup.png')
width, height = img.size

pixels = img.load()

text_area_x_start = 1800
text_area_x_end = 3500
text_area_y_start = 150
text_area_y_end = 950

# Sample corner colors from clean background areas
# Top-left corner (clean area)
tl_color = img.getpixel((100, 150))[:3]
# Bottom-left corner (clean area)
bl_color = img.getpixel((100, 900))[:3]

# For the right side, we need to interpolate based on the gradient
# Sample from the right side but in a clean area (below the text)
tr_color = img.getpixel((3400, 150))[:3]
br_color = img.getpixel((3400, 900))[:3]

print(f"TL: {tl_color}, BL: {bl_color}, TR: {tr_color}, BR: {br_color}")

# Apply bilinear interpolation for each pixel
for y in range(text_area_y_start, min(text_area_y_end, height)):
    # Normalize y position (0 to 1)
    y_factor = (y - text_area_y_start) / (text_area_y_end - text_area_y_start)

    for x in range(text_area_x_start, min(text_area_x_end, width)):
        # Normalize x position (0 to 1)
        x_factor = (x - text_area_x_start) / (text_area_x_end - text_area_x_start)

        # Bilinear interpolation
        # Top edge color (interpolate between TL and TR)
        top_r = int(tl_color[0] * (1 - x_factor) + tr_color[0] * x_factor)
        top_g = int(tl_color[1] * (1 - x_factor) + tr_color[1] * x_factor)
        top_b = int(tl_color[2] * (1 - x_factor) + tr_color[2] * x_factor)

        # Bottom edge color (interpolate between BL and BR)
        bottom_r = int(bl_color[0] * (1 - x_factor) + br_color[0] * x_factor)
        bottom_g = int(bl_color[1] * (1 - x_factor) + br_color[1] * x_factor)
        bottom_b = int(bl_color[2] * (1 - x_factor) + br_color[2] * x_factor)

        # Final color (interpolate between top and bottom)
        final_r = int(top_r * (1 - y_factor) + bottom_r * y_factor)
        final_g = int(top_g * (1 - y_factor) + bottom_g * y_factor)
        final_b = int(top_b * (1 - y_factor) + bottom_b * y_factor)

        pixels[x, y] = (final_r, final_g, final_b)

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
        subtitle_path = path.replace('BoldOblique', 'Oblique')
        try:
            subtitle_font = ImageFont.truetype(subtitle_path, 70)
        except:
            subtitle_font = ImageFont.truetype(path, 70)
        break
    except:
        continue

if not title_font:
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

# Save
img.save('cover.png')
print("Cover updated with perfect bilinear blend!")
