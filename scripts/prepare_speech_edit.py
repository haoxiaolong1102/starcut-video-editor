#!/usr/bin/env python3
"""Detect real non-speaking gaps and prepare a reversible StarCut rough cut.

FFmpeg silence detection proposes cuts. Word timestamps protect speech boundaries and
surface adjacent repeated words/phrases for contextual review. The generated cut list
is deliberately blocked until the review contract is satisfied.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path


START_RE = re.compile(r"silence_start:\s*([0-9.]+)")
END_RE = re.compile(r"silence_end:\s*([0-9.]+)")


def media_duration(path: Path) -> float:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        raise SystemExit("FFprobe not found. Run starcut_doctor.py before speech editing.")
    proc = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode:
        raise SystemExit(proc.stderr.strip() or "Unable to read media duration.")
    return float(proc.stdout.strip())


def run_silencedetect(path: Path, noise_db: float, min_silence: float) -> str:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("FFmpeg not found. Run starcut_doctor.py before speech editing.")
    proc = subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-nostats",
            "-i",
            str(path),
            "-af",
            f"silencedetect=noise={noise_db:g}dB:d={min_silence:g}",
            "-f",
            "null",
            "-",
        ],
        check=False,
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    if proc.returncode:
        raise SystemExit(proc.stderr[-2000:] or "FFmpeg silence analysis failed.")
    return proc.stderr


def parse_silences(log: str, duration: float) -> list[dict]:
    intervals: list[dict] = []
    open_start: float | None = None
    for line in log.splitlines():
        start = START_RE.search(line)
        if start:
            open_start = float(start.group(1))
        end = END_RE.search(line)
        if end and open_start is not None:
            finish = min(float(end.group(1)), duration)
            if finish > open_start:
                intervals.append({"start": open_start, "end": finish, "duration": finish - open_start})
            open_start = None
    if open_start is not None and duration > open_start:
        intervals.append({"start": open_start, "end": duration, "duration": duration - open_start})
    return intervals


def proposed_removals(silences: list[dict], edge_pad: float, min_remove: float, duration: float) -> list[dict]:
    removals: list[dict] = []
    for gap in silences:
        start, end = float(gap["start"]), float(gap["end"])
        cut_start = start if start <= 0.001 else start + edge_pad
        cut_end = end if end >= duration - 0.001 else end - edge_pad
        if cut_end - cut_start >= min_remove:
            removals.append(
                {
                    "source_in": round(cut_start, 6),
                    "source_out": round(cut_end, 6),
                    "duration": round(cut_end - cut_start, 6),
                    "reason": "detected non-speaking gap",
                }
            )
    return removals


def keep_segments(duration: float, removals: list[dict]) -> list[dict]:
    segments: list[dict] = []
    cursor = 0.0
    timeline = 0.0
    for removal in removals:
        start, end = float(removal["source_in"]), float(removal["source_out"])
        if start > cursor + 0.001:
            length = start - cursor
            segments.append(
                {
                    "source_in": round(cursor, 6),
                    "source_out": round(start, 6),
                    "timeline_in": round(timeline, 6),
                    "timeline_out": round(timeline + length, 6),
                    "reason": "keep spoken material",
                }
            )
            timeline += length
        cursor = max(cursor, end)
    if cursor < duration - 0.001:
        length = duration - cursor
        segments.append(
            {
                "source_in": round(cursor, 6),
                "source_out": round(duration, 6),
                "timeline_in": round(timeline, 6),
                "timeline_out": round(timeline + length, 6),
                "reason": "keep spoken material",
            }
        )
    return segments


def load_words(path: Path | None) -> list[dict]:
    if path is None:
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        raw_words = data
    elif isinstance(data.get("words"), list):
        raw_words = data["words"]
    else:
        raw_words = [word for segment in data.get("segments", []) for word in segment.get("words", [])]
    words = []
    for item in raw_words:
        text = str(item.get("word", item.get("text", ""))).strip()
        if not text or "start" not in item or "end" not in item:
            continue
        words.append({"word": text, "start": float(item["start"]), "end": float(item["end"])})
    return words


def normalize_word(value: str) -> str:
    return re.sub(r"[^\w\u3400-\u9fff]+", "", value.lower())


def repeat_candidates(words: list[dict], max_phrase_words: int = 6) -> list[dict]:
    tokens = [normalize_word(item["word"]) for item in words]
    found: list[dict] = []
    occupied: set[int] = set()
    for size in range(min(max_phrase_words, len(words) // 2), 0, -1):
        index = 0
        while index + size * 2 <= len(words):
            left = tokens[index:index + size]
            right = tokens[index + size:index + size * 2]
            duplicate_indexes = set(range(index + size, index + size * 2))
            if left and all(left) and left == right and not (duplicate_indexes & occupied):
                found.append(
                    {
                        "phrase": "".join(item["word"] for item in words[index:index + size]),
                        "first": {"start": words[index]["start"], "end": words[index + size - 1]["end"]},
                        "duplicate": {"start": words[index + size]["start"], "end": words[index + size * 2 - 1]["end"]},
                        "action": "review against the approved script; remove one take, never both",
                    }
                )
                occupied.update(duplicate_indexes)
                index += size * 2
            else:
                index += 1
    return sorted(found, key=lambda item: item["duplicate"]["start"])


def word_conflicts(words: list[dict], removals: list[dict], tolerance: float = 0.015) -> list[dict]:
    conflicts = []
    for removal in removals:
        start, end = removal["source_in"], removal["source_out"]
        touched = [word for word in words if min(end, word["end"]) - max(start, word["start"]) > tolerance]
        if touched:
            conflicts.append({"removal": removal, "words": touched})
    return conflicts


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a reviewed StarCut speech cut from real silence and word timing.")
    parser.add_argument("input", type=Path, help="RAW audio/video; read only")
    parser.add_argument("report", type=Path, help="speech-analysis.json destination")
    parser.add_argument("--cutlist", type=Path, required=True, help="rough-cutlist.json destination")
    parser.add_argument("--word-timeline", type=Path, help="Whisper-compatible JSON word timestamps")
    parser.add_argument("--noise-db", type=float, default=-38.0)
    parser.add_argument("--min-silence", type=float, default=0.35)
    parser.add_argument("--edge-pad", type=float, default=0.08)
    parser.add_argument("--min-remove", type=float, default=0.16)
    parser.add_argument("--allow-vad-only", action="store_true", help="Explicitly approve conservative silence cuts without words")
    parser.add_argument("--repeats-reviewed", action="store_true", help="Confirm repeated-word candidates were reviewed contextually")
    parser.add_argument("--silence-log", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--duration", type=float, help=argparse.SUPPRESS)
    args = parser.parse_args()

    if not args.input.is_file():
        raise SystemExit(f"Input media not found: {args.input}")
    duration = args.duration if args.duration is not None else media_duration(args.input)
    log = args.silence_log.read_text(encoding="utf-8") if args.silence_log else run_silencedetect(args.input, args.noise_db, args.min_silence)
    silences = parse_silences(log, duration)
    removals = proposed_removals(silences, args.edge_pad, args.min_remove, duration)
    words = load_words(args.word_timeline)
    repeats = repeat_candidates(words)
    conflicts = word_conflicts(words, removals) if words else []
    kept = keep_segments(duration, removals)
    clean_duration = kept[-1]["timeline_out"] if kept else 0.0
    word_review_ok = (bool(words) and not conflicts) or args.allow_vad_only
    repeat_review_ok = not repeats or args.repeats_reviewed
    approved = word_review_ok and repeat_review_ok

    report = {
        "schema_version": "0.2",
        "source": str(args.input.resolve()),
        "duration": duration,
        "clean_duration": clean_duration,
        "thresholds": {
            "noise_db": args.noise_db,
            "min_silence": args.min_silence,
            "edge_pad": args.edge_pad,
            "min_remove": args.min_remove,
        },
        "silence_intervals": silences,
        "proposed_removals": removals,
        "word_timeline": {
            "provided": bool(words),
            "word_count": len(words),
            "removal_conflicts": conflicts,
        },
        "repeat_candidates": repeats,
        "gate": {
            "silence_analysis": "PASS",
            "word_boundary_review": "PASS" if word_review_ok else "BLOCKER",
            "repeat_review": "PASS" if repeat_review_ok else "BLOCKER",
            "approved_for_visuals": approved,
        },
    }
    cutlist = {
        "schema_version": "0.2",
        "source": str(args.input.resolve()),
        "segments": kept,
        "removed": removals,
        "review": {
            "status": "PASS" if approved else "BLOCKER",
            "speech_analysis": str(args.report.resolve()),
            "notes": (
                "Silence boundaries checked against words; repeated candidates reviewed."
                if approved
                else "Do not render: provide word timestamps/check conflicts and review repeated wording."
            ),
        },
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.cutlist.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.cutlist.write_text(json.dumps(cutlist, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"approved_for_visuals": approved, "report": str(args.report), "cutlist": str(args.cutlist)}, ensure_ascii=False))
    return 0 if approved else 2


if __name__ == "__main__":
    raise SystemExit(main())
