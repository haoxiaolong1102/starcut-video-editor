# QA standard

## Editorial

- stumbles, false starts, duplicate wording, and perceptible empty gaps removed
- cuts sound continuous and retain natural breathing
- final script and spoken content agree
- first three seconds provide a concrete viewing reason
- no overly long stretch of presenter plus unchanged ordinary captions without intentional reason

## Semantic and evidence

- every visual corresponds to the current sentence
- real screenshots/recordings show the correct product, state, and target
- factual/data claims have provenance; generated art is not presented as evidence
- effect rationale is explanatory, not decorative

## Visual

- face, captions, software targets, and UI are not obstructed
- Chinese text fits and remains readable on a phone
- Screen Focus targets are correct; zoom is stable and not dizzying
- picturebook character, wardrobe, palette, scene, and direction remain consistent
- no black frames, accidental frozen frames, flashing, rapid bounce, or prolonged unreadable shot

## Face

- smoothing does not flicker or cross face edges
- eyes, brows, lips, hairline, beard, and facial identity retain detail
- no skin-tone, face-shape, or background change

## Audio

- speech is clear; no clicks at edits
- SFX are sparse and motivated
- music, if any, is licensed, audible but not dominant, and does not mask speech
- no fake/noise track substituted for unavailable music

## Technical

- final resolution 1080 x 1920 unless explicitly overridden
- valid H.264 video and AAC audio by default
- duration, frame rate, streams, and decode are verified with FFprobe/FFmpeg
- final file opens and plays through; no missing external asset

Use `assets/templates/QA_REPORT.md`. Any unresolved item marked `BLOCKER` prevents release.

Run `python3 scripts/qa_media.py path/to/final.mp4 --decode` for technical stream and full-decode checks. This complements, but never replaces, human editorial and visual review.
