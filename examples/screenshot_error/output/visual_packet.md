# Visual Packet

## Source
- File: `sample_error.png`
- Input type: `path`

## Image properties
- width: 900
- height: 520
- aspect_ratio: 1.731
- orientation: landscape
- megapixels: 0.47

## Visual features
- Brightness: bright (220.88)
- Contrast: medium (64.12)
- Edge density: low (1.97)
- Dominant colors: #f5f5f5, #fefefe, #263238, #a0a8b9, #f6f5f5, #212d33

## OCR blocks
- text_001 @ region_001: `Internal` bbox=[26, 19, 91, 33] confidence=0.96
- text_002 @ region_001: `Admin` bbox=[99, 19, 155, 33] confidence=0.96
- text_003 @ region_001: `Console` bbox=[163, 19, 233, 33] confidence=0.96
- text_004 @ region_005: `502` bbox=[312, 211, 361, 231] confidence=0.96
- text_005 @ region_005: `Bad` bbox=[375, 210, 424, 231] confidence=0.96
- text_006 @ region_005: `Gateway` bbox=[437, 211, 559, 237] confidence=0.96
- text_007 @ region_005: `Upstream` bbox=[312, 254, 396, 271] confidence=0.96
- text_008 @ region_005: `service` bbox=[404, 257, 467, 267] confidence=0.96
- text_009 @ region_005: `timeout` bbox=[474, 254, 544, 267] confidence=0.96

## Layout regions
- region_001: grid_cell bbox=[0, 0, 300, 173] weight=high text_ids=['text_001', 'text_002', 'text_003'] notes=top_left; brightness=178.5, complexity=91.9
- region_002: grid_cell bbox=[300, 0, 600, 173] weight=high text_ids=[] notes=top_center; brightness=174.9, complexity=94.4
- region_003: grid_cell bbox=[600, 0, 900, 173] weight=high text_ids=[] notes=top_right; brightness=175.2, complexity=94.3
- region_004: grid_cell bbox=[0, 173, 300, 346] weight=low text_ids=[] notes=middle_left; brightness=245.8, complexity=6.8
- region_005: grid_cell bbox=[300, 173, 600, 346] weight=medium text_ids=['text_004', 'text_005', 'text_006', 'text_007', 'text_008', 'text_009'] notes=middle_center; brightness=232.9, complexity=49.7
- region_006: grid_cell bbox=[600, 173, 900, 346] weight=low text_ids=[] notes=middle_right; brightness=245.8, complexity=6.7
- region_007: grid_cell bbox=[0, 346, 300, 520] weight=low text_ids=[] notes=bottom_left; brightness=245.0, complexity=0.0
- region_008: grid_cell bbox=[300, 346, 600, 520] weight=low text_ids=[] notes=bottom_center; brightness=245.0, complexity=0.0
- region_009: grid_cell bbox=[600, 346, 900, 520] weight=low text_ids=[] notes=bottom_right; brightness=245.0, complexity=0.0

## Image type hypotheses
- system_error_screenshot (medium_to_high): OCR contains error-like terms, text-heavy image

## Routing
- Recommended template: `screenshot_diagnosis`
- Reason: User or caller specified task.

## Uncertainties
- OCR may miss small, blurred, rotated, handwritten, or low-contrast text.
- Layout regions are grid-based and heuristic; they are evidence anchors, not semantic objects.
- Image type hypotheses are heuristic and must not be treated as confirmed facts.
- The tool does not use a multimodal LLM and cannot reliably identify arbitrary objects or scenes.
- Flow arrows and chart values are not fully parsed in v0.1; use human review for critical decisions.

## Agent notes
Image size: 900x520 (landscape, aspect_ratio=1.731).
Brightness: bright; contrast: medium; edge_density: low (1.97).
OCR blocks detected: 9. Layout regions: 9.
Top image type hypothesis: system_error_screenshot (medium_to_high). Evidence: OCR contains error-like terms, text-heavy image.
Recommended template: screenshot_diagnosis. Reason: User or caller specified task..
OCR excerpt: Internal | Admin | Console | 502 | Bad | Gateway | Upstream | service | timeout
Important: This packet is a visual translation. Treat heuristic labels as hypotheses, not facts.
