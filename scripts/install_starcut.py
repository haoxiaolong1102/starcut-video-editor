#!/usr/bin/env python3
"""Install the unpacked StarCut Skill into a supported or custom Skill directory."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


SKIP_DIRS = {".git", ".github", "dist", "__pycache__", ".venv", "venv", "node_modules"}
SKIP_SUFFIXES = {".pyc", ".pyo"}


def resolve_destination(args: argparse.Namespace) -> Path:
    if args.dest:
        return args.dest.expanduser().resolve() / "starcut-video-editor"
    if args.agent == "codex":
        if args.scope == "project":
            if not args.project:
                raise SystemExit("--project is required for Codex project scope")
            return args.project.expanduser().resolve() / ".agents" / "skills" / "starcut-video-editor"
        return Path.home() / ".codex" / "skills" / "starcut-video-editor"
    if args.agent == "workbuddy":
        if args.scope != "user":
            raise SystemExit("WorkBuddy automatic path is available only for --scope user; otherwise pass --dest")
        return Path.home() / ".workbuddy" / "skills" / "starcut-video-editor"
    raise SystemExit("Generic installation requires --dest")


def ignore(_directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name in SKIP_DIRS or Path(name).suffix.lower() in SKIP_SUFFIXES}


def validate_source(source: Path) -> None:
    skill = source / "SKILL.md"
    if not skill.is_file():
        raise SystemExit(f"SKILL.md not found in {source}")
    text = skill.read_text(encoding="utf-8")
    if "name: starcut-video-editor" not in text:
        raise SystemExit("Source SKILL.md is not starcut-video-editor")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install StarCut without downloading or modifying external dependencies.")
    parser.add_argument("--agent", choices=("codex", "workbuddy", "generic"), required=True)
    parser.add_argument("--scope", choices=("project", "user"), default="user")
    parser.add_argument("--project", type=Path)
    parser.add_argument("--dest", type=Path, help="Parent Skill directory for a custom/generic Agent")
    parser.add_argument("--backup-existing", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    source = Path(__file__).resolve().parents[1]
    validate_source(source)
    destination = resolve_destination(args)
    if source == destination or source in destination.parents:
        raise SystemExit("Refusing a recursive/self installation")

    report = {
        "agent": args.agent,
        "scope": args.scope,
        "source": str(source),
        "destination": str(destination),
        "backup": None,
        "dry_run": args.dry_run,
    }
    if args.dry_run:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() or destination.is_symlink():
        if not args.backup_existing:
            raise SystemExit(f"Destination already exists: {destination}. Use --backup-existing or choose another destination.")
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = destination.with_name(f"{destination.name}.backup-{stamp}")
        if backup.exists():
            raise SystemExit(f"Backup path already exists: {backup}")
        destination.rename(backup)
        report["backup"] = str(backup)

    shutil.copytree(source, destination, ignore=ignore)
    validate_source(destination)
    report["installed"] = True
    report["next"] = "Restart or reload Skill discovery, then invoke $starcut-video-editor"
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
