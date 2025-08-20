from PIL import Image, ImageDraw
from utils.font_loader import montserrat
import os

BG_DIR = "assets/backgrounds/posters/category_2"
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

def render_slide(slide, idx):
    white = "#fff"
    black = "#282828"
    handle_font = montserrat("Bold", 40)
    body_font = montserrat("Black", 85)

    # Slide 0: the cat cover, center text on the sign
    if idx == 0:
        bg = Image.open(os.path.join(BG_DIR, "start.png")).convert("RGBA")
        draw = ImageDraw.Draw(bg)
        big_font = montserrat("Black", 60)
        text = getattr(slide, "cover_title", "")
        text_box = (200, 790, 880, 1070)  # adjust if needed for your cat sign
        wrapped = wrap_text(text, big_font, text_box[2] - text_box[0])
        # vertically and horizontally center each line
        lines = wrapped.split('\n')
        line_spacing = 8
        total_h = sum((big_font.getbbox(line)[3] - big_font.getbbox(line)[1]) for line in lines) + (len(lines)-1)*line_spacing
        y_start = text_box[1] + ((text_box[3]-text_box[1])-total_h)//2
        for line in lines:
            bbox = big_font.getbbox(line)
            line_w = bbox[2] - bbox[0]
            line_h = bbox[3] - bbox[1]
            x = text_box[0] + ((text_box[2] - text_box[0]) - line_w)//2
            draw.text((x, y_start), line, font=big_font, fill=black)
            y_start += line_h + line_spacing
        return bg.convert("RGB")

    # Last slide: end
    if getattr(slide, "end_title", None):
        bg = Image.open(os.path.join(BG_DIR, "end.png")).convert("RGBA")
        return bg.convert("RGB")
    
    # All other slides: alternate bg, center white text
    _mid_file = "mid_1.png" if idx % 2 == 1 else "mid_2.png"
    bg = Image.open(os.path.join(BG_DIR, _mid_file)).convert("RGBA")
    draw = ImageDraw.Draw(bg)
    text = getattr(slide, "content", "")
    print(f"Rendering slide {idx} with text: {text}")
    text_box = (80, 280, ASPECT[0]-80, ASPECT[1]-220)
    wrapped = wrap_text(text, body_font, text_box[2] - text_box[0])
    lines = wrapped.split('\n')
    line_spacing = 20
    total_h = sum((body_font.getbbox(line)[3] - body_font.getbbox(line)[1]) for line in lines) + (len(lines)-1)*line_spacing
    y_start = text_box[1] + ((text_box[3]-text_box[1])-total_h)//2
    for line in lines:
        bbox = body_font.getbbox(line)
        line_w = bbox[2] - bbox[0]
        line_h = bbox[3] - bbox[1]
        x = text_box[0] + ((text_box[2] - text_box[0]) - line_w)//2
        draw.text((x, y_start), line, font=body_font, fill=white)
        y_start += line_h + line_spacing
    return bg.convert("RGB")