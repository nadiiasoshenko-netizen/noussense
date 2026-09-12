#!/usr/bin/env python3
"""Build the graded + audio-enhanced base clip for the premium HyperFrames path.

Implements the video-use Hard Rules, adapted for footage-in-engine:
  - Per-segment extract with the DLOG->Rec709 LUT baked in (per-segment grade).
  - 30ms audio fades at every segment boundary (no pops).
  - Lossless -c copy concat (no double-encode).
  - Voice enhancement on the concatenated audio: rumble highpass, FFT denoise,
    presence EQ, sibilance tame, then two-pass loudnorm to -14 LUFS (social).
  - Outputs clip.mp4 (graded video + enhanced audio) and voice.m4a (the
    separate audio track the premium template uses).

Usage:
  python build_base_clip.py <edl_beats.json> --lut <cube> --out-dir <dir> [--source <mp4>] [--fps 30]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def extract_segment(source: Path, start: float, dur: float, lut: Path,
                    out_path: Path, fps: int, video_end: float | None = None) -> None:
    # portrait: scale by height, keep AR; bake your camera's log->Rec709 LUT, then a grade
    # that replicates a hand-tuned Premiere Lumetri Basic Correction (a backlit-window reference look).
    # NOTE: this `post` chain is a proven STARTING POINT tuned for a DJI D-Log M backlit shot. Re-tune
    # the curve/colorbalance to match YOUR reference still and camera (see the skill's "match a reference"
    # step). The reference Lumetri values this emulates:
    #   Temp +8.3, Tint +0.7, Sat 92, Contrast -15.5, Highlights -61, Shadows +48,
    #   Whites -26, Blacks -31.5, PLUS an RGB S-curve.
    # Translated to ffmpeg (QA'd frame-by-frame against the reference image):
    #   - colorbalance = warm WB (Temp +8.3): boost red / cut blue across the range, tiny magenta.
    #   - curves = the Lumetri tone + S-curve as ONE net transfer:
    #       * deep toe (0.05->0.03)               = Blacks -31.5  -> rich, deep blacks (YMIN ~30)
    #       * steep low-mid lift (0.16->0.25, 0.30->0.42, 0.46->0.56) = Shadows +48 + S-curve
    #         -> backlit SUBJECT properly bright with real facial modeling (YAVG ~148)
    #       * shoulder recovery (0.62->0.65, 0.78->0.73, 0.90->0.85, 1->0.96) = Highlights -61 +
    #         Whites -26 -> window/skyline keeps DETAIL, not blown (YMAX ~227, window not clipped)
    #   - eq saturation 1.03 = vivid greens/teal water like the reference (warmth adds the rest).
    # KEY LESSON: deep blacks + S-curve mid-contrast are what let the highlight recovery stay
    # RICH instead of washed (the earlier "pull whites to 0.80, no deep black, no S" = milky veil).
    # NO sharpening (crispness comes from the lanczos downscale of the 3K source).
    # Refined 2026-06-03 to kill a residual yellow-GREEN cast (UAVG/VAVG were 122/126, both
    # < neutral 128) and recover the still-bright background: less warmth (rm/bm halved),
    # a magenta TINT across the range (g* negative = Lumetri Tint +0.7, neutralizes the green),
    # a harder highlight shoulder (0.88->0.77, 1->0.88) so the window/sky keeps detail instead
    # of reading blown, and saturation back to 1.0 so the foliage stops looking yellow-green.
    # QA'd: UAVG ~126 / VAVG ~128 (neutral), sun-bloom patch ~220->194 (recovered), skin still warm.
    post = ("colorbalance=rm=0.03:bm=-0.03:rs=0.01:bs=-0.02:rh=0.015:bh=-0.025:gm=-0.03:gs=-0.025:gh=-0.02,"
            "curves=all='0/0 0.05/0.03 0.16/0.25 0.30/0.42 0.46/0.55 0.60/0.62 0.74/0.68 0.88/0.77 1/0.88',"
            "eq=saturation=1.0")
    # punch-in crop (~13%) centred on the subject, then a crisp lanczos downscale to 1440p
    # (keeps real 3K detail; renders/downscales clean -- no upscaling, no fake sharpening).
    grade = f"crop=1500:2667:114:120,scale=-2:2560:flags=lanczos,lut3d={lut},{post}"
    if video_end is not None:
        # FREEZE-FILL: cut the video at `video_end` (e.g. just before a look-away / dead tail)
        # and hold the last clean frame to fill the rest of the segment. Audio stays the FULL
        # `dur`, so the segment's total length is unchanged -> nothing downstream (captions /
        # SFX / reframes keyed to clip time) shifts. The frozen tail covers silence only.
        vdur = video_end - start          # real (moving) video length
        freeze = max(0.0, dur - vdur)     # held-frame padding to reach the original duration
        vf = (f"trim=0:{vdur:.3f},setpts=PTS-STARTPTS,{grade},"
              f"tpad=stop_mode=clone:stop_duration={freeze:.3f}")
    else:
        vf = grade
    fade_out = max(0.0, dur - 0.03)
    af = f"afade=t=in:st=0:d=0.03,afade=t=out:st={fade_out:.3f}:d=0.03"
    cmd = [
        "ffmpeg", "-y",
        "-ss", f"{start:.3f}", "-i", str(source), "-t", f"{dur:.3f}",
        "-vf", vf, "-af", af,
        "-c:v", "libx264", "-preset", "slow", "-crf", "15",
        "-pix_fmt", "yuv420p", "-r", str(fps),
        "-g", "30", "-keyint_min", "30", "-sc_threshold", "0",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
        "-movflags", "+faststart",
        str(out_path),
    ]
    run(cmd)


def concat(seg_paths: list[Path], out_path: Path, work: Path) -> None:
    lst = work / "_concat.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in seg_paths))
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", "-movflags", "+faststart", str(out_path)])
    lst.unlink(missing_ok=True)


# Voice enhancement chain (before loudnorm):
#   highpass=80       remove low-frequency room rumble / handling
#   afftdn            broadband FFT noise reduction (gentle)
#   equalizer 200 -2  trim boxy low-mids
#   equalizer 3.6k +3 presence / intelligibility bump
#   equalizer 7.5k -3 tame harsh sibilance (soft de-ess)
ENHANCE_AF = (
    "highpass=f=80,"
    "afftdn=nr=12:nf=-28,"
    "equalizer=f=200:t=q:w=1.0:g=-2,"
    "equalizer=f=3600:t=q:w=1.2:g=3,"
    "equalizer=f=7500:t=q:w=1.5:g=-3"
)

LOUDNORM = "loudnorm=I=-14:TP=-1:LRA=11"


def measure_loudnorm(path: Path, pre_af: str) -> dict | None:
    af = f"{pre_af},{LOUDNORM}:print_format=json"
    proc = subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-nostats", "-i", str(path),
         "-af", af, "-vn", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    s = proc.stderr
    a, b = s.rfind("{"), s.rfind("}")
    if a == -1 or b <= a:
        return None
    try:
        d = json.loads(s[a:b + 1])
    except json.JSONDecodeError:
        return None
    need = {"input_i", "input_tp", "input_lra", "input_thresh", "target_offset"}
    return d if need.issubset(d) else None


def make_voice(base: Path, out_voice: Path) -> None:
    """Enhance + two-pass loudnorm the base audio -> voice.m4a."""
    m = measure_loudnorm(base, ENHANCE_AF)
    if m:
        ln = (f"{LOUDNORM}:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
              f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
              f":offset={m['target_offset']}:linear=true")
        print(f"  measured loudness I={m['input_i']} TP={m['input_tp']} LRA={m['input_lra']}")
    else:
        ln = LOUDNORM
        print("  loudnorm measurement failed -> one-pass")
    af = f"{ENHANCE_AF},{ln}"
    run(["ffmpeg", "-y", "-i", str(base), "-vn", "-af", af,
         "-c:a", "aac", "-b:a", "256k", "-ar", "48000", str(out_voice)])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("edl", type=Path)
    ap.add_argument("--lut", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--source", type=Path, default=None, help="override EDL source_path")
    ap.add_argument("--fps", type=int, default=30)
    args = ap.parse_args()

    edl = json.loads(args.edl.read_text())
    source = (args.source or Path(edl["source_path"])).resolve()
    lut = args.lut.resolve()
    out_dir = args.out_dir.resolve()
    work = out_dir / "clips_graded"
    work.mkdir(parents=True, exist_ok=True)

    if not source.exists():
        sys.exit(f"source not found: {source}")
    if not lut.exists():
        sys.exit(f"lut not found: {lut}")

    ranges = edl["ranges"]
    print(f"extracting {len(ranges)} graded segments @ {args.fps}fps")
    seg_paths: list[Path] = []
    for i, r in enumerate(ranges):
        start, end = float(r["start"]), float(r["end"])
        dur = end - start
        seg = work / f"seg_{i:02d}.mp4"
        ve = r.get("video_end")
        tag = f" [freeze tail @ {ve}]" if ve else ""
        print(f"  [{i:02d}] {start:7.2f}-{end:7.2f} ({dur:4.2f}s) {r.get('beat','')}{tag}")
        extract_segment(source, start, dur, lut, seg, args.fps, video_end=ve)
        seg_paths.append(seg)

    base = out_dir / "base_graded.mp4"
    print("concat -> base_graded.mp4")
    concat(seg_paths, base, out_dir)

    print("voice enhancement + loudnorm -> voice.m4a")
    voice = out_dir / "voice.m4a"
    make_voice(base, voice)

    print("mux graded video + enhanced voice -> clip.mp4")
    clip = out_dir / "clip.mp4"
    run(["ffmpeg", "-y", "-i", str(base), "-i", str(voice),
         "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "copy",
         "-movflags", "+faststart", "-shortest", str(clip)])

    # report
    def dur_of(p: Path) -> float:
        o = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "default=nw=1:nk=1", str(p)],
                           capture_output=True, text=True)
        return float(o.stdout.strip() or 0)
    print(f"\nclip.mp4  {dur_of(clip):.2f}s   voice.m4a {dur_of(voice):.2f}s")
    print("done")


if __name__ == "__main__":
    main()
