# Vision Harness Gotchas

These are the rules that prevent the agent from producing attractive but unreliable visual analysis.

## General

- Base64 is transport, not meaning. Never analyze raw base64 as if it were image content.
- A visual_packet is a translation. It can lose information.
- Do not treat image type hypotheses as facts.
- Do not hide uncertainty. If something is not visible, say it.
- Do not infer identity, age, race, political affiliation, medical conditions, or other sensitive attributes.
- Do not make medical, legal, security-critical, or safety-critical decisions from images.

## OCR

- OCR can miss small, blurred, low-contrast, rotated, handwritten, or stylized text.
- OCR can split one phrase into multiple blocks.
- OCR can merge neighboring labels.
- If a conclusion depends on exact text, mention the OCR confidence and ask for confirmation when needed.

## Layout regions

- v0.1 regions are evidence anchors, not semantic object detections.
- A high-complexity region may contain text, lines, icons, or noise.
- Region IDs support evidence tracing; they do not prove semantic meaning.

## Screenshot diagnosis

- A visible error message is a symptom, not automatically the root cause.
- A screenshot may represent stale state.
- Always ask for logs, operation steps, URL, timestamp, or environment when root cause cannot be determined.
- Next checks must be actionable.

## Workflow to SOP

- OCR text alone does not define process order.
- Do not invent missing arrows or branch conditions.
- Separate action nodes from decision points.
- Mark ambiguous arrows and broken links.

## UI audit

- Avoid generic praise.
- Tie recommendations to visible evidence.
- Do not claim conversion-rate effects without data.
- If brand or user persona is unknown, mark it as unknown.
