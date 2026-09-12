# Components — the parts bin

Copy these into `index.html` per beat. The template already ships the **caption engine**, the **reframe system**,
and the **flow/loop** diagram. This file documents the data formats + the other diagram types. All hot/accent
elements use a mood gradient class (`mood-silver` / `mood-cool` / `mood-warm`) + `grad-text` for gradient text.

## Caption data format (`GROUPS`)

```js
// one entry per caption group. 3-4 words. hero = index of the hero word (-1 = none).
{ mood:'cool', flavor:'spike', hero:0, words:[{w:'rewarded', s:1.1, e:1.9}] }
```
- `flavor:'baseline'` → single line, all Geist; hero (if set) becomes Instrument Serif + gradient inline.
- `flavor:'spike'` → support words on a line, hero word big on its own line (Instrument Serif + gradient).
- Word timestamps come from `edited.json` (the transcript remapped onto the trimmed clip).
- The engine auto-places a group in `zone-middle` if a reframe is active at its midpoint, else `zone-lower`.

## Reframe data format (`REFRAMES`)

```js
{ in:2.5, out:5.9, layout:'split-top', box:{ top:'5%', left:'27%', width:'46%', height:'40%', borderRadius:20 } }
```
Box presets (the wrapper animates to these, then back to `FULL`):
- **split-top:** `{ top:'5%', left:'27%', width:'46%', height:'40%', borderRadius:20 }` (diagram goes BOTTOM)
- **split-bottom:** `{ top:'55%', left:'27%', width:'46%', height:'40%', borderRadius:20 }` (diagram goes TOP)
- **pip-top:** `{ top:'5%', left:'33%', width:'34%', height:'30%', borderRadius:18 }` (big type/diagram below)

## Glass diagram shell (wrap every diagram)

```html
<div id="aid-X" class="aid" data-in="A" data-out="B" style="left:6%;right:6%;bottom:5%;">
  <div class="glass">
    <div class="d-eyebrow">label</div>
    <!-- diagram body here -->
  </div>
</div>
```
Position with `bottom:5%` (diagram below a split-top reframe) or `top:5%` (above a split-bottom). The generic
enter/exit (blur-in) is handled automatically for any `#aids .aid`. Add bespoke internal motion in the script.

## Diagram: flow / loop  (shipped in template)

Nodes + arrows; nodes pop in sequence. Last node `hot` (mood-filled chip). See template `#aid-loop`.

## Diagram: meter / gauge

```html
<div id="aid-meter" class="aid" data-in="A" data-out="B" style="left:6%;right:6%;bottom:5%;">
  <div class="glass">
    <div class="d-eyebrow">emotional entry fee</div>
    <div class="meter-track"><div class="meter-fill mood-warm" id="mfill"></div></div>
    <div class="meter-row"><span class="l">cost to start</span><span class="v grad-text mood-warm" id="mval">LOWERED ↓</span></div>
  </div>
</div>
```
```js
// fill drains on the spoken word; value fades in
tl.fromTo('#mfill', { scaleX:1 }, { scaleX:0.28, duration:0.7, ease:'power2.inOut' }, /*t=*/3.0);
tl.fromTo('#mval', { opacity:0 }, { opacity:1, duration:0.3 }, 3.4);
```

## Diagram: comparison (A vs B)

```html
<div id="aid-cmp" class="aid" data-in="A" data-out="B" style="left:6%;right:6%;bottom:5%;">
  <div class="glass">
    <div class="d-eyebrow">the task vs the starting</div>
    <div style="display:flex;flex-direction:column;gap:14px;margin-top:20px;">
      <div class="cmp-row" id="cmp-a" style="display:flex;align-items:center;gap:16px;padding:16px 22px;border-radius:14px;background:rgba(11,11,12,.5);border:1px solid var(--hair);">
        <span style="font-family:'Geist';font-weight:700;font-size:30px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;">the task</span>
        <span style="margin-left:auto;font-family:'Geist';font-weight:800;font-size:38px;color:var(--muted);">not hard</span>
      </div>
      <div class="cmp-row" id="cmp-b" style="display:flex;align-items:center;gap:16px;padding:16px 22px;border-radius:14px;background:rgba(11,11,12,.5);border:1px solid rgba(255,255,255,.4);">
        <span style="font-family:'Geist';font-weight:700;font-size:30px;color:var(--fg);text-transform:uppercase;letter-spacing:.05em;">the starting</span>
        <span class="grad-text mood-cool" style="margin-left:auto;font-family:'Geist';font-weight:800;font-size:38px;">feels gross</span>
      </div>
    </div>
  </div>
</div>
```
```js
tl.from('#cmp-a', { x:-30, opacity:0, duration:0.35, ease:'power3.out' }, /*t=*/A+0.1);
tl.from('#cmp-b', { x:-30, opacity:0, duration:0.35, ease:'power3.out' }, A+0.4);
tl.fromTo('#cmp-b', { scale:1 }, { scale:1.04, duration:0.2, yoyo:true, repeat:1 }, /*spoken word*/A+1.2);
```

## Diagram: stat callout (counting number)

```html
<div id="aid-stat" class="aid" data-in="A" data-out="B" style="left:6%;right:6%;bottom:5%;">
  <div class="glass" style="text-align:center;">
    <div class="d-eyebrow">just get there for</div>
    <div class="grad-text mood-cool" id="statnum" style="font-family:'Geist';font-weight:900;font-size:140px;line-height:1;font-variant-numeric:tabular-nums;">0s</div>
  </div>
</div>
```
```js
var o={n:0};
tl.to(o,{ n:60, duration:1.0, ease:'power2.out', onUpdate:function(){ document.getElementById('statnum').textContent = Math.round(o.n)+'s'; } }, /*t=*/A+0.2);
```

## Accents & transitions (from the Reel-05 study, 2026-06-03)

Use these **only when the moment calls for it** — they're seasoning, not defaults. Each notes its motion + SFX role.

### Gesture pill (contextual annotation)

Small dark pill that pops in next to the speaker's hand as he *names* a thing ("Dialer", "AI Avatar"). The
signature move of the reference reel. Anchor it to the spoken word; keep it inside the safe zone (not over the face).

```html
<div class="gpill" data-in="A" data-out="B" style="left:58%;top:30%;">AI Avatar</div>
```
```css
.gpill{ position:absolute; font-family:'Geist'; font-weight:600; font-size:30px; color:#fff;
  background:rgba(16,16,18,.86); border:1px solid rgba(255,255,255,.10); border-radius:14px;
  padding:10px 18px; box-shadow:0 8px 30px rgba(0,0,0,.35); backdrop-filter:blur(6px); }
```
```js
// pop with a SUBTLE overshoot (pills are allowed a little bounce; captions are not)
tl.fromTo('.gpill', { opacity:0, scale:0.8, y:10 },
  { opacity:1, scale:1, y:0, duration:0.28, ease:'back.out(1.7)' }, /*spoken word*/A);
tl.to('.gpill', { opacity:0, scale:0.96, duration:0.18, ease:'power2.in' }, B); // quick out
```
SFX: `pop` on entrance. Stack 2–3 in sequence (stagger ~0.12 s) when he lists items.

### Numbered step pill

Glassy "01 — Content" chips to structure a list/process.

```html
<div class="spill" data-in="A" data-out="B" style="left:50%;top:24%;transform:translateX(-50%);">
  <span class="n">02</span><span class="l">Content</span></div>
```
```css
.spill{ position:absolute; display:flex; align-items:center; gap:12px; font-family:'Geist';
  background:rgba(255,255,255,.10); border:1px solid rgba(255,255,255,.22); border-radius:16px;
  padding:10px 20px; backdrop-filter:blur(14px); box-shadow:0 10px 40px rgba(0,0,0,.25); }
.spill .n{ font-weight:800; font-size:26px; } .spill .l{ font-weight:600; font-size:30px; color:#fff; }
```
Same pop as the gesture pill. SFX: `pop` (or `ding` if it reads as a reveal).

### Glow hero (caption treatment variant)

The electric-blue glowing hero word ("$100K", "YOUR FACE"). A variant of `flavor:'spike'` — instead of (or with)
the gradient, give the hero word a cyan halo. Use for punchy money/number/payoff words.

```css
.grad-text.glow{ color:#bfe0ff; text-shadow:0 0 18px rgba(90,170,255,.85), 0 0 42px rgba(70,140,255,.45); }
```
```js
tl.fromTo('.hero.glow', { opacity:0, scale:0.92 }, { opacity:1, scale:1, duration:0.32, ease:'power3.out' }, A);
```
SFX: `pop` or `impact` on the word, depending on size. One glow hero per beat, same as the gradient rule.

### White-flash cleanser scene

A full-bleed white card holding a single icon/line ("business operating system") — a palette reset between
sections. Also doubles as a hard transition.

```html
<div id="flash-X" class="cleanser" data-in="A" data-out="B">
  <img src="assets/os-icon.png" style="width:42%"><div class="cl-cap">business operating system</div></div>
```
```css
.cleanser{ position:absolute; inset:0; background:#fff; display:flex; flex-direction:column;
  align-items:center; justify-content:center; gap:28px; }
.cl-cap{ font-family:'Geist'; font-weight:600; font-size:40px; color:#111; }
```
```js
tl.fromTo('#flash-X', { opacity:0 }, { opacity:1, duration:0.08, ease:'power2.out' }, A); // snaps in
tl.to('#flash-X', { opacity:0, duration:0.12, ease:'power2.in' }, B);                     // snaps out
```
SFX: `impact` on the snap-in (pair with the drop-out-before-hit move). Icon via Higgsfield (asset-generation.md).

### Whip + flash transition

Fast directional blur + white flash across a cut (~0.12 s). Much snappier than a crossfade; use on take/scene
changes. Apply to `#fwrap` (the footage wrapper) with a brief white overlay.

```js
// at the cut time T: blur-whip the footage, flash a white overlay over it
tl.fromTo('#fwrap', { filter:'blur(0px)', x:0 }, { filter:'blur(14px)', x:-60, duration:0.06, ease:'power4.in' }, T);
tl.to('#fwrap',     { filter:'blur(0px)', x:0, duration:0.10, ease:'power4.out' }, T+0.06);
tl.fromTo('#whiteflash', { opacity:0 }, { opacity:0.9, duration:0.05 }, T+0.03)
  .to('#whiteflash', { opacity:0, duration:0.09 }, T+0.08);
```
SFX: `whoosh` on the cut. (We can only approximate true motion-blur whip-pans; this reads close.)

> Motion-timing cheatsheet from the study: pills ~0.28 s `back.out`; glow hero ~0.32 s `power3.out`;
> reframe-to-PIP ~0.3 s (tighter than our current 0.7 — consider lowering); whip/flash ~0.12 s `power4`;
> white-flash cleanser snaps (~0.08 s in / 0.12 s out). Captions keep the existing blur-in + soft settle (no bounce).

## Rules

- One diagram on screen at a time. Position it in the half freed by the reframe.
- Hot/accent element uses the beat's mood gradient; everything else neutral.
- Deterministic only — no `Math.random()` / `Date.now()`. Sync motion to spoken timestamps.
- Every `.aid` needs `data-in`/`data-out`; the engine handles enter/exit + hard-kill.
