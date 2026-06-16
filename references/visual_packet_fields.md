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
OCR text blocks, with bounding boxes and confidence. May be empty if no OCR engine is installed.

## structure_candidates
Heuristic candidates for UI elements, flow nodes, and chart-related regions based on OCR terms and layout signals.

## image_type_hypotheses
Heuristic guesses. They are not facts.

## routing
Recommended task template. The agent may override it if the user intent clearly says otherwise.

## uncertainties
Known limitations of the extraction.
