# Input contract

## Minimum

- `script`: final spoken text, preserving intended order.
- `primary_audio_or_video`: talking-head, voice recording, or explicitly approved synthetic voice.

## Optional

- screencasts, screenshots, photos, B-roll, logos, brand guide, cover copy, music, SFX, visual references, factual sources.

## Project manifest

Use UTF-8 JSON. Required fields:

```json
{
  "schema_version": "0.1",
  "project_id": "safe-kebab-case-id",
  "title": "Human-readable title",
  "script": "path/to/final-script.md",
  "primary_media": "path/to/raw.mp4",
  "output": {"width": 1080, "height": 1920, "fps": 30},
  "assets": [],
  "brand": {},
  "adapters": {
    "music": "none",
    "renderer": "auto",
    "transcription": "auto",
    "project_root": "/absolute/path/to/video-project",
    "remotion_license": "unknown"
  },
  "caption_layout": {
    "box": {"x": 90, "y": 1390, "width": 900, "height": 300},
    "min_font": 42,
    "max_font": 72,
    "max_lines": 3
  }
}
```

Every asset entry records `path`, `kind`, `source`, `license_or_permission`, and optional `semantic_tags`. Do not accept “from internet” as provenance.

## Ingest checks

- Confirm paths exist and are readable.
- Probe media streams without rewriting files.
- Flag mismatches between final script and spoken content.
- Detect orientation; never stretch horizontal media into vertical.
- Keep user media outside the distributable Skill and release ZIP.
- Record missing inputs as explicit fallbacks, not invented assets.
- `remotion_license` stays `unknown` until the installed version and intended use have been checked; never infer eligibility.
- Caption boxes use final-frame coordinates and must be calibrated by `fit_caption_layout.py` before rendering.
