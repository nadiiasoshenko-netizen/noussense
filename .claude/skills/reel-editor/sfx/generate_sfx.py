#!/usr/bin/env python3
"""Generate the curated short-form SFX library with ElevenLabs Sound Effects (v2).

This file is BOTH the generator and the prompt record. Prompts follow ElevenLabs'
best practices: specific about source/material/envelope, onomatopoeia where useful,
tight durations for one-shots, higher prompt_influence (precision) for designed hits.

For each spec it:
  1. POSTs to https://api.elevenlabs.io/v1/sound-generation  (eleven_text_to_sound_v2)
  2. trims leading silence so the transient starts at t=0 (exact mix timing)
  3. peak-normalizes to -1 dBFS, converts to 48 kHz mono WAV
  4. writes to _shared-assets/sfx/<role>/<name>.wav
  5. upserts the clip into sfx.json (prompt + params stored, so it's reproducible)

Usage:
  python generate_sfx.py            # generate only missing files
  python generate_sfx.py --force    # regenerate everything
  python generate_sfx.py --only pop impact   # only these roles
  python generate_sfx.py --list     # print the prompt set, generate nothing

Key is read from the ELEVENLABS_API_KEY env var, or a .env file beside this script
(or in the current directory), e.g.  ELEVENLABS_API_KEY=sk_...
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys, tempfile, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
# look for a .env beside this script, then in the current working directory
ENV_CANDIDATES = [HERE / ".env", Path.cwd() / ".env"]
MANIFEST = HERE / "sfx.json"
API = "https://api.elevenlabs.io/v1/sound-generation"

# Per-role metadata used when a role is missing from sfx.json (new roles below).
ROLE_META = {
    "whoosh":   {"use_for": ["scene transitions", "reframe in/out", "whip cuts"], "default_gain_db": -9},
    "pop":      {"use_for": ["hero caption word", "gesture pill", "small text reveal"], "default_gain_db": -9},
    "ding":     {"use_for": ["UI/card reveal", "chip", "screenshot/repo card", "checklist tick"], "default_gain_db": -11},
    "click":    {"use_for": ["flow node", "small graphic beat", "cursor/select"], "default_gain_db": -13},
    "impact":   {"use_for": ["big landing/payoff", "number reveal", "white-flash hit", "combine"], "default_gain_db": -8},
    "riser":    {"use_for": ["tension build before a drop", "lead-in to a reveal"], "default_gain_db": -12},
    "keyboard": {"use_for": ["typing b-roll accent", "ASMR key click on a text beat", "tech/coding moments"], "default_gain_db": -12},
    "asmr":     {"use_for": ["satisfying tactile accent", "soft reveal", "palette-cleanser texture"], "default_gain_db": -12},
}

# (role, name, prompt, duration_s, prompt_influence)
SPECS = [
    # ---- transitions ----
    ("whoosh", "whoosh-soft-gen-01",   "A clean airy whoosh transition swooshing quickly past, smooth filtered white-noise sweep, short and crisp, professional sound design for a fast video cut", 0.8, 0.5),
    ("whoosh", "whoosh-fast-gen-01",   "A fast snappy swoosh swipe, quick high-frequency air movement, very short and tight, designed UI transition whoosh", 0.6, 0.6),
    ("whoosh", "whoosh-impact-gen-01", "A whoosh that sweeps in and lands on a soft deep thud, transition whoosh resolving into a clean sub-bass impact, cinematic and punchy", 1.2, 0.55),
    ("whoosh", "whoosh-reverse-gen-01","A reverse suck-in whoosh rising in pitch, smooth air pulled inward, short build-up transition before a cut", 1.0, 0.5),
    # ---- pops ----
    ("pop", "pop-tight-gen-01",  "A tight dry bubble pop, single short pluck with a quick transient, clean and punchy, for animated text popping in", 0.5, 0.6),
    ("pop", "pop-bubble-gen-01", "A juicy wet bubble pop, single satisfying bloop, rounded and bouncy, designed sound effect", 0.5, 0.6),
    ("pop", "pop-soft-gen-01",   "A soft subtle UI pop, gentle muted pop for a small element appearing, minimal and clean", 0.5, 0.55),
    # ---- dings / reveals ----
    ("ding", "ding-clean-gen-01",        "A single bright bell ding, clean glassy ting with a short shimmer tail, positive notification chime", 1.0, 0.55),
    ("ding", "ding-notification-gen-01", "A modern smartphone notification chime, two quick rising tones, clean digital ping, friendly", 1.0, 0.5),
    ("ding", "sparkle-reveal-gen-01",    "A magical sparkle shimmer, glittering bell twinkles cascading upward, light airy reveal accent, designed sound effect", 1.4, 0.5),
    ("ding", "chime-success-gen-01",     "A positive success chime, three ascending bright synth notes resolving happily, clean reward sound for a UI confirmation", 1.3, 0.5),
    # ---- clicks / ui ----
    ("click", "click-ui-gen-01",    "A single crisp UI click, one clean short tactile tap with a tight dry transient, minimal and clean, isolated, only one click", 0.5, 0.7),
    ("click", "click-tick-gen-01",  "A light dry tick, tiny short click like a toggle switch, very subtle and clean", 0.5, 0.6),
    ("click", "mouse-click-gen-01", "A single computer mouse click, crisp plastic button press and release, close-up, clean", 0.5, 0.65),
    ("click", "click-snap-gen-01",  "A single sharp tactile click, one short snappy tap with a tight punchy transient, clean and dry, isolated, one click only", 0.5, 0.7),
    ("click", "click-shutter-gen-01",      "A single camera shutter click, one quick crisp mechanical snap of a photo being taken, short clean and isolated, close-up, only one click", 0.5, 0.7),
    ("click", "click-shutter-soft-gen-01", "A single soft camera shutter click, one gentle crisp mechanical tick of a photo being taken, short clean and dry, close-up, just one click", 0.5, 0.7),
    # ---- impacts ----
    ("impact", "impact-sub-gen-01",      "A deep clean sub-bass impact hit, single punchy low boom with a tight decay, modern trailer impact with no reverb tail", 1.0, 0.55),
    ("impact", "impact-boom-gen-01",     "A cinematic boom impact, powerful deep hit with a short rumbling tail, dramatic and high quality", 1.6, 0.5),
    ("impact", "bass-drop-gen-01",       "A heavy 808 bass drop, deep sliding sub-bass landing hard, modern short-form drop, punchy", 1.4, 0.55),
    ("impact", "vine-boom-gen-01",       "A sudden dramatic bass boom, the classic deep meme impact, big low-end thud with a short tail, attention-grabbing", 1.2, 0.6),
    ("impact", "braam-cinematic-gen-01", "A spacious cinematic braam, deep brass trailer hit suitable for high-impact moments, bold and powerful", 1.8, 0.45),
    # ---- risers ----
    ("riser", "riser-tonal-gen-01", "A rising tonal riser building tension, smooth pitch sweep climbing to a peak, anticipation build-up before a drop", 2.5, 0.5),
    ("riser", "riser-noise-gen-01", "A white-noise riser sweeping upward, filtered noise build increasing in volume and brightness, tension build leading into an impact", 2.5, 0.5),
    # ---- keyboard (ASMR) ----
    ("keyboard", "keyboard-mech-single-gen-01", "A single keypress on a premium lubed mechanical keyboard, deep creamy thock with a soft cushioned bottom-out, intimate close-up ASMR, rich rounded and satisfying, no rattle", 0.5, 0.6),
    ("keyboard", "keyboard-mech-single-gen-02", "One tactile mechanical keyboard switch pressed once, rounded muted clack with a soft padded landing, deep and clean, close-up ASMR", 0.5, 0.6),
    ("keyboard", "keyboard-mech-typing-gen-01", "A short relaxed burst of typing on a premium lubed mechanical keyboard, creamy deep thocks with cushioned bottom-outs in an easy rhythm, intimate close-up ASMR", 1.8, 0.55),
    ("keyboard", "keyboard-soft-typing-gen-01", "Gentle typing on a quiet laptop keyboard, soft muted plastic taps in an easy rhythm, intimate close-up ASMR", 1.8, 0.6),
    ("keyboard", "keyboard-iphone-tap-gen-01",   "A single iPhone keyboard tap, the soft hollow muted tick of one iOS on-screen key press, short clean and isolated, close-up, only one tap", 0.5, 0.65),
    ("keyboard", "keyboard-iphone-tap-gen-02",   "One iOS touchscreen keyboard key press, a soft short hollow plastic tick, clean and muted, close-up, a single tap", 0.5, 0.65),
    ("keyboard", "keyboard-iphone-typing-gen-01","A short burst of typing on an iPhone touchscreen keyboard, soft hollow muted ticks in a quick light rhythm, the classic iOS keyboard click sound, close-up", 1.8, 0.6),
    ("keyboard", "keyboard-iphone-tap-gen-03",   "A single soft pitched pock, the familiar short muted hollow tap of a phone touchscreen keyboard key, like a tiny tuned woodblock tick, dry clean and very short, close-up, one tap only", 0.5, 0.7),
    ("keyboard", "keyboard-iphone-tap-gen-04",   "One short soft muted tock, a gentle hollow low-pitched key tap like a smartphone keyboard click, dry rounded and clean, a single isolated tap, close-up", 0.5, 0.7),
    # ---- asmr textures ----
    ("asmr", "asmr-wood-tap-gen-01",     "A soft fingernail tap on hollow wood, single gentle tok, warm crisp close-up ASMR", 0.6, 0.6),
    ("asmr", "asmr-wood-tap-gen-02",     "A single soft muted finger tap on solid wood, one warm gentle tok with a short dull resonance, intimate close-up ASMR, satisfying", 0.6, 0.6),
    ("asmr", "asmr-wood-tap-gen-03",     "A single soft knuckle tap on hollow wood, one muted rounded woody thock with a brief warm resonance, close-up ASMR", 0.6, 0.6),
    ("asmr", "asmr-wood-tap-gen-04",     "A single gentle muted tap on a wooden block, one soft warm dry tok, clean and intimate close-up ASMR", 0.5, 0.6),
    ("asmr", "asmr-wood-tap-gen-05",     "A single soft fingertip tap on bamboo, one muted mellow pock with a subtle hollow tone, satisfying close-up ASMR", 0.6, 0.6),
    ("asmr", "asmr-water-drop-gen-01",   "A single crisp water droplet plink dropping into water with a tiny resonant tail, satisfying close-up ASMR", 0.7, 0.6),
    ("asmr", "asmr-page-turn-gen-01",    "A paper page turning, soft crisp flip of a single book page, gentle close-up ASMR", 0.9, 0.6),
    ("asmr", "asmr-crinkle-gen-01",      "A soft plastic crinkle, gentle crackling of crisp packaging being squeezed, tingly close-up ASMR", 1.2, 0.6),
    ("asmr", "asmr-marble-click-gen-01", "A single isolated marble click, one clean crisp glassy tick ringing out into a smooth reverb tail, intimate close-up ASMR, satisfying and clean, only one hit", 1.1, 0.6),
    ("asmr", "asmr-marble-click-gen-02", "One single crisp click of a glass marble, a clean bright tick with a soft reverberant tail in a quiet room, close-up ASMR, satisfying, a single hit only", 1.1, 0.6),
    ("asmr", "asmr-pluck-gen-01",        "A soft tonal mouth pop, single satisfying rounded pock, clean close-up ASMR accent", 0.5, 0.6),
]


def load_key() -> str:
    # 1) environment variable wins
    env_key = os.environ.get("ELEVENLABS_API_KEY")
    if env_key:
        return env_key.strip()
    # 2) fall back to a .env file beside the script or in the cwd
    for env in ENV_CANDIDATES:
        if env.exists():
            for line in env.read_text().splitlines():
                if line.startswith("ELEVENLABS_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("ELEVENLABS_API_KEY not set (env var) and not found in a .env file")


def generate_mp3(key: str, prompt: str, dur: float, infl: float, out_mp3: Path) -> None:
    body = json.dumps({
        "text": prompt,
        "duration_seconds": dur,
        "prompt_influence": infl,
        "model_id": "eleven_text_to_sound_v2",
        "output_format": "mp3_44100_128",
    }).encode()
    req = urllib.request.Request(API, data=body, method="POST", headers={
        "xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    with urllib.request.urlopen(req, timeout=90) as r:
        out_mp3.write_bytes(r.read())


def peak_db(path: Path) -> float:
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
                        "-af", "volumedetect", "-vn", "-f", "null", "-"],
                       capture_output=True, text=True)
    for line in p.stderr.splitlines():
        if "max_volume:" in line:
            return float(line.split("max_volume:")[1].replace("dB", "").strip())
    return 0.0


def post_process(mp3: Path, wav: Path) -> None:
    """Trim leading silence -> peak-normalize to -1 dBFS -> 48k mono WAV."""
    gain = -1.0 - peak_db(mp3)
    af = (f"silenceremove=start_periods=1:start_duration=0:start_threshold=-50dB:detection=peak,"
          f"volume={gain:.2f}dB")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3),
                    "-af", af, "-ar", "48000", "-ac", "1", str(wav)], check=True)


def upsert_manifest(role: str, name: str, prompt: str, dur: float, infl: float) -> None:
    m = json.loads(MANIFEST.read_text())
    roles = m.setdefault("roles", {})
    if role not in roles:
        meta = ROLE_META.get(role, {"use_for": [], "default_gain_db": -12})
        roles[role] = {"use_for": meta["use_for"], "default_gain_db": meta["default_gain_db"], "clips": []}
    clips = roles[role].setdefault("clips", [])
    rel = f"{role}/{name}.wav"
    entry = {"file": rel, "tags": [], "rating": 3, "source": "elevenlabs gen 2026-06-03",
             "prompt": prompt, "duration_s": dur, "prompt_influence": infl}
    for i, c in enumerate(clips):
        if c.get("file") == rel:
            clips[i] = {**c, **entry}
            break
    else:
        clips.append(entry)
    MANIFEST.write_text(json.dumps(m, indent=2) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only", nargs="*", default=None, help="roles to limit to")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    specs = [s for s in SPECS if not args.only or s[0] in args.only]
    if args.list:
        for role, name, prompt, dur, infl in specs:
            print(f"[{role:9}] {name:30} {dur}s infl={infl}\n            {prompt}")
        print(f"\n{len(specs)} specs")
        return

    key = load_key()
    ok = skip = fail = 0
    for role, name, prompt, dur, infl in specs:
        (HERE / role).mkdir(parents=True, exist_ok=True)
        wav = HERE / role / f"{name}.wav"
        if wav.exists() and not args.force:
            print(f"  skip  {role}/{name}.wav (exists)"); skip += 1; continue
        try:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tf:
                tmp = Path(tf.name)
            generate_mp3(key, prompt, dur, infl, tmp)
            post_process(tmp, wav)
            tmp.unlink(missing_ok=True)
            upsert_manifest(role, name, prompt, dur, infl)
            print(f"  ok    {role}/{name}.wav"); ok += 1
        except urllib.error.HTTPError as e:
            print(f"  FAIL  {role}/{name}: HTTP {e.code} {e.read()[:200]!r}"); fail += 1
        except Exception as e:
            print(f"  FAIL  {role}/{name}: {e}"); fail += 1
    print(f"\ndone: {ok} generated, {skip} skipped, {fail} failed")


if __name__ == "__main__":
    main()
