# styles/category_1.py

from PIL import Image, ImageDraw
from utils.font_loader import montserrat
import os

BG_DIR = "assets/backgrounds/posters/category_1"
ASPECT = (1080, 1350)

def wrap_text(text, font, max_width):
    lines = []
    for paragraph in text.split('\n'):
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
    if getattr(slide, "cover_title", None):
        cover_title = slide.cover_title
        cover_subtitle = slide.cover_subtitle or ""
    else:
        myth_font = montserrat("Black", 85)                 
        myth_quote_font = montserrat("Bold", 53)            
        truth_font = montserrat("Black", 80)                
        truth_body_font = montserrat("Bold", 58)            

    white = "#fff"
    black = "#282828"
    pink = "#fbaccf"
    accent_pink = "#ffb3c5"

    if idx == 0:
        bg = Image.open(os.path.join(BG_DIR, "start.png")).convert("RGBA")
        draw = ImageDraw.Draw(bg)

        dark_mode = False

        main_font = montserrat("Black", 150)
        left_pad = 80
        y = 220

        words = cover_title.split()
        lines = []

        if len(words) >= 3:
            lines.append(" ".join(words[:2]))
            rest = words[2:]
            for w in rest:
                lines.append(w)
        else:
            lines = [" ".join(words)]

        for line in lines:
            bbox = main_font.getbbox(line)
            height = bbox[3] - bbox[1]
            draw.text((left_pad, y), line, font=main_font, fill=white)
            y += height + 20

        return bg.convert("RGB")
    
    elif idx == 6:
        if getattr(slide, "end_title", None):
            end_title = slide.end_title or ""
        bg = Image.open(os.path.join(BG_DIR, "end.png")).convert("RGBA")

        return bg.convert("RGB")
    
    elif idx % 2 == 0:
        bg = Image.open(os.path.join(BG_DIR, "mid_2.png")).convert("RGBA")
        draw = ImageDraw.Draw(bg)
        heading_color = "#ffff"
        accent_pink = "#3a3a3a"

        # Block layout
        block_padding_x = 36
        block_width = ASPECT[0] // 2 - block_padding_x * 2  # Each block takes about half width with padding

        myth_label_font   = montserrat("Black", 120)
        myth_quote_font   = montserrat("ExtraBold", 60)
        truth_label_font  = montserrat("Black", 120)
        truth_body_font   = montserrat("ExtraBold", 60)

        myth_top = 100
        truth_top = myth_top * 6

        # --- Left Block (MYTH) ---
        # Myth label
        draw.text(
            (block_padding_x, myth_top),
            slide.myth_title.upper(),
            font=myth_label_font,
            fill=accent_pink,
        )
        # measure myth label height for stacking
        myth_label_height = myth_label_font.getbbox(slide.myth_title.upper())[3] - myth_label_font.getbbox(slide.myth_title.upper())[1]
        myth_quote_y = myth_top + myth_label_height + 50

        # Myth quote, word-wrapped in left block
        myth_quote_width = block_width
        myth_quote_wrapped = wrap_text(str(slide.myth_quote), myth_quote_font, myth_quote_width)
        draw.multiline_text(
            (block_padding_x, myth_quote_y),
            myth_quote_wrapped,
            font=myth_quote_font,
            fill=heading_color,
            spacing=10,
            align="left",
        )

        # --- Right Block (TRUTH) ---
        block_shift = ASPECT[0] // 2 + block_padding_x
        draw.text(
            (block_shift, truth_top),
            slide.truth_label.upper(),
            font=truth_label_font,
            fill=accent_pink,
        )
        truth_label_height = truth_label_font.getbbox(slide.truth_label.upper())[3] - truth_label_font.getbbox(slide.truth_label.upper())[1]
        truth_body_y = truth_top + truth_label_height + 50

        truth_body_width = block_width
        truth_body_wrapped = wrap_text(str(slide.truth_body), truth_body_font, truth_body_width)
        draw.multiline_text(
            (block_shift, truth_body_y),
            truth_body_wrapped,
            font=truth_body_font,
            fill=heading_color,
            spacing=10,
            align="left"
        )

    else:
        bg = Image.open(os.path.join(BG_DIR, "mid_1.png")).convert("RGBA")
        draw = ImageDraw.Draw(bg)
        white = "#fff"
        accent_pink = "#ffb3c5"

        # Block layout
        block_padding_x = 36
        block_width = ASPECT[0] // 2 - block_padding_x * 2  # Each block takes about half width with padding

        myth_label_font   = montserrat("Black", 120)
        myth_quote_font   = montserrat("ExtraBold", 60)
        truth_label_font  = montserrat("Black", 120)
        truth_body_font   = montserrat("ExtraBold", 60)

        myth_top = 100
        truth_top = myth_top * 6

        # --- Left Block (MYTH) ---
        # Myth label
        draw.text(
            (block_padding_x, myth_top),
            slide.myth_title.upper(),
            font=myth_label_font,
            fill=accent_pink,
        )
        # measure myth label height for stacking
        myth_label_height = myth_label_font.getbbox(slide.myth_title.upper())[3] - myth_label_font.getbbox(slide.myth_title.upper())[1]
        myth_quote_y = myth_top + myth_label_height + 50

        # Myth quote, word-wrapped in left block
        myth_quote_width = block_width
        myth_quote_wrapped = wrap_text(str(slide.myth_quote), myth_quote_font, myth_quote_width)
        draw.multiline_text(
            (block_padding_x, myth_quote_y),
            myth_quote_wrapped,
            font=myth_quote_font,
            fill=white,
            spacing=10,
            align="left",
        )

        # --- Right Block (TRUTH) ---
        block_shift = ASPECT[0] // 2 + block_padding_x
        draw.text(
            (block_shift, truth_top),
            slide.truth_label.upper(),
            font=truth_label_font,
            fill=accent_pink,
        )
        truth_label_height = truth_label_font.getbbox(slide.truth_label.upper())[3] - truth_label_font.getbbox(slide.truth_label.upper())[1]
        truth_body_y = truth_top + truth_label_height + 50

        truth_body_width = block_width
        truth_body_wrapped = wrap_text(str(slide.truth_body), truth_body_font, truth_body_width)
        draw.multiline_text(
            (block_shift, truth_body_y),
            truth_body_wrapped,
            font=truth_body_font,
            fill=white,
            spacing=10,
            align="left"
        )

    return bg.convert("RGB")
