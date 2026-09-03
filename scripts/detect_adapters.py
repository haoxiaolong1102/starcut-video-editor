#!/usr/bin/env python3
"""Read-only detection of StarCut's external adapter candidates."""

from __future__ import annotations

import importlib.util
import argparse
import json
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def command(name: str, project_root: Path | None = None) -> dict:
    path = shutil.which(name)
    kind = "command" if path else None
    if not path:
        roots = [root for root in (project_root, project_root / "tools" / "OpenChatCut" if project_root else None, Path.cwd(), Path.cwd().parent) if root]
        candidates = [root / "node_modules" / ".bin" / name for root in roots]
        for candidate in candidates:
            if candidate.is_file():
                path = str(candidate)
                kind = "project-command"
                break
        if not path and name in {"remotion", "hyperframes"}:
            packages = [root / "node_modules" / name / "package.json" for root in roots]
            package = next((candidate for candidate in packages if candidate.is_file()), None)
            if package:
                path = str(package.parent)
                kind = "project-package"
    return {"available": bool(path), "path": path, "kind": kind}


def module(name: str) -> dict:
    spec = importlib.util.find_spec(name)
    return {"available": spec is not None, "path": getattr(spec, "origin", None)}


def openchatcut(project_root: Path) -> dict:
    candidates = [
        os.getenv("STARCUT_OPENCHATCUT_PATH"),
        str(project_root / "tools" / "OpenChatCut"),
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
    parser = argparse.ArgumentParser(description="Detect external StarCut adapters without installing anything.")
    parser.add_argument("--project-root", type=Path, default=Path.cwd(), help="Project containing local node_modules")
    args = parser.parse_args()
    project_root = args.project_root.expanduser().resolve()
    report = {
        "core": {"starcut": "0.1.0-rc.2", "skill_root": str(ROOT), "project_root": str(project_root)},
        "required": {"ffmpeg": command("ffmpeg", project_root), "ffprobe": command("ffprobe", project_root)},
        "renderers": {"hyperframes": command("hyperframes", project_root), "remotion": command("remotion", project_root)},
        "timeline": {"openchatcut": openchatcut(project_root)},
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
