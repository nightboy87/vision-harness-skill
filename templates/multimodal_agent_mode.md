# Multimodal Agent Mode

Use this mode when the agent can inspect images directly.

This mode makes a multimodal LLM analyze images with discipline instead of free-form description.

## Required inputs

Use all available inputs:

1. Original image
2. `annotated_regions.png`, if generated
3. `visual_packet.json` or `visual_packet.md`
4. Relevant task template

## Reading protocol

1. Classify the image type and user intent.
2. Scan the image globally.
3. Inspect evidence regions one by one.
4. Extract observed facts only.
5. Then derive inferences.
6. Attach evidence region IDs to each important inference.
7. Mark uncertainties.
8. Give task-specific recommended actions.

## Required output fields

```json
{
  "image_type": "",
  "user_intent": "",
  "observed_facts": [],
  "inferences": [],
  "evidence_chain": [
    {
      "claim": "",
      "evidence_regions": [],
      "evidence_text_blocks": [],
      "confidence": "low|medium|high"
    }
  ],
  "uncertainties": [],
  "recommended_actions": []
}
```

## Avoid

- Do not answer with only aesthetic comments.
- Do not say “clearly” when the relevant region is blurred, small, or not OCR-supported.
- Do not skip uncertainty.
- Do not ignore `visual_packet` when it exists.
