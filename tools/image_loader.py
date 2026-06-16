from __future__ import annotations

import base64
import hashlib
import os
import re
from io import BytesIO
from pathlib import Path
from typing import Tuple

from PIL import Image


def load_image(input_value: str) -> Tuple[Image.Image, dict]:
    """Load image from path, base64, or data URL.

    Returns RGB PIL image and source metadata.
    """
    source = {
        "input_type": "unknown",
        "filename": "inline_image",
        "sha256": ""
    }

    if os.path.exists(input_value):
        path = Path(input_value)
        raw = path.read_bytes()
        img = Image.open(BytesIO(raw)).convert("RGB")
        source.update({
            "input_type": "path",
            "filename": path.name,
            "sha256": hashlib.sha256(raw).hexdigest()
        })
        return img, source

    data_url_match = re.match(r"^data:image\/([a-zA-Z0-9.+-]+);base64,(.*)$", input_value, re.DOTALL)
    if data_url_match:
        raw = base64.b64decode(data_url_match.group(2))
        img = Image.open(BytesIO(raw)).convert("RGB")
        source.update({
            "input_type": f"data_url:image/{data_url_match.group(1)}",
            "filename": "data_url_image",
            "sha256": hashlib.sha256(raw).hexdigest()
        })
        return img, source

    try:
        raw = base64.b64decode(input_value)
        img = Image.open(BytesIO(raw)).convert("RGB")
        source.update({
            "input_type": "base64",
            "filename": "base64_image",
            "sha256": hashlib.sha256(raw).hexdigest()
        })
        return img, source
    except Exception as exc:
        raise ValueError("Cannot load image. Provide a local path, raw base64, or data:image/...;base64,... URL.") from exc
