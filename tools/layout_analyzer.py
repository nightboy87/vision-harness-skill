from __future__ import annotations

from typing import Dict, List
import re
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


def normalize_ocr_blocks(ocr_blocks: List[Dict]) -> None:
    """Add normalized text without destroying the raw OCR result."""
    for block in ocr_blocks:
        text = str(block.get("text", ""))
        normalized = re.sub(r"\s+", " ", text).strip()
        block["normalized_text"] = normalized


def text_line_groups(ocr_blocks: List[Dict], y_tolerance: int = 12) -> List[Dict]:
    """Group OCR blocks into approximate lines for screenshots, logs, and UI panels.

    This is intentionally simple and dependency-free. It gives text-only agents
    better context than isolated OCR blocks while remaining explicitly heuristic.
    """
    if not ocr_blocks:
        return []
    blocks = sorted(ocr_blocks, key=lambda b: ((b["bbox"][1] + b["bbox"][3]) / 2, b["bbox"][0]))
    lines: List[List[Dict]] = []
    for block in blocks:
        cy = (block["bbox"][1] + block["bbox"][3]) / 2
        placed = False
        for line in lines:
            line_cy = sum((b["bbox"][1] + b["bbox"][3]) / 2 for b in line) / len(line)
            if abs(cy - line_cy) <= y_tolerance:
                line.append(block)
                placed = True
                break
        if not placed:
            lines.append([block])

    groups = []
    for i, line in enumerate(lines, start=1):
        line = sorted(line, key=lambda b: b["bbox"][0])
        x1 = min(b["bbox"][0] for b in line)
        y1 = min(b["bbox"][1] for b in line)
        x2 = max(b["bbox"][2] for b in line)
        y2 = max(b["bbox"][3] for b in line)
        text = " ".join(b.get("normalized_text") or b.get("text", "") for b in line).strip()
        groups.append({
            "id": f"line_{i:03d}",
            "text": text,
            "bbox": [x1, y1, x2, y2],
            "text_ids": [b["id"] for b in line],
            "region_ids": sorted({b.get("region_id", "") for b in line if b.get("region_id")})
        })
    return groups


def evidence_quotes(ocr_blocks: List[Dict], max_items: int = 24) -> List[Dict]:
    """Pick high-signal OCR blocks that should be quoted in final answers.

    The agent should cite these raw/normalized strings when making important claims.
    This reduces the pattern where answers only cite text IDs without showing the evidence.
    """
    keywords = [
        "error", "failed", "fail", "exception", "warning", "warn", "denied", "timeout", "not found", "not exist",
        "成功", "失败", "异常", "错误", "警告", "找不到", "不存在", "存疑", "通过", "完成",
        "支付", "收款", "发货", "签收", "导出", "导入", "检查", "状态", "健康", "费用",
        "商品", "库存", "订单", "下单", "付款", "佣金", "物流", "设置", "查看", "用户", "运维", "客服", "商务", "仓储", "财务", "经销商",
        "总览", "工作区", "断言", "来源", "主题", "api", "lint", "obsidian", "agent", "预算", "服务", "运行"
    ]
    ranked = []
    for block in ocr_blocks:
        text = block.get("normalized_text") or block.get("text", "")
        low = text.lower()
        score = 0
        for kw in keywords:
            if kw in low or kw in text:
                score += 5
        # Longer text blocks are often log lines or labels with more context.
        score += min(len(text) / 20, 3)
        # Prefer higher OCR confidence if available.
        score += float(block.get("confidence", 0))
        if score >= 2:
            ranked.append((score, block))
    ranked.sort(key=lambda x: x[0], reverse=True)
    results = []
    for _, block in ranked[:max_items]:
        results.append({
            "id": block["id"],
            "region_id": block.get("region_id", ""),
            "raw_text": block.get("text", ""),
            "normalized_text": block.get("normalized_text") or block.get("text", ""),
            "bbox": block.get("bbox", []),
            "confidence": block.get("confidence", None)
        })
    return results


def detect_major_lines(img: Image.Image) -> Dict:
    """Detect coarse horizontal/vertical dark lines.

    This is not a full flowchart parser. It is a lightweight signal for swimlanes,
    tables, and dashboard separators. Consumers must treat it as a heuristic.
    """
    gray = np.array(img.convert("L")).astype(np.float32)
    h, w = gray.shape
    dark = gray < 120
    col_ratio = dark.mean(axis=0)
    row_ratio = dark.mean(axis=1)
    vertical = _collapse_positions([i for i, v in enumerate(col_ratio) if v > 0.35], min_gap=3, min_len=max(3, int(w * 0.002)))
    horizontal = _collapse_positions([i for i, v in enumerate(row_ratio) if v > 0.35], min_gap=3, min_len=max(3, int(h * 0.002)))
    return {
        "vertical_lines_x": vertical[:40],
        "horizontal_lines_y": horizontal[:40],
        "line_detection_note": "Heuristic dark-line detection. Useful for swimlanes/tables, not reliable for all diagrams."
    }


def spatial_layout_analysis(img: Image.Image, ocr_blocks: List[Dict], regions: List[Dict]) -> Dict:
    props = image_properties(img)
    lines = detect_major_lines(img)
    text_density = len(ocr_blocks) / max(props["megapixels"], 0.1)
    left_blocks = [b for b in ocr_blocks if ((b["bbox"][0] + b["bbox"][2]) / 2) < props["width"] * 0.2]
    right_blocks = [b for b in ocr_blocks if ((b["bbox"][0] + b["bbox"][2]) / 2) > props["width"] * 0.78]
    top_blocks = [b for b in ocr_blocks if ((b["bbox"][1] + b["bbox"][3]) / 2) < props["height"] * 0.16]
    bottom_blocks = [b for b in ocr_blocks if ((b["bbox"][1] + b["bbox"][3]) / 2) > props["height"] * 0.84]

    hints = []
    if len(left_blocks) >= max(4, len(ocr_blocks) * 0.18):
        hints.append("left_sidebar_or_left_rail_candidate")
    if len(right_blocks) >= max(3, len(ocr_blocks) * 0.12):
        hints.append("right_summary_rail_candidate")
    if len(top_blocks) >= max(3, len(ocr_blocks) * 0.12):
        hints.append("top_header_or_toolbar_candidate")
    if len(bottom_blocks) >= max(3, len(ocr_blocks) * 0.08):
        hints.append("bottom_status_or_footer_candidate")
    if len(lines["vertical_lines_x"]) >= 4 and len(lines["horizontal_lines_y"]) >= 3:
        hints.append("grid_or_swimlane_structure_candidate")

    return {
        "text_density_per_megapixel": round(text_density, 2),
        "major_line_signals": lines,
        "layout_hints": hints,
        "region_text_counts": [
            {"region_id": r["id"], "text_count": len(r.get("contains_text_ids", [])), "notes": r.get("notes", "")} for r in regions
        ]
    }


def infer_image_types(props: Dict, visual: Dict, ocr_blocks: List[Dict], regions: List[Dict]) -> List[Dict]:
    text = " ".join(b.get("text", "") for b in ocr_blocks).lower()
    text_original = " ".join(b.get("text", "") for b in ocr_blocks)
    hyp = []

    error_terms = ["error", "exception", "failed", "failure", "bad gateway", "timeout", "502", "404", "500", "unauthorized", "denied", "错误", "失败", "异常", "找不到", "不存在"]
    if any(t in text for t in error_terms) or any(t in text_original for t in ["错误", "失败", "异常", "找不到", "不存在"]):
        hyp.append({
            "type": "system_error_screenshot",
            "confidence": "medium_to_high" if ocr_blocks else "low",
            "evidence": ["OCR contains error-like terms", "text-heavy image"]
        })

    ui_terms = ["dashboard", "settings", "export", "import", "api", "状态", "总览", "导出", "导入", "设置", "检查", "工作区", "文件", "模型"]
    if props["orientation"] == "landscape" and visual["edge_density"]["label"] in {"medium", "high"} and len(ocr_blocks) >= 8 and any(t in text or t in text_original for t in ui_terms):
        hyp.append({
            "type": "ui_or_dashboard_screenshot",
            "confidence": "medium_to_high",
            "evidence": ["landscape ratio", "multiple OCR text blocks", "UI/dashboard-like terms"]
        })
    elif props["orientation"] == "landscape" and visual["edge_density"]["label"] in {"medium", "high"} and len(ocr_blocks) >= 3:
        hyp.append({
            "type": "ui_or_dashboard_screenshot",
            "confidence": "medium",
            "evidence": ["landscape ratio", "high edge density", "multiple OCR text blocks"]
        })

    flow_terms = ["start", "end", "yes", "no", "审批", "开始", "结束", "判断", "流程", "通过", "失败", "阶段", "泳道", "签收", "发货", "下单", "支付"]
    if any(t in text or t in text_original for t in flow_terms) or count_high_regions(regions) >= 4:
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
    if "system_error_screenshot" in types:
        return {"recommended_template": "screenshot_diagnosis", "reason": "Error-like visual signals detected."}
    if "workflow_or_diagram_candidate" in types and "ui_or_dashboard_screenshot" not in types:
        return {"recommended_template": "workflow_to_sop", "reason": "Diagram or process-like signals detected."}
    if "ui_or_dashboard_screenshot" in types:
        return {"recommended_template": "ui_audit", "reason": "UI/dashboard screenshot signals detected."}
    if "poster_or_mobile_screenshot" in types:
        return {"recommended_template": "ui_audit", "reason": "Portrait/mobile visual likely benefits from layout audit."}
    return {"recommended_template": "structured_visual_reading", "reason": "No specialized template matched with confidence."}


def structure_candidates(ocr_blocks: List[Dict], regions: List[Dict]) -> Dict:
    ui_elements = []
    flow_nodes = []
    decision_candidates = []
    chart_regions = []

    for b in ocr_blocks:
        text = b["text"].strip()
        low = text.lower()
        base = {"id": b["id"], "text": text, "bbox": b["bbox"], "region_id": b.get("region_id", "")}
        if any(k in low for k in ["ok", "cancel", "submit", "login", "save", "export", "import", "run", "关闭", "确定", "取消", "保存", "登录", "导出", "导入", "运行", "查看", "打开"]):
            ui_elements.append({**base, "type_hint": "button_or_action_text"})
        if any(k in low for k in ["start", "end", "process", "order", "payment", "ship", "开始", "结束", "审批", "通过", "失败", "商品", "下单", "支付", "发货", "收款", "签收", "订单", "库存"]):
            flow_nodes.append({**base, "type_hint": "process_node_text"})
        if any(k in low for k in ["yes", "no", "if", "whether", "是否", "判断", "通过", "失败", "是", "否"]):
            decision_candidates.append({**base, "type_hint": "possible_decision_text"})
        if any(k in low for k in ["%", "sales", "revenue", "trend", "增长", "下降", "同比", "环比", "评分", "总数", "数量"]):
            chart_regions.append({**base, "type_hint": "chart_or_metric_related_text"})

    return {
        "ui_elements": ui_elements,
        "flow_nodes": flow_nodes,
        "decision_candidates": decision_candidates,
        "arrow_candidates": [],
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


def _collapse_positions(positions: List[int], min_gap: int = 3, min_len: int = 3) -> List[int]:
    if not positions:
        return []
    groups = []
    start = positions[0]
    prev = positions[0]
    for p in positions[1:]:
        if p - prev <= min_gap:
            prev = p
        else:
            if prev - start + 1 >= min_len:
                groups.append((start, prev))
            start = prev = p
    if prev - start + 1 >= min_len:
        groups.append((start, prev))
    return [int((a + b) / 2) for a, b in groups]
