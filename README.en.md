# Vision Harness Skill

[中文说明](README.zh-CN.md)

Vision Harness Skill is a script-backed Agent Skill for structured visual understanding.

It has two goals:

1. **Make text-only agents see images.** It converts an image into a structured `visual_packet` so a text-only LLM agent can reason from OCR blocks, layout regions, visual features, routing hints, and uncertainty notes.
2. **Make multimodal agents read images better.** It gives multimodal LLM agents a structured reading protocol: observed facts, inferences, evidence regions, uncertainties, and recommended actions.

This project is not another multimodal model. It is a practical visual harness around agents.

---

## Why this exists

Native multimodal models can describe images, but agent workflows often need stricter outputs:

- evidence regions instead of vague claims;
- separation between facts and inferences;
- explicit uncertainty marking;
- machine-readable JSON;
- screenshot diagnosis;
- workflow-to-SOP conversion;
- UI audit with prioritized fixes;
- a fallback path for text-only LLM agents.

Vision Harness Skill turns image analysis from a free-form answer into a reusable agent workflow.

---

## What v0.1 includes

- `SKILL.md` for Claude Code, Codex, and similar skill-based agents;
- `tools/visual_extract.py` for image-to-`visual_packet` extraction;
- optional OCR support;
- annotated region map generation;
- Markdown and JSON visual packet outputs;
- task templates for:
  - screenshot diagnosis;
  - workflow-to-SOP conversion;
  - UI audit;
- JSON schemas;
- gotchas and safety boundaries;
- lightweight evaluation scaffolding.

---

## Project structure

```text
vision-harness-skill/
├─ SKILL.md
├─ README.md
├─ README.zh-CN.md
├─ requirements.txt
├─ tools/
│  ├─ visual_extract.py
│  ├─ image_loader.py
│  ├─ ocr_engine.py
│  ├─ layout_analyzer.py
│  ├─ region_marker.py
│  ├─ packet_builder.py
│  └─ schema_validate.py
├─ schemas/
├─ templates/
├─ references/
├─ examples/
└─ evals/
```

---

## Installation

Install the minimal dependencies:

```bash
pip install -r requirements.txt
```

Optional OCR support:

```bash
pip install rapidocr-onnxruntime
```

Or:

```bash
pip install pytesseract
```

If no OCR engine is installed, the tool still works, but `ocr_blocks` will be empty.

---

## Quick start

```bash
python tools/visual_extract.py examples/screenshot_error/sample_error.png --task screenshot_diagnosis --out outputs/screenshot_case
```

Expected outputs:

```text
outputs/screenshot_case/
├─ visual_packet.json
├─ visual_packet.md
├─ annotated_regions.png
├─ agent_instruction.md
└─ crops/
```

---

## Mode 1: Text-only agent mode

Use this mode when the agent cannot inspect images directly.

Run extraction first:

```bash
python tools/visual_extract.py input.png --task auto --out outputs/case1
```

Then give the text-only LLM agent:

- `visual_packet.md` or `visual_packet.json`;
- `templates/text_agent_mode.md`;
- the recommended task template from the packet.

The agent must clearly state that it is reasoning from a visual translation, not directly seeing the original image.

---

## Mode 2: Multimodal agent mode

Use this mode when the agent can already inspect images, but needs a stricter visual reasoning workflow.

Give the multimodal LLM agent:

- the original image;
- `annotated_regions.png`;
- `visual_packet.json` or `visual_packet.md`;
- `templates/multimodal_agent_mode.md`;
- the relevant task template.

The agent must cite region IDs and separate facts from inferences.

---

## Task templates

| Task | Use when | Template |
|---|---|---|
| Screenshot diagnosis | Error screenshots, software issues, UI error messages, dashboards | `templates/screenshot_diagnosis.md` |
| Workflow to SOP | Flowcharts, whiteboard processes, process diagrams, swimlanes | `templates/workflow_to_sop.md` |
| UI audit | Product screenshots, web or app screens, UX review, information architecture | `templates/ui_audit.md` |

---

## Example output discipline

Bad:

> The screenshot shows a serious backend issue.

Better:

```json
{
  "observed_facts": [
    "OCR block text_001 contains '502 Bad Gateway'.",
    "The error-like text is located around region_005."
  ],
  "inferences": [
    "The page may be failing at a gateway or reverse proxy layer."
  ],
  "evidence_regions": ["region_005", "text_001"],
  "next_checks": [
    "Check reverse proxy logs around the screenshot timestamp.",
    "Verify upstream service health and timeout settings."
  ],
  "uncertainties": [
    "The screenshot alone does not identify the root cause."
  ]
}
```

---

## Design principles

- Scripts handle deterministic extraction.
- LLMs handle reasoning.
- Skill files provide method, gotchas, schemas, and task templates.
- Every important claim should have evidence.
- Uncertainty is part of the output, not a failure.
- Text-only mode should not pretend to have native vision.
- Multimodal mode should not jump from image to conclusion without evidence.

---

## Limits

v0.1 does not:

- train or ship a vision model;
- use a multimodal model as an observer;
- perform computer-use clicking;
- guarantee OCR accuracy;
- parse every flowchart edge accurately;
- extract precise chart values;
- support high-risk medical, legal, security, identity, or surveillance decisions.

---

## Recommended development workflow

1. Run `visual_extract.py` on sample images.
2. Inspect `visual_packet.json` and `annotated_regions.png`.
3. Run a text-only LLM against the packet.
4. Run a multimodal LLM against the original image, annotated image, and packet.
5. Compare the result with a naked multimodal answer.
6. Add gotchas and update templates based on failures.
7. Add regression cases to `evals/`.

---

## Roadmap

Potential future versions may include:

- stronger OCR adapters;
- UI parsing adapters;
- document parsing adapters;
- chart-region parsing;
- flowchart topology enhancement;
- model-specific multimodal prompting templates;
- MCP or CLI wrappers for agent frameworks.

---

## License

MIT
