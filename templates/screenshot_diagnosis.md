# Screenshot Diagnosis Template

Use when the image is a software screenshot, error screenshot, dashboard, browser page, terminal capture, or system state image.

## Goal

Turn screenshot evidence into a structured troubleshooting diagnosis.

## Output schema

```json
{
  "task": "screenshot_diagnosis",
  "observed_facts": [],
  "error_signals": [],
  "inferences": [],
  "evidence_regions": [],
  "next_checks": [],
  "missing_info": [],
  "confidence": "low|medium|high",
  "uncertainties": []
}
```

## Procedure

1. Identify visible error messages or abnormal states.
2. Identify where they appear: region IDs and OCR text IDs.
3. Separate exact visual facts from likely causes.
4. Generate next checks that a human or Agent can perform.
5. Ask for missing logs, timestamps, URL, operation steps, or environment only if needed.

## Gotchas

- A visible error message is not the root cause.
- A 200 response or successful page load does not prove backend processing worked.
- A screenshot may show stale state.
- If the timestamp or URL is missing, mention that diagnosis is partial.
