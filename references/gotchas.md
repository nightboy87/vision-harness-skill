# Vision Harness Gotchas

These are the rules that prevent the agent from producing attractive but unreliable visual analysis.

## General

- Base64 is transport, not meaning. Never analyze raw base64 as if it were image content.
- A `visual_packet` is a translation. It can lose information.
- Do not treat image type hypotheses as facts.
- Do not hide uncertainty. If something is not visible, say it.
- Do not mention examples, old cases, placeholder strings, or prior test artifacts unless they appear in the current packet.
- Do not infer identity, age, race, political affiliation, medical conditions, or other sensitive attributes.
- Do not make medical, legal, security-critical, or safety-critical decisions from images.

## OCR

- OCR can miss small, blurred, low-contrast, rotated, handwritten, or stylized text.
- OCR can split one phrase into multiple blocks.
- OCR can merge neighboring labels.
- OCR may lose punctuation, slashes, spaces, Chinese punctuation, or path separators.
- If a conclusion depends on exact text, quote both `raw_text` and `normalized_text` when possible.
- Evidence IDs alone are not enough for critical conclusions. Include the text quote.

## Layout regions

- Grid regions are evidence anchors, not semantic object detections.
- A high-complexity region may contain text, lines, icons, or noise.
- Region IDs support evidence tracing; they do not prove semantic meaning.
- For workflow diagrams and UI recreation, coarse 3x3 regions are not sufficient for final topology or high-fidelity layout.

## Screenshot diagnosis

- A visible error message is a symptom, not automatically the root cause.
- A screenshot may represent stale state.
- Local PASS/success signals do not prove the entire workflow succeeded.
- UI labels with counts, such as `异常（0）`, may mean zero abnormal items; do not automatically mark contradiction.
- Always ask for logs, operation steps, URL, timestamp, or environment when root cause cannot be determined.
- Next checks must be actionable.

## Workflow to SOP

- OCR text alone does not define process order.
- Do not invent missing arrows or branch conditions.
- Separate action nodes from decision points.
- Only output `decision_points` when there is explicit visual or textual evidence.
- Split the result into extracted SOP, inferred interpretation, and suggested missing details.
- Mark ambiguous arrows and broken links.
- Workflow topology is beta in v0.1.2 unless manually verified.

## UI audit and HTML recreation

- Avoid generic praise.
- Tie recommendations to visible evidence.
- Do not claim conversion-rate effects without data.
- If brand or user persona is unknown, mark it as unknown.
- For UI recreation, distinguish semantic rebuild from high-fidelity clone.
- Do not redesign when the user asks to clone or recreate.
- Do not use emoji icons as substitutes for UI line icons.
- Preserve major spatial relationships: sidebar, header, alert strip, right rail, bottom grid, and status bar when present.
- HTML quality depends on the driving model's frontend coding ability; this skill supplies visual structure and constraints.
