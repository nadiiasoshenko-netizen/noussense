#!/usr/bin/env python3
"""Mix per-word ticks + layered role hits onto the voice (typing-caption style).

  layer 1: an iPhone-keyboard TICK on EVERY word onset (subtle typing texture)
  layer 2: louder role hits on beats — whoosh (transitions/flashes), pop (hero
           words), ding (reveals), click (flow nodes), impact (payoff)

All hit clips resolve from the curated library (_shared-assets/sfx) by ROLE,
preferring the highest user `rating` in sfx.json. The tick is the top-rated
'keyboard' clip (your real iPhone tap). Outputs voice_sfx.m4a. Run from project dir.
"""
import array, json, math, subprocess, wave
from pathlib import Path

VOICE = "voice_v3.m4a"
OUT = "voice_sfx.m4a"
EDITED = "edited.json"
S = 1.0044  # nominal -> encoded clip time

# --- per-word tick sync ---------------------------------------------------
# The library tick (iphone-real-01.wav) was sliced ~12.3 ms BEFORE the tap
# transient and never trimmed, so placing it at the word time made the audible
# tap land ~12 ms late. We pre-build a TRIMMED tick (edit/tick_trimmed.wav)
# whose transient sits at ~1.5 ms (a deliberate fade-in lead to kill the click).
# Measured: transient onset of the source = sample 592 (12.33 ms @48k).
TICK_TRIMMED = Path("edit/tick_trimmed.wav")
TICK_LEAD_S = 0.0015   # residual lead before transient inside the trimmed file (1.5 ms)

# Measured systematic voice-onset offset vs word.start*S: on the cleanest,
# well-isolated words ("including" +12.3, "motion" +16.4, "and" +6.8 ms) the
# audible voice energy lands a touch AFTER word.start*S — median ~+9.6 ms,
# mean ~+8 ms. We nudge the tick later by this much so it hits the voice, not
# the (slightly early) forced-aligner phoneme boundary.
VOICE_ONSET_OFFSET_S = 0.008   # +8 ms

# Net placement so the AUDIBLE transient lands at (word.start*S + 8 ms):
# place file head at  t*S + VOICE_ONSET_OFFSET_S - TICK_LEAD_S.
TICK_PLACE_OFFSET_S = VOICE_ONSET_OFFSET_S - TICK_LEAD_S   # +6.5 ms

# locate the shared SFX library (walk up to the dir holding _shared-assets)
def find_lib() -> Path:
    p = Path.cwd()
    for _ in range(8):
        if (p / "_shared-assets" / "sfx").exists():
            return p / "_shared-assets" / "sfx"
        p = p.parent
    raise SystemExit("could not locate _shared-assets/sfx")

LIB = find_lib()
MAN = json.loads((LIB / "sfx.json").read_text())


def pick(role: str) -> Path:
    """Highest-rated clip in a role."""
    clips = MAN["roles"][role]["clips"]
    best = max(clips, key=lambda c: c.get("rating", 0))
    return LIB / best["file"]

# Per-word tick: use the locally trimmed version (transient at head) instead of
# the raw library clip so taps land sample-accurate on each word.
if not TICK_TRIMMED.exists():
    raise SystemExit(f"missing {TICK_TRIMMED} — build it first (transient-trimmed iphone-real-01)")
TICK = TICK_TRIMMED
ROLE = {r: pick(r) for r in ("whoosh", "pop", "ding", "click", "impact")}

# ---- layer 2: role hits  (time_encoded_s, role, gain_dB) ----
HITS = [
    # section transitions / white-flash punches
    (4.2, "whoosh", -10), (10.3, "whoosh", -10), (18.5, "whoosh", -10),
    (25.9, "whoosh", -9), (35.0, "whoosh", -10), (41.55, "whoosh", -9), (46.9, "whoosh", -9),
    # one-big-word hero breakouts -> pop (loud)
    (3.62, "pop", -7), (12.62, "pop", -7), (16.11, "pop", -7),
    # inline glow heroes -> pop (softer)
    (19.01, "pop", -12), (26.79, "pop", -11), (34.82, "pop", -11), (46.65, "pop", -10), (53.08, "pop", -11),
    # reveals -> ding (chips, repo cards, lead-magnet phone)
    (7.0, "ding", -12), (8.35, "ding", -12), (9.16, "ding", -12),
    (26.0, "ding", -9), (35.1, "ding", -9), (47.85, "ding", -9),
    # workflow flow nodes -> click (synced to each spoken step)
    (19.85, "click", -14), (21.05, "click", -14), (22.1, "click", -14), (24.95, "click", -13),
    # REPO1 timeline editor: splice cuts -> click (sharper) + clean stitch -> ding
    (32.0, "click", -10), (32.6, "click", -10), (33.2, "click", -10), (33.7, "ding", -11),
    # NEW diagrams: hook repo pills / pain bars / stakes bottleneck nodes / cta comment
    (1.0, "ding", -13), (1.3, "ding", -13),
    (13.35, "ding", -11),
    (16.8, "click", -13), (17.05, "click", -13), (17.3, "click", -13),
    (52.75, "ding", -10),
    # payoff landings -> impact (combine merge)
    (44.1, "impact", -7),
]


def load_i16(path: Path):
    w = wave.open(str(path), "rb")
    ch, fr, n = w.getnchannels(), w.getframerate(), w.getnframes()
    a = array.array("h"); a.frombytes(w.readframes(n)); w.close()
    if ch == 2:
        a = a[0::2]
    return a, fr


def build_tick_track(dur: float, out_path: Path, gain_db: float = -19.0) -> None:
    tick, fr = load_i16(TICK)
    assert fr == 48000, f"tick must be 48k, got {fr}"
    g = 10 ** (gain_db / 20)
    n = int(dur * fr) + fr
    buf = array.array("i", bytes(4 * n))  # zeroed int32 accumulator
    words = json.loads(Path(EDITED).read_text())["words"]
    last = -1.0
    placed = 0
    for wd in words:
        t = wd["start"] * S
        if t - last < 0.05:      # avoid machine-gun doubling on ultra-fast words
            continue
        last = t                 # density gate stays on the raw word time
        # place the trimmed tick so its audible transient lands on the voice:
        #   word.start*S + voice-onset offset, minus the file's internal lead.
        place = t + TICK_PLACE_OFFSET_S
        off = int(round(place * fr))
        if off < 0:
            off = 0
        for j, s in enumerate(tick):
            k = off + j
            if k >= n:
                break
            buf[k] += int(s * g)
        placed += 1
    out = array.array("h", bytes(2 * n))
    for i in range(n):
        v = buf[i]
        out[i] = -32768 if v < -32768 else (32767 if v > 32767 else v)
    w = wave.open(str(out_path), "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(fr)
    w.writeframes(out.tobytes()); w.close()
    print(f"  tick track: {placed} ticks @ {gain_db}dB -> {out_path.name}")


def voice_dur() -> float:
    o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", VOICE], capture_output=True, text=True)
    return float(o.stdout.strip())


def main() -> None:
    dur = voice_dur()
    tick_path = Path("tick_track.wav")
    build_tick_track(dur, tick_path)

    hits = sorted(HITS)
    inputs = ["-i", VOICE, "-i", str(tick_path)]
    fc, labels = [], ["[0:a]", "[1:a]"]
    for i, (t, role, g) in enumerate(hits):
        inputs += ["-i", str(ROLE[role])]
        idx = i + 2
        fc.append(f"[{idx}:a]adelay={int(round(t*1000))}:all=1,volume={g}dB[s{i}]")
        labels.append(f"[s{i}]")
    fc.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first[mx];"
              f"[mx]alimiter=limit=0.97[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs,
                    "-filter_complex", ";".join(fc), "-map", "[out]",
                    "-c:a", "aac", "-b:a", "256k", "-ar", "48000", OUT], check=True)
    tick_path.unlink(missing_ok=True)
    from collections import Counter
    c = Counter(r for _, r, _ in hits)
    print(f"wrote {OUT}: tick=keyboard + {len(hits)} hits  " + ", ".join(f"{k}:{v}" for k, v in c.items()))
    print("  resolved:", "tick="+TICK.name, *[f"{r}={ROLE[r].name}" for r in ROLE])


if __name__ == "__main__":
    main()
