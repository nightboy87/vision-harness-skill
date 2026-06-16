# Workflow To SOP Template

Use when the image is a flowchart, whiteboard process, workflow diagram, swimlane, architecture sketch, or process screenshot.

## Goal

Extract a tentative process structure and convert it into a draft SOP while preserving uncertainty.

## Output schema

```json
{
  "task": "workflow_to_sop",
  "observed_facts": [],
  "nodes": [],
  "edges": [],
  "decision_points": [],
  "start_node": "",
  "end_nodes": [],
  "missing_links": [],
  "ambiguous_regions": [],
  "draft_sop": [],
  "uncertainties": []
}
```

## Procedure

1. List all visible node texts.
2. Identify likely start and end nodes.
3. Identify visible arrows or directional cues.
4. Extract decision points separately from action steps.
5. Build a draft SOP only from visible evidence.
6. Mark missing arrows, ambiguous branches, unreadable nodes, and crossing lines.

## Gotchas

- OCR text alone is not a workflow. Edges matter.
- Do not invent missing arrows.
- If arrow direction is unclear, put it into `ambiguous_regions`.
- If a flowchart has loops, do not force it into a linear SOP without noting the loop.
