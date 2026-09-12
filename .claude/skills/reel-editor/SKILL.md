---
name: reel-editor
description: Edit a phone-talking-head clip into a premium 1080×1920 vertical reel in one shot — combines video-use (transcribe/trim) + Hyperframes (compose/render) with a full proven pipeline: log→Rec709 color grade matched to a reference still, kinetic per-word captions, generated SFX (a tick on every word + role hits), studio voice enhancement, mistake-cover (freeze/b-roll/graphic), and best-quality Instagram export. Use when turning a raw vertical clip into a finished reel.
---

# Reel editor — one-shot vertical reel pipeline

Turn one raw phone clip into a finished, graded, captioned, sound-designed 1080×1920 reel. This skill orchestrates **video-use** (transcription + trimming) and **Hyperframes** (HTML composition + render) plus the proven grade / caption / SFX / export pipeline.

**Prerequisites (install once):**
- [video-use](https://github.com/browser-use/video-use) — transcription + trimming
- [Hyperframes](https://github.com/heygen-com/hyperframes) — HTML→MP4 composition/render (`npx hyperframes …`)
- `ffmpeg` + `ffprobe`, `python3`
- (optional) an ElevenLabs API key for generating your own SFX

**Bundled alongside this SKILL.md** (vendored from [saucetech/ai-video-editor](https://github.com/saucetech/ai-video-editor), MIT-licensed): `scripts/` (the three build scripts), `template/` (the master composition + fonts + parts bin), `sfx/` (SFX generator + QA), `docs/lut-guide.md` (get your camera's LUT). The build scripts are **proven reference implementations** — copy them into your project's `edit/` folder and adapt the per-video parameters (grade, beat config, SFX hits).

---

## Pipeline (raw clip → reel)

```
raw/<clip>.MP4
  │ 1. TRANSCRIBE + TRIM  (video-use)        → edl_beats.json (+ edited.json)
  │ 2. GRADE + AUDIO       build_base_clip.py → clip.mp4 (graded video + enhanced voice) + voice.m4a
  │ 3. CAPTIONS            build_captions.py  → caps.js (per-word kinetic captions)
  │ 4. COMPOSE            (fill template/index.html) → diagrams/reframes/captions on the GSAP timeline
  │ 5. SFX                build_sfx_mix.py    → voice_sfx.m4a (tick on every word + role hits)
  │ 6. RENDER             npx hyperframes …   → render.mp4 (footage graded INSIDE the engine)
  │ 7. EXPORT             ffmpeg copy + mux   → final.mp4 (stream-copy + voice_sfx, faststart)
  ↓  final.mp4
```

The footage lives **inside** the engine: `clip.mp4` is a `<video>` track, the voice is a separate `<audio>` track; the render bakes graphics + reframes over the footage (no separate overlay-composite step). **Get user approval on the motion board before building graphics.**

## 1 — Transcribe + trim (video-use)
Transcribe the raw clip (word-level timestamps) and pick the cleanest takes. Produce **`edl_beats.json`**: one range per beat `{start, end, beat, quote}` in **source** time; drop dead air / false starts. Produce **`edited.json`** (transcript remapped onto the trimmed timeline) — captions/SFX scripts read its `words`/`beats`. Optional per-range `video_end` → see §8 (cover a mistake).

## 2 — Grade + audio (`scripts/build_base_clip.py`)
```bash
python3 scripts/build_base_clip.py edl_beats.json \
  --lut <your-camera-log-to-rec709>.cube \
  --out-dir edit --source raw/<clip>.MP4 --fps 30
cp edit/clip.mp4 clip.mp4
```
Bakes your camera's **log→Rec709 LUT** per segment (see `docs/lut-guide.md` to get the right LUT for DJI / Sony / Canon / etc.), then a grade + **2-pass voice enhancement** (rumble high-pass, denoise, presence EQ, de-ess, −14 LUFS). **The grade rule that matters:** recover highlights freely (so a bright window keeps detail) BUT anchor with **deep blacks + an S-curve**, or it goes washed/milky. No sharpening (= the "filmed on a toaster" look) — crispness comes from a high-res lanczos downscale. To match YOUR look: tune the `post` chain and QA frames against a reference still (`signalstats`: deep blacks, unclipped highlights, neutral UAVG/VAVG ≈ 128).

## 3 — Captions (`scripts/build_captions.py`)
```bash
python3 scripts/build_captions.py edited.json -o caps.js
```
**Every word** animates. Mix `'big'` (one hero word, serif + glow) with `'line'` (running word-by-word). `BEAT_CFG` sets per-beat mood + hero/serif words. Mixed fonts (a clean sans + an italic serif) + cyan glow on hero words.

## 4 — Compose (fill `template/index.html`)
Copy `template/` into your project. From the approved motion board, set `data-duration`/`DUR` = clip length, write the `REFRAMES` (PIP/split-screen) array, and author the per-beat diagram HTML + GSAP **synced to when each word is spoken**. Two card systems by context: **Spotlight** (flat near-black + glow, graphics-on-black) and **Frosted** (glass over live footage, talking-head). Over BRIGHT footage make the frost more opaque + whiten titles. No cheap gray-gradient glass; no random gesture pills — use purposeful diagrams. Respect the safe area (captions `bottom:26%`; cards end by y≤1300; sides ≥5.5%) — see `template/` README/comments.

## 5 — SFX (`scripts/build_sfx_mix.py`)
```bash
python3 scripts/build_sfx_mix.py     # reads your voice, edited.json, and the sfx/ library
```
Produces **`voice_sfx.m4a`** = voice + a subtle **keyboard tick on EVERY word** (sample-accurate to voice onset) + **role hits** on beats (whoosh/pop/ding/click/impact). Generate + QA your own library with `sfx/generate_sfx.py` + `sfx/qa_sfx.py` (a real "buzz" defect = high flat-factor; prompt with concrete materials + "a single/isolated" hit, avoid the word "electronic"). Ticks MUST be tight to the spoken word.

## 6 — Render (Hyperframes)
```bash
npx hyperframes lint
npx hyperframes render --output edit/render.mp4 --fps 30 --quality high --crf 12 --resolution portrait
```
1080×1920, limited-range bt709, ~8–9 Mbps.

## 7 — Export (best quality, IG-ready)
The render is already crf-12 high-quality — **stream-copy the video (zero re-encode loss) + mux the SFX voice:**
```bash
ffmpeg -y -i edit/render.mp4 -i voice_sfx.m4a \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -ar 48000 \
  -movflags +faststart -shortest final.mp4
```
H.264 High @ 1080×1920, 30fps, **standard limited-range bt709** (do NOT expand `tv→pc` / tag `color_range=pc` — Instagram renders that with wrong levels), faststart. Always mux the voice explicitly (the engine's own render audio is unreliable).

## 8 — Cover look-aways / flubs
When the subject glances off-camera or fumbles, cut it out and cover the gap with whatever fits: **b-roll, a motion graphic, a full-screen graphic, a freeze-frame, or a de-focus blur** — freeze is just one option. The only hard constraint: **preserve the segment's duration** so captions/SFX/reframes stay synced. The built-in **freeze-fill** does this automatically — add `"video_end": <source_seconds>` to the EDL range (`build_base_clip.py` cuts just before the moment and clones the last clean frame to the range's `end`). For a graphic/b-roll cover, overlay it for that exact window instead.

## QA before delivery (always)
Extract frames and LOOK (color matches the reference; deep blacks; unclipped highlights; neutral cast). Confirm ticks land on words and no buzzy SFX. `volumedetect` shows real speech in the final. Nothing critical in the top 11.5% / bottom 26%. No look-aways/flubs left.

**Anti-spiral:** motion-board approval gate is sacred; cap self-verify at 2 passes; if lint/render fails 3× stop and report.
