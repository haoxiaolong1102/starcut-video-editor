#!/usr/bin/env python3
"""Fit multilingual captions inside explicit design boxes before rendering.

Uses real font metrics when Pillow and a font path are available. Otherwise it uses
a conservative Unicode-width estimate and marks the measurement mode in the output.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path


def parse_box(value: str) -> dict:
    try:
        x, y, width, height = (float(part) for part in value.split(","))
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError("Box must be x,y,width,height")
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("Box width and height must be positive")
    return {"x": x, "y": y, "width": width, "height": height}


def font_measurer(font_path: Path | None):
    if font_path:
        try:
            from PIL import ImageFont  # type: ignore

            if font_path.is_file():
                def measured(text: str, size: int) -> float:
                    return float(ImageFont.truetype(str(font_path), size=size).getlength(text))

                return measured, "font-metrics"
        except (ImportError, OSError):
            pass

    def estimated(text: str, size: int) -> float:
        units = 0.0
        for char in text:
            if char.isspace():
                units += 0.32
            elif unicodedata.east_asian_width(char) in {"W", "F"}:
                units += 1.0
            elif char.isupper():
                units += 0.64
            elif char.islower():
                units += 0.56
            elif char.isdigit():
                units += 0.58
            else:
                units += 0.5
        return units * size

    return estimated, "conservative-unicode-estimate"


def tokens_for_wrap(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9._/+\-]*|\s+|.", text, flags=re.DOTALL)


def wrap_text(text: str, size: int, max_width: float, measure) -> list[str]:
    lines: list[str] = []
    current = ""
    for token in tokens_for_wrap(text):
        if token == "\n":
            lines.append(current.rstrip())
            current = ""
            continue
        proposal = (current + token).lstrip() if not current else current + token
        if current and measure(proposal, size) > max_width:
            lines.append(current.rstrip())
            current = token.lstrip()
        else:
            current = proposal
    if current or not lines:
        lines.append(current.rstrip())
    return lines


def fit_one(text: str, box: dict, min_font: int, max_font: int, max_lines: int, line_height: float, measure) -> dict:
    selected = None
    for size in range(max_font, min_font - 1, -1):
        lines = wrap_text(text, size, box["width"], measure)
        width = max((measure(line, size) for line in lines), default=0.0)
        height = len(lines) * size * line_height
        if len(lines) <= max_lines and width <= box["width"] + 0.01 and height <= box["height"] + 0.01:
            selected = (size, lines, width, height, True)
            break
    if selected is None:
        size = min_font
        lines = wrap_text(text, size, box["width"], measure)
        width = max((measure(line, size) for line in lines), default=0.0)
        height = len(lines) * size * line_height
        selected = (size, lines, width, height, False)
    size, lines, width, height, fits = selected
    return {
        "font_size": size,
        "lines": lines,
        "line_height_px": round(size * line_height, 3),
        "measured_width": round(width, 3),
        "measured_height": round(height, 3),
        "fits": fits,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fit caption text into a renderer-neutral design box.")
    parser.add_argument("captions", type=Path, help="JSON list or object containing cues")
    parser.add_argument("output", type=Path, help="caption-layout.json destination")
    parser.add_argument("--frame-width", type=int, default=1080)
    parser.add_argument("--frame-height", type=int, default=1920)
    parser.add_argument("--box", type=parse_box, default=parse_box("90,1390,900,300"))
    parser.add_argument("--safe-margin", type=int, default=60)
    parser.add_argument("--min-font", type=int, default=42)
    parser.add_argument("--max-font", type=int, default=72)
    parser.add_argument("--max-lines", type=int, default=3)
    parser.add_argument("--line-height", type=float, default=1.2)
    parser.add_argument("--font", type=Path, help="Optional local font for exact measurement; never bundled")
    args = parser.parse_args()

    data = json.loads(args.captions.read_text(encoding="utf-8"))
    cues = data if isinstance(data, list) else data.get("cues", [])
    if not isinstance(cues, list) or not cues:
        raise SystemExit("Caption input must contain a non-empty cues list.")
    if args.min_font <= 0 or args.max_font < args.min_font or args.max_lines <= 0 or args.line_height <= 0:
        raise SystemExit("Invalid font or line constraints.")

    measure, measurement_mode = font_measurer(args.font)
    layouts = []
    previous_end = 0.0
    for index, cue in enumerate(cues):
        text = str(cue.get("text", "")).strip()
        box = cue.get("box", args.box)
        if not text:
            layouts.append({"id": cue.get("id", f"C{index + 1:03d}"), "text": text, "box": box, "fits": False, "blocker": "empty caption"})
            continue
        resolved = fit_one(text, box, args.min_font, args.max_font, args.max_lines, args.line_height, measure)
        inside_safe = (
            box["x"] >= args.safe_margin
            and box["y"] >= args.safe_margin
            and box["x"] + box["width"] <= args.frame_width - args.safe_margin
            and box["y"] + box["height"] <= args.frame_height - args.safe_margin
        )
        resolved.update(
            {
                "id": cue.get("id", f"C{index + 1:03d}"),
                "start": cue.get("start"),
                "end": cue.get("end"),
                "text": text,
                "box": box,
                "inside_safe_area": inside_safe,
            }
        )
        try:
            start, end = float(cue.get("start")), float(cue.get("end"))
            timing_valid = start >= -0.001 and end > start and start >= previous_end - 0.001
            previous_end = max(previous_end, end)
        except (TypeError, ValueError):
            timing_valid = False
        resolved["timing_valid"] = timing_valid
        resolved["fits"] = bool(resolved["fits"] and inside_safe)
        if not resolved["fits"] or not timing_valid:
            resolved["blocker"] = "caption does not fit its design box/safe area or has invalid clean-timeline timing"
        layouts.append(resolved)

    passed = all(item.get("fits") and item.get("timing_valid") for item in layouts)
    output = {
        "schema_version": "0.2",
        "frame": {"width": args.frame_width, "height": args.frame_height, "safe_margin": args.safe_margin},
        "measurement_mode": measurement_mode,
        "font": str(args.font.resolve()) if args.font and args.font.is_file() else None,
        "overall_pass": passed,
        "cues": layouts,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"overall_pass": passed, "measurement_mode": measurement_mode, "output": str(args.output)}, ensure_ascii=False))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
