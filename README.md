# StarCut v0.1.0-rc.2

StarCut is a portable Agent Skill for directing and editing vertical, speech-led videos. It turns a final script, a talking-head or voice recording, and optional real media into a clean speech edit, word timeline, semantic SHOTBOOK, evidence-led visual plan, captions, restrained motion, optional skin-only smoothing, and a QA-checked 9:16 master.

Repository: <https://github.com/haoxiaolong1102/starcut-video-editor>

Downloads: [latest release](https://github.com/haoxiaolong1102/starcut-video-editor/releases/latest) · [portable Agent Skill ZIP](https://github.com/haoxiaolong1102/starcut-video-editor/releases/download/v0.1.0-rc.2/starcut-video-editor.zip) · [WorkBuddy manual package](https://github.com/haoxiaolong1102/starcut-video-editor/releases/download/v0.1.0-rc.2/starcut-video-editor-workbuddy-manual.zip)

It is not a renderer, a caption-only tool, or a repackaged third-party project. The ZIP contains StarCut's original instructions, schemas, validators, templates, and adapter contracts. FFmpeg, transcription engines, renderers, face models, image generators, and music services remain external.

## What it can direct

- talking-head explainers and opinion videos
- software and web demonstrations with semantic Screen Focus
- product explainers and evidence tours
- vlogs with continuous narration and reframed inserts
- consistent picturebook/collage sequences with limited motion
- renderer-neutral motion plans for HyperFrames or Remotion

## Quick start

1. Download and unzip `starcut-video-editor.zip`.
2. Run `python3 scripts/install_starcut.py --agent codex --scope project --project /path/to/project` (or choose WorkBuddy/generic as documented in `INSTALL.md`).
3. Run `python3 scripts/starcut_doctor.py --project-root /path/to/video-project` and `python3 scripts/detect_adapters.py --project-root /path/to/video-project`.
4. Ask the agent to use `starcut-video-editor` and provide the final script plus media paths.
5. Review the clean speech edit and SHOTBOOK before the full render.

For client-specific setup, see `adapters/`. For clients without Agent Skill import, use `adapters/generic-agent/`.

See `BUNDLE_MANIFEST.md` for the exact included capabilities and external adapter boundary.

## Safety and licensing

RAW assets are read-only. Music is optional and defaults to no music. StarCut never silently uploads media and never bundles third-party source, models, fonts, footage, or audio. See `LICENSE_AUDIT.md` and `THIRD_PARTY_NOTICES.md` before distribution.

## Status

`0.1.0-rc.2`: adds mandatory executable gates for silence/repetition editing, automatic eligible-Remotion routing with real render receipts, and caption font/line fitting inside designed boxes. External renderer/API integrations still require environment-specific smoke tests before a production release.
