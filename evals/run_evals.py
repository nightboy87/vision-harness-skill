#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def check_case(case_dir: Path) -> dict:
    result = {
        "case_dir": str(case_dir),
        "visual_packet_json": (case_dir / "visual_packet.json").exists(),
        "visual_packet_md": (case_dir / "visual_packet.md").exists(),
        "annotated_regions_png": (case_dir / "annotated_regions.png").exists(),
        "schema_like": False,
        "ocr_blocks_count": 0,
        "text_line_groups_count": 0,
        "evidence_quotes_count": 0,
        "layout_regions_count": 0,
        "uncertainties_count": 0,
        "has_spatial_layout_analysis": False,
    }
    packet_path = case_dir / "visual_packet.json"
    if packet_path.exists():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        required = ["source", "image_properties", "visual_features", "layout_regions", "ocr_blocks", "routing", "uncertainties"]
        result["schema_like"] = all(k in packet for k in required)
        result["ocr_blocks_count"] = len(packet.get("ocr_blocks", []))
        result["text_line_groups_count"] = len(packet.get("text_line_groups", []))
        result["evidence_quotes_count"] = len(packet.get("evidence_quotes", []))
        result["layout_regions_count"] = len(packet.get("layout_regions", []))
        result["uncertainties_count"] = len(packet.get("uncertainties", []))
        result["has_spatial_layout_analysis"] = "spatial_layout_analysis" in packet
    result["pass"] = result["visual_packet_json"] and result["visual_packet_md"] and result["annotated_regions_png"] and result["schema_like"]
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dirs", nargs="+", help="Output case directories to check")
    args = parser.parse_args()
    results = [check_case(Path(p)) for p in args.case_dirs]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    failed = [r for r in results if not r["pass"]]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
