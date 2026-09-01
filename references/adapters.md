# Adapter architecture

StarCut plans and validates; external adapters implement capabilities. Detection must never mutate the environment.

## Status contract

Every adapter reports `available`, `version`, `path_or_endpoint`, `license_status`, `configured`, and `notes`. `available` does not imply configured, licensed for the user's use, or successful.

## Required

- **FFmpeg/FFprobe**: probe, cut, mix, and encode. Install separately. Check build flags and license before redistribution.

## Optional

- **Whisper-compatible transcription/alignment**: create word timestamps. No bundled model.
- **HyperFrames**: fast HTML composition and render. External install.
- **Remotion**: advanced React composition. External install and license eligibility review.
- **OpenChatCut**: timeline/editor bridge. External user installation only.
- **OpenCV + MediaPipe**: skin-only smoothing. External Python packages and model.
- **Image generation**: original picturebook/collage frames; record provider and permissions.
- **Music**: local licensed track or configured provider. Missing capability means `NO_MUSIC`.

## Fallback ladder

- advanced renderer missing → SHOTBOOK + generic edit manifest, or another available renderer
- image generation missing → screenshot/B-roll/information graphic/presenter
- face stack missing → `SMOOTH_OFF`
- transcription missing → user-provided word timeline or stop automated dialogue cutting
- music missing → `NO_MUSIC`

Adapter documents live under `adapters/`. They may describe commands but must not vendor third-party source or models.
