# Vision Harness Skill

[中文说明](README.zh-CN.md)

Vision Harness Skill is a structured visual understanding skill package for agents.

It is not another multimodal model. Instead, it provides a visual harness layer around agents:

* It helps text-only LLM agents understand images through structured visual packets.
* It helps multimodal LLM agents analyze images with evidence, regions, uncertainty, and task-specific reading protocols.

The current version focuses on three scenarios:

1. Technical screenshot diagnosis
2. UI screenshot analysis and semantic HTML reconstruction
3. Early-stage workflow / swimlane diagram extraction

---

## Why this project exists

Agents often struggle with image-based tasks in two different ways.

Text-only LLM agents cannot directly read screenshots, diagrams, or UI mockups.

Multimodal LLM agents can see images, but they often jump directly to conclusions without a stable evidence trail. They may also mix observed facts, inferred explanations, and uncertain assumptions.

Vision Harness Skill does not try to make the model itself smarter. It makes the visual analysis process more structured, auditable, and useful for downstream agent work.

---

## Core capabilities

### 1. Text-only Agent Mode

For text-only LLM agents.

The image is converted into a structured `visual_packet`, including:

* Image size, orientation, dominant colors, brightness, and complexity
* OCR text blocks
* Text line groups
* Region layout
* Evidence quotes
* Spatial layout hints
* Task-specific agent instructions

A text-only LLM can then use this packet to diagnose screenshots, analyze UI layouts, or extract early workflow structures.

### 2. Multimodal Agent Mode

For multimodal LLM agents.

A multimodal agent can inspect the original image while using the skill's protocols and templates to produce:

* `observed_facts`: what is directly visible
* `inferences`: what is inferred from visible evidence
* `evidence_quotes`: raw and normalized OCR evidence
* `evidence_regions`: visual regions used as support
* `uncertainties`: what needs human review
* `recommended_actions`: what to do next

---

## Use cases

### Technical screenshot diagnosis

Useful for screenshots containing logs, errors, configuration panels, command outputs, IDEs, dashboards, or enterprise software screens.

Example prompt:

```text
Analyze this screenshot, identify the likely root cause, and provide actionable next steps.
```

### UI screenshot analysis and HTML reconstruction

Useful for product mockups, dashboards, admin panels, and internal tools.

Supported modes:

* `ui_audit`: analyze UI structure and issues
* `ui_semantic_rebuild`: rebuild a semantic HTML draft
* `ui_fidelity_clone`: assist with layout-preserving UI recreation

Note: HTML reconstruction quality depends not only on this skill, but also on the frontend coding ability of the driving agent model.

### Workflow / swimlane diagram extraction

Useful for extracting early structure from process diagrams:

* Stages
* Roles / swimlanes
* Nodes
* Candidate edges
* Draft SOP
* Missing details for human review

In the current version, arrow direction and complex topology recovery are still heuristic. Generated SOPs should be manually reviewed.

---

## Installation

```bash
pip install -r requirements.txt
```

Recommended Python version:

```text
Python 3.10+
```

OCR quality depends on the local OCR environment. If no OCR engine is available, the tool can still produce basic visual metadata, but text extraction will be limited.

---

## Quick start

```bash
python tools/visual_extract.py examples/screenshot_error/sample_error.png --task screenshot_diagnosis --out outputs/screenshot_case
```

The output directory will contain:

```text
visual_packet.json
visual_packet.md
annotated_regions.png
agent_instruction.md
crops/
```

What each file means:

* `visual_packet.json`: structured visual data
* `visual_packet.md`: Markdown version for direct agent use
* `annotated_regions.png`: image with region annotations
* `agent_instruction.md`: task-specific instruction for the agent
* `crops/`: cropped regions

---

## CLI usage

```bash
python tools/visual_extract.py <image> --task <task> --out <output_dir>
```

Supported tasks:

```text
auto
screenshot_diagnosis
workflow_to_sop
ui_audit
structured_visual_reading
```

Examples:

```bash
python tools/visual_extract.py ./input.png --task ui_audit --out ./outputs/ui_case
```

```bash
python tools/visual_extract.py ./workflow.png --task workflow_to_sop --out ./outputs/workflow_case
```

---

## Output discipline

Vision Harness Skill encourages agents to separate:

```text
Facts: directly visible information
Inferences: judgments based on evidence
Evidence: OCR quotes, regions, or visual signals
Uncertainties: items requiring human review
Actions: recommended next steps
```

Recommended output structure:

```text
observed_facts
evidence_quotes
inferences
uncertainties
recommended_actions
```

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
│  ├─ packet_builder.py
│  └─ schema_validate.py
├─ schemas/
├─ templates/
├─ references/
├─ examples/
└─ evals/
```

---

## Current limits

Vision Harness Skill v0.1.2 is still an early release.

It is currently useful for:

* OCR-rich technical screenshot diagnosis
* UI screenshot analysis and semantic HTML draft generation
* Early workflow / swimlane diagram extraction

It does not claim to provide:

* General-purpose image understanding
* Reliable face, object, or natural-scene recognition
* Pixel-perfect UI recreation
* Full automatic flowchart topology recovery
* Final SOP generation without human review

---

## Version

Current version: `v0.1.2`

Main improvements:

* Added `evidence_quotes`
* Added `text_line_groups`
* Improved `spatial_layout_analysis`
* Strengthened screenshot diagnosis templates
* Reworked workflow-to-SOP guardrails
* Added layout tree, spatial constraints, and fidelity self-check for UI reconstruction

See [CHANGELOG.md](CHANGELOG.md) for details.

---

## License

MIT
