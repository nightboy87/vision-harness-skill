from __future__ import annotations

from typing import Dict, List
import numpy as np
from PIL import Image, ImageStat


def image_properties(img: Image.Image) -> Dict:
    w, h = img.size
    aspect = round(w / max(h, 1), 3)
    if aspect > 1.35:
        orientation = "landscape"
    elif aspect < 0.75:
        orientation = "portrait"
    else:
        orientation = "square_or_near_square"
    return {
        "width": w,
        "height": h,
        "aspect_ratio": aspect,
        "orientation": orientation,
        "megapixels": round(w * h / 1_000_000, 2)
    }


def color_features(img: Image.Image, palette_size: int = 6) -> Dict:
    small = img.resize((160, 160))
    gray = small.convert("L")
    gray_arr = np.array(gray).astype(np.float32)
    brightness = float(np.mean(gray_arr))
    contrast = float(np.std(gray_arr))
    stat = ImageStat.Stat(small)
    mean_rgb = [round(x, 2) for x in stat.mean]

    quantized = small.quantize(colors=palette_size)
    palette = quantized.getpalette()
    counts = quantized.getcolors() or []
    counts = sorted(counts, key=lambda x: x[0], reverse=True)
    total = max(sum(c for c, _ in counts), 1)
    dominant = []
    for count, idx in counts[:palette_size]:
        rgb = palette[idx * 3: idx * 3 + 3]
        dominant.append({
            "rgb": rgb,
            "hex": "#{:02x}{:02x}{:02x}".format(*rgb),
            "ratio": round(count / total, 3)
        })

    return {
        "mean_rgb": mean_rgb,
        "brightness_value": round(brightness, 2),
        "brightness": label(brightness, 85, 170, "dark", "medium", "bright"),
        "contrast_value": round(contrast, 2),
        "contrast": label(contrast, 35, 75, "low", "medium", "high"),
        "dominant_colors": dominant
    }


def edge_density(img: Image.Image) -> Dict:
    gray = img.convert("L").resize((320, 320))
    arr = np.array(gray).astype(np.float32)
    gx = np.abs(np.diff(arr, axis=1))
    gy = np.abs(np.diff(arr, axis=0))
    score = float((np.mean(gx) + np.mean(gy)) / 2.0)
    return {
        "value": round(score, 2),
        "label": label(score, 10, 24, "low", "medium", "high")
    }


def grid_regions(img: Image.Image, rows: int = 3, cols: int = 3) -> List[Dict]:
    w, h = img.size
    gray = img.convert("L").resize((cols * 120, rows * 120))
    arr = np.array(gray).astype(np.float32)
    cell_w, cell_h = 120, 120
    regions = []
    rid = 1
    for r in range(rows):
        for c in range(cols):
            cell = arr[r * cell_h:(r + 1) * cell_h, c * cell_w:(c + 1) * cell_w]
            bright = float(np.mean(cell))
            complexity = float(np.std(cell))
            x1 = int(c * w / cols)
            y1 = int(r * h / rows)
            x2 = int((c + 1) * w / cols)
            y2 = int((r + 1) * h / rows)
            regions.append({
                "id": f"region_{rid:03d}",
                "type_hint": "grid_cell",
                "bbox": [x1, y1, x2, y2],
                "visual_weight": label(complexity, 30, 65, "low", "medium", "high"),
                "contains_text_ids": [],
                "notes": f"{position_label(r, c)}; brightness={round(bright, 1)}, complexity={round(complexity, 1)}"
            })
            rid += 1
    return regions


def assign_text_to_regions(ocr_blocks: List[Dict], regions: List[Dict]) -> None:
    for block in ocr_blocks:
        cx = (block["bbox"][0] + block["bbox"][2]) / 2
        cy = (block["bbox"][1] + block["bbox"][3]) / 2
        for region in regions:
            x1, y1, x2, y2 = region["bbox"]
            if x1 <= cx <= x2 and y1 <= cy <= y2:
                block["region_id"] = region["id"]
                region.setdefault("contains_text_ids", []).append(block["id"])
                break


def infer_image_types(props: Dict, visual: Dict, ocr_blocks: List[Dict], regions: List[Dict]) -> List[Dict]:
    text = " ".join(b.get("text", "") for b in ocr_blocks).lower()
    hyp = []

    error_terms = ["error", "exception", "failed", "failure", "bad gateway", "timeout", "502", "404", "500", "unauthorized", "denied"]
    if any(t in text for t in error_terms):
        hyp.append({
            "type": "system_error_screenshot",
            "confidence": "medium_to_high" if ocr_blocks else "low",
            "evidence": ["OCR contains error-like terms", "text-heavy image"]
        })

    if props["orientation"] == "landscape" and visual["edge_density"]["label"] in {"medium", "high"} and len(ocr_blocks) >= 3:
        hyp.append({
            "type": "ui_or_dashboard_screenshot",
            "confidence": "medium",
            "evidence": ["landscape ratio", "high edge density", "multiple OCR text blocks"]
        })

    flow_terms = ["start", "end", "yes", "no", "审批", "开始", "结束", "判断", "流程", "通过", "失败"]
    if any(t in text for t in flow_terms) or count_high_regions(regions) >= 4:
        hyp.append({
            "type": "workflow_or_diagram_candidate",
            "confidence": "low_to_medium",
            "evidence": ["process-like OCR terms or distributed complexity regions"]
        })

    if props["orientation"] == "portrait" and props["aspect_ratio"] < 0.7:
        hyp.append({
            "type": "poster_or_mobile_screenshot",
            "confidence": "low_to_medium",
            "evidence": ["portrait mobile-like ratio"]
        })

    if not hyp:
        hyp.append({
            "type": "unknown_visual_material",
            "confidence": "low",
            "evidence": ["No strong heuristic matched"]
        })
    return hyp


def routing_suggestion(hypotheses: List[Dict], task: str) -> Dict:
    if task and task != "auto":
        return {"recommended_template": task, "reason": "User or caller specified task."}
    types = [h["type"] for h in hypotheses]
    if "system_error_screenshot" in types or "ui_or_dashboard_screenshot" in types:
        return {"recommended_template": "screenshot_diagnosis", "reason": "Screenshot or error-like visual signals detected."}
    if "workflow_or_diagram_candidate" in types:
        return {"recommended_template": "workflow_to_sop", "reason": "Diagram or process-like signals detected."}
    if "poster_or_mobile_screenshot" in types:
        return {"recommended_template": "ui_audit", "reason": "Portrait/mobile visual likely benefits from layout audit."}
    return {"recommended_template": "structured_visual_reading", "reason": "No specialized template matched with confidence."}


def structure_candidates(ocr_blocks: List[Dict], regions: List[Dict]) -> Dict:
    ui_elements = []
    flow_nodes = []
    arrow_candidates = []
    chart_regions = []

    for b in ocr_blocks:
        text = b["text"].strip()
        low = text.lower()
        if any(k in low for k in ["ok", "cancel", "submit", "login", "save", "关闭", "确定", "取消", "保存", "登录"]):
            ui_elements.append({"id": b["id"], "type_hint": "button_or_action_text", "text": text, "bbox": b["bbox"], "region_id": b.get("region_id", "")})
        if any(k in low for k in ["start", "end", "yes", "no", "开始", "结束", "判断", "审批", "通过", "失败"]):
            flow_nodes.append({"id": b["id"], "type_hint": "process_node_text", "text": text, "bbox": b["bbox"], "region_id": b.get("region_id", "")})
        if any(k in low for k in ["%", "sales", "revenue", "trend", "增长", "下降", "同比", "环比"]):
            chart_regions.append({"id": b["id"], "type_hint": "chart_related_text", "text": text, "bbox": b["bbox"], "region_id": b.get("region_id", "")})

    return {
        "ui_elements": ui_elements,
        "flow_nodes": flow_nodes,
        "arrow_candidates": arrow_candidates,
        "chart_regions": chart_regions
    }


def label(value: float, low: float, high: float, low_label: str, mid_label: str, high_label: str) -> str:
    if value < low:
        return low_label
    if value > high:
        return high_label
    return mid_label


def position_label(r: int, c: int) -> str:
    vertical = ["top", "middle", "bottom"][r]
    horizontal = ["left", "center", "right"][c]
    return f"{vertical}_{horizontal}"


def count_high_regions(regions: List[Dict]) -> int:
    return sum(1 for r in regions if r.get("visual_weight") == "high")
