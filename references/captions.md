# Caption direction

- Generate captions from the cleaned narration timeline, not the RAW source.
- Prefer one complete short phrase at a time; break at meaning and natural breath.
- Use high-contrast Chinese-capable typography and mobile-safe sizing.
- Keep captions away from the face, software target, native UI, and platform chrome.
- Highlight only semantic keywords, numbers, negation, contrast, or the result.
- Do not animate every word with identical bounce.
- On screencasts, choose a dedicated caption band or adaptive position based on the active focus target.
- On picturebook shots, preserve illustration focal points and negative space.
- Check punctuation, English terms, proper names, and numbers manually. Check line overflow programmatically before render and visually after render.

Captions may interact with subjects or diagrams only when the compositing is stable and the result remains readable. Plain captions are the correct fallback.

## Box-fit contract

Every layout state supplies the caption box as `x,y,width,height` in 1080 x 1920 coordinates or as a per-cue `box` object. Run:

```bash
python3 scripts/fit_caption_layout.py captions.json caption-layout.json --box 90,1390,900,300
```

The renderer must consume the returned `lines`, `font_size`, and `line_height_px`; it must not recompute a larger style afterward. Provide `--font /legal/local/font.ttf` for exact Pillow metrics when available. Without it, StarCut uses a conservative Unicode estimate and records that mode. Any `fits: false`, unsafe box, clipped glyph, or mismatch between the layout manifest and rendered frame is a blocker.

Test the longest Chinese cue, mixed Chinese/English cue, largest highlighted keyword, and each layout state at a phone-sized preview. Reducing text, moving the box, or reducing the font is preferable to clipping.
