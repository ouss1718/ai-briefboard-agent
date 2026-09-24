"""Render an original, text-led Instagram carousel at 1080 x 1350."""
from pathlib import Path
from urllib.parse import urlsplit

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
NAVY = (8, 16, 32)
CREAM = (244, 241, 229)
LIME = (204, 244, 102)
MUTED = (169, 185, 190)
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(str(FONT_DIR / name), size)


def draw_lines(draw, text, xy, max_width, size, color, bold=False, spacing=18):
    x, y = xy
    words = text.split()
    current = ""
    lines = []
    for word in words:
        proposed = (current + " " + word).strip()
        if draw.textbbox((0, 0), proposed, font=font(size, bold))[2] <= max_width:
            current = proposed
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    for line in lines:
        draw.text((x, y), line, font=font(size, bold), fill=color)
        y += size + spacing
    return y


def base(index, total, date, label):
    image = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(image)
    for i in range(18):
        x = 780 + i * 43
        draw.line((x, 0, x - 350, H), fill=(16, 31, 47), width=2)
    draw.rounded_rectangle((64, 64, 174, 174), radius=29, fill=LIME)
    draw.text((95, 74), "B", font=font(72, True), fill=NAVY)
    draw.text((198, 104), "THE AI BRIEFBOARD", font=font(33, True), fill=CREAM)
    draw.line((64, 210, 1016, 210), fill=(56, 75, 87), width=2)
    draw.text((66, 255), label.upper(), font=font(29, True), fill=LIME)
    draw.line((64, 1226, 1016, 1226), fill=(56, 75, 87), width=2)
    draw.text((66, 1264), "@THEAIBRIEFBOARD", font=font(25, True), fill=MUTED)
    draw.text((810, 1264), f"{index:02d} / {total:02d}", font=font(25, True), fill=MUTED)
    return image, draw


def render_carousel(stories, date, output, config):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    total = len(stories) + 2
    names = []

    im, d = base(1, total, date, "the daily brief · " + date)
    y = draw_lines(d, "AI news,", (66, 420), 950, 108, CREAM, True)
    draw_lines(d, "made clear.", (66, y + 10), 950, 108, LIME, True)
    count = f"{len(stories)} update" + ("" if len(stories) == 1 else "s")
    d.text((68, 954), f"{count}. Original sources.", font=font(40), fill=CREAM)
    d.text((68, 1022), "Swipe for what matters  →", font=font(38), fill=MUTED)
    names.append("01_cover.png")
    im.save(output / names[-1], optimize=True)

    for index, story in enumerate(stories, 2):
        # Shrink text step by step until the slide fits above the footer line.
        for head, body, why in [(75, 43, 35), (68, 39, 32), (62, 35, 29), (56, 32, 27)]:
            im, d = base(index, total, date, f"update {index - 1:02d}")
            y = draw_lines(d, story["headline"], (66, 376), 930, head, CREAM, True, 22)
            d.rounded_rectangle((66, y + 40, 1014, y + 50), radius=5, fill=LIME)
            y = draw_lines(d, story["summary"], (66, y + 100), 925, body, CREAM, spacing=16)
            y = max(y + 45, 840)
            d.text((66, y), "WHY IT MATTERS", font=font(28, True), fill=LIME)
            y = draw_lines(d, story["why_it_matters"], (66, y + 54), 925, why, CREAM, spacing=14)
            if y <= 1200:
                break
        names.append(f"{index:02d}_story.png")
        im.save(output / names[-1], optimize=True)

    im, d = base(total, total, date, "original sources")
    d.text((66, 385), "Go to the source.", font=font(70, True), fill=CREAM)
    for i, story in enumerate(stories):
        y = 580 + i * 164
        d.rounded_rectangle((66, y, 144, y + 76), radius=20, fill=LIME)
        d.text((83, y + 15), f"{i+1:02d}", font=font(32, True), fill=NAVY)
        domain = urlsplit(story["source_url"]).hostname or "source"
        d.text((170, y + 4), domain[:37], font=font(35, True), fill=CREAM)
        d.text((170, y + 54), story["announcement_date"], font=font(29), fill=MUTED)
    d.text((66, 1144), "Full source links in the caption.", font=font(30), fill=LIME)
    names.append(f"{total:02d}_sources.png")
    im.save(output / names[-1], optimize=True)
    return names
