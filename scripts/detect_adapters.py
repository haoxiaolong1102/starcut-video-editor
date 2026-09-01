#!/usr/bin/env python3
"""Read-only detection of StarCut's external adapter candidates."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def command(name: str) -> dict:
    path = shutil.which(name)
    if not path:
        for candidate in (Path.cwd() / "node_modules" / ".bin" / name, Path.cwd().parent / "node_modules" / ".bin" / name):
            if candidate.is_file():
                path = str(candidate)
                break
    return {"available": bool(path), "path": path}


def module(name: str) -> dict:
    spec = importlib.util.find_spec(name)
    return {"available": spec is not None, "path": getattr(spec, "origin", None)}


def openchatcut() -> dict:
    candidates = [
        os.getenv("STARCUT_OPENCHATCUT_PATH"),
        str(Path.cwd() / "tools" / "OpenChatCut"),
        str(Path.home() / "OpenChatCut"),
        "/Applications/OpenChatCut.app",
    ]
    existing = next((str(Path(value).expanduser().resolve()) for value in candidates if value and Path(value).expanduser().exists()), None)
    return {
        "available": bool(existing or os.getenv("STARCUT_OPENCHATCUT_URL")),
        "path": existing,
        "endpoint_configured": bool(os.getenv("STARCUT_OPENCHATCUT_URL")),
        "license": "AGPL-3.0-or-later; external only",
    }


def main() -> int:
    report = {
        "core": {"starcut": "0.1.0-rc.1", "skill_root": str(ROOT)},
        "required": {"ffmpeg": command("ffmpeg"), "ffprobe": command("ffprobe")},
        "renderers": {"hyperframes": command("hyperframes"), "remotion": command("remotion")},
        "timeline": {"openchatcut": openchatcut()},
        "transcription": {"whisper": module("whisper")},
        "smoothing": {name: module(name) for name in ("cv2", "mediapipe", "numpy")},
        "music": {
            "configured": any(os.getenv(key) for key in ("MUREKA_API_KEY", "MINIMAX_API_KEY", "ATLAS_API_KEY", "SONILO_API_KEY")),
            "fallback": "NO_MUSIC",
        },
        "policy": "Detection only. No third-party source, binary, model, media, or credential is bundled or installed.",
    }
    report["ready_for_media"] = all(item["available"] for item in report["required"].values())
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ready_for_media"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
