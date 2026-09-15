---
name: ns-reel-editor
description: Edit uploaded Instagram Reels footage for Nous Sense — trimming dead air/weak sections, adding dynamic on-brand animated captions, and inserting big-number and infographic moments (comparison bars, directional arrows). Use this skill whenever the user uploads a video of themselves speaking and wants it turned into a finished reel, wants captions added or the video "trimmed where necessary," wants text that "isn't just plain subtitles," wants numbers/stats visually emphasized, or references Nous Sense's brand colors (wine-red, cream, espresso, taupe) or retention/hook principles in the context of editing a video. This is an EDITING skill for footage that already exists — it does not source B-roll, generate video from scratch, run trend research, or produce thumbnails/music selection.
---

# NS Reel Editor

Takes footage the user has already filmed and turns it into a finished,
on-brand Instagram Reel: trim what's not earning its place, add animated
captions in Nous Sense's exact visual language, and land the numbers
that matter as designed infographic moments instead of things that are only
spoken. It's built to feel like a designed motion graphic — not auto-generated
subtitles with a color swap, and not a generic template.

**This skill is scoped to editing existing footage.** It doesn't source
B-roll, generate new video, do outlier/trend research, pick music, or design
thumbnails — if the user wants any of that, it's a different, bigger job
than what this skill covers. Say so rather than quietly attempting it.

## Why this exists (read before making any edit)

The single biggest failure mode is producing something that looks like
plain captions with a brand color applied. Everything below exists to
prevent that — don't skip steps because a flatter version would render
faster:

1. **Trim before captioning, always.** A weak opening, dead air, or a
   redundant restatement doesn't get fixed by adding good captions on top
   of it — it needs to be cut. See `references/editorial-principles.md`
   for what's worth cutting and why. If trimming is happening at all, do
   it first and author every caption timestamp against the *trimmed*
   output, never the original footage.
2. **Mode variety, not one caption style repeated.** Every line gets
   classified into one of four modes (kicker / statement / hook / stat),
   each genuinely different in font, color, and position — not just a
   color change. Never let more than two consecutive beats share a mode.
3. **Phrase-by-phrase reveal**, not whole sentences sitting on screen for
   their full duration — the single biggest thing that separates a
   designed caption from a subtitle track. Handled automatically as long
   as beats are authored as natural sentences, not pre-chunked.
4. **Numbers that matter get a visual, not just a mention.** A comparison,
   a multiplier, or the one number the whole story hinges on should get a
   synced bar-compare, arrow, or bubble callout — timed to the exact
   moment it's spoken.

## Workflow

### Step 1: Watch the raw footage and find the hook

Before cutting anything, identify: where's the line that would make a
stranger stop scrolling? Usually a question or a contradiction, not a
statement of the lesson. See `references/editorial-principles.md` for what
strong vs. weak hook material sounds like. If the strongest line isn't near
the start, that's a trim decision, not a captioning problem.

### Step 2: Decide what to trim (if anything)

Run `scripts/trim_reel.py detect --video <raw.mp4>` to surface candidate
silence/dead-air windows — treat these as hints, not decisions; a pause for
emphasis isn't the same as dead air, so check what's actually being said
around each candidate before cutting it. Apply the "boring test" from
`references/editorial-principles.md`: cut dead air, slow openings, restated
points, and weak endings.

Once the keep-segments are decided (as `[start, end]` pairs in the
*original* footage's timeline):

```bash
python3 scripts/trim_reel.py cut --video raw.mp4 \
  --keep '[[0,4.2],[6.8,22.1],[24.0,41.5]]' \
  --output trimmed.mp4
```

If nothing needs trimming, skip this step and work directly with the
original file — don't trim for the sake of it.

### Step 3: Turn the (trimmed) script into `beats.json`

Working against the trimmed video's timeline from here on, get precise
timing from the actual recording where possible — if the environment has
network access, transcribe the audio with word-level timestamps (e.g.
`openai-whisper` or `faster-whisper`) and align it against the known
script, since people pause and ad-lib differently than a read-through
suggests. Otherwise use the user's rough per-beat timestamps.

For each beat, decide:
- **mode** (`kicker` / `statement` / `hook` / `stat`) — see the table in
  `references/editorial-principles.md`
- **background** (`"dark"` or `"light"`) — based on the actual footage
  behind that beat, controls text color for legibility
- **graphic** (optional, on `stat` beats only) — attach only when the
  number is a comparison, a rise/fall, or the single most important number
  in the video; see `scripts/build_reel.py`'s docstring for the exact
  field schema per graphic type

Write real sentences for `text` — the chunking logic in `generate_ass.py`
handles breaking them into phrase-chunks automatically. Don't pre-split
sentences in the JSON.

### Step 4: Render

```bash
python3 scripts/build_reel.py --video trimmed.mp4 --beats beats.json --output final.mp4
```

Generates the styled `.ass` captions, generates any graphic PNGs the
timeline calls for, and composites everything in one ffmpeg pass, keeping
the original audio. Assumes a 1080×1920 vertical frame throughout — the
script warns if the input isn't already that size.

### Step 5: QA pass before calling it done

Pull frames at each beat boundary (`ffmpeg -ss <t> -frames:v 1 frame.png`)
and actually look at them. Run through the quick checklist at the end of
`references/editorial-principles.md`: first-frame test, silent test,
safe-zone check (nothing sitting under Instagram's own UI — see the safe
zone table in `references/design-tokens.md`), and mode-variety check. Fix
anything that fails before delivering — cheap to catch now, expensive once
published.

## Fonts

The exact brand serif (Playfair Display) and sans (Inter) aren't bundled —
drop the real font files into `assets/fonts/` if there's network access to
fetch them from Google Fonts (see `assets/fonts/README.md` for exact
filenames). Without them, everything falls back to DejaVu Serif/Sans
automatically with a printed note — layout and color are still correct,
just not a pixel-perfect type match until the real fonts are added.

## Reference

- `references/editorial-principles.md` — hook selection, what's worth
  trimming, caption-mode-to-editorial-function mapping, and the pre-delivery
  QA checklist. Read this before making trim or mode-classification
  decisions.
- `references/design-tokens.md` — exact colors, type, per-mode styling, and
  Instagram safe-zone pixel values. Read this before writing beats.json or
  placing a custom graphic for the first time in a session.
- `scripts/trim_reel.py` — `detect` (candidate cut points) and `cut`
  (concatenate keep-segments) subcommands.
- `scripts/generate_ass.py` — caption engine; full beats.json schema in its
  docstring.
- `scripts/generate_graphics.py` — graphic overlay generator (arrows, bar
  comparisons, bubble stat); runnable standalone for quick previews.
- `scripts/build_reel.py` — the main orchestrator; run this one directly
  for the final render.
