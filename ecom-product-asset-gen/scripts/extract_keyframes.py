#!/usr/bin/env python3
"""Extract review frames from a product demo video and build contact sheets.

Why: picking product views (front / side / top / detail) from a demo video needs a
fast overview first. This script dumps 1 frame per interval and tiles them into
contact sheets so the agent can eyeball 25 frames per image instead of 25 reads.

Usage:
    python extract_keyframes.py --video "D:/x/demo.mp4" --out "D:/x/frames"
    python extract_keyframes.py --video demo.mp4 --out frames --fps 1 --cols 5 --tile 144x256
    python extract_keyframes.py --video demo.mp4 --out frames --shot 4.5 6.5 9.0

Notes:
- Requires ffmpeg/ffprobe on PATH.
- Chinese / non-ASCII paths are fine for ffmpeg on Windows.
- Dependencies: Python 3.10+ standard library only.
"""
import argparse
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.stderr.write(" ".join(map(str, cmd)) + "\n" + (r.stderr or "")[-2000:] + "\n")
        raise SystemExit(1)
    return r.stdout


def probe(video: Path):
    out = run(["ffprobe", "-v", "error", "-show_entries",
               "format=duration:stream=width,height,r_frame_rate",
               "-of", "json", str(video)])
    data = json.loads(out)
    stream = next((s for s in data.get("streams", []) if s.get("width")), {})
    return {
        "duration": float(data.get("format", {}).get("duration", 0) or 0),
        "width": stream.get("width"),
        "height": stream.get("height"),
        "fps": stream.get("r_frame_rate"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--out", required=True, help="directory for extracted jpg frames")
    ap.add_argument("--fps", type=float, default=1.0, help="frames per second to sample")
    ap.add_argument("--shot", nargs="*", type=float, default=None,
                    help="if given, extract exactly these timestamps (seconds) instead of fps sampling")
    ap.add_argument("--cols", type=int, default=5)
    ap.add_argument("--tile", default="144x256", help="contact-sheet thumbnail size WxH")
    args = ap.parse_args()

    video = Path(args.video)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    info = probe(video)
    print(f"video: {video.name}  {info['width']}x{info['height']}  {info['duration']:.2f}s  fps={info['fps']}")

    frames = []
    if args.shot:
        for t in args.shot:
            p = out / f"t_{t:g}.jpg"
            run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t}", "-i", str(video),
                 "-frames:v", "1", "-q:v", "2", str(p)])
            frames.append(p)
        print(f"extracted {len(frames)} shot frames")
    else:
        run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-vf", f"fps={args.fps}",
             "-q:v", "2", str(out / "f_%03d.jpg")])
        frames = sorted(out.glob("f_*.jpg"))
        print(f"extracted {len(frames)} frames at {args.fps} fps")

    # contact sheets: cols x cols tiles per sheet, starting at frame N
    if not args.shot:
        per_sheet = args.cols * args.cols
        for i in range(0, len(frames), per_sheet):
            sheet = out / f"sheet_{i // per_sheet + 1}.jpg"
            run(["ffmpeg", "-y", "-v", "error", "-start_number", str(i + 1),
                 "-i", str(out / "f_%03d.jpg"),
                 "-vf", f"scale={args.tile},tile={args.cols}x{args.cols}",
                 "-frames:v", "1", str(sheet)])
            print("contact sheet:", sheet)


if __name__ == "__main__":
    main()
