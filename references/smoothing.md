# Skin-only smoothing

## Levels

- `SMOOTH_OFF`: no processing.
- `SMOOTH_NORMAL`: restrained denoise and edge-preserving blend on skin.
- `SMOOTH_HIGH`: visibly smoother but still textured; StarCut default when the face pipeline is available.

`SMOOTH_CUSTOM` may tune values later but is not a portable preset.

## Mask contract

Track face landmarks temporally and feather a skin-only mask. Exclude eyes, eyebrows, eyelashes, lips, nostrils, hairline, and as much beard texture as possible. Restore detail only in those protected areas; never sharpen the entire face.

## Prohibited changes

No whitening, recoloring, face slimming, eye enlargement, nose/chin reshaping, automatic makeup, lipstick, or tooth whitening. Do not change background or global color.

## Stability

- Smooth landmark/mask movement over time.
- Limit frame-to-frame strength variation.
- Test speech, blinking, head turns, partial occlusion, and re-entry.
- If tracking confidence drops, reduce/disable the effect instead of freezing a stale mask.
- Process to a derivative file and retain RAW.

Use `scripts/smooth_skin_pipeline.py` only after installing its documented external dependencies and supplying a legally obtained compatible face-landmarker model.
