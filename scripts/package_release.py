#!/usr/bin/env python3
"""Create deterministic StarCut release ZIPs and reject accidental media/vendor files."""

from __future__ import annotations

import argparse
import hashlib
import os
import zipfile
from pathlib import Path


EXCLUDED_DIRS = {"dist", ".git", "node_modules", "__pycache__", ".venv", "venv"}
FORBIDDEN_EXTENSIONS = {
    ".mp4", ".mov", ".mkv", ".avi", ".webm", ".mp3", ".wav", ".m4a", ".aac",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ttf", ".otf", ".woff", ".woff2",
    ".task", ".onnx", ".bin", ".dylib", ".so", ".dll", ".exe", ".app", ".zip",
}
REQUIRED = {"SKILL.md", "README.md", "README.zh-CN.md", "INSTALL.md", "BUNDLE_MANIFEST.md", "LICENSE", "LICENSE_AUDIT.md", "THIRD_PARTY_NOTICES.md", "CHANGELOG.md", "QA_REPORT.md"}


def collect(root: Path) -> list[Path]:
    files = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        if not path.is_file():
            continue
        if path.suffix.lower() in FORBIDDEN_EXTENSIONS:
            raise SystemExit(f"Forbidden distributable artifact: {rel}")
        files.append(path)
    missing = sorted(REQUIRED - {p.name for p in files if p.parent == root})
    if missing:
        raise SystemExit("Missing release files: " + ", ".join(missing))
    return files


def write_zip(root: Path, destination: Path, files: list[Path], prefix: str = "starcut-video-editor") -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            info = zipfile.ZipInfo(str(Path(prefix) / path.relative_to(root)))
            info.date_time = (2026, 9, 1, 0, 0, 0)
            info.external_attr = (0o755 if os.access(path, os.X_OK) else 0o644) << 16
            archive.writestr(info, path.read_bytes())


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    output = (args.output or root / "dist" / "starcut-video-editor.zip").resolve()
    files = collect(root)
    write_zip(root, output, files)
    checksum = output.with_suffix(output.suffix + ".sha256")
    checksum.write_text(f"{digest(output)}  {output.name}\n", encoding="utf-8")
    workbuddy = output.parent / "starcut-video-editor-workbuddy-manual.zip"
    write_zip(root, workbuddy, files)
    workbuddy_checksum = workbuddy.with_suffix(workbuddy.suffix + ".sha256")
    workbuddy_checksum.write_text(f"{digest(workbuddy)}  {workbuddy.name}\n", encoding="utf-8")
    print(f"Created {output} ({len(files)} files)")
    print(f"SHA-256 {digest(output)}")
    print(f"Created {workbuddy} (manual compatibility package)")
    print(f"SHA-256 {digest(workbuddy)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
