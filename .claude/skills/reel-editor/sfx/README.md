# SFX library — your curated sound-design kit

Drop the sound effects you like in here. The reel mix script pulls from this library by **role** (not by
filename), so you can swap or add favorites and every future edit picks them up automatically. This is the
"sounds I like" folder — curate it.

## Folders = roles

| Folder | Role | Fires on (in the edit) |
|---|---|---|
| `whoosh/` | transition | scene changes, reframe in/out, whip cuts, footage shrink to PIP |
| `pop/` | text accent | hero caption word, gesture pill, numbered step pill, small text reveal |
| `ding/` | reveal | UI/card reveal, deliverable chip, screenshot/repo card, checklist tick |
| `click/` | small UI | flow-diagram node, light tick, cursor/select, small graphic beat |
| `impact/` | landing | big payoff, number reveal, white-flash hit, diagram merge |
| `riser/` | build | tension build that leads into an impact |
| `keyboard/` | typing | typing b-roll accent, ASMR key click on a tech/text beat |
| `asmr/` | texture | satisfying tactile accent, soft reveal, palette-cleanser texture |
| `bed/` | music | short ambient loops/stings (full songs go in `../music/`) |

## How to add a sound you like

1. Drop the file in the matching role folder.
2. Name it `<role>-<descriptor>-NN.wav` — e.g. `whoosh-tape-03.wav`, `pop-bubble-02.wav`, `impact-cinematic-01.wav`.
3. Convert to 48 kHz WAV if it isn't already:
   `ffmpeg -i in.mp3 -ar 48000 -ac 1 whoosh/whoosh-tape-03.wav`
4. Add an entry in [`sfx.json`](sfx.json) under that role with a `rating` (1–5). **The mix prefers your highest-rated clip.**
   Rate the ones you love `5`; the picker uses those first.

That's it — no need to touch the edit code. Re-run the project's `build_sfx_mix.py` and it resolves the role to
your top-rated clip.

## What's seeded now

- **Approved viral set from reel 01** (the swooshes/pops/dings you signed off on), rated 5 — `*-01.wav` / `*-02.wav`.
- **30 ElevenLabs-generated SFX** (`*-gen-01.wav`) across every role, rated 3 — covers the most-used short-form
  sounds plus keyboard + ASMR. Listen, then bump the ones you love to `5` (the mix prefers your top-rated clip).

## Generate more (ElevenLabs)

Prompts + generator live in [`generate_sfx.py`](generate_sfx.py) — it IS the prompt record. Each prompt follows
ElevenLabs best practices (specific source/material/envelope, onomatopoeia, tight one-shot durations, higher
`prompt_influence` for precision). It generates → trims leading silence (transient at t=0) → peak-normalizes →
48 kHz mono WAV → upserts `sfx.json` (prompt + params stored, so every clip is reproducible).

```bash
python3 generate_sfx.py --list            # print the prompt set, generate nothing
python3 generate_sfx.py                    # generate only missing files
python3 generate_sfx.py --force            # re-roll everything (generation is non-deterministic)
python3 generate_sfx.py --only impact asmr # re-roll just these roles
```

To **re-roll one sound you don't like**: delete its `.wav`, tweak its prompt in `generate_sfx.py`, re-run. To **add
a new one**: append a `(role, name, prompt, duration_s, prompt_influence)` tuple to `SPECS` and run. Key comes from
`CONTENT/.env` (`ELEVENLABS_API_KEY`).

## Real recordings (when generation can't nail an iconic sound)

ElevenLabs approximates from a description — it can't clone a specific, instantly-recognizable sample (e.g. the
**iOS keyboard tap**). For those, drop a real recording in and I'll slice clean single hits out of it:

- Source recording lives in the role folder (e.g. `keyboard/iphone-keyboard.mp3` = ~23 s of real iPhone typing).
- Single taps sliced from it: `keyboard/iphone-real-01.wav` (rated 5), `-02`, `-03` — these ARE the genuine sound.
- Method: pick a tap with a big gap after it, extract a ~0.28 s window from ~12 ms before the onset, fade out the
  tail, peak-normalize to −1.5 dB, 48 kHz mono. QA confirms a single transient (one spike + decay, no 2nd tap).

To add your own: record the sound (a few isolated hits in a quiet room), drop the file in the role folder, and
ask me to slice it — or do it with the one-liner pattern in the project's extraction step.

## Sound-design rules (how these get used)

Full rationale lives in `_templates/_styles/editorial-playbook.md` → **Sound design**. Short version:

- **Selective, not a bed of effects.** One sound per meaningful beat. Silence between is what makes the hits land.
- **The mix drops out right before a big impact** (≈150 ms of near-silence), then punches — that's the dopamine.
- **A music bed runs the whole time** at ≈ −22 dB under the voice; SFX sit on top, voice stays the loudest thing.
- Final loudness target: **−14 LUFS**, true-peak ≈ −1 dB, brickwall limiter at 0.96.
