# UI Audit and UI Reconstruction Template

Use when the image is a product UI, web page, app screen, form, dashboard, desktop software interface, or product screenshot.

## Goal

Analyze the UI with evidence and, when requested, provide a structured basis for HTML/CSS reconstruction.

## Choose the mode

- `ui_audit`: review usability, information architecture, hierarchy, consistency, and risks.
- `ui_semantic_rebuild`: generate a runnable HTML draft that preserves content and major modules, but may simplify layout.
- `ui_fidelity_clone`: generate a closer HTML/CSS recreation that must preserve major spatial positions and avoid redesign.

If the user says “复刻”, “还原”, “clone”, or “recreate”, default to `ui_fidelity_clone` unless they explicitly ask for redesign.

## Required output schema

```json
{
  "task": "ui_audit",
  "mode": "ui_audit|ui_semantic_rebuild|ui_fidelity_clone",
  "observed_facts": [],
  "layout_tree": {},
  "spatial_constraints": [],
  "information_density": "low|medium|high|unknown",
  "primary_focus": "",
  "issues": [],
  "evidence_regions": [],
  "priority_fixes": [],
  "fidelity_checklist": [],
  "html_recreation_notes": [],
  "uncertainties": []
}
```

## Procedure for UI audit

1. Describe the page type and likely product purpose.
2. Extract the layout tree before judging the UI.
3. Evaluate hierarchy, readability, density, consistency, and action clarity.
4. Tie every major issue to region IDs and OCR quotes.
5. Give prioritized fixes, not generic praise.

## Procedure for HTML recreation

Before writing HTML, first produce:

1. `layout_tree`
2. `region_to_component_map`
3. `spatial_constraints`
4. `style_tokens`
5. `fidelity_checklist`

Only then write the HTML/CSS.

## Layout tree expectations

For dashboard or SaaS screenshots, check whether these exist:

- window title bar;
- left sidebar;
- top header/title area;
- top action buttons;
- alert/status strip;
- main statistics area;
- right summary rail;
- bottom card grid;
- table/list area;
- bottom status bar.

The generated HTML should preserve these major spatial relationships unless the user explicitly asks for redesign.

## Spatial constraints for fidelity clone

When `mode = ui_fidelity_clone`, follow these rules:

- Preserve the left/right/top/bottom position of major regions.
- Do not move a right-side summary rail into top statistic cards.
- Do not stack bottom two-column cards vertically unless screen size requires responsive behavior.
- Do not remove a visible alert/status strip merely because it looks redundant.
- Do not add new large sections not present in the original image.
- Do not use emoji icons as substitutes for line icons. Use simple CSS shapes, inline SVG placeholders, or text labels.
- Use visual similarity over aesthetic redesign.

## Fidelity self-check

After generating HTML, include a short self-check:

1. Is the window/title-bar structure represented if visible?
2. Is the sidebar width and position roughly preserved?
3. Is the top alert/status strip preserved if visible?
4. Is the right summary rail preserved if visible?
5. Are bottom cards horizontal or vertical as in the original?
6. Did the output add sections that were not in the image?
7. Did the output move core modules to different regions?

## Gotchas

- Do not output vague comments like “整体不错”.
- Do not judge brand fit unless brand requirements are provided.
- Do not claim conversion impact without evidence.
- UI copy containing counts, such as `异常（0）`, may mean zero items; do not treat it as a contradiction unless the wording clearly says the state is abnormal.
- HTML recreation quality also depends on the driving model's front-end coding ability. This skill supplies visual structure and constraints; it does not guarantee pixel-perfect code generation.
