#!/usr/bin/env python3
"""Remove the platform "AI生成 / WORKBUDDY" watermark burned into generated images.

How it works: the watermark is light-grey text at a corner (default bottom-right).
A white top-hat filter isolates the small bright glyph strokes (robust even when they
sit on bright backgrounds where a plain brightness threshold would light up everything),
then cv2.inpaint (TELEA) reconstructs only the glyph pixels -- background texture and
product edges survive, unlike blur/cover approaches.

Why a script: cv2.imread cannot open non-ASCII (Chinese) Windows paths -> imread returns
None. This script reads via np.fromfile + imdecode and writes via imencode + write_bytes.

Usage:
    python remove_ai_watermark.py --input "D:/assets/product"                       # in place
    python remove_ai_watermark.py --input "D:/assets/product" --output "D:/assets/clean"
    python remove_ai_watermark.py --input img.png --corner bottom-right --thresh 45
    python remove_ai_watermark.py --input dir --corner bottom-left --roi 0.72 --sheet check.jpg

Requires: Python 3.10+ with numpy + opencv-python.
"""
import argparse
from pathlib import Path

import cv2
import numpy as np

CORNERS = ("bottom-right", "bottom-left", "top-right", "top-left")
EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def read_img(p: Path):
    img = cv2.imdecode(np.fromfile(str(p), dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise SystemExit(f"cannot decode image: {p}")
    return img


def write_img(p: Path, img):
    ext = p.suffix if p.suffix.lower() in EXTS else ".png"
    ok, buf = cv2.imencode(ext, img)
    if not ok:
        raise SystemExit(f"cannot encode image: {p}")
    p.write_bytes(buf.tobytes())


def region(h, w, corner, frac, hfrac):
    """ROI box (x0, y0, x1, y1). Default: a narrow band (8% of height, 28% of width)
    at the given corner -- wide enough for 'AI生成 WORKBUDDY', narrow enough to avoid
    eating bright foam/background above the text line."""
    rw, rh = int(w * frac), int(h * hfrac)
    if corner == "bottom-right":
        return w - rw, h - rh, w, h
    if corner == "bottom-left":
        return 0, h - rh, rw, h
    if corner == "top-right":
        return w - rw, 0, w, rh
    return 0, 0, rw, rh


def clean(img, corner="bottom-right", frac=0.28, hfrac=0.08, thresh=45, sat_max=90,
          dilate=2, radius=5, max_area=2500):
    h, w = img.shape[:2]
    x0, y0, x1, y1 = region(h, w, corner, frac, hfrac)
    roi = img[y0:y1, x0:x1]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    # white top-hat: isolates SMALL bright structures (glyph strokes) even when they sit
    # on bright backgrounds (white countertop, foam, steel pole), where a plain
    # brightness threshold would also light up the whole background.
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
    tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
    mask = (tophat > thresh).astype(np.uint8) * 255
    if dilate:
        mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=dilate)
    full = np.zeros((h, w), np.uint8)
    full[y0:y1, x0:x1] = mask
    return cv2.inpaint(img, full, radius, cv2.INPAINT_TELEA), int((mask > 0).sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="image file or directory")
    ap.add_argument("--output", default=None, help="output dir (default: overwrite in place)")
    ap.add_argument("--corner", default="bottom-right", choices=CORNERS)
    ap.add_argument("--roi", type=float, default=0.28, help="ROI width as fraction of image width")
    ap.add_argument("--hfrac", type=float, default=0.08, help="ROI height as fraction of image height")
    ap.add_argument("--thresh", type=int, default=45,
                    help="top-hat response threshold for glyph pixels (lower = more sensitive)")
    ap.add_argument("--sat-max", type=int, default=90, help="max saturation for glyph pixels")
    ap.add_argument("--dilate", type=int, default=2)
    ap.add_argument("--radius", type=int, default=5, help="inpaint radius")
    ap.add_argument("--max-area", type=int, default=2500,
                    help="drop mask components larger than this (background highlights)")
    ap.add_argument("--sheet", default=None, help="write a contact sheet of cleaned corners")
    args = ap.parse_args()

    src = Path(args.input)
    files = sorted([p for p in src.iterdir() if p.suffix.lower() in EXTS]) if src.is_dir() else [src]
    if not files:
        raise SystemExit("no images found")

    outdir = Path(args.output) if args.output else None
    if outdir:
        outdir.mkdir(parents=True, exist_ok=True)

    crops = []
    for f in files:
        img = read_img(f)
        out, px = clean(img, args.corner, args.roi, args.hfrac, args.thresh, args.sat_max,
                        args.dilate, args.radius, args.max_area)
        dst = (outdir / f.name) if outdir else f
        write_img(dst, out)
        print(f"{f.name}: mask_px={px} -> {dst}")
        if args.sheet:
            h, w = out.shape[:2]
            crops.append(cv2.resize(out[int(h * 0.90):, int(w * 0.68):], (324, 156)))

    if args.sheet and crops:
        cols = min(4, len(crops))
        rows = []
        for i in range(0, len(crops), cols):
            row = crops[i:i + cols]
            while len(row) < cols:
                row.append(np.zeros_like(crops[0]))
            rows.append(np.hstack(row))
        write_img(Path(args.sheet), np.vstack(rows))
        print("sheet:", args.sheet)

    print(f"done, {len(files)} image(s)")


if __name__ == "__main__":
    main()
