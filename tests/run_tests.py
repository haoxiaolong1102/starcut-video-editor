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

    print(json.dumps({"passed": not failures, "results": results, "failures": failures}, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
