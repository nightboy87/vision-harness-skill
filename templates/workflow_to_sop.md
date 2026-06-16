# Workflow To SOP Template

Use when the image is a flowchart, whiteboard process, workflow diagram, swimlane, architecture sketch, or process screenshot.

## Goal

Extract a tentative process structure and produce a draft SOP **without hiding topology uncertainty**.

In v0.1.2, this template is best for:

- extracting visible nodes;
- identifying swimlanes, stages, and roles;
- drafting a human-reviewable SOP skeleton.

It is not yet a fully reliable automatic topology parser.

## Required output schema

```json
{
  "task": "workflow_to_sop",
  "observed_facts": [],
  "nodes": [
    {
      "node_id": "",
      "text": "",
      "role_or_lane": "",
      "stage": "",
      "evidence_text_blocks": [],
      "evidence_regions": [],
      "confidence": "low|medium|high"
    }
  ],
  "confirmed_edges": [],
  "candidate_edges": [],
  "unresolved_connectors": [],
  "decision_points": [],
  "missing_links": [],
  "ambiguous_regions": [],
  "extracted_sop": [],
  "inferred_business_interpretation": [],
  "suggested_missing_details": [],
  "uncertainties": []
}
```

## Procedure

1. Identify the diagram type: swimlane, simple flowchart, whiteboard sketch, architecture diagram, or unknown.
2. Extract visible role/lane labels and stage labels as observed facts.
3. Extract visible node texts. Preserve raw wording.
4. Assign role/lane and stage only when spatial evidence supports it. If uncertain, mark `role_or_lane: unknown`.
5. Separate edges into:
   - `confirmed_edges`: arrows/lines clearly visible or explicitly represented in `visual_packet`;
   - `candidate_edges`: inferred from proximity or business logic;
   - `unresolved_connectors`: visible or suspected connectors whose direction is unclear.
6. Build `extracted_sop` only from visible nodes and confirmed/candidate edges, with confidence labels.
7. Put business-common-sense explanations into `inferred_business_interpretation`, not into observed facts.
8. Put missing conditions, exception branches, required fields, SLA, owners, and validation steps into `suggested_missing_details`.

## Hard rules

- OCR text alone is not process order. Edges matter.
- Do not invent missing arrows.
- Do not generate decision points unless there is explicit evidence: diamond shapes, condition words, `是否`, `判断`, `通过/失败`, `yes/no`, or equivalent visible text.
- If no explicit decision point is detected, write: `未检测到显式决策点；以下条件仅作为业务补充建议。`
- Do not mix extracted SOP with business enrichment. Keep `extracted_sop`, `inferred_business_interpretation`, and `suggested_missing_details` separate.
- Do not silently convert a non-linear workflow into a linear SOP.
- If lane assignment depends on coarse grid regions only, mark lane confidence as low or medium.

## v0.1.2 known limitation

The tool can detect OCR text, coarse grid regions, text line groups, and heuristic major line signals. It does not yet perform robust arrow-endpoint detection or full graph reconstruction. Treat workflow topology as beta unless manually verified.
