#!/usr/bin/env python3
"""Choose renderers per shot and require Remotion when it is the best ready adapter."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


ADVANCED_MODES = {
    "screen_focus",
    "data",
    "process",
    "comparison",
    "motion_2d",
    "remotion_advanced",
    "three_d",
    "shader_mask_morph",
}
HYPERFRAMES_MODES = {"kinetic_type", "info_card", "screenshot", "collage"}


def adapter_available(report: dict, name: str) -> bool:
    if isinstance(report.get("renderers", {}).get(name), dict):
        return bool(report["renderers"][name].get("available"))
    if isinstance(report.get("commands", {}).get(name), dict):
        return bool(report["commands"][name].get("available"))
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Build an auditable StarCut renderer plan.")
    parser.add_argument("shotbook", type=Path)
    parser.add_argument("adapter_report", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--renderer", choices=("auto", "remotion", "hyperframes", "basic"), default="auto")
    parser.add_argument(
        "--remotion-license",
        choices=("eligible", "unknown", "ineligible"),
        default=os.getenv("STARCUT_REMOTION_LICENSE", "unknown"),
        help="Explicit user/organization eligibility result for the installed Remotion version",
    )
    args = parser.parse_args()

    book = json.loads(args.shotbook.read_text(encoding="utf-8"))
    adapters = json.loads(args.adapter_report.read_text(encoding="utf-8"))
    remotion_ready = adapter_available(adapters, "remotion")
    hyperframes_ready = adapter_available(adapters, "hyperframes")
    blockers: list[str] = []
    plans = []

    for shot in book.get("shots", []):
        advanced = shot.get("visual_mode") in ADVANCED_MODES or int(shot.get("effect_level", 0)) >= 2
        preferred = "remotion" if advanced else ("hyperframes" if shot.get("visual_mode") in HYPERFRAMES_MODES else "basic")
        selected = preferred
        reason = "Use the lowest renderer that faithfully implements this shot."

        if args.renderer != "auto":
            selected = args.renderer
            reason = f"Project explicitly selected {args.renderer}."
        elif preferred == "remotion":
            if remotion_ready and args.remotion_license == "eligible":
                selected = "remotion"
                reason = "Level 2/3 semantic motion requires Remotion and the detected adapter is eligible."
            elif remotion_ready and args.remotion_license == "unknown":
                selected = "pending"
                blockers.append(f"{shot['id']}: Remotion is installed but license eligibility is unconfirmed")
                reason = "Do not silently skip a ready advanced renderer; confirm license eligibility first."
            elif hyperframes_ready and shot.get("visual_mode") not in {"three_d", "shader_mask_morph", "remotion_advanced"}:
                selected = "hyperframes"
                reason = "Remotion is unavailable/ineligible; use the supported HyperFrames fallback and record the downgrade."
            else:
                selected = "basic"
                reason = "Advanced adapter unavailable; use an explicit low-complexity fallback instead of claiming Remotion ran."
        elif preferred == "hyperframes" and not hyperframes_ready:
            selected = "basic"
            reason = "HyperFrames is unavailable; use a static/basic fallback."

        if selected == "remotion":
            if not remotion_ready:
                blockers.append(f"{shot['id']}: Remotion selected but adapter not found")
            elif args.remotion_license != "eligible":
                blockers.append(f"{shot['id']}: Remotion selected without eligible license status")
        if selected == "hyperframes" and not hyperframes_ready:
            blockers.append(f"{shot['id']}: HyperFrames selected but adapter not found")

        plans.append(
            {
                "shot_id": shot["id"],
                "visual_mode": shot.get("visual_mode"),
                "effect_level": shot.get("effect_level"),
                "preferred_renderer": preferred,
                "selected_renderer": selected,
                "requires_render_receipt": selected in {"remotion", "hyperframes"},
                "reason": reason,
            }
        )

    result = {
        "schema_version": "0.2",
        "project_id": book.get("project_id"),
        "overall_pass": not blockers,
        "adapter_state": {
            "remotion_available": remotion_ready,
            "remotion_license": args.remotion_license,
            "hyperframes_available": hyperframes_ready,
        },
        "shots": plans,
        "blockers": sorted(set(blockers)),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"overall_pass": result["overall_pass"], "output": str(args.output), "blockers": result["blockers"]}, ensure_ascii=False))
    return 0 if result["overall_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
