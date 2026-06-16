# Structured Visual Reading Protocol

## Principle

Visual analysis should move from observation to interpretation, not the reverse.

## Steps

1. Determine user intent.
2. Determine image type.
3. Extract visible facts.
4. Attach evidence to facts and inferences.
5. Separate inferences from observations.
6. Mark unknowns and weak evidence.
7. Recommend next actions.

## Fact vs inference

Fact:
- OCR block `text_001` says `502 Bad Gateway`.
- Region `region_005` contains the highest visual complexity.

Inference:
- The service may be behind a reverse proxy.
- The page likely failed during upstream request handling.

Both are useful, but they must not be mixed.
