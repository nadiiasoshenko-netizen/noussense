#!/usr/bin/env python3
"""
Main entry point: takes a filmed video + a beats.json timeline and produces
a final MP4 with NS-styled captions burned in and any synced graphics
composited on top.

Usage:
    python3 build_reel.py --video raw.mp4 --beats beats.json --output final.mp4

beats.json: see generate_ass.py docstring for the caption schema. A beat can
additionally carry a "graphic" object to overlay a synced icon/chart:

  {
    "start": 21.0, "end": 24.0, "mode": "stat", "text": "$60M", "stat_is_hook": true,
    "graphic": {
      "type": "bar_compare",          # arrow_up | arrow_down | bar_compare | bubble_stat
      "x": 160, "y": 1500,             # top-left position in the 1080x1920 frame
      "small_label": "FRAGRANCE LIQUID", "small_value": "$15",
      "large_label": "WHAT YOU PAY", "large_value": "$240"
    }
  }

Only attach a graphic to stats where it genuinely clarifies something (a
comparison, a rise/fall, or the one number the whole story hinges on) — see
references/design-tokens.md. Most stat beats don't need one.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import generate_ass  # noqa: E402
import generate_graphics  # noqa: E402


def probe_dimensions(video_path: str) -> tuple[int, int]:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=s=x:p=0", video_path],
        capture_output=True, text=True, check=True,
    )
    w, h = out.stdout.strip().split("x")
    return int(w), int(h)


def make_graphic_png(graphic: dict, out_path: str, on_dark: bool = True):
    kind = graphic["type"]
    if kind in ("arrow_up", "arrow_down"):
        generate_graphics.arrow("up" if kind == "arrow_up" else "down", out_path)
    elif kind == "bar_compare":
        generate_graphics.bar_compare(
            out_path,
            small_label=graphic.get("small_label", ""),
            small_value=graphic.get("small_value", ""),
            large_label=graphic.get("large_label", ""),
            large_value=graphic.get("large_value", ""),
            on_dark=on_dark,
        )
    elif kind == "bubble_stat":
        generate_graphics.bubble_stat(out_path, diameter=graphic.get("diameter", 260))
    else:
        raise ValueError(f"Unknown graphic type: {kind}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--video", required=True)
    p.add_argument("--beats", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--fonts-dir", default=os.path.join(SCRIPT_DIR, "..", "assets", "fonts"))
    p.add_argument("--keep-temp", action="store_true", help="Keep intermediate files for debugging")
    args = p.parse_args()

    with open(args.beats) as f:
        beats = json.load(f)

    width, height = probe_dimensions(args.video)
    if (width, height) != (1080, 1920):
        print(
            f"WARNING: input video is {width}x{height}, not 1080x1920. Caption "
            "positions in design-tokens.md assume a 1080x1920 vertical frame — "
            "consider re-exporting the source video vertically first, or expect "
            "captions/graphics to be positioned proportionally off.",
            file=sys.stderr,
        )

    workdir = tempfile.mkdtemp(prefix="ge_reel_")
    ass_path = os.path.join(workdir, "captions.ass")

    # --- Step 1: generate the styled ASS captions ---
    with open(ass_path, "w") as f:
        serif, sans = generate_ass.pick_fonts(args.fonts_dir)
        header = (
            "[Script Info]\nScriptType: v4.00+\n"
            f"PlayResX: {generate_ass.PLAY_RES_X}\nPlayResY: {generate_ass.PLAY_RES_Y}\n"
            "ScaledBorderAndShadow: yes\n\n"
        )
        f.write(header + generate_ass.build_styles(serif, sans) + "\n\n" + generate_ass.build_events(beats) + "\n")
    print(f"[1/3] Wrote captions: {ass_path}")

    # --- Step 2: generate any graphic PNGs this timeline needs ---
    overlays = []  # list of (png_path, x, y, start, end)
    for i, beat in enumerate(beats):
        graphic = beat.get("graphic")
        if not graphic:
            continue
        png_path = os.path.join(workdir, f"graphic_{i}.png")
        make_graphic_png(graphic, png_path, on_dark=(beat.get("background", "dark") == "dark"))
        overlays.append((
            png_path,
            graphic.get("x", 160),
            graphic.get("y", 1500),
            graphic.get("start", beat["start"]),
            graphic.get("end", beat["end"]),
        ))
    print(f"[2/3] Generated {len(overlays)} graphic overlay(s)")

    # --- Step 3: single ffmpeg pass — burn captions, then overlay graphics ---
    # ass= must run before overlays that should sit visually above/below it in
    # the same filter chain are ordered deliberately: captions first, then each
    # graphic layered on top, since graphics are meant to sit alongside (not
    # under) the caption text.
    filter_parts = [f"[0:v]ass={ass_path}[v0]"]
    last_label = "v0"
    inputs = ["-i", args.video]
    for idx, (png_path, x, y, start, end) in enumerate(overlays):
        inputs += ["-i", png_path]
        in_idx = idx + 1
        out_label = f"v{idx + 1}"
        filter_parts.append(
            f"[{last_label}][{in_idx}:v]overlay=x={x}:y={y}:"
            f"enable='between(t,{start},{end})'[{out_label}]"
        )
        last_label = out_label

    filter_complex = ";".join(filter_parts)
    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", filter_complex,
        "-map", f"[{last_label}]", "-map", "0:a?",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
        args.output,
    ]
    print("[3/3] Running ffmpeg:\n  " + " ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"\nDone: {args.output}")

    if not args.keep_temp:
        import shutil
        shutil.rmtree(workdir, ignore_errors=True)
    else:
        print(f"(intermediate files kept in {workdir})")


if __name__ == "__main__":
    main()
