#!/usr/bin/env python3
"""Per-word kinetic captions for the reel (EVERY word animates).

Emits window.__CAPS = [segment,...]. Two segment kinds give the "mix of running
line + one-big-word" look:
  - 'line': 2-4 words on one centered line; each word pops in on its spoken time,
            then the line is replaced by the next segment. Mixed fonts (Geist +
            occasional Instrument Serif), weight variation = kinetic typography.
  - 'big' : a single hero word, huge + serif + glow, alone in the band (the line
            hides). Used only on full-stage beats (suppressed while a diagram owns
            the screen, where the hero stays inline serif+glow instead).

Per word: {w, s, e, font:'sans'|'serif', glow:bool, weight:700|800}
Timing is nominal (edited.json); the engine scales by SCALE.

Usage: python build_captions.py ../edited.json -o ../caps.js
"""
import argparse, json, re
from pathlib import Path

# per-beat: mood, hero words that go BIG (one-big-word breakout), inline serif emphasis
BEAT_CFG = {
    "HOOK":              {"mood": "cool",   "big": ["team"],         "serif": ["replace"]},
    "PROOF_META":        {"mood": "cool",   "big": [],               "serif": ["entire", "captions"]},
    "PAIN":              {"mood": "warm",   "big": ["hours"],        "serif": ["time"]},
    "STAKES":            {"mood": "warm",   "big": ["bottlenecks"],  "serif": ["content"]},
    "WORKFLOW":          {"mood": "silver", "big": ["simple"],       "serif": ["iPhone", "publish"]},
    "REPO1_VIDEO_USE":   {"mood": "cool",   "big": ["video-use"],    "serif": ["takes", "cleanest"], "merge": ("video", "use")},
    "REPO2_HYPERFRAMES": {"mood": "cool",   "big": ["hyperframes"],  "serif": ["graphics", "talk"]},
    "COMBINE":           {"mood": "cool",   "big": ["shot"],         "serif": ["one", "skill"]},
    "CTA":               {"mood": "silver", "big": ["video"],        "serif": ["setup", "DM"]},
}

# windows (nominal s) where a diagram owns the screen -> demote BIG to inline serif+glow
DIAGRAM_WINDOWS = [(4.3, 10.2), (18.7, 25.7), (25.9, 34.5), (34.9, 41.3), (41.6, 46.9), (47.7, 54.3)]
SENT_END = (".", "!", "?")
MAX_LINE = 4


def clean(t: str) -> str:
    t = t.strip().strip('"').strip("'")
    t = t.replace("Cloud Code", "Claude Code")
    if t.lower() == "cloud":
        t = "Claude"
    return t


def disp(t: str) -> str:
    return clean(t).rstrip(".,;:")


def in_diagram(t: float) -> bool:
    return any(a <= t <= b for a, b in DIAGRAM_WINDOWS)


def beat_words(words, b, cfg):
    bw = [w for w in words if w["start"] >= b["out_start"] - 0.001 and w["end"] <= b["out_end"] + 0.001]
    merge = cfg.get("merge")
    if merge:
        out, i = [], 0
        while i < len(bw):
            if (i + 1 < len(bw) and disp(bw[i]["text"]).lower() == merge[0]
                    and disp(bw[i + 1]["text"]).lower() == merge[1]):
                out.append({"text": "video-use", "start": bw[i]["start"], "end": bw[i + 1]["end"]})
                i += 2
            else:
                out.append(bw[i]); i += 1
        bw = out
    return bw


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("edited", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    args = ap.parse_args()
    d = json.loads(args.edited.read_text())
    words = d["words"]

    segs = []
    for b in d["beats"]:
        cfg = BEAT_CFG.get(b["beat"], {"mood": "silver", "big": [], "serif": []})
        mood = cfg["mood"]
        bigset = [x.lower() for x in cfg["big"]]
        serifset = [x.lower() for x in cfg["serif"]]
        bw = beat_words(words, b, cfg)

        line = []
        def flush():
            nonlocal line
            if line:
                segs.append({"kind": "line", "mood": mood, "words": line})
                line = []

        for w in bw:
            raw = clean(w["text"])
            dd = disp(w["text"])
            if not dd:
                continue
            low = dd.lower()
            is_big_word = any(k in low or low in k for k in bigset)
            is_serif = is_big_word or any(low == s or low in s.split() for s in serifset)
            glow = is_big_word
            weight = 800 if (is_serif or len(dd) >= 7) else 700
            wd = {"w": dd, "s": round(w["start"], 3), "e": round(w["end"], 3),
                  "font": "serif" if is_serif else "sans", "glow": glow, "weight": weight}

            if is_big_word and not in_diagram(w["start"]):
                flush()
                segs.append({"kind": "big", "mood": mood, "words": [wd]})
                continue
            line.append(wd)
            hard = raw.endswith(SENT_END)
            soft = raw.endswith(",") and len(line) >= 2
            if len(line) >= MAX_LINE or hard or soft:
                flush()
        flush()

    # compute show windows: each segment visible until the next one begins
    for i, sg in enumerate(segs):
        sg["in"] = round(sg["words"][0]["s"] - 0.06, 3)
        if i + 1 < len(segs):
            sg["out"] = round(segs[i + 1]["words"][0]["s"] - 0.02, 3)
        else:
            sg["out"] = round(sg["words"][-1]["e"] + 0.4, 3)
        # keep a big word up at least 0.4s when possible
        if sg["kind"] == "big":
            sg["out"] = max(sg["out"], round(sg["words"][0]["s"] + 0.40, 3))

    args.out.write_text("window.__CAPS = " + json.dumps(segs, separators=(",", ":")) + ";\n")
    nbig = sum(1 for s in segs if s["kind"] == "big")
    nwords = sum(len(s["words"]) for s in segs)
    print(f"wrote {args.out}: {len(segs)} segments ({nbig} big), {nwords} words")
    for s in segs:
        tag = "BIG " if s["kind"] == "big" else "line"
        em = "".join(("*" if w["font"] == "serif" else "") + ("^" if w["glow"] else "") for w in s["words"])
        print(f"  {s['in']:6.2f}-{s['out']:6.2f} {s['mood']:6} {tag} {' '.join(w['w'] for w in s['words'])}")


if __name__ == "__main__":
    main()
