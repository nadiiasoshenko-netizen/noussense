# The Growth Edit — Editorial Principles for Editing Uploaded Footage

This distills The Growth Edit's Reel Editor philosophy down to the parts that
apply when the raw material is **already filmed** — someone's uploaded a
talking-head video and the job is to trim it, caption it, and add
big-number/infographic moments. It deliberately leaves out everything about
sourcing B-roll, trend research, thumbnail design, and music selection —
those are real parts of full production but out of scope for this skill.

Read this before making trim decisions or choosing which lines become which
caption mode — the two decisions are related and both come from the same
underlying goal: **retention**, not polish.

## The core reframe

A technically clean edit with weak retention is still a failed edit. Every
decision below — what to cut, what becomes a hook, when a number gets its
own big-text moment — should be justified by "does this keep someone
watching," not "does this look nice."

## What "the hook" means for a talking-head video

Somewhere in the raw footage, the speaker says the line that's designed to
make a stranger stop scrolling — usually a question or a contradiction, not
a business-lesson statement. Find it before deciding anything else:

- **Good hook material:** "Why does this cost 10 times more?" / "This is
  the same drink." / a specific, surprising number said early.
- **Weak hook material:** "Let's talk about perceived value," "here are
  three things brands do" — anything that announces a lesson instead of
  posing a question.

If the strongest hook line isn't already near the start of the raw footage,
that's a signal to **trim the opening** so it leads with the hook rather
than with preamble, a greeting, or throat-clearing context. Don't caption
your way around a weak opening — fix the trim first.

## Trimming: what to cut

Apply "the boring test" to the raw footage before touching captions. Look
for, and cut:

- Dead air, false starts, and long pauses that aren't doing narrative work
  (a pause for genuine emphasis before a reveal is different — don't cut
  those)
- Restating the same point twice in different words
- A slow or throat-clearing opening before the actual hook line
- Context that isn't making the central question more interesting (context
  should sharpen curiosity, not just add information)
- A weak or trailing-off ending — the last line on screen should be the
  payoff or the follow-bridge line, not an afterthought

Use `scripts/trim_reel.py detect` to surface candidate silence gaps as a
starting point, but the actual keep/cut decision is a content judgment, not
a threshold — always sanity-check what's actually being said around a
candidate gap before cutting it.

**Cut order matters for sync:** always trim first, then author caption
timestamps against the trimmed video. Never write beats.json against the
original footage's timeline if you're also planning to trim.

## Editing rhythm (applies to caption pacing, not just cuts)

Not every beat needs the same on-screen duration. As a rough guide:
- A pattern-interrupt moment (a big number landing, a hard turn in the
  story) can be brief — let it hit and move on.
- Normal explanatory statements need enough time to actually read.
- The moment carrying the most emotional or informational weight (the twist,
  the payoff) can hold longer than a normal beat — resist the urge to keep
  pace uniform if a moment deserves room to land.

This is why the caption system already varies duration and style by mode
(see design-tokens.md) — mechanically identical caption timing across an
entire video is what makes an edit feel like an algorithm made it.

## When a number earns a big-text / infographic moment

Not every number needs one. Reserve it for:
- A genuine comparison ("only a fraction of," "ten times more") — pair with
  `bar_compare`
- A rise or fall framed directionally — pair with `arrow_up`/`arrow_down`
- The single number the whole story hinges on — this is the one place
  `bubble_stat` earns its use, and it should happen once per video at most

If a video has many numbers, resist making all of them big-text moments —
that's the on-screen equivalent of shouting every sentence. Pick the one or
two that matter and let the rest stay as normal statement captions.

## On-screen text hierarchy (maps directly to the four caption modes)

| What's being said | Caption mode | Why |
|---|---|---|
| A section transition or aside ("quick context," "here's the turn") | `kicker` | Signals structure without competing for attention |
| Regular explanation, the connective tissue | `statement` | The default — most of the video lives here |
| The line designed to be quoted or remembered | `hook` | Gets the accent color and extra hold time — should happen once or twice per video, not every sentence |
| A number worth seeing, not just hearing | `stat` | Gets the giant-number treatment, sometimes paired with a graphic |

Never let a whole video sit in one mode. If you notice five statement beats
in a row, look for one that's actually functioning as a hook or aside and
recategorize it — variety in caption mode is itself a pattern-interrupt
that keeps the video from feeling flat.

## The follow-bridge line (optional, don't force it)

If the story naturally lands on perceived value, pricing, branding, status,
or scarcity, The Growth Edit's recurring closing thought works well as the
final caption: *"So what else are you paying for — because someone made it
feel valuable?"* Only use it when the story actually earns it — forcing it
onto a video that isn't about that theme will feel mechanical, which is the
opposite of the goal.

## Quick QA pass before calling an edit done

Borrowed from the full production process, scaled down to what's relevant
for a captioned/trimmed edit:

- **First-frame test:** does the very first frame (silent, static) make a
  stranger want to know what happens next?
- **Silent test:** with sound off, does the caption/graphic track alone
  still tell the story and land the reveal?
- **Safe-zone check:** do any captions or graphics sit under where
  Instagram's own UI renders (see design-tokens.md's Reels safe zones)?
- **Mode variety check:** does any single caption mode run more than two
  beats in a row?

If any of these fail, fix it before calling the edit finished — these are
cheap to check and expensive to get wrong on a published reel.
