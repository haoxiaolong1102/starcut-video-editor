#!/usr/bin/env python3
"""Run StarCut's dependency-free routing and schema tests."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
CASES = {
    "talking-head-ai": ("talking-head-ai-project.json", "talking-head-ai-segments.json", ["kinetic_type", "talking_head", "data", "info_card"]),
    "screencast": ("screencast-project.json", "screencast-segments.json", ["kinetic_type", "screen_focus", "screencast", "talking_head"]),
    "picturebook": ("picturebook-project.json", "picturebook-segments.json", ["kinetic_type", "picturebook", "process", "talking_head"]),
}


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)


def main() -> int:
    failures = []
    results = []
    with tempfile.TemporaryDirectory(prefix="starcut-tests-") as temp:
        temp_path = Path(temp)
        for name, (project_file, segments_file, expected_modes) in CASES.items():
            shotbook = temp_path / f"{name}-shotbook.json"
            routed = run([sys.executable, str(ROOT / "scripts" / "route_visuals.py"), str(FIXTURES / segments_file), str(shotbook)])
            validated = run([sys.executable, str(ROOT / "scripts" / "validate_project.py"), str(FIXTURES / project_file), str(shotbook), "--json"])
            modes = []
            if shotbook.exists():
                modes = [shot["visual_mode"] for shot in json.loads(shotbook.read_text(encoding="utf-8"))["shots"]]
            passed = routed.returncode == 0 and validated.returncode == 0 and modes == expected_modes
            results.append({"case": name, "passed": passed, "modes": modes})
            if not passed:
                failures.append({"case": name, "route": routed.stdout, "validate": validated.stdout, "modes": modes, "expected": expected_modes})

        install_parent = temp_path / "agent-skills"
        installed = run([
            sys.executable,
            str(ROOT / "scripts" / "install_starcut.py"),
            "--agent", "generic",
            "--dest", str(install_parent),
        ])
        installed_root = install_parent / "starcut-video-editor"
        install_passed = (
            installed.returncode == 0
            and (installed_root / "SKILL.md").is_file()
            and not (installed_root / "dist").exists()
            and not (installed_root / ".git").exists()
        )
        results.append({"case": "portable-install", "passed": install_passed, "destination": str(installed_root)})
        if not install_passed:
            failures.append({"case": "portable-install", "output": installed.stdout})

        detected = run([sys.executable, str(ROOT / "scripts" / "detect_adapters.py")])
        try:
            detection = json.loads(detected.stdout)
        except json.JSONDecodeError:
            detection = {}
        detection_passed = "required" in detection and detection.get("policy", "").startswith("Detection only")
        results.append({"case": "adapter-detection", "passed": detection_passed, "ready_for_media": detection.get("ready_for_media")})
        if not detection_passed:
            failures.append({"case": "adapter-detection", "output": detected.stdout})

        local_project = temp_path / "local-remotion-project"
        local_package = local_project / "node_modules" / "remotion" / "package.json"
        local_package.parent.mkdir(parents=True)
        local_package.write_text('{"name":"remotion","version":"test"}', encoding="utf-8")
        local_detected = run([
            sys.executable,
            str(ROOT / "scripts" / "detect_adapters.py"),
            "--project-root", str(local_project),
        ])
        try:
            local_detection = json.loads(local_detected.stdout)
        except json.JSONDecodeError:
            local_detection = {}
        local_remotion = local_detection.get("renderers", {}).get("remotion", {})
        local_remotion_passed = local_remotion.get("available") and local_remotion.get("kind") == "project-package"
        results.append({"case": "project-remotion-detection", "passed": local_remotion_passed, "kind": local_remotion.get("kind")})
        if not local_remotion_passed:
            failures.append({"case": "project-remotion-detection", "output": local_detected.stdout})

        raw = temp_path / "raw-placeholder.mp4"
        raw.write_bytes(b"test-only-placeholder")
        speech_report = temp_path / "speech-analysis.json"
        cutlist = temp_path / "rough-cutlist.json"
        speech = run([
            sys.executable,
            str(ROOT / "scripts" / "prepare_speech_edit.py"),
            str(raw),
            str(speech_report),
            "--cutlist", str(cutlist),
            "--word-timeline", str(FIXTURES / "word-timeline.json"),
            "--silence-log", str(FIXTURES / "silence-log.txt"),
            "--duration", "5.0",
        ])
        speech_data = json.loads(speech_report.read_text(encoding="utf-8")) if speech_report.exists() else {}
        cut_data = json.loads(cutlist.read_text(encoding="utf-8")) if cutlist.exists() else {}
        speech_passed = (
            speech.returncode == 0
            and speech_data.get("gate", {}).get("approved_for_visuals") is True
            and len(cut_data.get("segments", [])) == 2
            and cut_data.get("review", {}).get("status") == "PASS"
        )
        results.append({"case": "speech-gap-gate", "passed": speech_passed, "removed": speech_data.get("proposed_removals", [])})
        if not speech_passed:
            failures.append({"case": "speech-gap-gate", "output": speech.stdout, "report": speech_data, "cutlist": cut_data})

        caption_layout = temp_path / "caption-layout.json"
        fitted = run([
            sys.executable,
            str(ROOT / "scripts" / "fit_caption_layout.py"),
            str(FIXTURES / "captions.json"),
            str(caption_layout),
        ])
        layout_data = json.loads(caption_layout.read_text(encoding="utf-8")) if caption_layout.exists() else {}
        caption_passed = fitted.returncode == 0 and layout_data.get("overall_pass") and all(cue.get("fits") for cue in layout_data.get("cues", []))
        results.append({"case": "caption-box-fit", "passed": caption_passed, "measurement_mode": layout_data.get("measurement_mode")})
        if not caption_passed:
            failures.append({"case": "caption-box-fit", "output": fitted.stdout, "layout": layout_data})

        render_plan = temp_path / "render-plan.json"
        planned = run([
            sys.executable,
            str(ROOT / "scripts" / "build_render_plan.py"),
            str(temp_path / "talking-head-ai-shotbook.json"),
            str(FIXTURES / "render-adapters.json"),
            str(render_plan),
            "--remotion-license", "eligible",
        ])
        plan_data = json.loads(render_plan.read_text(encoding="utf-8")) if render_plan.exists() else {}
        data_shot = next((shot for shot in plan_data.get("shots", []) if shot.get("visual_mode") == "data"), {})
        remotion_passed = planned.returncode == 0 and data_shot.get("selected_renderer") == "remotion"
        results.append({"case": "remotion-auto-route", "passed": remotion_passed, "selected": data_shot.get("selected_renderer")})
        if not remotion_passed:
            failures.append({"case": "remotion-auto-route", "output": planned.stdout, "plan": plan_data})

        receipts = []
        for shot in plan_data.get("shots", []):
            if shot.get("requires_render_receipt"):
                rendered = temp_path / f"{shot['shot_id']}.mp4"
                rendered.write_bytes(b"test-render-receipt")
                receipts.append({"shot_id": shot["shot_id"], "renderer": shot["selected_renderer"], "status": "success", "output": str(rendered)})
        receipts_path = temp_path / "render-receipts.json"
        receipts_path.write_text(json.dumps({"receipts": receipts}), encoding="utf-8")
        production = run([
            sys.executable,
            str(ROOT / "scripts" / "validate_production.py"),
            str(speech_report),
            str(render_plan),
            str(caption_layout),
            "--render-receipts", str(receipts_path),
        ])
        production_passed = production.returncode == 0
        results.append({"case": "mandatory-production-gates", "passed": production_passed})
        if not production_passed:
            failures.append({"case": "mandatory-production-gates", "output": production.stdout})

        blocked_production = run([
            sys.executable,
            str(ROOT / "scripts" / "validate_production.py"),
            str(speech_report),
            str(render_plan),
            str(caption_layout),
        ])
        missing_receipt_blocked = blocked_production.returncode != 0 and "renderer receipts are required" in blocked_production.stdout
        results.append({"case": "missing-render-receipt-blocked", "passed": missing_receipt_blocked})
        if not missing_receipt_blocked:
            failures.append({"case": "missing-render-receipt-blocked", "output": blocked_production.stdout})

    print(json.dumps({"passed": not failures, "results": results, "failures": failures}, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
