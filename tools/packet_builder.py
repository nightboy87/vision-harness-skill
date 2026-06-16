from __future__ import annotations

from typing import Dict


def build_agent_notes(packet: Dict) -> str:
    props = packet["image_properties"]
    visual = packet["visual_features"]
    routing = packet["routing"]
    ocr_blocks = packet.get("ocr_blocks", [])
    hyps = packet.get("image_type_hypotheses", [])
    spatial = packet.get("spatial_layout_analysis", {})

    lines = []
    lines.append(f"Image size: {props['width']}x{props['height']} ({props['orientation']}, aspect_ratio={props['aspect_ratio']}).")
    lines.append(f"Brightness: {visual['color']['brightness']}; contrast: {visual['color']['contrast']}; edge_density: {visual['edge_density']['label']} ({visual['edge_density']['value']}).")
    lines.append(f"OCR blocks detected: {len(ocr_blocks)}. Layout regions: {len(packet.get('layout_regions', []))}. Text line groups: {len(packet.get('text_line_groups', []))}.")
    if spatial.get("layout_hints"):
        lines.append("Layout hints: " + ", ".join(spatial.get("layout_hints", [])) + ".")
    if hyps:
        h = hyps[0]
        lines.append(f"Top image type hypothesis: {h['type']} ({h['confidence']}). Evidence: {', '.join(h.get('evidence', []))}.")
    lines.append(f"Recommended template: {routing['recommended_template']}. Reason: {routing['reason']}.")
    if packet.get("evidence_quotes"):
        top = [f"{q['id']}={q['normalized_text']}" for q in packet["evidence_quotes"][:8]]
        lines.append("High-signal evidence quotes: " + " | ".join(top))
    elif ocr_blocks:
        top_text = [b.get('normalized_text') or b['text'] for b in ocr_blocks[:12]]
        lines.append("OCR excerpt: " + " | ".join(top_text))
    else:
        lines.append("No OCR text was detected or OCR engine is unavailable. Do not infer exact text from this packet.")
    lines.append("Important: This packet is a visual translation. Treat heuristic labels as hypotheses, not facts. Important claims should cite region IDs and raw OCR quotes.")
    return "\n".join(lines)


def to_markdown(packet: Dict) -> str:
    lines = ["# Visual Packet", ""]
    lines.append("## Source")
    lines.append(f"- File: `{packet['source']['filename']}`")
    lines.append(f"- Input type: `{packet['source']['input_type']}`")
    if packet["source"].get("sha256"):
        lines.append(f"- SHA256: `{packet['source']['sha256']}`")
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

    lines.append("## Spatial layout analysis")
    spatial = packet.get("spatial_layout_analysis", {})
    lines.append(f"- Text density per megapixel: {spatial.get('text_density_per_megapixel', 'unknown')}")
    if spatial.get("layout_hints"):
        lines.append("- Layout hints: " + ", ".join(spatial.get("layout_hints", [])))
    major = spatial.get("major_line_signals", {})
    if major:
        lines.append(f"- Vertical line candidates: {major.get('vertical_lines_x', [])[:20]}")
        lines.append(f"- Horizontal line candidates: {major.get('horizontal_lines_y', [])[:20]}")
    lines.append("")

    lines.append("## Evidence quotes")
    if packet.get("evidence_quotes"):
        for q in packet["evidence_quotes"]:
            lines.append(f"- {q['id']} @ {q.get('region_id', '')}: raw=`{q.get('raw_text', '')}` normalized=`{q.get('normalized_text', '')}` bbox={q.get('bbox', [])} confidence={q.get('confidence')}")
    else:
        lines.append("- No high-signal evidence quotes selected.")
    lines.append("")

    lines.append("## Text line groups")
    if packet.get("text_line_groups"):
        for line in packet["text_line_groups"][:80]:
            lines.append(f"- {line['id']} @ {line.get('region_ids', [])}: `{line['text']}` text_ids={line.get('text_ids', [])}")
        if len(packet.get("text_line_groups", [])) > 80:
            lines.append(f"- ... {len(packet.get('text_line_groups', [])) - 80} more line groups omitted in markdown view.")
    else:
        lines.append("- No text line groups detected.")
    lines.append("")

    lines.append("## OCR blocks")
    if packet.get("ocr_blocks"):
        for b in packet["ocr_blocks"]:
            raw = b.get("text", "")
            norm = b.get("normalized_text", raw)
            lines.append(f"- {b['id']} @ {b.get('region_id', '')}: raw=`{raw}` normalized=`{norm}` bbox={b['bbox']} confidence={b['confidence']}")
    else:
        lines.append("- No OCR blocks detected or OCR engine unavailable.")
    lines.append("")

    lines.append("## Layout regions")
    for r in packet.get("layout_regions", []):
        lines.append(f"- {r['id']}: {r['type_hint']} bbox={r['bbox']} weight={r.get('visual_weight', '')} text_ids={r.get('contains_text_ids', [])} notes={r.get('notes', '')}")
    lines.append("")

    lines.append("## Structure candidates")
    candidates = packet.get("structure_candidates", {})
    for key in ["ui_elements", "flow_nodes", "decision_candidates", "arrow_candidates", "chart_regions"]:
        vals = candidates.get(key, [])
        lines.append(f"### {key}")
        if vals:
            for item in vals[:40]:
                lines.append(f"- {item}")
            if len(vals) > 40:
                lines.append(f"- ... {len(vals) - 40} more omitted.")
        else:
            lines.append("- none")
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
