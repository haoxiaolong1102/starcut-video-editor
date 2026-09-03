# Third-Party Notices

StarCut v0.1.0-rc.2 does **not** bundle third-party source code, executables, models, fonts, stock media, sound effects, or music. Its MIT license applies only to StarCut-original files.

The following optional external software may be detected or called when separately installed by the user. Each remains governed by its own license and terms:

| Optional dependency | Purpose | License / terms | Bundled? |
|---|---|---|---|
| FFmpeg / FFprobe | media probing, cutting, mixing, encoding | LGPL/GPL depending on build; see <https://ffmpeg.org/legal.html> | no |
| HyperFrames | HTML-native video composition/rendering | Apache-2.0; see <https://github.com/heygen-com/hyperframes> | no |
| Remotion | React video composition/rendering | Remotion License; see <https://github.com/remotion-dev/remotion/blob/main/LICENSE.md> | no |
| OpenAI Whisper | transcription/alignment | MIT for repository code; see <https://github.com/openai/whisper> | no |
| MediaPipe | face landmarks | Apache-2.0 for framework; see <https://github.com/google-ai-edge/mediapipe> | no |
| OpenCV | image/video processing | Apache-2.0; see <https://github.com/opencv/opencv> | no |
| NumPy | numerical processing | BSD-3-Clause; see <https://github.com/numpy/numpy> | no |
| OpenChatCut | optional editor/timeline bridge | AGPL-3.0-or-later; see <https://github.com/0xsline/OpenChatCut> | no |
| GSAP, Lottie, Three.js, map SDKs | optional animation/render capabilities | version/provider-specific terms | no |
| Mureka, MiniMax, Atlas, Sonilo | future music providers | service-specific terms and API access | no |

## Explicit exclusions

- `video-talkcraft` is not included or adapted. Its toolkit is PolyForm Noncommercial 1.0.0 and requires authorization for commercial use: <https://github.com/Vincentwei1021/video-talkcraft/blob/main/LICENSE>.
- `video-spec-builder` is not included. Its local copy is MIT-licensed and remains a separate Skill with its own copyright notice.
- Xingjue brand masters, user footage, screenshots, generated illustrations, the local face-landmarker model, OpenChatCut fonts, and Remotion lab packages are not included.

Users are responsible for installing optional dependencies and confirming that their intended use complies with the relevant license and service terms.
