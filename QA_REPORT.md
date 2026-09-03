# StarCut v0.1.0-rc.2 QA Report

Date: 2026-09-03
Scope: portable Skill package, speech-edit gate, deterministic renderer routing, caption box fitting, schema tests, dependency detection, and prior representative render evidence.
Result: **PASS WITH NOTES — Public prerelease, not stable v0.1.0**

## Format and package

- PASS — Agent Skills name/description/frontmatter validate with the bundled skill-creator validator.
- PASS — `SKILL.md` uses progressive disclosure and routes detail to focused references.
- PASS — core workflow contains no platform-exclusive dependency.
- PASS — release packager rejects video, audio, images, fonts, models, binaries, nested ZIPs, vendor directories, and unknown build caches.
- PASS — MIT license and third-party audit/notices are present.
- PASS — a synthetic 1080 x 1920 H.264/AAC source was cut from two keep segments by `render_cutlist.py`; the derivative fully decoded without errors.
- PASS — the cross-Agent installer copied a clean Skill into an isolated generic Agent directory without `dist`, `.git`, caches, or vendor dependencies.
- PASS — external adapter detection reports actual availability and preserves `NO_MUSIC`/other fallbacks without installing anything.
- PASS — silence-log fixture removes a verified 1.04-second non-speaking interval while preserving adjacent word spans.
- PASS — unapproved word boundaries or repeated-word review block cut-list rendering and visual assembly.
- PASS — a Level 2 data shot automatically selects detected, explicitly eligible Remotion.
- PASS — multilingual captions are automatically sized and line-broken inside the declared design box and mobile safe area.
- PASS — the production validator requires clean-speech approval, actual renderer receipts, and passing caption layout before delivery.

## Test A — Talking-head AI knowledge explainer

- Fixture: `tests/fixtures/talking-head-ai-*`
- PASS — routed Hook to kinetic type, opinion to presenter, quantity/structure to data visual, and recap to information card.
- PASS — generated SHOTBOOK passed timing, role, mode, effect-level, and output-schema validation.
- PASS — an existing representative 9:16 production master was probed as H.264/AAC, 1080 x 1920 and fully decoded without errors.
- NOTE — user footage and its output are evidence only and are not included in the release package.

## Test B — Software operation / screencast

- Fixture: `tests/fixtures/screencast-*`
- PASS — routed actual operation to `screen_focus`, verified screen evidence to `screencast`, and retained presenter for warning/context.
- PASS — focus contract includes FULL VIEW/ZOOM/HOLD/RETURN and target-accuracy fallback.
- PASS — generated SHOTBOOK passed schema/provenance validation.
- PASS — archived representative production metadata reports H.264/AAC, 1080 x 1920, 30 fps, and a renderer check with zero runtime/motion errors.
- NOTE — the archived renderer check contained non-blocking layout/contrast warnings from the old project. StarCut's new QA standard requires resolving equivalent warnings before a future final release.

## Test C — Vlog / continuous picturebook mode

- Fixture: `tests/fixtures/picturebook-*`
- PASS — routed story to continuous picturebook with one continuity ID, process to a flow, and CTA back to presenter.
- PASS — generated SHOTBOOK passed continuity and schema validation.
- PASS — existing continuous-picturebook preview decoded as 1080 x 1920 H.264 at 30 fps; representative final master decoded as 1080 x 1920 H.264/AAC.
- NOTE — no generated/user illustration is included in the portable ZIP.

## Environment

- PASS — FFmpeg 8.0.1 and FFprobe 8.0.1 detected.
- PASS — Node.js and `npx` detected.
- PASS — project-root detection finds the external Remotion package used by the local OpenChatCut installation; no global HyperFrames command is present.
- EXPECTED FALLBACK — main Python environment lacks MediaPipe and Whisper; `SMOOTH_OFF` and external/user-supplied word timeline are required until configured.
- PASS — no music provider/API key detected; fallback is `NO_MUSIC` and production remains unblocked.

## Editorial/visual runtime checklist

These checks apply to every real project and cannot be universally pre-certified by a Skill ZIP:

- speech cuts and repeated-word removal require source-specific listening
- caption accuracy/face obstruction require final-frame review
- real screenshot and focus target correctness require source-specific review
- picturebook identity and edge continuity require generated-asset review
- smoothing flicker requires a talking/turning 10-second proof
- audio balance and complete playback require the actual final master

The Skill correctly treats unresolved items as project blockers rather than claiming they passed.

## RC decision

StarCut v0.1.0-rc.2 passes portable format, original-rule boundary, deterministic router, the three reported production gates, representative workflow fixtures, dependency fallback, and packaging tests. Before stable `v0.1.0`, perform fresh end-to-end renders on a clean machine for each chosen external adapter and resolve client-specific import verification.
