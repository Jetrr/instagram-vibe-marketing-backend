from PIL import Image, ImageDraw
from utils.font_loader import montserrat
import os

BG_DIR = "assets/backgrounds/posters/category_3"
ASPECT = (1080, 1350)

def wrap_text(text, font, max_width):
    lines = []
    for paragraph in (text or "").split('\n'):
        words = paragraph.split()
        if not words:
            lines.append('')
            continue
        line = []
        while words:
            line.append(words.pop(0))
            test_line = ' '.join(line + words[:1])
            bbox = font.getbbox(test_line)
            test_width = bbox[2] - bbox[0]
            if test_width > max_width:
                lines.append(' '.join(line))
                line = []
        if line:
            lines.append(' '.join(line))
    return '\n'.join(lines)

def center_draw_text(draw, text, font, fill, box, line_spacing=16):
    # Draw multi-line text centered vertically and horizontally inside the box
    lines = text.split('\n')
    total_h = sum((font.getbbox(line)[3] - font.getbbox(line)[1]) for line in lines) + (len(lines)-1)*line_spacing
    y = box[1] + ((box[3]-box[1]) - total_h) // 2
    for line in lines:
        bbox = font.getbbox(line)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = box[0] + ((box[2] - box[0]) - w) // 2
        draw.text((x, y), line, font=font, fill=fill)
        y += h + line_spacing

def render_slide(slide, idx):
    pink = "#ffb3c5"
    white = "#fff"
    black = "#282828"
    big_font = montserrat("Black", 85)
    # Padding for main centered text
    text_box = (100, 240, ASPECT[0]-100, ASPECT[1]-220)
    # Emoji below text if needed
    emoji_offset_y = 40

    # --- START SLIDE ---
    if idx == 0:
        bg = Image.open(os.path.join(BG_DIR, "start.png")).convert("RGBA")
        draw = ImageDraw.Draw(bg)
        text = getattr(slide, "cover_title", "")
        wrapped = wrap_text(text, big_font, text_box[2] - text_box[0])
        center_draw_text(draw, wrapped, big_font, pink, text_box, line_spacing=18)
        # Optionally: add emoji below the final text line here by your needs!
        return bg.convert("RGB")

    # --- END SLIDE ---
    if getattr(slide, "end_title", None):
        bg = Image.open(os.path.join(BG_DIR, "end.png")).convert("RGBA")
        # If you want text on end slide, repeat centering here.
        return bg.convert("RGB")

    # --- MID SLIDES ---    
    # idx:  1(mid_1/white), 2(mid_2/pink), 3(mid_1/white), 4(mid_2/pink), ...
    is_mid1 = idx % 2 == 1
    mid_bg = "mid_1.png" if is_mid1 else "mid_2.png"
    bg = Image.open(os.path.join(BG_DIR, mid_bg)).convert("RGBA")
    draw = ImageDraw.Draw(bg)
    text = getattr(slide, "content", "")
    wrapped = wrap_text(text, big_font, text_box[2] - text_box[0])
    color = white if is_mid1 else pink
    center_draw_text(draw, wrapped, big_font, color, text_box, line_spacing=18)
    return bg.convert("RGB")