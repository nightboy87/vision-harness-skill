# Text Agent Mode

Use this mode when the current LLM cannot directly inspect images.

## Required workflow

1. Run the visual extraction tool:

```bash
python tools/visual_extract.py <image_path_or_base64_or_data_url> --task auto --out <output_dir>
```

2. Read `visual_packet.json` or `visual_packet.md`.
3. Select the recommended template from `routing.recommended_template`.
4. Answer using only evidence from the packet.

## Required answer structure

```markdown
## 结论

## 观察到的事实
- ...

## 推测与解释
- 推测：...
  - 依据：region_..., text_...

## 不确定点
- ...

## 下一步动作
- ...
```

## Non-negotiable rules

- You are not directly seeing the image. You are reasoning from a visual translation.
- Do not invent objects, people, UI controls, or chart values that are not in the packet.
- If OCR is empty or low-confidence, say text could not be reliably read.
- If a user asks for a high-risk decision, refuse or ask for professional/human review.
