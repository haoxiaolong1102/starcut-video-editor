#!/usr/bin/env python3
"""Fail final delivery when speech, renderer, or caption proof is missing."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path) -> dict:
    if not path.is_file():
        raise SystemExit(f"Required production artifact not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate StarCut's three mandatory production gates.")
    parser.add_argument("speech_report", type=Path)
    parser.add_argument("render_plan", type=Path)
    parser.add_argument("caption_layout", type=Path)
    parser.add_argument("--render-receipts", type=Path, help="JSON receipts from actual Remotion/HyperFrames renders")
    parser.add_argument("--planning-only", action="store_true", help="Allow missing render receipts before final rendering")
    args = parser.parse_args()

    speech = load(args.speech_report)
    plan = load(args.render_plan)
    captions = load(args.caption_layout)
    errors = []

    if not speech.get("gate", {}).get("approved_for_visuals"):
        errors.append("speech gate failed: unresolved silence boundary or repeated-word review")
    if not plan.get("overall_pass") or plan.get("blockers"):
        errors.append("render plan has blockers")
    if not captions.get("overall_pass") or any(not cue.get("fits") for cue in captions.get("cues", [])):
        errors.append("caption layout overflowed its design box or safe area")
    cue_ends = [float(cue["end"]) for cue in captions.get("cues", []) if cue.get("end") is not None]
    clean_duration = float(speech.get("clean_duration", 0.0))
    if cue_ends and clean_duration and max(cue_ends) > clean_duration + 0.15:
        errors.append("caption timing extends beyond the clean narration timeline")

    required = {
        (shot["shot_id"], shot["selected_renderer"])
        for shot in plan.get("shots", [])
        if shot.get("requires_render_receipt")
    }
    if required and not args.planning_only:
        if not args.render_receipts:
            errors.append("actual renderer receipts are required before final delivery")
        else:
            receipts_data = load(args.render_receipts)
            receipts = {
                (item.get("shot_id"), item.get("renderer")): item
                for item in receipts_data.get("receipts", [])
                if item.get("status") == "success"
            }
            for key in sorted(required):
                receipt = receipts.get(key)
                if not receipt:
                    errors.append(f"missing successful {key[1]} receipt for {key[0]}")
                    continue
                output = Path(str(receipt.get("output", ""))).expanduser()
                if not output.is_file():
                    errors.append(f"renderer receipt output missing for {key[0]}: {output}")

    result = {
        "pass": not errors,
        "speech_gate": speech.get("gate", {}),
        "render_plan_pass": plan.get("overall_pass"),
        "caption_layout_pass": captions.get("overall_pass"),
        "required_renderer_receipts": [f"{shot}:{renderer}" for shot, renderer in sorted(required)],
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
