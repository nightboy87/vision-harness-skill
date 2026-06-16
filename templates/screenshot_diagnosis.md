# Screenshot Diagnosis Template

Use when the image is a software screenshot, error screenshot, dashboard, browser page, terminal capture, IDE/build log, or system state image.

## Goal

Turn screenshot evidence into a structured troubleshooting diagnosis. The result must be useful for a human or another agent to perform the next checks.

## Required output schema

```json
{
  "task": "screenshot_diagnosis",
  "observed_facts": [],
  "error_signals": [
    {
      "signal": "",
      "severity": "info|warning|fail|critical",
      "evidence_regions": [],
      "evidence_text_blocks": [],
      "evidence_quotes": []
    }
  ],
  "success_signals": [],
  "inferences": [
    {
      "claim": "",
      "evidence_regions": [],
      "evidence_text_blocks": [],
      "confidence": "low|medium|high"
    }
  ],
  "next_checks": [],
  "missing_info": [],
  "confidence": "low|medium|high",
  "uncertainties": []
}
```

## Procedure

1. Scan high-signal `evidence_quotes` first. Quote `raw_text` or `normalized_text` when making critical claims.
2. Identify visible error messages, failure states, warnings, abnormal statuses, or contradictory states.
3. Identify visible success signals separately. A local success does not prove the whole task succeeded.
4. Build a short timeline only if timestamps or ordered log lines are visible in the packet.
5. Separate exact visual facts from likely causes.
6. Generate next checks that a human or agent can actually perform.
7. Ask for missing logs, timestamps, URL, operation steps, environment, or config only when needed.

## Hard rules

- Only OCR text, image metadata, layout regions, line groups, and directly visible UI states may be listed as `observed_facts`.
- Root causes, dependency mapping, toolchain assumptions, service relationships, and build-stage interpretation must be listed as `inferences`.
- Every `critical` or `fail` signal must include at least one evidence quote, not only an ID.
- Do not mention examples, placeholder strings, or old-case OCR errors unless they appear in the current `visual_packet`.
- Do not treat local PASS / success as global success if later failure signals exist.
- If OCR confidence is low or text is garbled, quote it and mark uncertainty instead of silently normalizing it.

## Gotchas

- A visible error message is a symptom, not automatically the root cause.
- A 200 response or successful page load does not prove backend processing worked.
- A screenshot may show stale state.
- UI status labels with counts, such as `异常（0）`, may mean zero abnormal items; do not assume contradiction without confirming wording.
- If the timestamp, URL, config, or operation history is missing, state that diagnosis is partial.
