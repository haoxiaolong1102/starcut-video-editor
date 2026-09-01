# StarCut v0.1.0 License Audit

Audit date: 2026-09-01  
Scope: current `Xingjue_AI_Video_Editor` project and the StarCut release candidate.  
This is an engineering distribution audit, not legal advice.

## Release decision

The public ZIP contains only StarCut-original Markdown, JSON templates, and Python scripts under MIT. It contains no third-party repository source, package cache, binary, model, font, user media, image, SFX, or music. External tools are represented only by vendor-neutral adapter documentation and read-only detection.

## Classification

- **A — Original**: created for the current project and rewritten/generalized for StarCut.
- **B — Redistributable with terms**: license permits redistribution if its conditions are followed.
- **C — External only**: StarCut may detect/call it, but does not package it.
- **D — Notice required if bundled**: redistribution would require license/notice preservation.
- **E — Do not redistribute in StarCut**: license or provenance is incompatible/unclear for this public package.

## Audit table

| Item | Local evidence / upstream | License finding | Class | StarCut decision |
|---|---|---|---|---|
| StarCut core | `starcut-video-editor/` | MIT, original | A | bundled |
| Existing `xingjue` Skill rules/scripts | `.agents/skills/xingjue/` | project-original; no standalone license file | A/E | rewritten into generic StarCut rules; no brand art/model/lab copied |
| `video-spec-builder` | `.agents/skills/video-spec-builder/LICENSE` | MIT, copyright feicaiclub | B/D | not bundled; StarCut uses an original SHOTBOOK contract |
| video-talkcraft | upstream `Vincentwei1021/video-talkcraft` | PolyForm Noncommercial 1.0.0; commercial use requires prior authorization | C/E | no code, recipes, demos, SFX, or assets bundled; ideas not copied |
| OpenChatCut | `tools/OpenChatCut/LICENSE`, `package.json`, upstream `0xsline/OpenChatCut` | AGPL-3.0-or-later | C/D/E | external optional adapter only; repo and bundled fonts excluded |
| HyperFrames | upstream `heygen-com/hyperframes` | Apache-2.0 | B/C/D | external optional renderer; no source/package bundled |
| Remotion | upstream `remotion-dev/remotion/LICENSE.md` | custom source-available Remotion License with organization eligibility thresholds | C/E | external optional renderer; user must verify eligibility; no source/package bundled |
| GSAP | used by external HyperFrames projects | current usage terms are product/version dependent | C/E | no GSAP source/plugin bundled; renderer user resolves license |
| FFmpeg/FFprobe | system binary | LGPL 2.1+ by default; GPL/nonfree flags can change redistributability | C/D/E | required external executable; never bundled; doctor reports build/version only |
| Whisper | external package/model | code MIT; model artifact remains separately obtained | B/C/D | optional external transcription adapter; no code/model bundled |
| MediaPipe | Python dependency/model | framework Apache-2.0; model provenance is separate | B/C/D/E | external packages; no `face_landmarker.task` bundled |
| OpenCV | Python dependency | Apache-2.0 for current releases | B/C/D | external package only |
| NumPy | Python dependency | BSD-3-Clause | B/C/D | external package only |
| Lottie / Three.js / map SDKs | capability references only | varies by library and asset/provider | C/E | no library, animation JSON, map tiles, or keys bundled |
| Fonts | OpenChatCut fonts and local project fonts inspected by path | some OFL, others custom/free-commercial terms | C/D/E | no font files bundled; use system/user-licensed fonts |
| Images and branded visual masters | `.agents/skills/xingjue/assets/visual-masters/` | project/brand specific; provenance not suitable for generic redistribution | E | excluded |
| Face landmark model | `.agents/skills/xingjue/assets/models/face_landmarker.task` | exact artifact provenance not documented in project | E | excluded; user supplies verified model path |
| User videos/screenshots | `videos/` and attachments | user content, privacy and platform rights vary | E | excluded from package and tests |
| Music/SFX | project outputs and third-party tools | no universal redistributable set established | E | no media bundled; Music Adapter defaults to `NO_MUSIC` |
| Root OpenChatCut/music helper scripts | `scripts/openchatcut_mcp_call.mjs`, `scripts/generate_xingjue_bgm.mjs` | project-specific; former tightly coupled, latter unsuitable audio method | A/C/E | excluded; StarCut uses original adapter contracts and never random-tone fallback |

## Source-specific conclusions

### video-talkcraft

The upstream license states that toolkit commercial use requires authorization and uses PolyForm Noncommercial 1.0.0. StarCut therefore does not redistribute or derive code/recipe cards from it. It may be mentioned only as an external project the user can evaluate separately: <https://github.com/Vincentwei1021/video-talkcraft/blob/main/LICENSE>.

### OpenChatCut

The checked-out project declares `AGPL-3.0-or-later`. Releasing a modified or combined network-facing work can create source-availability obligations, and bundled font terms are mixed. StarCut does not copy or ship it. The adapter only documents how to detect a user-managed installation: <https://github.com/0xsline/OpenChatCut>.

### HyperFrames

Upstream identifies the project as Apache-2.0. It could be redistributed with its conditions, but StarCut intentionally keeps it external to stay small and renderer-neutral: <https://github.com/heygen-com/hyperframes>.

### Remotion

Remotion's current license is source-available rather than a permissive open-source license and includes organization-size/usage conditions. StarCut never packages it and makes no eligibility representation: <https://github.com/remotion-dev/remotion/blob/main/LICENSE.md>.

### FFmpeg

FFmpeg explains that its default license is LGPL and can become GPL depending on enabled components; nonfree configurations are not redistributable. StarCut requires a user/system installation and does not ship an executable: <https://ffmpeg.org/legal.html>.

## Publication gate

The MIT `LICENSE` is valid for the current StarCut-only ZIP because the packaging test rejects common binary/media/model/font/archive extensions and known third-party repository paths. Re-run this audit before adding any asset, dependency source, example media, or generated file.
