# Vision Harness Skill

[中文说明](README.zh-CN.md)

Vision Harness Skill is a script-backed Agent Skill for structured visual understanding.

It has two goals:

1. **Make text-only agents see images.** It converts an image into a structured `visual_packet` so a text-only LLM agent can reason from OCR blocks, evidence quotes, text line groups, layout regions, visual features, routing hints, and uncertainty notes.
2. **Make multimodal agents read images better.** It gives multimodal LLM agents a structured reading protocol: observed facts, inferences, evidence regions, evidence quotes, uncertainties, and recommended actions.

This project is not another multimodal model. It is a practical visual harness around agents.

---

## What is new in v0.1.2

v0.1.2 is based on three real scenario tests:

- OCR-rich technical screenshot diagnosis;
- workflow swimlane extraction;
- UI screenshot analysis and HTML reconstruction.

Improvements:

- added `evidence_quotes` so important OCR-based claims can quote raw/normalized text;
- added `text_line_groups` for logs, tables, dashboards, and UI text clusters;
- added heuristic `spatial_layout_analysis` for sidebars, right rails, status bars, grid/swimlane candidates, and line signals;
- strengthened screenshot diagnosis rules: no stale examples, no local-success-as-global-success, and stricter fact/inference separation;
- revised workflow-to-SOP template: extracted SOP, inferred interpretation, and suggested missing details are now separated;
- decision points in workflow diagrams now require explicit evidence;
- revised UI template with `ui_audit`, `ui_semantic_rebuild`, and `ui_fidelity_clone` modes;
- added UI `layout_tree`, `spatial_constraints`, and fidelity self-check rules.

---

## Best current use cases

Best for:

1. OCR-rich technical screenshot diagnosis;
2. UI screenshot analysis and semantic HTML reconstruction;
3. early-stage workflow diagram extraction and SOP skeleton drafting.

Not yet for:

1. pixel-perfect UI recreation;
2. fully automatic flowchart topology recovery;
3. final SOP generation without human review;
4. high-risk medical, legal, security, identity, or surveillance decisions.

---

## Why this exists

Native multimodal models can describe images, but agent workflows often need stricter outputs:

- evidence regions instead of vague claims;
- evidence quotes instead of only text IDs;
- separation between facts and inferences;
- explicit uncertainty marking;
- machine-readable JSON;
- screenshot diagnosis;
- workflow-to-SOP extraction;
- UI audit and UI reconstruction guidance;
- a fallback path for text-only LLM agents.

Vision Harness Skill turns image analysis from a free-form answer into a reusable agent workflow.

---

## Project structure

```text
vision-harness-skill/
├─ SKILL.md
├─ README.md
├─ README.zh-CN.md
├─ CHANGELOG.md
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
pip install paddleocr
```

Or the lighter OCR option:

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

The agent must cite region IDs, quote evidence when text matters, and separate facts from inferences.

---

## Task templates

| Task | Use when | Template |
|---|---|---|
| Screenshot diagnosis | Error screenshots, build logs, software issues, UI error messages, dashboards | `templates/screenshot_diagnosis.md` |
| Workflow to SOP | Flowcharts, whiteboard processes, process diagrams, swimlanes | `templates/workflow_to_sop.md` |
| UI audit / reconstruction | Product screenshots, web/app screens, UX review, UI semantic rebuild, UI fidelity clone | `templates/ui_audit.md` |

---

## Design principles

- Scripts handle deterministic extraction.
- LLMs handle reasoning and generation.
- Skill files provide method, gotchas, schemas, and task templates.
- Every important claim should have evidence.
- Text-based claims should include raw/normalized OCR quotes where available.
- Uncertainty is part of the output, not a failure.
- Text-only mode should not pretend to have native vision.
- Multimodal mode should not jump from image to conclusion without evidence.

---

## Limits

v0.1.2 does not:

- train or ship a vision model;
- use a multimodal model as an observer;
- perform computer-use clicking;
- guarantee OCR accuracy;
- parse every flowchart edge accurately;
- extract precise chart values;
- guarantee pixel-perfect HTML/CSS reconstruction;
- support high-risk medical, legal, security, identity, or surveillance decisions.

---

## Development workflow

1. Run `visual_extract.py` on a real image.
2. Check `visual_packet.md` and `annotated_regions.png`.
3. Run the recommended template with a text-only or multimodal agent.
4. Check whether the answer separates facts, inferences, evidence, uncertainties, and actions.
5. Add new gotchas or template rules when failures appear.
