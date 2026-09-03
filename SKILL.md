---
name: starcut-video-editor
description: Direct and edit semantic-first 9:16 videos from talking-head footage, a final script, and optional screencasts, screenshots, images, B-roll, or visual references. Use for rough-cutting speech, word timelines, hooks, SHOTBOOK planning, evidence-led visual routing, screen focus, picturebook motion, captions, skin-only smoothing, sound design, optional music, rendering, and QA for explainers, AI education, vlogs, product demos, and opinion videos.
license: MIT
metadata:
  author: StarCut contributors
  version: "0.1.0-rc.2"
---

# StarCut Video Editor

Build one coherent video from meaning, evidence, and the presenter. Do not decorate every sentence and do not pretend an unavailable adapter ran.

Compatibility: the Agent must be able to read files and run local commands. FFmpeg/FFprobe are required for media work; transcription, renderers, face landmarks, image generation, and music are optional external adapters.

## Non-negotiable rules

1. Treat every RAW input as read-only. Write derivatives to a separate work or render directory.
2. Understand the sentence before choosing its visual form.
3. Prefer evidence in this order: real evidence, real screencast, real screenshot, infographic, original generated visual, pure decoration.
4. Keep the presenter as the narrative anchor, but do not force a static talking head full-screen when a demonstration explains the point better.
5. Delete real silence, stumbles, false starts, and repeated wording; preserve enough breath for speech to sound human. Never trust amplitude-only cutting without word-timeline review.
6. Use an effect only if removing it would make the idea harder to understand.
7. If an optional dependency or API is missing, choose the documented fallback. Never fabricate a recording, citation, generated image, song, or successful render.
8. Do not upload media or publish externally without explicit authorization.
9. Do not begin visual assembly until the speech analysis gate passes and the clean narration derivative exists.
10. Do not silently ignore a detected, eligible Remotion adapter for Level 2/3 shots; create an explicit render plan and retain successful render receipts.
11. Do not render captions from guessed CSS sizes. Fit every cue to its actual design box first; overflow is a blocker.

## Required inputs and safe assumptions

Inspect supplied files before asking questions. The minimum production input is a final script plus either a voice/talking-head recording or an approved synthetic voice track. Screencasts, screenshots, B-roll, brand rules, reference media, music, and cover copy are optional.

If unspecified, use 1080 x 1920, 30 fps, H.264/AAC, safe mobile margins, no music, restrained motion, and `SMOOTH_HIGH` only when the smoothing adapter is available and verified. Record assumptions in the project brief; do not invent facts or brand assets.

Read [references/input-contract.md](references/input-contract.md) when ingesting a project.

## Workflow

### 1. Diagnose and preserve

- Run `python3 scripts/starcut_doctor.py --json --project-root /path/to/video-project` from this skill directory.
- Inventory inputs, licenses/provenance, duration, dimensions, frame rate, audio tracks, and intended output.
- Copy or reference RAW assets without overwriting them.
- Create the project brief from `assets/templates/PROJECT_BRIEF.md`.

### 2. Build the speech edit

- Produce word-level timestamps with an available transcription adapter.
- Align the final script to spoken words.
- Mark silence, filler, false starts, repeated phrases, misreads, and retakes as edit candidates.
- Review edit boundaries on both waveform and speech context. Add short audio crossfades where required.
- Export a continuous clean narration edit before designing visuals.

Run the executable gate rather than merely describing the edit:

```bash
python3 scripts/prepare_speech_edit.py RAW.mp4 work/speech-analysis.json \
  --cutlist work/rough-cutlist.json --word-timeline work/words.json
python3 scripts/render_cutlist.py RAW.mp4 work/rough-cutlist.json work/clean-speech.mp4
```

If the first command exits with a blocker, resolve word-boundary conflicts and repeated-word candidates before continuing. `render_cutlist.py` refuses an unapproved manifest. Listen through the clean derivative once; visuals and captions must use this cleaned timeline, never RAW timing.

Read [references/talking-head-editing.md](references/talking-head-editing.md). If transcription is unavailable, stop automated word cutting and request/provide a timestamped transcript fallback; do not guess.

### 3. Segment semantics and judge the Hook

Split by complete meaning, not by subtitle line. Label each segment with one primary role such as hook, claim, evidence, demonstration, comparison, process, data, story, opinion, warning, recap, or CTA. The first three seconds must contain a concrete viewing reason, not only branding.

### 4. Create the SHOTBOOK

Generate structured `shotbook.json` and a readable `SHOTBOOK.md` using [references/shotbook-schema.md](references/shotbook-schema.md). Every shot must point to source time, spoken meaning, visual choice, asset provenance, effect level, fallback, and why that visual helps.

Validate it with:

```bash
python3 scripts/validate_project.py path/to/project.json path/to/shotbook.json
```

### 5. Route visuals intelligently

Read [references/visual-router.md](references/visual-router.md) for every project. Load only the needed specialist reference:

- visual effects and complexity: [references/effect-library.md](references/effect-library.md)
- software demonstrations: [references/screen-focus.md](references/screen-focus.md)
- continuous illustrated scenes: [references/picturebook-motion.md](references/picturebook-motion.md)
- captions: [references/captions.md](references/captions.md)
- audio/music: [references/audio-and-music.md](references/audio-and-music.md)

Use real source media at its natural aspect ratio. Crop or reframe deliberately; do not stretch it to fit a decorative frame. Generated visuals must be original and consistently art-directed.

### 6. Select external adapters

Read [references/adapters.md](references/adapters.md). Choose from capabilities detected by the doctor:

- FFmpeg/FFprobe: required media inspection, assembly, audio, and encoding.
- Whisper-compatible aligner: optional word timeline.
- HyperFrames: optional fast HTML information packaging.
- Remotion: optional React-based advanced motion; users must verify current license eligibility.
- OpenChatCut: optional external timeline/editor bridge; never bundled.
- Face landmarks/OpenCV: optional skin-only smoothing.
- Image generator: optional original picturebook or collage assets.
- Music provider/local library: optional and non-blocking.

Core planning and QA remain renderer-neutral. Platform-specific setup belongs in `adapters/`, never in the core workflow.

Save the detector output and create a per-shot renderer plan:

```bash
python3 scripts/detect_adapters.py --project-root /path/to/video-project > work/adapter-report.json
python3 scripts/build_render_plan.py work/shotbook.json work/adapter-report.json work/render-plan.json \
  --remotion-license eligible
```

Use `eligible` only after the installed Remotion version and the user's use have been checked. When an automatic Level 2/3 shot selects Remotion, build and render it with the external Remotion project and record a successful receipt using `assets/templates/RENDER_RECEIPTS.json`. Planning or HTML mockups are not proof that Remotion ran.

### 7. Composite, captions, skin, and sound

- Keep face, captions, operating targets, and platform UI unobstructed.
- Prefer restrained easing, stable holds, and semantic camera moves. Avoid flashing, rapid bouncing, cursor-chasing, and fast local-to-local jumps.
- Apply skin-only smoothing as a non-destructive derivative. Default `SMOOTH_HIGH`; preserve eyes, eyebrows, eyelashes, lips, nostrils, hairline, beard, face shape, and skin tone. Read [references/smoothing.md](references/smoothing.md).
- Keep speech intelligible. Use sparse semantic SFX. Music defaults to `NO_MUSIC` unless a licensed local file or configured provider exists.
- Generate caption cues from `clean-speech.mp4`, define the real designed box for each layout state, and run `python3 scripts/fit_caption_layout.py work/captions.json work/caption-layout.json --box x,y,width,height`. Apply the returned line breaks and font size in the renderer. A cue with `fits: false` must be shortened, reboxed, or restyled before rendering.

### 8. Render and QA

Render a short proof first when a new adapter, face pipeline, picturebook character, or camera system is used. Then render the final master and run [references/qa-standard.md](references/qa-standard.md). Create `QA_REPORT.md` from the template; unresolved blocking checks mean the deliverable is not complete.

Before calling a video finished, run the mandatory artifact gate:

```bash
python3 scripts/validate_production.py work/speech-analysis.json work/render-plan.json \
  work/caption-layout.json --render-receipts work/render-receipts.json
```

Then run technical media QA. A missing clean-speech approval, missing Remotion/HyperFrames receipt, or caption overflow is a release blocker.

## Deliverables

Unless the user narrows scope, deliver:

- clean speech master or edit decision list
- word timeline
- `speech-analysis.json` and approved reversible cut list
- project brief
- `shotbook.json` and `SHOTBOOK.md`
- source/provenance manifest
- editable project files for the selected renderer
- `render-plan.json`, renderer receipts, and `caption-layout.json`
- final 1080 x 1920 MP4
- `QA_REPORT.md`

Report exact output paths. Clean temporary files only after explicit confirmation and never delete RAW inputs.

## Boundaries

- StarCut does not include third-party renderers, transcription models, face-landmark models, fonts, stock footage, SFX, or music.
- StarCut may call them only after detection, license review, and user configuration.
- Do not copy recipes or source from video-talkcraft, OpenChatCut, or another project into a StarCut output.
- Do not claim that WorkBuddy, Yuanqi, Doubao, or another client supports one-click Skill import unless its current official product documentation confirms it.
- Read [references/licensing-boundaries.md](references/licensing-boundaries.md) before distributing or embedding any dependency or media.
