# Instagram Reels — Build Guidelines

Applies `design-system.md` to Instagram Reels. Read that file first for the
full token set, type scale, and component specs — this doc is the
format-specific layer on top of it: cover frame, on-screen text, and motion.

## Canvas

- **1080 × 1920px**, 9:16 vertical, 30fps minimum (matches Instagram's native
  Reels export — don't crop down from a square or landscape source).
- **Safe zone:** keep all text and key visual elements within a **940 ×
  1500px** centered area (roughly 70px side margins, 220px top, 200px
  bottom). Instagram's UI — profile name, caption line, like/comment/share
  rail, "..." menu — sits over the outer edges, especially the bottom-right
  rail and the bottom caption strip.
- **Cover frame** (the still shown on the grid and as the Reel's thumbnail)
  must work as a standalone image, same as a carousel cover slide: one
  serif statement or a title card, not a mid-motion freeze-frame. Design it
  first, as its own 1080 × 1920 frame, before storyboarding the motion.

## Type on-canvas

Slightly smaller than the carousel scale, since Reels text sits over moving
footage and needs more contrast/legibility margin:

| Role | Size | Notes |
|---|---|---|
| Cover / hook statement | 56–72px | Playfair Display, tight line-height (0.95–1.05) |
| In-video headline / beat | 36–48px | One line or two short lines max per beat — never a paragraph on screen |
| Body / caption overlay | 22–28px | Inter, short phrases, 6–8 words per line max |
| Labels / brand mark | 13–15px, uppercase, tracked | Same treatment as carousels |

Always set text on a **solid or near-solid card** (ink, cream, wine, sand, or
dust-blue block, per §2 color rhythm) rather than directly over busy footage
with no backing — the moodboards' contrast principle applies to video the
same way it does to print. A translucent ink or cream scrim (70–85% opacity)
behind text is acceptable when the shot needs to stay visible underneath.

## Color rhythm

Same rule as everywhere else in the system: ink/cream first, wine as the one
accent moment — usually the cover frame or the CTA end-card, not both. Don't
tint the whole video wine or dust-blue; use those as card/overlay colors for
text moments, not as color grades on the footage itself.

## Structure (beats, not scenes)

Reels for this brand read as a short stack of statement cards intercut with
footage, mirroring the carousel's slide logic rather than a conventional
edited video:

| Beat | Duration | Treatment |
|---|---|---|
| **Cover / hook** | 0–1.5s | Full-bleed statement card (ink or wine), same rules as a carousel cover. Must also stand alone as the thumbnail. |
| **Footage / demonstration** | bulk of runtime | Muted, low-contrast studio footage per `design-system.md` §6. Minimal on-screen text — a label or eyebrow at most, positioned in the safe zone. |
| **Beat cards** | 1–2s each, as needed | Full-frame or lower-third statement cards dropped between footage clips to punctuate a point — same visual language as a carousel "statement" slide. |
| **CTA / close** | last 1–2s | Wine or ink card, short directive line, brand mark. Same content as a carousel's CTA slide. |

Keep total runtime tight — 7–15 seconds is typical for this brand's
declarative voice; don't pad. Favor a few strong beat cards over constant
on-screen text.

## Components available for reuse

Same set as carousels — pull from `design-system.md` §5, don't redesign:
sticky note (works well as a quick "reminder" beat card, held 1–2s), pinned
quote card (for a testimonial beat), polaroid stack (as a static cover or
closing frame), eyebrow/tag label (lower-third, footage beats), wax seal
mark (closing brand moment). One studio object per beat, same restraint rule
as print.

## Audio & captions

- Native on-screen text (per the beats above) should carry the message even
  muted — Reels are frequently watched without sound.
- If burned-in captions are used over footage (not the beat cards), set them
  in Inter, not Playfair — captions are UI, not headline.
- Voiceover/dialogue, if present, stays short and declarative, matching the
  written voice in `design-system.md` §7.

## Build workflow

1. Storyboard beats in words first — one line per beat (role, duration,
   copy), same as the carousel slide-sequence step. Confirm with the user
   before producing anything if the Reel runs 6+ beats or footage isn't
   sourced yet.
2. Build each **card beat** (cover, statement cards, CTA) as its own HTML
   frame at 1080 × 1920px, using the tokens and type scale above — same
   HTML → PNG export approach as carousels:
   ```bash
   npx playwright screenshot --viewport-size=1080,1920 cover.html cover.png
   ```
3. Hand off card PNGs plus footage clips to whatever video assembly tool is
   in use (CapCut, Premiere, Reels' native editor) for the cut — this design
   system governs the look of every static/text frame, not the video
   assembly itself.
4. Always render and check the **cover frame** on its own first — it's the
   most-seen asset (grid thumbnail) and must read correctly as a still.

## Voice on-screen

Same as carousels: short, declarative fragments, sentence-case for
intimacy, uppercase reserved for labels only. Full guidance in
`design-system.md` §7.
