# Asset generation — Higgsfield CLI

Some premium-reel components need bespoke art the engine can't draw from CSS: photoreal **3D isometric icons**
(the frosted "operating-system" block), **orbiting brand-logo** art, **b-roll** cutaways, **textured backplates**,
and **on-brand likeness** shots to cover look-aways. Generate these with the **Higgsfield CLI** and drop the
output into the project's `assets/` (or `_shared-assets/images/` if reusable), then place it in `index.html`
like any other image/video clip.

> Status (2026-06-03): **not installed yet.** The `hf` on this machine is the Hugging Face CLI, not Higgsfield.
> Install before first use (below). Uses Higgsfield credits via browser OAuth — no API key to manage.

## Install + auth (one time)

```bash
npm install -g @higgsfield/cli         # or: brew install higgsfield-ai/tap/higgsfield
higgsfield auth login                  # opens browser, device-code OAuth, ~5s
higgsfield model list                  # confirm available models
```

## The one command

```bash
higgsfield generate create <model> --prompt "..." [flags] --wait
```
`--wait` blocks until the job finishes and prints the result URL (download it to the project).

Common flags: `--aspect_ratio 9:16` · `--resolution 2k` (or `4k`/`1080p`) · `--start-image ./ref.png` (image-to-x) ·
`--duration 5` (video seconds, ≤15) · `--quality` / `--mode pro`.

## Which model for which asset

| Need | Type | Model | Notes |
|---|---|---|---|
| 3D isometric app/OS icons, glass objects | image | `nano_banana_2` (Nano Banana Pro) or `flux` | clean product-render look; up to 4K |
| Stylized backplates / textured hero cards | image | `flux` / `soul` | |
| On-brand **consistent likeness** (you / your host) | character | `soul-id create` → then generate | trains a reusable identity; use for avatar/b-roll so the face matches |
| B-roll motion (push-ins, abstract loops, product motion) | video | `kling3_0` · `veo` · `seedance` | ≤15s, any aspect; use `--start-image` to animate a generated still |
| Cutaway to cover a look-away / dead beat | video | `kling3_0 --start-image <likeness>.png` | animate a soul-id still into a short cutaway |

## Examples

```bash
# 3D isometric "operating system" icon, transparent-ish on white, 9:16 safe
higgsfield generate create nano_banana_2 \
  --prompt "isometric 3D render of a frosted glass server/operating-system tower with small floating app tiles orbiting it, soft blue tint, clean white studio background, subtle shadow, Apple product render style" \
  --aspect_ratio 9:16 --resolution 2k --wait

# Train your reusable likeness (once), then a cutaway b-roll clip
higgsfield soul-id create --name host   # follow prompts to upload reference shots
higgsfield generate create kling3_0 \
  --prompt "same person, seated in a modern apartment with floor-to-ceiling windows, subtle slow push-in, cinematic, shallow depth of field" \
  --start-image ./host_ref.png --duration 4 --aspect_ratio 9:16 --mode pro --wait
```

## Workflow rules

1. **Generate to a file, then place it.** Save into `<project>/assets/clips/` (video) or `<project>/assets/` /
   `_shared-assets/images/` (stills). Reference it as a normal Hyperframes `<video>`/`<img>` clip.
2. **9:16 + 2k minimum** for anything full-bleed; icons/cards can be smaller but keep them crisp at render scale.
3. **Match the grade.** Generated stills/b-roll should sit in the same clean, slightly-cool look — colorgrade in
   ffmpeg if needed so they don't clash with the DJI footage.
4. **Determinism note:** generation happens *before* the render (it's an asset step). The Hyperframes render
   itself stays deterministic — no live generation inside the composition.
5. **Cost:** each generation spends credits; prefer one good still + animate it (`--start-image`) over many video
   gens. Reuse via `_shared-assets/` when an asset is brand-generic.

## MCP alternative

For agent-driven generation you can also add the Higgsfield skill/MCP to Claude Code:
`npx skills add higgsfield-ai/skills`. The CLI is simpler/cheaper for scripted asset steps; MCP is handy for
exploratory "make me three options" prompting.
