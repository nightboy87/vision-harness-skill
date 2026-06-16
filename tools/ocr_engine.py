from __future__ import annotations

from typing import List, Dict
from PIL import Image


def run_ocr(img: Image.Image) -> List[Dict]:
    """Run OCR with optional engines.

    Priority:
    1. paddleocr, if installed. Usually better for Chinese UI/flowchart screenshots.
    2. rapidocr_onnxruntime, if installed. Lightweight and fast.
    3. pytesseract, if installed and system tesseract is available.
    4. return empty list with no hard failure.
    """
    paddle = _try_paddleocr(img)
    if paddle:
        return paddle
    rapid = _try_rapidocr(img)
    if rapid:
        return rapid
    tess = _try_pytesseract(img)
    if tess:
        return tess
    return []


def _try_paddleocr(img: Image.Image) -> List[Dict]:
    try:
        import numpy as np
        from paddleocr import PaddleOCR
    except Exception:
        return []

    try:
        # Constructor arguments differ slightly across PaddleOCR versions.
        try:
            engine = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)
        except TypeError:
            engine = PaddleOCR(use_angle_cls=True, lang="ch")
        result = engine.ocr(np.array(img), cls=True)
        blocks = []
        # Newer/older PaddleOCR versions may nest results differently.
        pages = result if result and isinstance(result, list) else []
        if pages and pages and isinstance(pages[0], list) and pages and pages[0] and isinstance(pages[0][0], list) and len(pages) == 1:
            items = pages[0]
        else:
            items = pages
        for item in items:
            try:
                points = item[0]
                text = str(item[1][0])
                conf = float(item[1][1])
            except Exception:
                continue
            xs = [int(p[0]) for p in points]
            ys = [int(p[1]) for p in points]
            if text.strip():
                blocks.append({
                    "id": f"text_{len(blocks)+1:03d}",
                    "text": text.strip(),
                    "bbox": [min(xs), min(ys), max(xs), max(ys)],
                    "confidence": round(conf, 3),
                    "region_id": ""
                })
        return blocks
    except Exception:
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
        for item in result:
            points, text, conf = item[0], str(item[1]), float(item[2])
            xs = [int(p[0]) for p in points]
            ys = [int(p[1]) for p in points]
            if text.strip():
                blocks.append({
                    "id": f"text_{len(blocks)+1:03d}",
                    "text": text.strip(),
                    "bbox": [min(xs), min(ys), max(xs), max(ys)],
                    "confidence": round(conf, 3),
                    "region_id": ""
                })
        return blocks
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
