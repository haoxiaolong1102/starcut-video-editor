#!/usr/bin/env python3
"""Render a reversible keep-segment cut list with external FFmpeg."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Render clean speech media from source keep segments.")
    parser.add_argument("input", type=Path, help="RAW source; never overwritten")
    parser.add_argument("cutlist", type=Path, help="JSON with segments containing source_in/source_out")
    parser.add_argument("output", type=Path, help="Derivative MP4 path")
    parser.add_argument("--crf", type=int, default=18)
    args = parser.parse_args()

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("FFmpeg not found. Install it separately and re-run starcut_doctor.py.")
    if args.input.resolve() == args.output.resolve():
        raise SystemExit("Refusing to overwrite RAW input.")
    if not args.input.is_file() or not args.cutlist.is_file():
        raise SystemExit("Input media or cut list does not exist.")
    data = json.loads(args.cutlist.read_text(encoding="utf-8"))
    segments = data.get("segments", [])
    if not segments:
        raise SystemExit("Cut list contains no keep segments.")

    filters = []
    labels = []
    previous = -1.0
    for index, segment in enumerate(segments):
        start = float(segment["source_in"])
        end = float(segment["source_out"])
        if start < 0 or end <= start or start < previous:
            raise SystemExit(f"Invalid or unsorted segment at index {index}: {start}..{end}")
        previous = end
        filters.append(f"[0:v]trim=start={start:.6f}:end={end:.6f},setpts=PTS-STARTPTS[v{index}]")
        filters.append(f"[0:a]atrim=start={start:.6f}:end={end:.6f},asetpts=PTS-STARTPTS[a{index}]")
        labels.append(f"[v{index}][a{index}]")
    filters.append("".join(labels) + f"concat=n={len(segments)}:v=1:a=1[vout][aout]")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".fffilter", encoding="utf-8", delete=False) as handle:
        handle.write(";\n".join(filters))
        filter_path = Path(handle.name)
    try:
        command = [
            ffmpeg, "-hide_banner", "-y", "-i", str(args.input),
            "-filter_complex_script", str(filter_path),
            "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-crf", str(args.crf), "-preset", "medium", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(args.output),
        ]
        proc = subprocess.run(command, check=False)
        if proc.returncode:
            raise SystemExit(proc.returncode)
    finally:
        filter_path.unlink(missing_ok=True)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
