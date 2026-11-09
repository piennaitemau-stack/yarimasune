#!/usr/bin/env python3
"""Generate launcher icons for こども学習."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "android" / "app" / "src" / "main" / "res"
FONT = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"

DENSITIES = {
    "mdpi": 1,
    "hdpi": 1.5,
    "xhdpi": 2,
    "xxhdpi": 3,
    "xxxhdpi": 4,
}


def rounded_rect(draw: ImageDraw.ImageDraw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def make_glyph(size: int, *, round_mask: bool) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    bg = (251, 191, 36, 255)  # amber-400
    cream = (255, 251, 235, 255)
    brown = (120, 53, 15, 255)
    orange = (234, 88, 12, 255)
    star = (255, 237, 74, 255)

    pad = int(size * 0.08)
    radius = int(size * 0.22)
    if round_mask:
        draw.ellipse([pad, pad, size - pad, size - pad], fill=bg)
    else:
        rounded_rect(draw, [pad, pad, size - pad, size - pad], radius, bg)

    # inner cream circle
    inner = int(size * 0.18)
    draw.ellipse([inner, inner, size - inner, size - inner], fill=cream)

    font_size = int(size * 0.46)
    font = ImageFont.truetype(FONT, font_size)
    text = "学"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (size - tw) / 2 - bbox[0]
    ty = (size - th) / 2 - bbox[1] + size * 0.02
    draw.text((tx, ty), text, font=font, fill=brown)

    # small star in the corner
    cx, cy = size * 0.78, size * 0.22
    r = size * 0.08
    points = []
    import math

    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rad = r if i % 2 == 0 else r * 0.42
        points.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(points, fill=star, outline=orange)

    return img


def make_foreground(size: int) -> Image.Image:
    """Adaptive-icon foreground. Safe zone is the center 66%."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cream = (255, 251, 235, 255)
    brown = (120, 53, 15, 255)
    orange = (234, 88, 12, 255)
    star = (255, 237, 74, 255)

    inner = int(size * 0.22)
    draw.ellipse([inner, inner, size - inner, size - inner], fill=cream)

    font_size = int(size * 0.38)
    font = ImageFont.truetype(FONT, font_size)
    text = "学"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (size - tw) / 2 - bbox[0]
    ty = (size - th) / 2 - bbox[1] + size * 0.015
    draw.text((tx, ty), text, font=font, fill=brown)

    import math

    cx, cy = size * 0.70, size * 0.30
    r = size * 0.07
    points = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rad = r if i % 2 == 0 else r * 0.42
        points.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(points, fill=star, outline=orange)
    return img


def save(img: Image.Image, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG")


def main():
    for name, scale in DENSITIES.items():
        legacy = int(48 * scale)
        fg = int(108 * scale)
        folder = RES / f"mipmap-{name}"
        save(make_glyph(legacy, round_mask=False), folder / "ic_launcher.png")
        save(make_glyph(legacy, round_mask=True), folder / "ic_launcher_round.png")
        save(make_foreground(fg), folder / "ic_launcher_foreground.png")
    print("icons written under", RES)


if __name__ == "__main__":
    main()
