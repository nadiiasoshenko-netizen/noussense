#!/usr/bin/env python3
"""
Convert a beats.json timeline into a styled .ass subtitle file using The
Growth Edit's four caption modes (kicker / statement / hook / stat).

beats.json schema — a list of beat objects:
[
  {
    "start": 0.0,           # seconds
    "end": 3.2,
    "mode": "statement",    # kicker | statement | hook | stat
    "text": "Every bottle of Le Labo was mixed in front of you.",
    "chunk": true,          # optional, default true for statement/hook —
                             # splits text into progressive phrase-chunks
                             # rather than showing the whole line at once
    "background": "dark"    # optional, "dark" or "light" — flips text color
                             # for legibility against the footage. Default "dark".
  },
  ...
]

Why phrase-chunking matters: showing a whole sentence at once, sitting on
screen for its full duration, is what makes a caption feel like a plain
subtitle. Breaking it into 3-6 word chunks that pop in sequentially, each
holding for a fraction of the beat's duration, is what makes it feel like a
designed motion graphic. See references/design-tokens.md for the full
rationale — don't skip chunking just because it's more code.

Usage:
    python3 generate_ass.py beats.json output.ass --fonts-dir assets/fonts
"""
import argparse
import json
import re
import sys

PLAY_RES_X, PLAY_RES_Y = 1080, 1920

# Hex (RGB) -> ASS (&HAABBGGRR). Kept as a function, not a hardcoded table,
# so this script and design-tokens.md never drift out of sync.
def hex_to_ass(hex_rgb: str, alpha: int = 0) -> str:
    hex_rgb = hex_rgb.lstrip("#")
    r, g, b = hex_rgb[0:2], hex_rgb[2:4], hex_rgb[4:6]
    return f"&H{alpha:02X}{b}{g}{r}".upper()

ESPRESSO = hex_to_ass("1c130e")
CREAM = hex_to_ass("f1eae0")
TAUPE = hex_to_ass("c9b48c")
WINE = hex_to_ass("6b2430")

def pick_fonts(fonts_dir: str | None):
    """Prefer real brand fonts if present, else fall back — see
    references/design-tokens.md. Returns (serif_name, sans_name) as they'll
    be referenced in the ASS Fontname field; ffmpeg's libass resolves these
    via fontconfig, so a font with that family name must be installed or
    embedded, not just present as a file on disk."""
    import subprocess
    def family_available(name: str) -> bool:
        try:
            out = subprocess.run(["fc-list", f":family={name}"], capture_output=True, text=True)
            return bool(out.stdout.strip())
        except FileNotFoundError:
            return False

    serif = "Playfair Display" if family_available("Playfair Display") else "DejaVu Serif"
    sans = "Inter" if family_available("Inter") else "DejaVu Sans"
    if serif == "DejaVu Serif" or sans == "DejaVu Sans":
        print(
            "NOTE: Playfair Display / Inter not found via fontconfig — falling back to "
            "DejaVu. For an exact brand match, install the real fonts (see "
            "references/design-tokens.md) and re-run.",
            file=sys.stderr,
        )
    return serif, sans


def chunk_text(text: str, max_words: int = 5) -> list[str]:
    """Split a sentence into progressive phrase-chunks at natural boundaries
    (punctuation first, then word count) rather than mid-syllable."""
    parts = re.split(r"(?<=[,;—-])\s+", text)
    chunks = []
    for part in parts:
        words = part.split()
        for i in range(0, len(words), max_words):
            chunks.append(" ".join(words[i:i + max_words]))
    return chunks or [text]


def build_styles(serif: str, sans: str) -> str:
    # Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour,
    # OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX,
    # ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment,
    # MarginL, MarginR, MarginV, Encoding
    return "\n".join([
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: kicker_dark,{sans},34,{TAUPE},{TAUPE},&H00000000,&H00000000,1,0,0,0,100,100,4,0,1,0,0,7,72,72,120,1",
        f"Style: kicker_light,{sans},34,{WINE},{WINE},&H00000000,&H00000000,1,0,0,0,100,100,4,0,1,0,0,7,72,72,120,1",
        f"Style: statement_dark,{serif},62,{CREAM},{CREAM},&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,2,80,80,300,1",
        f"Style: statement_light,{serif},62,{ESPRESSO},{ESPRESSO},&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,2,80,80,300,1",
        f"Style: hook,{serif},64,{WINE},{WINE},&H00000000,&H00000000,1,1,0,0,100,100,0,0,1,0,0,2,90,90,320,1",
        f"Style: stat_dark,{serif},150,{CREAM},{CREAM},&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,80,80,900,1",
        f"Style: stat_light,{serif},150,{ESPRESSO},{ESPRESSO},&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,80,80,900,1",
        f"Style: stat_hook,{serif},150,{WINE},{WINE},&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,80,80,900,1",
    ])


def fmt_time(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def style_for(beat: dict) -> str:
    mode = beat["mode"]
    bg = beat.get("background", "dark")
    if mode == "kicker":
        return "kicker_dark" if bg == "dark" else "kicker_light"
    if mode == "statement":
        return "statement_dark" if bg == "dark" else "statement_light"
    if mode == "hook":
        return "hook"
    if mode == "stat":
        if beat.get("stat_is_hook"):
            return "stat_hook"
        return "stat_dark" if bg == "dark" else "stat_light"
    raise ValueError(f"Unknown mode: {mode}")


def build_events(beats: list[dict]) -> str:
    lines = [
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for beat in beats:
        style = style_for(beat)
        start, end = beat["start"], beat["end"]
        duration = end - start
        text = beat["text"]
        should_chunk = beat.get("chunk", beat["mode"] in ("statement", "hook"))

        if should_chunk and duration > 0:
            chunks = chunk_text(text)
            slice_dur = duration / len(chunks)
            gap = min(0.15, slice_dur * 0.1)  # small breathing gap between chunks
            for i, chunk in enumerate(chunks):
                c_start = start + i * slice_dur
                c_end = c_start + slice_dur - gap
                if c_end <= c_start:
                    c_end = c_start + slice_dur
                lines.append(
                    f"Dialogue: 0,{fmt_time(c_start)},{fmt_time(c_end)},{style},,0,0,0,,"
                    f"{{\\fad(120,120)}}{chunk}"
                )
        else:
            lines.append(
                f"Dialogue: 0,{fmt_time(start)},{fmt_time(end)},{style},,0,0,0,,"
                f"{{\\fad(120,120)}}{text}"
            )
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("beats_json")
    p.add_argument("output_ass")
    p.add_argument("--fonts-dir", default=None, help="Unused directly by this script "
                    "(fontconfig resolves by family name), kept for symmetry with build_reel.py")
    args = p.parse_args()

    with open(args.beats_json) as f:
        beats = json.load(f)

    serif, sans = pick_fonts(args.fonts_dir)

    header = "\n".join([
        "[Script Info]",
        "ScriptType: v4.00+",
        f"PlayResX: {PLAY_RES_X}",
        f"PlayResY: {PLAY_RES_Y}",
        "ScaledBorderAndShadow: yes",
        "",
    ])
    styles = build_styles(serif, sans)
    events = build_events(beats)

    with open(args.output_ass, "w") as f:
        f.write(header + styles + "\n\n" + events + "\n")

    print(f"Wrote {args.output_ass} ({len(beats)} beats)")


if __name__ == "__main__":
    main()
