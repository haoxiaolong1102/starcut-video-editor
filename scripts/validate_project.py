#!/usr/bin/env python3
"""Validate a StarCut project manifest and SHOTBOOK without third-party modules."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROLES = {"hook", "claim", "evidence", "demonstration", "comparison", "process", "data", "story", "opinion", "warning", "recap", "cta"}
MODES = {"talking_head", "screencast", "screenshot", "broll", "info_card", "kinetic_type", "data", "process", "comparison", "screen_focus", "picturebook", "collage", "motion_2d", "remotion_advanced", "three_d", "shader_mask_morph", "none"}
PRESENTERS = {"primary", "pip", "cropped_panel", "hidden"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(project: dict, book: dict) -> list[str]:
    errors: list[str] = []
    for key in ("schema_version", "project_id", "title", "script", "primary_media", "output", "assets", "adapters"):
        if key not in project:
            errors.append(f"project missing {key}")
    output = project.get("output", {})
    if output and (output.get("width") != 1080 or output.get("height") != 1920):
        errors.append("release fixture output must be 1080x1920")
    if project.get("project_id") != book.get("project_id"):
        errors.append("project_id mismatch")
    shots = book.get("shots")
    if not isinstance(shots, list) or not shots:
        return errors + ["shotbook must contain shots"]

    ids: set[str] = set()
    previous_end = 0.0
    for index, shot in enumerate(shots):
        label = shot.get("id", f"index {index}")
        required = ("id", "start", "end", "narration", "semantic_role", "visual_mode", "presenter_mode", "effect_level", "rationale", "fallback")
        for key in required:
            if key not in shot:
                errors.append(f"{label} missing {key}")
        if shot.get("id") in ids:
            errors.append(f"duplicate shot id {label}")
        ids.add(shot.get("id"))
        try:
            start, end = float(shot["start"]), float(shot["end"])
            if start < 0 or end <= start:
                errors.append(f"{label} has invalid timing")
            if start < previous_end - 0.001:
                errors.append(f"{label} overlaps previous shot")
            previous_end = end
        except (KeyError, TypeError, ValueError):
            errors.append(f"{label} timing is not numeric")
        if shot.get("semantic_role") not in ROLES:
            errors.append(f"{label} invalid semantic_role")
        if shot.get("visual_mode") not in MODES:
            errors.append(f"{label} invalid visual_mode")
        if shot.get("presenter_mode") not in PRESENTERS:
            errors.append(f"{label} invalid presenter_mode")
        if shot.get("effect_level") not in (0, 1, 2, 3):
            errors.append(f"{label} invalid effect_level")
        if shot.get("visual_mode") in {"three_d", "shader_mask_morph"} and shot.get("effect_level") != 3:
            errors.append(f"{label} advanced mode requires effect level 3")
        if shot.get("visual_mode") == "screen_focus" and "screen_focus" not in shot:
            errors.append(f"{label} screen_focus mode missing parameters")
        if shot.get("visual_mode") == "picturebook" and not shot.get("continuity_id"):
            errors.append(f"{label} picturebook missing continuity_id")
        if shot.get("semantic_role") == "evidence" and not (shot.get("provenance_refs") or any("source pending" in note.lower() for note in shot.get("qa_notes", []))):
            errors.append(f"{label} evidence lacks provenance or blocker")
        music = shot.get("music")
        if music and music != "none" and not isinstance(music, dict):
            errors.append(f"{label} music must be none or an adapter result")

    if abs(float(shots[0].get("start", 99))) > 0.15:
        errors.append("first shot must begin near zero")
    if abs(float(book.get("duration", -1)) - float(shots[-1].get("end", -2))) > 0.05:
        errors.append("duration must equal final shot end")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("shotbook", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    errors = validate(load(args.project), load(args.shotbook))
    result = {"valid": not errors, "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else ("PASS" if not errors else "FAIL\n- " + "\n- ".join(errors)))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
