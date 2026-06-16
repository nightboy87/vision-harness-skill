#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

# Allow running as a standalone script from tools/ or repo root.
import sys
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from image_loader import load_image
from ocr_engine import run_ocr
from layout_analyzer import (
    image_properties,
    color_features,
    edge_density,
    grid_regions,
    assign_text_to_regions,
    infer_image_types,
    routing_suggestion,
    structure_candidates,
)
from packet_builder import build_agent_notes, to_markdown
from region_marker import annotate_regions, crop_regions


def build_packet(input_value: str, task: str = "auto") -> tuple:
    img, source = load_image(input_value)
    props = image_properties(img)
    color = color_features(img)
    edge = edge_density(img)
    regions = grid_regions(img)
    ocr_blocks = run_ocr(img)
    assign_text_to_regions(ocr_blocks, regions)
    visual = {"color": color, "edge_density": edge}
    hypotheses = infer_image_types(props, visual, ocr_blocks, regions)
    routing = routing_suggestion(hypotheses, task)
    candidates = structure_candidates(ocr_blocks, regions)

    uncertainties = [
        "OCR may miss small, blurred, rotated, handwritten, or low-contrast text.",
        "Layout regions are grid-based and heuristic; they are evidence anchors, not semantic objects.",
        "Image type hypotheses are heuristic and must not be treated as confirmed facts.",
        "The tool does not use a multimodal LLM and cannot reliably identify arbitrary objects or scenes.",
        "Flow arrows and chart values are not fully parsed in v0.1; use human review for critical decisions."
    ]
    if not ocr_blocks:
        uncertainties.append("No OCR text was detected, or no OCR engine is installed. Text content may be missing from the packet.")

    packet = {
        "version": "0.1.0",
        "mode": "visual_bridge",
        "task": task,
        "source": source,
        "image_properties": props,
        "visual_features": visual,
        "layout_regions": regions,
        "ocr_blocks": ocr_blocks,
        "structure_candidates": candidates,
        "image_type_hypotheses": hypotheses,
        "routing": routing,
        "uncertainties": uncertainties,
    }
    packet["agent_notes"] = build_agent_notes(packet)
    return img, packet


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert an image into a Vision Harness visual_packet.")
    parser.add_argument("image", help="Image path, raw base64, or data:image/...;base64,... URL")
    parser.add_argument("--task", default="auto", choices=["auto", "screenshot_diagnosis", "workflow_to_sop", "ui_audit", "structured_visual_reading"], help="Target task template")
    parser.add_argument("--out", default="outputs/vision_harness_case", help="Output directory")
    parser.add_argument("--no-crops", action="store_true", help="Do not write region crop images")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    img, packet = build_packet(args.image, args.task)

    packet_path = out_dir / "visual_packet.json"
    packet_md_path = out_dir / "visual_packet.md"
    annotated_path = out_dir / "annotated_regions.png"

    packet_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    packet_md_path.write_text(to_markdown(packet), encoding="utf-8")
    annotate_regions(img, packet["layout_regions"], packet["ocr_blocks"], str(annotated_path))
    if not args.no_crops:
        crop_regions(img, packet["layout_regions"], str(out_dir / "crops"))

    instruction = build_agent_instruction(packet)
    (out_dir / "agent_instruction.md").write_text(instruction, encoding="utf-8")

    print(json.dumps({
        "visual_packet": str(packet_path),
        "visual_packet_md": str(packet_md_path),
        "annotated_regions": str(annotated_path),
        "recommended_template": packet["routing"]["recommended_template"],
        "ocr_blocks": len(packet["ocr_blocks"]),
        "layout_regions": len(packet["layout_regions"])
    }, ensure_ascii=False, indent=2))
    return 0


def build_agent_instruction(packet: dict) -> str:
    template = packet["routing"]["recommended_template"]
    return f"""# Agent Instruction

Use Vision Harness Skill with template: `{template}`.

You are analyzing an image through a `visual_packet`. If you are a text-only agent, you cannot directly see the original image; reason only from the packet and be explicit about uncertainty. If you are a multimodal agent, inspect the original image, `annotated_regions.png`, and the packet together.

Required output sections:

1. Observed facts
2. Inferences
3. Evidence regions / OCR blocks
4. Uncertainties
5. Recommended actions

Rules:

- Do not treat OCR as perfect truth.
- Do not treat image type hypotheses as confirmed facts.
- Cite region IDs such as `region_003` and OCR IDs such as `text_001` when supporting a claim.
- If a region is unclear, say so instead of filling in missing details.
- Do not perform identity, medical, legal, security-critical, or sensitive-attribute judgments.
"""


if __name__ == "__main__":
    raise SystemExit(main())
