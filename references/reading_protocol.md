# Structured Visual Reading Protocol

## Principle

Visual analysis should move from observation to interpretation, not the reverse.

## Steps

1. Determine user intent.
2. Determine image type.
3. Extract visible facts.
4. Attach evidence to facts and inferences.
5. Quote raw/normalized OCR text when a claim depends on text.
6. Separate inferences from observations.
7. Mark unknowns and weak evidence.
8. Recommend next actions.
9. Run the task-specific self-check before finalizing.

## Fact vs inference

Fact:

- OCR block `text_001` says `502 Bad Gateway`.
- Region `region_005` contains the highest visual complexity.
- The packet contains a right-side cluster of text blocks.

Inference:

- The service may be behind a reverse proxy.
- The page likely failed during upstream request handling.
- The right-side cluster is probably a summary rail.

Both are useful, but they must not be mixed.

## Evidence quality levels

High:

- Clear OCR quote plus region ID.
- Visible label or state is directly available.
- Multiple packet fields support the same claim.

Medium:

- OCR quote exists but may be merged or low-confidence.
- Region/location supports the interpretation, but exact label is unclear.

Low:

- Proximity-only or business-logic-only inference.
- Coarse grid region without a precise node, control, or arrow.

## Self-check

Before final answer, ask:

- Did I quote evidence for critical claims?
- Did I move any inference into observed facts?
- Did I invent missing arrows, decisions, UI sections, or root causes?
- Did I mention uncertainty where the packet is weak?
- Did I accidentally include examples from old cases?
