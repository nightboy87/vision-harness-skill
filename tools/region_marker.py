from __future__ import annotations

from pathlib import Path
from typing import List, Dict
from PIL import Image, ImageDraw, ImageFont


def annotate_regions(img: Image.Image, regions: List[Dict], ocr_blocks: List[Dict], out_path: str) -> None:
    canvas = img.copy().convert("RGB")
    draw = ImageDraw.Draw(canvas)
    font = _font(18)
    small_font = _font(14)

    for region in regions:
        x1, y1, x2, y2 = region["bbox"]
        color = "red" if region.get("visual_weight") == "high" else "orange" if region.get("visual_weight") == "medium" else "blue"
        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
        label = region["id"]
        draw.rectangle([x1, y1, min(x1 + 110, x2), min(y1 + 24, y2)], fill="white", outline=color)
        draw.text((x1 + 4, y1 + 3), label, fill=color, font=font)

    for block in ocr_blocks:
        x1, y1, x2, y2 = block["bbox"]
        draw.rectangle([x1, y1, x2, y2], outline="green", width=2)
        draw.text((x1, max(0, y1 - 16)), block["id"], fill="green", font=small_font)

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path)


def crop_regions(img: Image.Image, regions: List[Dict], crops_dir: str) -> None:
    path = Path(crops_dir)
    path.mkdir(parents=True, exist_ok=True)
    for region in regions:
        x1, y1, x2, y2 = region["bbox"]
        crop = img.crop((x1, y1, x2, y2))
        crop.save(path / f"{region['id']}.png")


def _font(size: int):
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except Exception:
        return ImageFont.load_default()
