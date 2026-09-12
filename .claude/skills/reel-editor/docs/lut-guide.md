# Get your camera's color LUT

This skill grades footage that was filmed in a **flat "log" picture profile** (the washed-out, low-contrast
look). The first step of the grade applies a **log → Rec.709 LUT** — a `.cube` file from your camera
manufacturer that converts that flat log image into normal, natural color. After the LUT, the pipeline adds
the cinematic grade on top.

**No LUTs are bundled** with this plugin (manufacturers don't license their LUTs for redistribution). Download
the right one for your camera — they're all **free** from the manufacturer.

## Where to get it (free, official)

| Camera | Log profile | Where to download the LUT |
|---|---|---|
| **DJI** (Osmo Pocket 3, Action 4/5, Mavic, Air, Osmo 360) | **D-Log M** (recent bodies) or D-Log | DJI's official LUT page — search "DJI D-Log M to Rec709 LUT download". Pick **D-Log M** for Pocket 3 / recent cameras, classic **D-Log** for older ones. |
| **Sony** (a7 / FX series, ZV) | **S-Log3** | Sony's "S-Log3 to Rec709" LUTs (Sony Creators' Cloud / support site). |
| **Canon** (R5/R6, C-series) | **C-Log3** (or C-Log2) | Canon's official LUTs (Canon "Look" / EOS LUT downloads). |
| **Panasonic** (Lumix S/GH) | **V-Log** | Panasonic V-Log → Rec709 LUT (Lumix support). |
| **Fujifilm** | **F-Log / F-Log2** | Fujifilm F-Log to WDR/Rec709 LUTs. |
| **GoPro** | **Flat** profile | GoPro "Protune Flat to Rec709" community/official LUTs. |
| **Apple / iPhone** (ProRes **Log**) | **Apple Log** | Apple's official "Apple Log to Rec. 709" LUT (Apple support / Final Cut resources). |

> Tip: a web search for `"<your camera> <log profile> to Rec709 .cube LUT"` finds the official download fast.

## Use it

Pass the `.cube` to the grade script:

```bash
python3 scripts/build_base_clip.py edl_beats.json \
  --lut /path/to/your_camera_log_to_rec709.cube \
  --out-dir edit --source raw/<clip>.MP4 --fps 30
```

## Didn't film in log?

If you shot a normal/standard profile (already Rec.709 — most phones in their default mode), you don't need a
LUT. Skip the `lut3d` step and grade directly (lift/contrast/white-balance to taste). Log footage just gives
the grade far more room — especially for recovering a bright window behind a backlit subject.

## The grade after the LUT (the part that matters)

The bundled grade (in `scripts/build_base_clip.py`) is a proven **starting point**. Re-tune it to match a
reference still you like. The one rule that prevents the washed-out look: **recover highlights freely, but
always anchor with deep blacks and an S-curve** — and never add artificial sharpening (that's the "filmed on a
toaster" look). Crispness comes from filming high-res and downscaling cleanly.
