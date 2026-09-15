# Nous Sense — Reel Caption Design Tokens

This is the single source of truth for colors, type, and style-mode rules used by
`scripts/generate_ass.py` and `scripts/generate_graphics.py`. If the brand system
changes, update this file first — the scripts read their defaults from here (or
mirror these exact values if hardcoded).

## Colors (RGB hex → ASS BGR)

ASS subtitle colors use `&HAABBGGRR` (alpha, blue, green, red — reverse byte order
from normal hex). Get this wrong and colors render subtly off, so the conversion
is spelled out here rather than left to memory:

| Name | Hex (RGB) | ASS (&HAABBGGRR) | Use |
|---|---|---|---|
| Espresso ink | `#1c130e` | `&H000E131C` | Dark backgrounds, body text on light bg |
| Cream / ivory | `#f1eae0` | `&H00E0EAF1` | Light backgrounds, text on dark bg |
| Cream (alt) | `#faf6f0` | `&H00F0F6FA` | Secondary light bg tone |
| Taupe | `#c9b48c` | `&H008CB4C9` | Kicker text on dark/photo backgrounds |
| Light stone | `#d9d0c2` | `&H00C2D0D9` | Muted bar-chart baseline segments |
| Cool blue-grey | `#acb9c6` | `&H00C6B9AC` | Dividers, secondary bar segments |
| Wine-red (accent) | `#6b2430` | `&H0030246B` | The ONE saturated color — hooks, emphasis, kicker labels on light bg, stat numbers when the number itself is the "hook" |
| Muted grey | `#6b6157` | `&H00576166` | Small labels under bar-chart segments |

**Rule: only one accent color per video.** Wine-red is it. Never introduce a second
saturated color (no blue, no green, no orange) even for "variety" — variety comes
from typography and layout, not from adding colors.

## Typography

- **Serif (headlines, stats, hooks):** Playfair Display. Drop the actual font files
  (`PlayfairDisplay-Regular.ttf`, `PlayfairDisplay-Medium.ttf`,
  `PlayfairDisplay-BoldItalic.ttf`) into `assets/fonts/` for an exact match —
  download from Google Fonts if the environment has network access. If absent,
  the scripts fall back to **DejaVu Serif**, which is close enough in weight and
  proportion not to look broken, but flag this to the user once so they know to
  add the real fonts later.
- **Sans (kickers, small labels):** Inter. Same pattern — drop
  `Inter-Bold.ttf` / `Inter-SemiBold.ttf` into `assets/fonts/`, fall back to
  **DejaVu Sans Bold** or **Liberation Sans Bold** if absent.
- Kicker text is always small caps styling via actual uppercase characters (ASS
  doesn't reliably support CSS-style small-caps), bold, letter-spaced (`\fsp4` or
  higher in ASS tags).

## The four caption modes

Every spoken line gets classified into exactly one of these. Mixing modes across
consecutive beats is what makes the video feel designed instead of like a plain
subtitle track — never let more than two consecutive beats share a mode.

### 1. `kicker`
Short (2–5 word) section labels — spoken transitions like "quick context," "here's
the turn," "so here's the lesson." Not every sentence needs one; use at natural
section boundaries, roughly once per 3–5 statement beats.
- Font: Inter Bold, small size (~34px at 1080×1920), letter-spaced
- Color: wine-red on light/neutral background footage, taupe if the footage is
  dark (contrast check matters more than rigid color assignment here)
- Position: top-left, matching the carousel kicker convention
- Motion: simple fade in/out, no scale or slide — kickers are quiet, not loud

### 2. `statement`
The default mode. Regular explanatory sentences — the connective tissue of the
script.
- Font: Playfair Display Regular/Medium, mid-large size (~60–66px)
- Color: cream on dark footage, espresso ink on light footage
- Position: lower-third, centered
- Motion: phrase-by-phrase reveal (break sentences into 3–6 word chunks that pop
  in sequentially rather than the whole sentence appearing at once) — this is the
  single biggest thing that separates "designed caption" from "plain subtitle"

### 3. `hook`
The line in each beat designed to land — the quotable insight, the turn, the
punchline. There's usually exactly one hook per beat/section, not one per
sentence.
- Font: Playfair Display Bold Italic, larger than statement (~58–70px)
- Color: wine-red, always — this is the one place the accent color appears in
  running text, which is exactly why it reads as emphasis
- Position: centered, slightly larger vertical margin so it feels like a "moment"
- Motion: fade in with a touch more hold time than statement beats — let it sit

### 4. `stat`
Any spoken number, price, percentage, or quantity worth seeing, not just hearing.
- Font: Playfair Display, very large (~130–170px), the same scale used for the
  giant-number carousel slides
- Color: cream on dark footage, espresso ink on light footage — UNLESS the number
  itself is the emotional turn (e.g., "$60 million"), in which case use wine-red
  to double down on it landing as a hook
- Position: center screen, brief hold (1.5–2.5s is usually enough — don't let a
  giant number sit so long it starts to feel like a slide, not a video)
- Pair with a small supporting graphic (see below) roughly half the time — not
  every number needs a chart, but comparisons and multipliers almost always
  benefit from one

## Supporting graphics (generate_graphics.py)

Keep these as understated as the carousel infographics — thin lines, no drop
shadows, no gradients, no 3D. Three types cover almost everything:

- **`arrow_up` / `arrow_down`**: a single thin wine-red arrow, used when a number
  is framed as a rise or fall ("prices went up," "that dropped to..."). Don't
  pair with stats that aren't directional — an arrow next to "$240" with no
  before/after implied is confusing, not clarifying.
- **`bar_compare`**: two horizontal bars, one short (light stone), one long
  (wine-red), same visual language as the carousel bar charts. Use for any
  "X vs Y" or "only a fraction of" moment — this is usually the single most
  effective graphic in the whole video because the disproportion is visible,
  not just stated.
- **`bubble_stat`**: a thin circular or pill outline around a number, used
  sparingly (roughly once per video) to mark the number the whole story hinges
  on — the "if you remember one number from this" moment.

Graphics should appear via a hard cut or very quick fade (≤150ms) synced exactly
to the moment the number is spoken — a slow fade-in on a graphic that's meant to
land with a spoken beat will feel out of sync even if the video timing is
technically correct.

## Instagram Reels safe zones (1080×1920 frame)

Instagram's own UI sits on top of the video and will cover anything placed
in these zones — check every custom graphic's `x`/`y` against these, since
graphics use raw pixel coordinates (unlike ASS captions, which already
account for this via their MarginV defaults):

- **Top:** avoid the top ~120px — occasionally used for a "Following/For You"
  ribbon.
- **Bottom:** avoid the bottom ~260px — this is where Instagram renders the
  caption, username, audio title, and (for the first couple of seconds) the
  "Original audio" disc.
- **Right edge:** avoid the right ~140px for anything below the vertical
  midpoint of the frame — this is the like/comment/share/save/more action
  column.

The caption styles in `generate_ass.py` already respect these via their
MarginV values (statement/hook sit at MarginV 300–320, well clear of the
260px bottom UI zone). When placing a custom graphic via `build_reel.py`'s
`x`/`y` fields, keep `y` above `1660` (1920 − 260) if it needs to clear the
bottom UI, and keep `x + graphic_width` under `940` (1080 − 140) if it
extends into the lower two-thirds of the frame.

## Caption mode ↔ editorial function

See `references/editorial-principles.md` for the full reasoning behind when
to use each mode and how it maps to retention/pacing decisions — this file
covers the *what* (exact values), that file covers the *when and why*.

## Pacing rules

- No single caption on screen for less than ~0.8s (unreadable) or more than
  ~3.5s (starts to feel static, defeats the point of a "video" caption system).
- Break sentences over ~10 words into two or more phrase-chunks.
- Leave a beat of empty caption space (0.2–0.4s) between phrase-chunks even
  within the same sentence — a clean cut reads as intentional, a caption that
  changes mid-syllable reads as broken.
