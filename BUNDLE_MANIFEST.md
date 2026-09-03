# StarCut Integration Manifest

StarCut is one installable Skill package, not a renamed collection of third-party repositories.

## Included in the ZIP

| Capability | Origin | Delivery |
|---|---|---|
| semantic-first editing workflow | StarCut original, generalized from the creator's verified Xingjue production workflow | core `SKILL.md` and references |
| talking-head silence/repetition workflow | StarCut original | FFmpeg silence analyzer + word-boundary/repetition gate + reversible cut-list renderer |
| SMART VISUAL ROUTER | StarCut original | deterministic router + schema |
| SHOTBOOK | StarCut original | JSON/Markdown contract + validator |
| Screen Focus | StarCut original | FULL VIEW / ZOOM / HOLD / RETURN director rules |
| picturebook/collage continuity | StarCut original | continuity bible and limited-motion rules |
| kinetic type, data, flow, parallax, mask, morph, 3D routing | StarCut original behavior contracts | renderer-neutral effect library |
| presenter and captions | StarCut original | framing rules + automatic caption box/font/line fitter |
| skin-only smoothing | StarCut original implementation | optional OpenCV/MediaPipe script; no model bundled |
| optional music interface | StarCut original | provider-neutral contract; `NO_MUSIC` fallback |
| media and project QA | StarCut original | speech/render/caption production gates, FFprobe/full-decode QA and templates |
| cross-Agent installation | StarCut original | Codex, WorkBuddy and custom-directory installer |

## Detected and called, but not copied

| External project | Why it stays external | StarCut integration |
|---|---|---|
| OpenChatCut | AGPL-3.0-or-later and mixed bundled asset terms | endpoint/path detection and optional timeline adapter |
| video-talkcraft | PolyForm Noncommercial; commercial use requires authorization | no code or recipe import; not an install target |
| HyperFrames | separate Apache-2.0 renderer and release cycle | optional HTML renderer adapter |
| Remotion | custom source-available license and eligibility conditions | optional React renderer adapter |
| FFmpeg/FFprobe | actual binary license depends on build flags | required external media engine |
| Whisper-compatible aligner | code/model acquisition and runtime vary | optional word-timestamp contract |
| MediaPipe/OpenCV/NumPy | Python packages and model are separate artifacts | optional smoothing adapter |
| Mureka/MiniMax/Atlas/Sonilo/local music | API, cost and music rights vary | optional music contract |

## Explicitly excluded

User footage, screenshots, brand images, fonts, model files, music, SFX, stock footage, third-party `node_modules`, external repositories, API keys, tokens, browser data, and project caches are never included.

This design lets another Agent install one StarCut package and obtain the full production logic while keeping external tools legally and operationally independent.
