#!/usr/bin/env python3
"""Create a conservative, renderer-neutral SHOTBOOK draft from semantic segments."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROUTES = {
    "hook": ("kinetic_type", "primary", 1),
    "claim": ("talking_head", "primary", 0),
    "evidence": ("screenshot", "pip", 1),
    "demonstration": ("screen_focus", "pip", 2),
    "comparison": ("comparison", "cropped_panel", 2),
    "process": ("process", "cropped_panel", 2),
    "data": ("data", "cropped_panel", 2),
    "story": ("picturebook", "hidden", 2),
    "opinion": ("talking_head", "primary", 0),
    "warning": ("talking_head", "primary", 1),
    "recap": ("info_card", "cropped_panel", 1),
    "cta": ("talking_head", "primary", 0),
}


def choose(segment: dict) -> tuple[str, str, int, str]:
    role = segment["semantic_role"]
    available = set(segment.get("available_assets", []))
    preferred, presenter, level = ROUTES[role]

    if role == "evidence":
        if "real_screencast" in available:
            return "screencast", "pip", 1, "Show the strongest available real evidence."
        if "real_screenshot" not in available:
            return "talking_head", "primary", 0, "No verified evidence asset is available; do not fabricate one."
    if role == "demonstration" and "real_screencast" not in available:
        if "real_screenshot" in available:
            return "screenshot", "pip", 1, "Use verified steps as still evidence because no recording is available."
        return "talking_head", "primary", 0, "Keep the presenter and mark the missing demonstration asset."
    if role == "story" and "image_generation" not in available and "broll" not in available:
        return "talking_head", "primary", 0, "No story asset adapter is available; use the presenter fallback."
    if role == "story" and "broll" in available:
        return "broll", "hidden", 1, "Use real or licensed B-roll before generated art."

    reasons = {
        "kinetic_type": "Turn the central wording into the immediate viewing reason.",
        "talking_head": "The speaker's judgment or relationship is the most meaningful visual.",
        "screenshot": "A verified source makes the claim easier to trust.",
        "screen_focus": "The viewer must see the exact operation on a phone screen.",
        "comparison": "The contrast is clearer when both states share one visual grammar.",
        "process": "A progressive flow exposes order and dependency.",
        "data": "A scaled data view makes the quantity understandable.",
        "picturebook": "A continuous original scene makes an otherwise unseen story concrete.",
        "info_card": "A compact summary consolidates the takeaway.",
    }
    return preferred, presenter, level, reasons[preferred]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("segments", type=Path, help="JSON file containing project_id and segments")
    parser.add_argument("output", type=Path, help="Destination shotbook.json")
    args = parser.parse_args()
    data = json.loads(args.segments.read_text(encoding="utf-8"))
    shots = []
    for index, segment in enumerate(data["segments"], 1):
        mode, presenter, level, rationale = choose(segment)
        shot = {
            "id": f"S{index:03d}",
            "start": segment["start"],
            "end": segment["end"],
            "narration": segment["narration"],
            "semantic_role": segment["semantic_role"],
            "visual_mode": mode,
            "presenter_mode": presenter,
            "effect_level": level,
            "rationale": rationale,
            "fallback": "talking_head",
            "asset_refs": segment.get("asset_refs", []),
            "provenance_refs": segment.get("provenance_refs", []),
        }
        if mode == "screen_focus":
            shot["screen_focus"] = {"state": "FULL_VIEW", "target": "pending", "zoom": 1.35, "hold": 1.5}
        if mode == "picturebook":
            shot["continuity_id"] = segment.get("continuity_id", f"{data['project_id']}-story")
        if segment["semantic_role"] == "evidence" and not shot["provenance_refs"]:
            shot["qa_notes"] = ["BLOCKER: source pending"]
        shots.append(shot)

    result = {
        "schema_version": "0.1",
        "project_id": data["project_id"],
        "duration": shots[-1]["end"] if shots else 0,
        "shots": shots,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
