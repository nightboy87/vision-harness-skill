# Agent Instruction

Use Vision Harness Skill with template: `screenshot_diagnosis`.

You are analyzing an image through a `visual_packet`. If you are a text-only agent, you cannot directly see the original image; reason only from the packet and be explicit about uncertainty. If you are a multimodal agent, inspect the original image, `annotated_regions.png`, and the packet together.

Required output sections:

1. Observed facts
2. Inferences
3. Evidence regions / OCR blocks
4. Uncertainties
5. Recommended actions

Rules:

- Do not treat OCR as perfect truth.
- Do not treat image type hypotheses as confirmed facts.
- Cite region IDs such as `region_003` and OCR IDs such as `text_001` when supporting a claim.
- If a region is unclear, say so instead of filling in missing details.
- Do not perform identity, medical, legal, security-critical, or sensitive-attribute judgments.
