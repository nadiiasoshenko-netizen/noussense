---
name: nous-sense-carousels
description: Design and build Instagram carousel slides for Nous Sense using its locked visual identity (White/Paper/Stone/Plaster/Sand/Grey/Espresso, Inter throughout, the 80/20 Espresso-moment rule). Use this skill whenever the user asks to create, design, draft, or export Instagram carousel slides, posts, story graphics, or any social content for "Nous Sense," or mentions carousel slides / IG posts alongside this brand's look. Also use it if the user asks to reuse "the design system," "the moodboard style," or "the brand colors" for social content, even without naming the project. Covers slide layout conventions, on-brand components, growth-format slide templates (result/list/tool-drop), and the HTML → PNG export workflow.
---

# Nous Sense — Instagram Carousel Skill

Builds on-brand Instagram carousel slides for **Nous Sense** using the studio's
editorial design system (see `references/design-system.md` for the full token set —
read it before building anything if you need exact hex values, type scale, or
component specs beyond the summary below).

Use this skill for any request to design, draft, mock up, or export carousel
slides, single posts, or story graphics for this brand. If the user just wants
copy/caption writing with no visual, this skill isn't needed — jump straight to
writing.

## 1. Design tokens (quick reference)

This is the locked Nous Sense visual identity (`Nous Sense/13 - NS Website
Visual Identity.md`), applied brand-wide — the same system as the website
and Reels, not a separate carousel-only palette.

```css
--white:     #FFFFFF;  /* page ground itself */
--paper:     #F5F0E6;  /* card / section surface, sits on white */
--stone:     #E9DCBF;  /* secondary card / section surface */
--plaster:   #D2C0A3;  /* the ONE accent panel per composition (primary) */
--sand:      #C9B79C;  /* swappable alternate for the accent panel */
--grey:      #8A7F6B;  /* muted / secondary text */
--espresso:  #201810;  /* the ONE deliberate dark moment per composition */
```

- **Fonts:** Inter does everything — headlines, body, labels, and the
  wordmark itself (700 weight, ~0.32em letter-spacing, uppercase, for the
  quiet "NOUS SENSE" wordmark device). Schibsted Grotesk is held in reserve
  for exactly one job: whatever copy sits inside the Espresso band (see
  below) — not used anywhere else. No serif, no handwritten face.
- **The 80/20 rule:** every slide should read as roughly 80% light
  (White/Paper/Stone/Plaster/Sand) to 20% Espresso, used once, deliberately
  — usually the cover or the CTA (never both unless it's a 3+ slide set).
  This is the system's one "loud" moment; it's color, not typography.
  Plaster and Sand are optional seasoning (an accent panel, a card surface),
  not defaults — don't force them into every carousel.

## 2. Carousel specs

- **Canvas:** 1080 × 1350px per slide (4:5 portrait — Instagram's native
  carousel ratio). Build each slide as its own HTML page at these exact
  dimensions; don't scale up from square.
- **Safe margin:** 72px on all sides. Keep headlines and body text inside this
  margin — Instagram's UI (profile row, caption, dots) crops close to the
  edges on mobile.
- **Slide count:** for general editorial/statement carousels (single big
  ideas, quotes, brand voice pieces), 5–8 slides suits this brand's short,
  declarative-fragment voice (see design-system.md §7). For **growth/
  performance carousels** (see §7 below — result, list, tool-drop formats),
  default to **8 slides**, with an `extended: true` option pushing to 9–10.
  2026 performance data shows 8–10 slide carousels consistently out-save and
  out-engage shorter ones, with list/framework formats saving best at 7–8+
  slides. Don't pad length just to hit a number — every extra slide needs its
  own job (a second proof point, an extra list item, an objection-handling
  FAQ), never filler.
- **Slide 1 carries the weight:** the hook slide accounts for roughly 80% of
  a carousel's total engagement (2026 data). It earns 80% of the design
  effort too — spend the most iteration there, on every format.
- **Type scale on canvas:** headlines run larger than the desktop web scale —
  start around 64–84px for a cover statement, 40–52px for supporting slide
  headlines, 22–26px for body copy, 13–15px uppercase/tracked for labels and
  the brand mark.
- **Brand mark:** small, consistent, same position every slide (bottom-center
  or bottom-left, per the moodboard reference) — either the quiet "NOUS SENSE"
  wordmark (Inter 700, ~0.32em tracking, uppercase), or the Sealed Ring mark
  component. Pick one and repeat it across the whole set; never mix.

## 3. Standard slide types

Reuse these — don't invent new layouts per carousel unless the content
genuinely doesn't fit. (For growth/performance carousels, prefer the format
templates in §7 instead — they sequence these same slide types into
higher-saving structures.)

| Slide role | Background | Layout |
|---|---|---|
| **Cover / hook** | `--espresso` (this slide is the composition's 20%) | Large Inter 700 statement — or the quiet wordmark sized up — centered or lower-third, brand mark small at the base. This is the one slide that's allowed to be the loud moment in the set. |
| **Statement** | `--white` or `--paper` | One big headline in Inter, nothing else competing. Headline *is* the content — resist adding a paragraph under it. |
| **List / point** | `--paper` | Small bracketed micro-label (`[ Eyebrow ]`) at top, short Inter sub-headline, 2–4 short body lines below. Numbers or short bullets, not paragraphs. |
| **Quote / testimonial** | `--stone` or `--plaster` | Pinned-note component (see §5) holding one italic-set line, 15–20 words max. |
| **Data / stat / receipt** | `--paper` | One large number set in Inter, one short line of context beneath. For a claimed result (money, time, count), style it as the "receipt" component (§5) so the number reads as substantiated, not asserted. |
| **CTA / close** | `--espresso` | Short directive line ("Save this for later.", "Follow for more."), brand mark, optional handle/URL in caption size — set in Schibsted Grotesk, the one place that face appears. On growth carousels, this slide must **bookend** slide 1 — see §7. |

Alternate light and dark slides through the set (paper → paper → the one
Espresso moment → paper → paper) rather than clustering dark slides together
or repeating the loud moment more than once per composition — the 80/20 rule
holds across the whole set, not just per slide.

## 4. Build workflow (HTML → PNG)

1. **Draft the slide sequence in words first** — one line per slide describing
   its role (from the table above, or the chosen §7 format) and its copy.
   Confirm with the user before building if the carousel is long (6+ slides)
   or the copy isn't supplied yet.
2. **Build one HTML file per slide** (or one HTML file with `.slide` sections
   sized `1080px × 1350px` each, whichever is easier to export) using the
   tokens in §1. Reuse `/mnt/skills/public/frontend-design/SKILL.md` guidance
   for layout polish if it's available in this environment.
3. **Export to PNG** at the exact canvas size, 2x scale for crispness. In
   Claude Code, the simplest path is a headless-browser screenshot script:

   ```bash
   npx playwright screenshot --viewport-size=1080,1350 slide-01.html slide-01.png
   ```

   or, if Playwright/Puppeteer isn't available, a Python approach with
   `playwright` or `selenium` works the same way. Whichever tool is already
   in the project, use it — don't add a new dependency for a one-off export
   if an equivalent tool exists.
4. **Name files sequentially**: `slide-01.png`, `slide-02.png`, … so the
   carousel order is unambiguous on upload.
5. **Sanity check before exporting the full set**: render slide 1 alone,
   confirm the margins/type scale read correctly at actual size, then batch
   the rest.

## 5. Components available for reuse

Pull these directly from the existing design system (full CSS in
`references/design-system.md` §5) rather than redesigning them per carousel:

- Pinned quote card (photo + clipped note, on Stone or Plaster paper)
- Polaroid stack (two overlapping white-bordered tiles)
- Bracketed micro-label (`[ Eyebrow ]` — square-bracket tracked caps,
  replaces plain eyebrow labels)
- Sealed Ring mark (double concentric ring, seven dots around the inner rim
  — one per Commercial Sense — serif "N" centered, drawn in Espresso)
- **Receipt** (screenshot/number-hero styling): a bordered "document" card —
  paper background, thin hairline rule, a monospace or tabular-figure number
  set large in Inter, one small caption line beneath it (source or
  timeframe, e.g. "across 6 weeks"). Use it any time a slide asserts a
  specific number — money saved, hours saved, output count — so the claim
  reads as evidenced rather than just stated. This is required for the
  hero-number slide in the RESULT format and the "after" slide in TOOL DROP
  (§7).

Use at most one "studio object" component per slide — they're accents, and
the moodboards never stack more than one per frame.

## 6. Voice on-canvas

Short, declarative fragments, not full sentences where a fragment will do
("Structured. Scaleable. Smart." not "Our approach is structured, scaleable,
and smart."). Sentence-case for intimacy on statement slides, uppercase
reserved for small labels only (brand mark, eyebrows) — see
design-system.md §7 for the full voice guidance.

## 7. Growth-format slide templates (2026 performance data)

For carousels meant to drive saves, shares, and DM/comment conversions
(as opposed to a pure editorial/statement piece), pick one of three formats
via a `format` choice: **`result`**, **`list`**, or **`tool_drop`**. All three
share the same underlying logic, in order of design priority: hook (most
effort) → contrast/before-after → specific, substantiated proof → identity or
urgency bridge (no price, ever — community/member count only) → single-
keyword CTA.

Shared rules across all three formats:

- **Word caps, enforced per slide:** hook and CTA slides ≤12 words; general
  body slides ≤15–20 words; list-item slides ≤5 words per headline. If a
  draft runs over, cut copy — don't shrink the type to fit it.
- **Bookend the CTA to the hook.** The CTA slide must reuse the exact same
  background and type treatment as slide 1 (e.g. both `--espresso` with the
  same headline weight), so the set opens and closes as one visual statement
  rather than shifting into a jarring "ad" slide at the end. Pull both from
  the same token pair automatically — never let CTA styling drift from the
  locked system, and never spend the composition's one Espresso moment
  twice on different slides within the same carousel.
- **Single-keyword CTA + DM automation.** One comment keyword, not a
  multi-ask CTA ("comment X" beats "comment X, follow, and share"). Note in
  the caption/copy handoff that the keyword is wired to DM automation.
- **No pricing on the bridge slide, ever.** The identity/urgency slide before
  the CTA uses a community or member count field only ("Join 4,200+ founders
  building this way") — never a price or offer detail.
- **Numbers need receipts.** Any slide making a specific, attributable
  numeric claim (money saved, hours saved, output count) uses the Receipt
  component (§5), both for on-brand polish and because unsubstantiated
  numeric result claims invite FTC scrutiny — the visual should read as
  evidence, not just a bold assertion.
- **Length:** default 8 slides. Extend to 9–10 only via an explicit
  `extended: true` flag (or when the content genuinely doesn't compress —
  e.g. a list with 5+ items) — never hardcode to exactly 8 if the format
  below calls for a flex slide.

### Format: `result` (case study)

8 slides, +1–2 optional.

1. **Hook** — Cold open on the *result*, not the tool/method. Bold headline,
   high color contrast (`--espresso`). ≤12 words.
   e.g. "She cancelled her $500/month contractor."
2. **The win** — Literal split-screen layout: before | after, one line of
   copy on each side, plus a caption strip stating who + how fast. Build this
   as an actual two-column visual split, not just paired copy.
3. **Before state** — The manual pain, in concrete specifics only (name the
   tool, the hours/week, the dollar cost). ≤20 words.
4. **First move** — The plain-English ask, styled as a quoted prompt/chat
   bubble component, not a prose paragraph.
5. **What shipped** — Name the exact output; use a screenshot- or
   receipt-styled visual, not an abstract icon.
6. **The number** — One hero number, full-bleed, using the Receipt component
   (§5). Time saved, money saved, or output count — a real, attributable
   figure. This is the slide designed to be saved and screenshotted, so give
   it the same design weight as the hook.
7. **Bridge** — Identity/urgency framing ("if this is you—"), community/
   member count only, no price.
8. **CTA** — Single comment keyword → DM automation. Bookends slide 1
   exactly (same background/accent + type treatment).

*Optional 9–10:* a second proof slide — an FAQ objection or a second, smaller
result. Use it to push into the 8–10 slide range that correlates with higher
save rates, without diluting the hook.

### Format: `list`

8 slides, expandable to 9–10 by adding items.

1. **Hook** — Lead with the count. ≤10 words.
2. **Combined outcome** — What having *all* the items unlocks together,
   stated as one outcome — not a recap/preview of the list itself.
3–7. **One item per slide** — ≤5 words headline + one supporting visual or
   icon per slide. Specific beats clever; name the real thing, not a
   metaphor for it.
8. **Bridge** — identity or urgency framing, community count only, no price.
9. **CTA** — single keyword, bookend styling with slide 1.

*Note:* if the list naturally runs 5+ items, extend to 9–10 slides (one item
per slide, unchanged) rather than compressing multiple items onto one slide —
list/framework carousels are the highest-saving format type at 7–8+ slides,
so length here is an asset, not something to trim.

### Format: `tool_drop`

8 slides.

1. **Hook** — Lead with the *builder outcome*, not the tool name or a
   feature list. e.g. "Built a tool that turns messy notes into a
   client-ready deck."
2. **The tool** — Name it once, one plain-English line on what it does.
3. **Who it's for** — Identity-marker slide ("if you're a ___ who ___") —
   this is the slide that drives saves from the right audience, so make the
   identity specific.
4. **Before** — The manual/painful version of this workflow, in concrete
   terms.
5. **After** — What changed, shown as a demo/output visual using the Receipt
   component (§5) — not described in prose.
6. **One feature, specific** — Pick the single most impressive capability.
   ≤5 words headline + visual.
7. **Bridge** — Access/urgency framing, community count only, no price.
8. **CTA** — Single keyword, bookend styling with slide 1.

## Reference

`references/design-system.md` — the complete token set, type scale, spacing
system, and component CSS this skill draws from. Read it when you need exact
values or are building a component not summarized above.
