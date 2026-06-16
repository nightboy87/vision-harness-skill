---
name: vision-harness-skill
description: Use this skill when the user asks an agent to analyze an image, screenshot, UI screenshot, error screenshot, flowchart, swimlane, diagram, dashboard, chart-like visual, or visual material and needs structured facts, evidence quotes, evidence regions, OCR/layout extraction, visual_packet output, screenshot diagnosis, workflow-to-SOP extraction, UI audit, UI semantic rebuild, or UI fidelity clone. For text-only LLM agents, run tools/visual_extract.py to convert the image into a visual_packet. For multimodal LLM agents, use the structured visual reading protocol to separate observed facts, inferences, evidence regions, OCR quotes, uncertainties, and recommended actions.
---

# Vision Harness Skill

Vision Harness Skill is a dual-mode visual understanding skill for agents.

It has two goals:

1. **Text-only agent mode**: convert an image into a structured `visual_packet` so a text-only LLM agent can reason about the image without native vision.
2. **Multimodal agent mode**: make a multimodal LLM analyze images with a disciplined reading protocol, evidence regions, evidence quotes, fact/inference separation, and uncertainty marking.

This skill is not a general computer-use agent, not a replacement for a multimodal model, and not a medical, legal, security, or identity-recognition system.

## What changed in v0.1.2

v0.1.2 is based on three real scenario tests: technical screenshot diagnosis, workflow swimlane extraction, and UI screenshot-to-HTML reconstruction.

It improves:

- evidence quotes for important OCR-based claims;
- stricter fact/inference separation;
- no stale example or template-pollution language;
- workflow output split into extracted SOP, inferred interpretation, and suggested missing details;
- stricter rules for decision points in workflow diagrams;
- UI reconstruction modes: `ui_audit`, `ui_semantic_rebuild`, and `ui_fidelity_clone`;
- layout tree, spatial constraints, and fidelity self-check for UI recreation.

## When to use

Use this skill when the user asks things like:

- “帮我看这张截图是什么问题。”
- “根据这个报错截图给我排查建议。”
- “把这张流程图转成 SOP。”
- “分析这个 UI 截图的问题。”
- “根据这个 UI 截图复刻一个 HTML 页面。”
- “这张图里哪些信息能被 Agent 继续使用？”
- “让文本模型也能处理这张图片。”
- “让多模态模型不要只泛泛描述图片，而是给证据链。”

## First decision: choose the mode

### Use text-only agent mode when

- The current agent or LLM cannot directly inspect images.
- The user explicitly says the agent is text-only.
- The workflow requires a structured image-to-text bridge.
- The image must be converted into JSON or Markdown before reasoning.

Read: `templates/text_agent_mode.md`

Required action:

```bash
python tools/visual_extract.py <image_path_or_base64_or_data_url> --task auto --out <output_dir>
```

Then reason only from:

- `visual_packet.json`
- `visual_packet.md`
- optionally `annotated_regions.png` if another multimodal step is available

### Use multimodal agent mode when

- The current agent is already driven by a multimodal LLM.
- The user wants better image analysis, not merely a description.
- The answer must include observed facts, inferences, evidence regions, evidence quotes, and uncertainties.

Read: `templates/multimodal_agent_mode.md`

Recommended action:

1. Generate `visual_packet` and `annotated_regions.png` if the image file is available.
2. Analyze the original image plus annotated image.
3. Structure the answer according to the relevant task template.

## Task templates

Choose one of the task templates after reading the image and user intent.

| Task | Use when | Template |
|---|---|---|
| Screenshot diagnosis | error screenshots, build logs, software issues, UI error messages, dashboards | `templates/screenshot_diagnosis.md` |
| Workflow to SOP | flowcharts, whiteboard processes, swimlanes, process diagrams | `templates/workflow_to_sop.md` |
| UI audit / reconstruction | product screenshots, web/app screens, UX review, UI semantic rebuild, UI fidelity clone | `templates/ui_audit.md` |

If no task fits, use the generic structured visual reading rules in `templates/multimodal_agent_mode.md`.

## Mandatory output discipline

Never jump directly to conclusions.

Always separate:

1. `observed_facts`: things visible in the image or extracted in the visual_packet.
2. `inferences`: interpretations based on the facts.
3. `evidence_regions`: region IDs, OCR block IDs, or visual features supporting the inference.
4. `evidence_quotes`: raw or normalized OCR text supporting important claims.
5. `uncertainties`: what is unclear, not detected, possibly OCR-wrong, or needs human confirmation.
6. `recommended_actions`: what to do next.

## Critical gotchas

Before finalizing an answer, check `references/gotchas.md`.

High-priority rules:

- Do not analyze raw base64 as natural language.
- Do not treat OCR as perfect truth.
- Do not treat heuristic image type as a confirmed label.
- Do not mention examples, old cases, or placeholder OCR errors unless they appear in the current `visual_packet`.
- Do not claim certainty when the visual_packet says uncertainty.
- Do not perform identity, sensitive attribute, medical, legal, or security-critical judgments.
- In multimodal mode, cite region IDs for important conclusions whenever annotated regions exist.
- In text-only mode, be clear that the agent is reasoning from a visual translation, not directly seeing the image.
- For workflow diagrams, do not invent arrows, decisions, or branches.
- For UI recreation, distinguish semantic rebuild from high-fidelity clone; preserve major spatial relationships when cloning.

## Main tool

`tools/visual_extract.py` converts images into a structured visual packet and annotated region map.

Basic usage:

```bash
python tools/visual_extract.py input.png --task screenshot_diagnosis --out outputs/case1
```

Outputs:

- `visual_packet.json`
- `visual_packet.md`
- `annotated_regions.png`
- `crops/region_*.png`
- `agent_instruction.md`

## Validation

Use `evals/run_evals.py` and `evals/prompts.csv` to run basic artifact validation and protocol checks.

A usable result should satisfy:

- visual_packet exists and validates against schema.
- annotated_regions exists.
- OCR blocks, text line groups, or layout regions exist for text-heavy images.
- final answer separates facts, inferences, evidence, uncertainties, and actions.
- critical text-based claims include evidence quotes.
