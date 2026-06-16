# UI Audit Template

Use when the image is a product UI, web page, app screen, form, dashboard, or interface screenshot and the user wants review or improvement advice.

## Goal

Produce a structured UI review with evidence regions and prioritized fixes.

## Output schema

```json
{
  "task": "ui_audit",
  "observed_facts": [],
  "layout_summary": "",
  "information_density": "low|medium|high|unknown",
  "primary_focus": "",
  "issues": [
    {
      "issue": "",
      "evidence_regions": [],
      "severity": "low|medium|high",
      "reason": ""
    }
  ],
  "evidence_regions": [],
  "priority_fixes": [],
  "uncertainties": []
}
```

## Procedure

1. Describe layout and primary focus.
2. Evaluate information density.
3. Check readability, hierarchy, call-to-action clarity, and possible confusion points.
4. Tie every major issue to a region ID.
5. Give prioritized fixes, not generic praise.

## Gotchas

- Do not output vague comments like “整体不错”.
- Do not judge brand fit unless brand requirements are provided.
- Do not claim conversion impact without evidence.
- If text is unreadable, mark readability uncertainty.
