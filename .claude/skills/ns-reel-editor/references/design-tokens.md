# Nous Sense — Reel Caption Design Tokens

This is the single source of truth for colors, type, and style-mode rules used by
`scripts/generate_ass.py` and `scripts/generate_graphics.py`. If the brand system
changes, update this file first — the scripts read their defaults from here (or
mirror these exact values if hardcoded).

**This is the locked Nous Sense visual identity** (`Nous Sense/13 - NS Website
Visual Identity.md`), applied brand-wide — carousels, Reels, and the website all
share one system now. It supersedes the earlier ink/cream/wine/Playfair system.

## Colors (RGB hex → ASS BGR)

ASS subtitle colors use `&HAABBGGRR` (alpha, blue, green, red — reverse byte order
from normal hex). Get this wrong and colors render subtly off, so the conversion
is spelled out here rather than left to memory:

| Name | Hex (RGB) | ASS (&HAABBGGRR) | Use |
|---|---|---|---|
| White | `#ffffff` | `&H00FFFFFF` | Page/canvas ground itself |
| Paper | `#f5f0e6` | `&H00E6F0F5` | Light backgrounds, text on dark bg |
| Stone | `#e9dcbf` | `&H00BFDCE9` | Secondary light surface, muted bar-chart baseline segments |
| Plaster (Pale Clay) | `#d2c0a3` | `&H00A3C0D2` | The one accent panel per composition (primary) |
| Sand | `#c9b79c` | `&H009CB7C9` | Swappable alternate accent panel; kicker text on dark footage |
| Grey | `#8a7f6b` | `&H006B7F8A` | Muted / secondary text, kicker text on light footage |
| Espresso | `#201810` | `&H00101820` | The ONE deliberate dark moment per composition — hooks, emphasis, stat numbers when the number itself is the "hook" |

**The 80/20 rule:** any given composition (a whole carousel slide, a reel's full
frame at a given moment) should read as roughly 80% light (White/Paper/Stone/
Plaster/Sand) to 20% Espresso, used once, deliberately. This is the system's one
"loud" moment — it is color, not typography. There is no separate saturated
accent color (no wine, no "ember" amber — both were tried on the website and
dropped); Espresso itself, used sparingly, is the emphasis mechanism.

## Typography

Two families only, per the locked system:

- **Inter** — does everything: body copy, small tracked labels/kickers,
  statement and stat text, and the wordmark. Drop `Inter-Regular.ttf`,
  `Inter-Medium.ttf`, `Inter-SemiBold.ttf`, `Inter-Bold.ttf` into
  `assets/fonts/` for an exact match — download from Google Fonts if the
  environment has network access. If absent, the scripts fall back to
  **DejaVu Sans**, which is close enough not to look broken, but flag this
  to the user once so they know to add the real fonts later.
- **Schibsted Grotesk** — held in reserve, with exactly one job: whatever
  sits inside the Espresso "band" moment — in a reel, that's the `hook` and
  `stat_hook` (number-is-the-hook) styles. Not used anywhere else. Drop
  `SchibstedGrotesk-Bold.ttf` into `assets/fonts/` if available; without it,
  hook/stat_hook fall back to Inter Bold, which still reads as the loud
  moment via the Espresso box (below) even without the exact typeface.
- Kicker text renders as a **bracketed micro-label** — `[ QUICK CONTEXT ]` —
  the locked structural device, not plain uppercase alone (handled
  automatically by `generate_ass.py`). Actual uppercase characters, not
  CSS-style small-caps (ASS doesn't reliably support that), bold,
  letter-spaced (`\fsp4` or higher in ASS tags).

## The four caption modes

Every spoken line gets classified into exactly one of these. Mixing modes across
consecutive beats is what makes the video feel designed instead of like a plain
subtitle track — never let more than two consecutive beats share a mode.

### 1. `kicker`
Short (2–5 word) section labels — spoken transitions like "quick context," "here's
the turn," "so here's the lesson." Not every sentence needs one; use at natural
section boundaries, roughly once per 3–5 statement beats.
- Font: Inter Bold, small size (~34px at 1080×1920), letter-spaced
- Displayed as a bracketed micro-label: `[ QUICK CONTEXT ]`
- Color: Sand on dark footage, Grey on light footage (contrast check matters
  more than rigid color assignment here)
- Position: top-left, matching the carousel kicker convention
- Motion: simple fade in/out, no scale or slide — kickers are quiet, not loud

### 2. `statement`
The default mode. Regular explanatory sentences — the connective tissue of the
script.
- Font: Inter Regular/Medium, mid-large size (~60–66px)
- Color: Paper on dark footage, Espresso on light footage
- Position: lower-third, centered
- Motion: phrase-by-phrase reveal (break sentences into 3–6 word chunks that pop
  in sequentially rather than the whole sentence appearing at once) — this is the
  single biggest thing that separates "designed caption" from "plain subtitle"

### 3. `hook`
The line in each beat designed to land — the quotable insight, the turn, the
punchline. There's usually exactly one hook per beat/section, not one per
sentence. This is the reel's Espresso band moment.
- Font: Schibsted Grotesk Bold (Inter Bold fallback), larger than statement
  (~68px)
- Treatment: a solid Espresso box (opaque background, not just colored text)
  with Paper text — background-independent by design, always, the one place
  the "loud" moment appears in running text, which is exactly why it reads
  as emphasis regardless of what footage is behind it
- Position: centered, slightly larger vertical margin so it feels like a "moment"
- Motion: fade in with a touch more hold time than statement beats — let it sit

### 4. `stat`
Any spoken number, price, percentage, or quantity worth seeing, not just hearing.
- Font: Inter, very large (~150px), the same scale used for the
  giant-number carousel slides
- Color: Paper on dark footage, Espresso on light footage — UNLESS the number
  itself is the emotional turn (e.g., "$60 million"), in which case use the
  same Espresso-box/Schibsted-Grotesk treatment as `hook` to double down on
  it landing as the video's one loud moment
- Position: center screen, brief hold (1.5–2.5s is usually enough — don't let a
  giant number sit so long it starts to feel like a slide, not a video)
- Pair with a small supporting graphic (see below) roughly half the time — not
  every number needs a chart, but comparisons and multipliers almost always
  benefit from one

## Supporting graphics (generate_graphics.py)

Keep these as understated as the carousel infographics — thin lines, no drop
shadows, no gradients, no 3D. Three types cover almost everything:

- **`arrow_up` / `arrow_down`**: a single thin arrow in this video's emphasis
  color (Paper on dark footage, Espresso on light footage), used when a number
  is framed as a rise or fall ("prices went up," "that dropped to..."). Don't
  pair with stats that aren't directional — an arrow next to "$240" with no
  before/after implied is confusing, not clarifying.
- **`bar_compare`**: two horizontal bars, one short (Stone), one long (this
  video's emphasis color), same visual language as the carousel bar charts.
  Use for any "X vs Y" or "only a fraction of" moment — this is usually the
  single most effective graphic in the whole video because the disproportion
  is visible, not just stated.
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
