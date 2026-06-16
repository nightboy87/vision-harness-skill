# Visual Packet Fields

## source
Input metadata, including filename, input type, and hash.

## image_properties
Dimensions, aspect ratio, orientation, and megapixels.

## visual_features
Low-level visual signals: brightness, contrast, edge density, dominant colors.

## layout_regions
Grid-based evidence anchors. Region IDs are used by the agent to cite where evidence appears.

## ocr_blocks
OCR text blocks, with raw text, normalized text, bounding boxes, confidence, and region IDs. May be empty if no OCR engine is installed.

## text_line_groups
Approximate OCR line grouping by vertical position. Useful for logs, tables, dashboards, and UI text clusters. Heuristic only.

## evidence_quotes
High-signal OCR blocks selected for easier citation in final answers. Agents should quote these for critical claims.

## spatial_layout_analysis
Heuristic spatial signals: text density, major dark-line candidates, region text counts, and layout hints such as left sidebar, right rail, top toolbar, bottom status area, or swimlane/grid candidate.

## structure_candidates
Heuristic candidates for UI elements, flow nodes, decision text, and chart-related regions based on OCR terms and layout signals.

## image_type_hypotheses
Heuristic guesses. They are not facts.

## routing
Recommended task template. The agent may override it if the user intent clearly says otherwise.

## uncertainties
Known limitations of the extraction.
