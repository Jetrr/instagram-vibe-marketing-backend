# utils/font_loader.py

from PIL import ImageFont
import os

FONT_DIR = os.path.join("assets","fonts", "static")

def montserrat(weight="Bold", size=80, italic=False):
    name = "Montserrat-"
    if weight.lower() == "black":
        name += "Black"
    elif weight.lower() == "extrabold":
        name += "ExtraBold"
    elif weight.lower() == "bold":
        name += "Bold"
    elif weight.lower() == "semibold":
        name += "SemiBold"
    elif weight.lower() == "medium":
        name += "Medium"
    elif weight.lower() == "regular":
        name += "Regular"
    elif weight.lower() == "light":
        name += "Light"
    else:
        name += "Regular"
    if italic:
        name += "Italic"
    name += ".ttf"
    path = os.path.join(FONT_DIR, name)
    return ImageFont.truetype(path, size)