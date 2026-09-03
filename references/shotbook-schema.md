# SHOTBOOK schema

`shotbook.json` is the machine contract; `SHOTBOOK.md` is its readable projection. Timing is expressed on the clean narration timeline.

## Root

```json
{
  "schema_version": "0.1",
  "project_id": "example",
  "duration": 12.4,
  "shots": []
}
```

## Shot fields

Required:

- `id`: unique `S001` form.
- `start`, `end`: numeric seconds, `0 <= start < end`, monotonic, no unexplained overlap.
- `narration`: the spoken semantic unit.
- `semantic_role`: `hook|claim|evidence|demonstration|comparison|process|data|story|opinion|warning|recap|cta`.
- `visual_mode`: `talking_head|screencast|screenshot|broll|info_card|kinetic_type|data|process|comparison|screen_focus|picturebook|collage|motion_2d|remotion_advanced|three_d|shader_mask_morph|none`.
- `presenter_mode`: `primary|pip|cropped_panel|hidden`.
- `effect_level`: integer 0–3.
- `rationale`: one sentence answering how the visual improves understanding.
- `fallback`: valid lower-complexity replacement.

Optional:

- `asset_refs`: asset IDs from the project manifest.
- `provenance_refs`: citations, capture notes, or permissions.
- `screen_focus`: `{state, target, zoom, hold}`.
- `on_screen_text`: short text, never a transcript dump.
- `caption_style`, `caption_box`, `preferred_renderer`, `sfx`, `music`, `transition_in`, `transition_out`, `qa_notes`.

## Invariants

- The first shot begins at 0 within a 0.15-second tolerance.
- `screen_focus` requires `screencast` or `screen_focus` mode.
- `three_d` and `shader_mask_morph` require level 3 and a concrete explanatory rationale.
- Evidence claims require an asset/provenance reference or a visible `source pending` QA blocker.
- Picturebook sequences share a continuity ID and asset bible.
- Music may be `none`; a provider name without a rendered/licensed file is invalid.
- A renderer plan created from the final SHOTBOOK records the actual renderer for every shot; selected Remotion/HyperFrames shots require render receipts.
- `caption_box` is measured in final-frame coordinates and must pass the caption layout fitter.
