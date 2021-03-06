from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

W = 1280
H = 720


def draw_thumbnail(title: str, subtitle: str, other_subtitle: str) -> None:
    img = Image.new('RGB', (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    title_font = ImageFont.truetype("./OpenSans-Regular.ttf", 140)
    title_w, title_h = draw.textsize(title, font=title_font)
    draw.text(((W - title_w) / 2, (H - title_h) / 2 - 140), title, font=title_font, fill=(255, 255, 255))

    subtitle_font = ImageFont.truetype("./OpenSans-Regular.ttf", 100)
    subtitle_w, subtitle_h = draw.textsize(subtitle, font=subtitle_font)
    draw.text(((W - subtitle_w) / 2, (H - subtitle_h) / 2 + 50), subtitle, font=subtitle_font, fill=(255, 255, 255))

    subtitle_font = ImageFont.truetype("./OpenSans-Regular.ttf", 80)
    subtitle_w, subtitle_h = draw.textsize(other_subtitle, font=subtitle_font)
    draw.text(((W - subtitle_w) / 2, (H - subtitle_h) / 2 + 180), other_subtitle, font=subtitle_font, fill=(255, 255, 255))

    with open('thumbnail.jpg', 'w') as outfile:
        img.save(outfile, 'JPEG')


