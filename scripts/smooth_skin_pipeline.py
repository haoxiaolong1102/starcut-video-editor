#!/usr/bin/env python3
"""Non-destructive, skin-only smoothing adapter for StarCut.

Requires external numpy, opencv-python and mediapipe packages plus a separately
obtained Face Landmarker model. This package intentionally ships no model.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Preset:
    blend: float
    diameter: int
    sigma_color: float
    sigma_space: float


PRESETS = {
    "SMOOTH_OFF": Preset(0.0, 5, 18.0, 7.0),
    "SMOOTH_NORMAL": Preset(0.25, 7, 30.0, 9.0),
    "SMOOTH_HIGH": Preset(0.42, 9, 44.0, 12.0),
}

# MediaPipe face mesh groups. Exact model compatibility is validated at runtime.
FACE_OVAL = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
LEFT_BROW = [70, 63, 105, 66, 107]
RIGHT_BROW = [336, 296, 334, 293, 300]
OUTER_LIPS = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 375, 321, 405, 314, 17, 84, 181]
NOSE_DETAIL = [168, 6, 197, 195, 5, 4, 1, 19, 94, 2, 164]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply temporally stable skin-only smoothing to a derivative video.")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--model", type=Path, required=True, help="User-supplied MediaPipe Face Landmarker .task model")
    parser.add_argument("--level", choices=tuple(PRESETS), default="SMOOTH_HIGH")
    parser.add_argument("--custom-blend", type=float, help="Override blend in range 0..0.55")
    parser.add_argument("--mask-smoothing", type=float, default=0.78, help="Previous-mask weight in range 0..0.95")
    return parser.parse_args()


def polygon(points, landmarks, width, height):
    import numpy as np

    return np.array([(int(landmarks[i].x * width), int(landmarks[i].y * height)) for i in points], dtype=np.int32)


def main() -> int:
    args = parse_args()
    if args.input.resolve() == args.output.resolve():
        raise SystemExit("Refusing to overwrite RAW input; choose a separate output path.")
    if not args.input.is_file():
        raise SystemExit(f"Input not found: {args.input}")
    if not args.model.is_file():
        raise SystemExit(f"Face Landmarker model not found: {args.model}")
    if not 0 <= args.mask_smoothing <= 0.95:
        raise SystemExit("--mask-smoothing must be between 0 and 0.95")

    try:
        import cv2
        import mediapipe as mp
        import numpy as np
    except ImportError as exc:
        raise SystemExit("Install the external packages listed in scripts/requirements-smoothing.txt") from exc

    preset = PRESETS[args.level]
    blend = preset.blend if args.custom_blend is None else args.custom_blend
    if not 0 <= blend <= 0.55:
        raise SystemExit("--custom-blend must be between 0 and 0.55")

    capture = cv2.VideoCapture(str(args.input))
    if not capture.isOpened():
        raise SystemExit(f"Cannot open input: {args.input}")
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = capture.get(cv2.CAP_PROP_FPS) or 30.0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(args.output), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    if not writer.isOpened():
        raise SystemExit(f"Cannot create output: {args.output}")

    BaseOptions = mp.tasks.BaseOptions
    FaceLandmarker = mp.tasks.vision.FaceLandmarker
    FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
    RunningMode = mp.tasks.vision.RunningMode
    options = FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=str(args.model)),
        running_mode=RunningMode.VIDEO,
        num_faces=1,
        min_face_detection_confidence=0.55,
        min_face_presence_confidence=0.55,
        min_tracking_confidence=0.55,
    )

    previous_mask = None
    frame_index = 0
    with FaceLandmarker.create_from_options(options) as detector:
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            if blend == 0:
                writer.write(frame)
                frame_index += 1
                continue

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            result = detector.detect_for_video(image, int(frame_index * 1000 / fps))
            current = np.zeros((height, width), dtype=np.float32)
            if result.face_landmarks:
                marks = result.face_landmarks[0]
                cv2.fillPoly(current, [polygon(FACE_OVAL, marks, width, height)], 1.0)
                for protected in (LEFT_EYE, RIGHT_EYE, LEFT_BROW, RIGHT_BROW, OUTER_LIPS, NOSE_DETAIL):
                    hull = cv2.convexHull(polygon(protected, marks, width, height))
                    cv2.fillConvexPoly(current, hull, 0.0)
                # Keep hairline and lower beard zone less affected.
                ys = [marks[i].y for i in FACE_OVAL]
                top, bottom = int(min(ys) * height), int(max(ys) * height)
                fade_top = max(1, int((bottom - top) * 0.12))
                current[top : top + fade_top] *= np.linspace(0.0, 1.0, fade_top)[:, None]
                beard_start = top + int((bottom - top) * 0.72)
                current[beard_start:bottom] *= 0.58
                current = cv2.GaussianBlur(current, (0, 0), sigmaX=max(width, height) * 0.006)

            if previous_mask is None:
                stable = current
            else:
                stable = args.mask_smoothing * previous_mask + (1 - args.mask_smoothing) * current
                if current.max() == 0:  # tracking lost: fade out instead of freezing stale mask
                    stable *= 0.72
            previous_mask = stable

            filtered = cv2.bilateralFilter(frame, preset.diameter, preset.sigma_color, preset.sigma_space)
            alpha = np.clip(stable * blend, 0.0, 1.0)[..., None]
            output = (frame.astype(np.float32) * (1 - alpha) + filtered.astype(np.float32) * alpha).astype(np.uint8)
            writer.write(output)
            frame_index += 1

    capture.release()
    writer.release()
    print(args.output)
    print("Note: OpenCV output is silent. Remux the untouched cleaned narration track with FFmpeg after visual QA.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
