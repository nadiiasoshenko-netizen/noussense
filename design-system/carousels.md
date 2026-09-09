# Instagram Carousels — Build Guidelines

Applies `design-system.md` to Instagram carousel posts. Read that file first
for the full token set, type scale, and component specs — this doc is the
format-specific layer on top of it.

## Canvas

- **1080 × 1350px** per slide (4:5 portrait, Instagram's native carousel
  ratio). Build each slide at these exact dimensions — don't scale up from a
  square canvas.
- **Safe margin: 72px** on all sides. Keep headlines and body copy inside it;
  Instagram's UI (profile row, caption, dots) crops close to the edges on
  mobile.
- **Slide count:** 5–8 is the sweet spot for this brand's voice. Don't pad to
  10 unless asked.

## Type scale on canvas

Runs larger than the desktop web scale in `design-system.md`:

| Role | Size |
|---|---|
| Cover statement | 64–84px |
| Supporting slide headline | 40–52px |
| Body copy | 22–26px |
| Labels / brand mark | 13–15px, uppercase, tracked |

## Brand mark

Small, consistent, same position on every slide — bottom-center or
bottom-left. Either "THE GROWTH EDIT" set in the label style, or the wax-seal
mark. Pick one per carousel and repeat it across the whole set; never mix.

## Color rhythm

Read as ink/cream first. Wine appears on exactly one slide type per carousel
(usually the cover or the CTA — never both unless it's a 3+ slide set).
Dust-blue and the beige `--black` card are optional seasoning, not defaults.
Alternate light and dark rather than clustering: cream → cream → dark accent
→ cream → dark accent.

## Standard slide types

Reuse these; don't invent new layouts unless content genuinely doesn't fit.

| Slide role | Background | Layout |
|---|---|---|
| **Cover / hook** | `--ink` or `--wine` | Large serif statement, centered or lower-third, brand mark small at the base. The one slide allowed to be the boldest color in the set. |
| **Statement** | `--cream` or `--paper` | One big serif headline, nothing else competing. Headline *is* the content. |
| **List / point** | `--paper` | Uppercase eyebrow label at top, short serif sub-headline, 2–4 short body lines. Numbers or short bullets, not paragraphs. |
| **Quote / testimonial** | `--sand` or `--dust-blue` | Pinned-note or sticky-note component holding one italic line, 15–20 words max. |
| **Data / stat** | `--cream` | One large number/stat in Playfair Display, one short line of context in Inter beneath. |
| **CTA / close** | `--wine` or `--ink` | Short directive line ("Save this for later.", "Follow for more."), brand mark, optional handle/URL at caption size. |

## Components available for reuse

Pull straight from `design-system.md` §5 rather than redesigning per
carousel: pinned quote card, sticky note, polaroid stack, eyebrow/tag label,
wax seal mark. Use at most one "studio object" component per slide.

## Build workflow (HTML → PNG)

1. Draft the slide sequence in words first — one line per slide with its role
   and copy. Confirm with the user before building if 6+ slides or copy isn't
   supplied yet.
2. Build one HTML file per slide (or one file with `.slide` sections sized
   `1080px × 1350px` each) using the tokens and type scale above.
3. Export to PNG at exact canvas size, 2x scale for crispness:
   ```bash
   npx playwright screenshot --viewport-size=1080,1350 slide-01.html slide-01.png
   ```
4. Name files sequentially: `slide-01.png`, `slide-02.png`, … so order is
   unambiguous on upload.
5. Sanity check slide 1 alone before batching the rest — confirm margins and
   type scale read correctly at actual size.

## Voice on-canvas

Short, declarative fragments over full sentences ("Structured. Scaleable.
Smart." not "Our approach is structured, scaleable, and smart.").
Sentence-case for intimacy on statement slides; uppercase reserved for small
labels only (brand mark, eyebrows). Full voice guidance: `design-system.md` §7.
