# Changelog

## v0.1.2

This release is based on three scenario tests: technical screenshot diagnosis, workflow swimlane extraction, and UI screenshot reconstruction.

### Added

- Added `evidence_quotes` to `visual_packet` for raw/normalized OCR citation.
- Added `text_line_groups` to preserve line-level context for logs, dashboards, and UI text clusters.
- Added heuristic `spatial_layout_analysis`, including text density, major line signals, region text counts, and layout hints.
- Added stricter UI reconstruction modes: `ui_audit`, `ui_semantic_rebuild`, and `ui_fidelity_clone`.
- Added UI layout tree, spatial constraints, and fidelity self-check requirements.

### Changed

- Strengthened screenshot diagnosis template with explicit evidence quotes and stricter fact/inference separation.
- Revised workflow-to-SOP template to separate extracted SOP, inferred business interpretation, and suggested missing details.
- Decision points in workflow diagrams now require explicit visual or textual evidence.
- Updated README and SKILL.md to clarify current best use cases and boundaries.

### Fixed

- Added rules to prevent template pollution from old examples or placeholder OCR errors.
- Added gotchas for local success versus global success in technical screenshots.
- Added gotchas for status labels with counts, such as `异常（0）`.

### Known limits

- Flowchart topology recovery remains beta.
- UI reconstruction is semantic unless the driving model has strong frontend coding ability and follows fidelity constraints.
- OCR quality depends on installed OCR engine and image quality.

## v0.1.1

- Added separate English and Chinese README files.
- Improved release packaging.

## v0.1.0

- Initial script-backed skill package.
- Added visual packet extraction, annotated region generation, task templates, schemas, gotchas, and eval scaffold.
