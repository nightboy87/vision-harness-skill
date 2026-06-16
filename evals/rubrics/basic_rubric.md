# Basic Rubric

Score each item 0/1.

## Artifact checks

- `visual_packet.json` exists.
- `visual_packet.md` exists.
- `annotated_regions.png` exists.
- JSON validates against `schemas/visual_packet.schema.json`.
- `text_line_groups` is present.
- `spatial_layout_analysis` is present.

## Answer checks

- Has observed facts.
- Has inferences separated from facts.
- Important OCR-based claims include evidence quotes, not only IDs.
- Has evidence region IDs or OCR block IDs.
- Has uncertainties.
- Has recommended actions or next checks.
- Does not mention old examples or placeholder OCR errors.
- Does not make unsupported high-risk claims.

## Screenshot diagnosis checks

- Distinguishes local success from global success.
- Treats visible errors as symptoms unless root cause evidence exists.
- Gives actionable next checks.

## Workflow checks

- Does not invent decision points without explicit evidence.
- Separates extracted SOP from inferred business interpretation.
- Marks candidate edges and unresolved connectors when arrow direction is uncertain.

## UI checks

- Produces a layout tree before HTML recreation.
- Preserves spatial constraints for fidelity clone.
- Does not use emoji icons as line-icon substitutes for UI recreation.
- Includes a fidelity self-check when generating HTML/CSS.
