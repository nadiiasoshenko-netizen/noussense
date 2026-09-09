# The Content Dept. — Design System

Editorial, moody-luxe design language for a content strategy studio. Built from three
Instagram moodboard grids: dark espresso backdrops, wine-red and dusty-blue paper
accents, high-contrast serif headlines, and tactile "studio desk" objects — polaroids,
wax seals, sticky notes, binder clips.

## 1. Principles

- **Editorial contrast.** Warm near-black is the anchor, cream is the relief. Wine
  and dusty blue are used sparingly, as punctuation, never as the dominant color.
- **Type as texture.** Large serif headlines carry the same visual weight as a
  photograph — they're a graphic element, not just a label sitting above content.
- **Grid as gallery.** Content lives in an even 3-across grid, the way a moodboard
  or an Instagram profile does. Cards mix photography, typographic statements, and
  physical objects so the grid feels curated, not templated.
- **Restraint on ornament.** Corners are square except where an object is
  physically a photograph (polaroids, pinned notes). Shadows are soft and reserved
  for things that are "lifted" off the page. No gradients, no glow.

## 2. Color

| Token | Hex | Use |
|---|---|---|
| `--ink` | `#1C130E` | Primary dark background (espresso/near-black), primary body text on light |
| `--black` | `#C9B48C` | The one lighter card in the grid — a warm beige, used in place of true black to break the ink/black rhythm on purpose |
| `--cream` | `#F1EAE0` | Primary light background (paper), reversed text on dark |
| `--paper` | `#FBF8F3` | Card surfaces, lightest neutral |
| `--wine` | `#6B2430` | Primary accent — seals, tags, one card per grid, links |
| `--wine-deep` | `#4E1A22` | Wine hover/pressed state, deep card backgrounds |
| `--dust-blue` | `#ACB9C6` | Secondary accent — notebook/paper moments, cool contrast to wine |
| `--sand` | `#C7B8A3` | Warm neutral — photography backdrops, muted mid-tone fills |
| `--line` | `#D9D0C2` | Hairline dividers and borders on light surfaces |

Everything else stays as the original espresso/cream/wine base — only the true-black
token (`--black`, formerly `#0B0B0B`) has been swapped for a warm beige. It still
plays its original role (the one card per grid that isn't ink, cream, or an
accent color), it's just beige now instead of black.

Rule of thumb: every grid or page should read as ink/cream first, with **one**
wine moment and, optionally, **one** dust-blue moment. Never split accent usage
evenly — that flattens the hierarchy the moodboards establish.

## 3. Typography

Two working families, one accent script used sparingly.

| Role | Family | Notes |
|---|---|---|
| Display / headline | **Playfair Display** | High-contrast serif. Set big, set tight (line-height 0.95–1.05). Regular weight for most headlines, italic reserved for the script-style accent moments ("Getting Inspired", "subdue"). |
| Body / UI / labels | **Inter** | Workhorse sans. Small sizes get wide tracking (labels, eyebrows, buttons); body copy sits at normal tracking. |
| Handwritten accent | **Caveat** | Used only for "sticky note" style asides — a reminder, a marginal comment. Never for headlines or body copy. |

### Scale

| Token | Size / Line-height | Use |
|---|---|---|
| `display-xl` | 64px / 0.95 | Cover-card statements ("The way she knows") |
| `display-lg` | 44px / 1.0 | Section headlines |
| `display-md` | 30px / 1.05 | Card headlines |
| `label` | 12px / 1.4, tracking 0.14em, uppercase | Eyebrows, tags, "BRAND NAME" style marks |
| `body-lg` | 17px / 1.55 | Lede paragraphs |
| `body` | 15px / 1.6 | Standard copy |
| `caption` | 13px / 1.4 | Captions, meta, URLs |

## 4. Spacing & Grid

- Base unit: **8px**. Common steps: 8 / 16 / 24 / 32 / 48 / 64 / 96.
- Layout grid: **3 columns, no gutter** for the moodboard/gallery view (cards
  touch edge-to-edge, like a photo grid); **12-column, 24px gutter** for standard
  page layouts.
- Card padding: 32–48px on dark/photo cards, 24–32px on compact utility cards
  (tags, buttons).

## 5. Components

- **Cover card** — full-bleed dark background, centered or left-aligned wordmark,
  small caption line beneath. Used to open a series.
- **Statement card** — cream or dark background, one large serif headline,
  nothing else. Headline *is* the content.
- **Photo card** — full-bleed photography, optional label pill top-left,
  optional caption strip at the base.
- **Quote / pull card** — small note card (often on a contrasting paper color),
  attached to a photo with a binder clip, holding a short italic line.
- **Sticky note** — cream or white square, hand-written accent line, torn or
  clipped edge; sits on top of a photo, slightly rotated.
- **Polaroid stack** — two or three white-bordered photo tiles, casually
  overlapping, slight rotation.
- **Tag / eyebrow label** — uppercase, wide tracking, 12px, no background or a
  hairline border; marks a category ("TODAY'S NEWS", "BEHIND THE SCENES").
- **Wax seal mark** — circular emblem in wine, used as a brand seal or divider.
- **Button** — text-only or hairline-bordered, uppercase label, no fill unless
  it's the single primary action on a dark card (then: cream fill, ink text).

## 6. Photography direction

Muted, low-contrast studio photography: black tailoring, taupe and cream
backdrops, natural light. Hands, gesture, and cropped-body compositions
(no full faces required) read as more editorial than posed portraits.
Avoid saturated color in photography — let the wine/blue accents carry color
instead.

## 7. Voice

Short, declarative headline fragments ("Structured. Scaleable. Smart.");
lowercase or sentence-case for intimacy ("the algorithm explained"), full
capitals reserved for small system labels, not headlines. Body copy is
confident and brief — one or two short sentences per card, never a wall
of text.
