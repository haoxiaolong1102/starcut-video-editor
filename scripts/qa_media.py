#!/usr/bin/env python3
"""Technical media QA using external FFprobe and optional full FFmpeg decode."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("media", type=Path)
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--decode", action="store_true", help="Decode the complete file and report errors")
    args = parser.parse_args()
    ffprobe, ffmpeg = shutil.which("ffprobe"), shutil.which("ffmpeg")
    if not ffprobe or (args.decode and not ffmpeg):
        raise SystemExit("Required FFprobe/FFmpeg command not found.")
    if not args.media.is_file():
        raise SystemExit(f"Media not found: {args.media}")

    probe = subprocess.run(
        [ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(args.media)],
        check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if probe.returncode:
        print(json.dumps({"pass": False, "errors": [probe.stderr.strip()]}, ensure_ascii=False, indent=2))
        return 1
    info = json.loads(probe.stdout)
    video = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)
    audio = next((s for s in info.get("streams", []) if s.get("codec_type") == "audio"), None)
    errors = []
    notes = []
    if not video:
        errors.append("missing video stream")
    else:
        if (video.get("width"), video.get("height")) != (args.width, args.height):
            errors.append(f"expected {args.width}x{args.height}, got {video.get('width')}x{video.get('height')}")
        if video.get("codec_name") != "h264":
            notes.append(f"video codec is {video.get('codec_name')}, not default h264")
    if not audio:
        errors.append("missing audio stream")
    elif audio.get("codec_name") != "aac":
        notes.append(f"audio codec is {audio.get('codec_name')}, not default aac")

    decode_ok = None
    if args.decode:
        decoded = subprocess.run(
            [ffmpeg, "-v", "error", "-i", str(args.media), "-map", "0", "-f", "null", "-"],
            check=False, text=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
        )
        decode_ok = decoded.returncode == 0
        if not decode_ok:
            errors.append("full decode failed: " + decoded.stderr[-1000:])
    result = {
        "pass": not errors,
        "media": str(args.media.resolve()),
        "duration": info.get("format", {}).get("duration"),
        "video": video,
        "audio": audio,
        "decode_ok": decode_ok,
        "errors": errors,
        "notes": notes,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
