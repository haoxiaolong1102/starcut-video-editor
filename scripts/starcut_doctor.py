#!/usr/bin/env python3
"""Read-only StarCut capability probe. It never installs or changes dependencies."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def command_info(name: str) -> dict:
    path = shutil.which(name)
    result = {"available": bool(path), "path": path, "version": None}
    if not path:
        return result
    probes = {
        "ffmpeg": [path, "-version"],
        "ffprobe": [path, "-version"],
        "node": [path, "--version"],
        "npx": [path, "--version"],
        "python3": [path, "--version"],
        "hyperframes": [path, "--version"],
        "remotion": [path, "--version"],
    }
    try:
        proc = subprocess.run(
            probes.get(name, [path, "--version"]),
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=4,
        )
        result["version"] = (proc.stdout or "").splitlines()[0][:240]
    except (OSError, subprocess.TimeoutExpired):
        pass
    return result


def module_info(name: str) -> dict:
    spec = importlib.util.find_spec(name)
    return {"available": spec is not None, "path": getattr(spec, "origin", None)}


def local_binary(name: str) -> str | None:
    candidates = [
        Path.cwd() / "node_modules" / ".bin" / name,
        Path.cwd().parent / "node_modules" / ".bin" / name,
    ]
    return str(next((p for p in candidates if p.is_file()), "")) or None


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe StarCut dependencies without modifying the system.")
    parser.add_argument("--json", action="store_true", help="Print JSON only")
    args = parser.parse_args()

    commands = {name: command_info(name) for name in ("ffmpeg", "ffprobe", "python3", "node", "npx")}
    for name in ("hyperframes", "remotion"):
        info = command_info(name)
        if not info["available"]:
            local = local_binary(name)
            info.update({"available": bool(local), "path": local})
        commands[name] = info

    report = {
        "starcut": "0.1.0-rc.1",
        "required_ready": commands["ffmpeg"]["available"] and commands["ffprobe"]["available"],
        "commands": commands,
        "python_modules": {name: module_info(name) for name in ("cv2", "mediapipe", "numpy", "whisper")},
        "configuration": {
            "openchatcut_endpoint_configured": bool(os.getenv("STARCUT_OPENCHATCUT_URL")),
            "face_model_configured": bool(os.getenv("STARCUT_FACE_MODEL")),
            "music_provider_configured": any(
                bool(os.getenv(key))
                for key in ("MUREKA_API_KEY", "MINIMAX_API_KEY", "ATLAS_API_KEY", "SONILO_API_KEY")
            ),
        },
        "fallbacks": {
            "music": "configured provider/local licensed file" if any(
                bool(os.getenv(key))
                for key in ("MUREKA_API_KEY", "MINIMAX_API_KEY", "ATLAS_API_KEY", "SONILO_API_KEY")
            ) else "NO_MUSIC",
            "smoothing": "available after model check" if os.getenv("STARCUT_FACE_MODEL") else "SMOOTH_OFF",
        },
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"StarCut {report['starcut']} dependency report")
        for name, info in commands.items():
            print(f"  {'OK' if info['available'] else '--'} {name}: {info['path'] or 'not found'}")
        for name, info in report["python_modules"].items():
            print(f"  {'OK' if info['available'] else '--'} python:{name}")
        print(f"  Music fallback: {report['fallbacks']['music']}")
        print(f"  Required media tools ready: {report['required_ready']}")
    return 0 if report["required_ready"] else 2


if __name__ == "__main__":
    sys.exit(main())
