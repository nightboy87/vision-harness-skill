from __future__ import annotations

from typing import List, Dict
from PIL import Image


def run_ocr(img: Image.Image) -> List[Dict]:
    """Run OCR with optional engines.

    Priority:
    1. rapidocr_onnxruntime, if installed
    2. pytesseract, if installed and system tesseract is available
    3. return empty list with no hard failure
    """
    rapid = _try_rapidocr(img)
    if rapid:
        return rapid
    tess = _try_pytesseract(img)
    if tess:
        return tess
    return []


def _try_rapidocr(img: Image.Image) -> List[Dict]:
    try:
        import numpy as np
        from rapidocr_onnxruntime import RapidOCR
    except Exception:
        return []

    try:
        engine = RapidOCR()
        result, _ = engine(np.array(img))
        blocks = []
        if not result:
            return []
        for i, item in enumerate(result, start=1):
            points, text, conf = item[0], str(item[1]), float(item[2])
            xs = [int(p[0]) for p in points]
            ys = [int(p[1]) for p in points]
            blocks.append({
                "id": f"text_{i:03d}",
                "text": text.strip(),
                "bbox": [min(xs), min(ys), max(xs), max(ys)],
                "confidence": round(conf, 3),
                "region_id": ""
            })
        return [b for b in blocks if b["text"]]
    except Exception:
        return []


def _try_pytesseract(img: Image.Image) -> List[Dict]:
    try:
        import pytesseract
        from pytesseract import Output
    except Exception:
        return []

    try:
        data = pytesseract.image_to_data(img, output_type=Output.DICT)
        blocks = []
        n = len(data.get("text", []))
        for i in range(n):
            text = str(data["text"][i]).strip()
            if not text:
                continue
            try:
                conf = float(data["conf"][i])
            except Exception:
                conf = -1.0
            if conf < 0:
                continue
            x, y, w, h = int(data["left"][i]), int(data["top"][i]), int(data["width"][i]), int(data["height"][i])
            blocks.append({
                "id": f"text_{len(blocks)+1:03d}",
                "text": text,
                "bbox": [x, y, x + w, y + h],
                "confidence": round(conf / 100.0, 3),
                "region_id": ""
            })
        return blocks
    except Exception:
        return []
