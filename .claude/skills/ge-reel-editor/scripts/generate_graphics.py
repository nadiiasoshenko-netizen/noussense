#!/usr/bin/env python3
"""
Generate GE-styled transparent PNG overlays for reel captions: arrows and
comparison bars. Kept deliberately simple (thin lines, no shadows, no
gradients) to match the carousel infographic style — see
references/design-tokens.md for the full rationale.

Usage (called by build_reel.py, but runnable standalone for testing):
    python3 generate_graphics.py arrow_up out.png
    python3 generate_graphics.py arrow_down out.png
    python3 generate_graphics.py bar_compare out.png --small-label "STANDARD" --small-value 20 \
        --large-label "LE LABO" --large-value 240
    python3 generate_graphics.py bubble_stat out.png --diameter 260
"""
import argparse
from PIL import Image, ImageDraw, ImageFont

WINE = (107, 36, 48, 255)          # #6b2430
LIGHT_STONE = (217, 208, 194, 255)  # #d9d0c2
MUTED_GREY = (107, 97, 87, 255)     # #6b6157
CREAM = (241, 234, 224, 255)         # #f1eae0
TRANSPARENT = (0, 0, 0, 0)


def _font(size, bold=True):
    """Try Inter, fall back to DejaVu Sans Bold — see design-tokens.md."""
    candidates = [
        "assets/fonts/Inter-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def arrow(direction: str, out_path: str, size=(200, 200), stroke=8):
    """A single thin wine-red arrow. direction: 'up' or 'down'."""
    w, h = size
    img = Image.new("RGBA", size, TRANSPARENT)
    d = ImageDraw.Draw(img)
    cx = w // 2
    top, bottom = int(h * 0.15), int(h * 0.85)
    if direction == "down":
        top, bottom = bottom, top
    d.line([(cx, bottom), (cx, top)], fill=WINE, width=stroke)
    head = int(h * 0.22)
    dy = 1 if top < bottom else -1
    d.line(
        [(cx - head, top + head * dy), (cx, top), (cx + head, top + head * dy)],
        fill=WINE, width=stroke, joint="curve",
    )
    img.save(out_path)


def bar_compare(out_path, small_label="", small_value="", large_label="",
                 large_value="", bar_width=620, value_margin=140,
                 small_frac=0.12, on_dark=True):
    """
    Two horizontal bars: a short light-stone bar and a long wine-red bar,
    matching the carousel comparison-chart language. small_frac controls how
    short the small bar renders relative to the large one (visual emphasis,
    not literal proportion — see design-tokens.md on why literal proportion
    often isn't legible for extreme ratios).

    bar_width is the drawable bar length; value_margin is extra canvas width
    reserved to the right of the bars for the value labels — the canvas is
    bar_width + value_margin wide, so labels never get clipped off the edge.

    on_dark: whether this overlay sits on dark video footage (the common
    case for reels) or light footage. This controls label/value text color —
    getting it wrong means text can vanish against the background, so don't
    hardcode a single color here.
    """
    width = bar_width + value_margin
    bar_h = 44
    gap = 46
    label_h = 34
    total_h = label_h + bar_h + gap + label_h + bar_h + 10
    img = Image.new("RGBA", (width, total_h), TRANSPARENT)
    d = ImageDraw.Draw(img)
    f_label = _font(22)
    f_value = _font(22)
    label_color = CREAM if on_dark else MUTED_GREY
    value_color = CREAM if on_dark else (28, 19, 14, 255)

    y = 0
    d.text((0, y), small_label, font=f_label, fill=label_color)
    y += label_h
    small_w = max(30, int(bar_width * small_frac))
    d.rectangle([0, y, small_w, y + bar_h], fill=LIGHT_STONE)
    d.text((small_w + 16, y + 6), str(small_value), font=f_value, fill=value_color)
    y += bar_h + gap

    d.text((0, y), large_label, font=f_label, fill=label_color)
    y += label_h
    d.rectangle([0, y, bar_width, y + bar_h], fill=WINE)
    d.text((bar_width + 16, y + 6), str(large_value), font=f_value, fill=value_color)

    img.save(out_path)


def bubble_stat(out_path, diameter=260, stroke=4):
    """A thin wine-red circular outline to ring the 'remember this number' stat.
    Draws only the ring — composite the actual number as a separate ASS caption
    centered on top of it."""
    pad = stroke * 2
    size = diameter + pad * 2
    img = Image.new("RGBA", (size, size), TRANSPARENT)
    d = ImageDraw.Draw(img)
    d.ellipse([pad, pad, pad + diameter, pad + diameter], outline=WINE, width=stroke)
    img.save(out_path)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("kind", choices=["arrow_up", "arrow_down", "bar_compare", "bubble_stat"])
    p.add_argument("out_path")
    p.add_argument("--small-label", default="")
    p.add_argument("--small-value", default="")
    p.add_argument("--large-label", default="")
    p.add_argument("--large-value", default="")
    p.add_argument("--diameter", type=int, default=260)
    p.add_argument("--on-dark", action="store_true", default=True)
    p.add_argument("--on-light", dest="on_dark", action="store_false")
    args = p.parse_args()

    if args.kind == "arrow_up":
        arrow("up", args.out_path)
    elif args.kind == "arrow_down":
        arrow("down", args.out_path)
    elif args.kind == "bar_compare":
        bar_compare(args.out_path, args.small_label, args.small_value,
                    args.large_label, args.large_value, on_dark=args.on_dark)
    elif args.kind == "bubble_stat":
        bubble_stat(args.out_path, args.diameter)
    print(f"Wrote {args.out_path}")
