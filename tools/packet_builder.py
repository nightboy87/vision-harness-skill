from __future__ import annotations

from typing import Dict, List


def build_agent_notes(packet: Dict) -> str:
    props = packet["image_properties"]
    visual = packet["visual_features"]
    routing = packet["routing"]
    ocr_blocks = packet.get("ocr_blocks", [])
    hyps = packet.get("image_type_hypotheses", [])

    lines = []
    lines.append(f"Image size: {props['width']}x{props['height']} ({props['orientation']}, aspect_ratio={props['aspect_ratio']}).")
    lines.append(f"Brightness: {visual['color']['brightness']}; contrast: {visual['color']['contrast']}; edge_density: {visual['edge_density']['label']} ({visual['edge_density']['value']}).")
    lines.append(f"OCR blocks detected: {len(ocr_blocks)}. Layout regions: {len(packet.get('layout_regions', []))}.")
    if hyps:
        h = hyps[0]
        lines.append(f"Top image type hypothesis: {h['type']} ({h['confidence']}). Evidence: {', '.join(h.get('evidence', []))}.")
    lines.append(f"Recommended template: {routing['recommended_template']}. Reason: {routing['reason']}.")
    if ocr_blocks:
        top_text = [b['text'] for b in ocr_blocks[:12]]
        lines.append("OCR excerpt: " + " | ".join(top_text))
    else:
        lines.append("No OCR text was detected or OCR engine is unavailable. Do not infer exact text from this packet.")
    lines.append("Important: This packet is a visual translation. Treat heuristic labels as hypotheses, not facts.")
    return "\n".join(lines)


def to_markdown(packet: Dict) -> str:
    lines = ["# Visual Packet", ""]
    lines.append("## Source")
    lines.append(f"- File: `{packet['source']['filename']}`")
    lines.append(f"- Input type: `{packet['source']['input_type']}`")
    lines.append("")

    props = packet["image_properties"]
    lines.append("## Image properties")
    for k, v in props.items():
        lines.append(f"- {k}: {v}")
    lines.append("")

    lines.append("## Visual features")
    color = packet["visual_features"]["color"]
    lines.append(f"- Brightness: {color['brightness']} ({color['brightness_value']})")
    lines.append(f"- Contrast: {color['contrast']} ({color['contrast_value']})")
    lines.append(f"- Edge density: {packet['visual_features']['edge_density']['label']} ({packet['visual_features']['edge_density']['value']})")
    lines.append("- Dominant colors: " + ", ".join(c["hex"] for c in color.get("dominant_colors", [])[:6]))
    lines.append("")

    lines.append("## OCR blocks")
    if packet.get("ocr_blocks"):
        for b in packet["ocr_blocks"]:
            lines.append(f"- {b['id']} @ {b.get('region_id', '')}: `{b['text']}` bbox={b['bbox']} confidence={b['confidence']}")
    else:
        lines.append("- No OCR blocks detected or OCR engine unavailable.")
    lines.append("")

    lines.append("## Layout regions")
    for r in packet.get("layout_regions", []):
        lines.append(f"- {r['id']}: {r['type_hint']} bbox={r['bbox']} weight={r.get('visual_weight', '')} text_ids={r.get('contains_text_ids', [])} notes={r.get('notes', '')}")
    lines.append("")

    lines.append("## Image type hypotheses")
    for h in packet.get("image_type_hypotheses", []):
        lines.append(f"- {h['type']} ({h['confidence']}): {', '.join(h.get('evidence', []))}")
    lines.append("")

    lines.append("## Routing")
    lines.append(f"- Recommended template: `{packet['routing']['recommended_template']}`")
    lines.append(f"- Reason: {packet['routing']['reason']}")
    lines.append("")

    lines.append("## Uncertainties")
    for u in packet.get("uncertainties", []):
        lines.append(f"- {u}")
    lines.append("")

    lines.append("## Agent notes")
    lines.append(packet.get("agent_notes", ""))
    lines.append("")
    return "\n".join(lines)
