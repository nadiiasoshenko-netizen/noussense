#!/usr/bin/env python3
"""QA gate for the SFX library — catches bad generations WITHOUT listening.

For each clip it measures objective features and flags likely defects:
  - BUZZ/SUSTAIN : low crest factor + high flat factor on a role that should be a
                   punchy transient (a drone/buzz instead of a clean hit).
  - MULTI        : more onsets than a single-hit role should have (e.g. "multiple
                   marbles" when we asked for one click).
  - HOT          : peak above -0.3 dBFS (clipping risk).
  - SILENT       : essentially no signal.

Punchy roles (click/pop/impact/ding/asmr) are held to the transient profile.
Swell/texture roles (whoosh/riser/keyboard/bed) are NOT buzz-checked — a whoosh is a
sweep and typing is many taps; those are supposed to be sustained/multi.

Usage:
  python qa_sfx.py                 # report on the whole library
  python qa_sfx.py --only click    # one role
  python qa_sfx.py --spectro       # also dump _qa/sp_<name>.png spectrograms
  python qa_sfx.py --fails         # print only flagged clips
"""
from __future__ import annotations
import argparse, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
# TRANSIENT roles must be a sharp snap (high crest). TONAL roles (bells/booms/bass,
# muted taps) are dense/ring naturally -> low crest is FINE; only a high flat factor
# (sustained constant-level noise) means a real buzz/drone.
TRANSIENT = {"click", "pop"}
TONAL     = {"ding", "impact", "asmr"}
# SWELL/TEXTURE roles (whoosh sweep, riser, typing) are meant to be sustained/multi.
MULTI_OK = ("typing", "crinkle", "page", "sparkle", "chime", "mouse")  # name substrings

FLAT_BUZZ  = 2.0   # flat factor above this => sustained noise / buzz (THE real signal)
CREST_DULL = 5.0   # dB; a click/pop below this is smeared/dull, not a clean snap
PEAK_HOT   = -0.3  # dBFS


def astats(path: Path) -> dict:
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
                        "-af", "astats=metadata=1", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    out = {}
    for key, label in [("crest", "Crest factor"), ("flat", "Flat factor"),
                       ("rms", "RMS level dB"), ("peak", "Peak level dB")]:
        for line in p.splitlines():
            if label in line:
                try: out[key] = float(line.split(":")[1])
                except ValueError: pass
                break
    return out


def onsets(path: Path) -> int:
    """Count sharp energy onsets via a 10ms RMS envelope (rising edges into loud)."""
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
                        "-af", "asetnsamples=n=480,astats=metadata=1:reset=1,"
                        "ametadata=print:key=lavfi.astats.Overall.RMS_level",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    env = []
    for line in p.splitlines():
        if "RMS_level=" in line:
            try: env.append(float(line.split("=")[1]))
            except ValueError: env.append(-90.0)
    n, armed = 0, True
    for v in env:
        if armed and v > -28:        # crossed into a loud window
            n += 1; armed = False
        elif v < -42:                # quiet again -> ready for next onset
            armed = True
    return n


def dur(path: Path) -> float:
    o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(path)], capture_output=True, text=True)
    return float(o.stdout.strip() or 0)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--spectro", action="store_true")
    ap.add_argument("--fails", action="store_true")
    args = ap.parse_args()
    if args.spectro: (HERE / "_qa").mkdir(exist_ok=True)

    files = sorted(HERE.glob("*/*.wav"))
    print(f"{'file':42} {'dur':>5} {'crest':>6} {'flat':>5} {'peak':>6} {'onset':>5}  flags")
    nflag = 0
    for f in files:
        role = f.parent.name
        if args.only and role not in args.only: continue
        s = astats(f); d = dur(f); on = onsets(f)
        crest, flat, peak = s.get("crest", 0), s.get("flat", 0), s.get("peak", -99)
        flags = []
        name = f.stem
        if peak == -99 or s.get("rms", -99) < -60: flags.append("SILENT")
        if peak > PEAK_HOT: flags.append("HOT")
        if role in TRANSIENT or role in TONAL:
            if flat > FLAT_BUZZ:
                flags.append("BUZZ")
            if role in TRANSIENT and crest < CREST_DULL:
                flags.append("DULL")
            if on > 2 and not any(t in name for t in MULTI_OK):
                flags.append(f"MULTI({on})")
        flagstr = " ".join(flags)
        if flags: nflag += 1
        if args.fails and not flags: continue
        print(f"{role+'/'+name:42} {d:5.2f} {crest:6.1f} {flat:5.2f} {peak:6.1f} {on:5}  {flagstr}")
        if args.spectro:
            subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(f),
                            "-lavfi", "showspectrumpic=s=420x240:legend=0:color=intensity",
                            str(HERE / "_qa" / f"sp_{name}.png")])
    print(f"\n{nflag} flagged")


if __name__ == "__main__":
    main()
