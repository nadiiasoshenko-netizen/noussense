#!/usr/bin/env python3
"""
Trim raw uploaded footage down to the segments worth keeping, before any
captioning happens. Two jobs:

1. `detect` — surface *candidate* cut points (silences, long static stretches)
   for a human or Claude to review. This never cuts anything automatically —
   silence-based auto-cutting on a talking-head video is unreliable (people
   pause mid-thought), so treat this as a hint, not a decision.

2. `cut` — given a list of segments to KEEP (in the original footage's
   timeline), concatenate them into a single trimmed output. This is a
   deliberate decision made by whoever authored the keep-list, informed by
   the retention principles in references/editorial-principles.md (cut dead
   air, slow openings, redundant restatements; keep escalating information
   density) — not a blind automated trim.

IMPORTANT: caption timestamps in beats.json must always be authored against
the TRIMMED output's timeline, not the original raw footage. Always run
`cut` (if trimming at all) before authoring beats.json, never after.

Usage:
    # See candidate silence gaps to help decide what to cut
    python3 trim_reel.py detect --video raw.mp4

    # Cut to the specified keep-segments (seconds, in raw.mp4's timeline)
    python3 trim_reel.py cut --video raw.mp4 --keep '[[0,4.2],[6.8,22.1],[24.0,41.5]]' --output trimmed.mp4
"""
import argparse
import json
import subprocess
import sys
import tempfile


def detect_silence(video_path: str, noise_db: str = "-30dB", min_duration: float = 0.6):
    """Run ffmpeg's silencedetect and parse out candidate silence windows.
    These are CANDIDATES for cut points (dead air, long pauses) — always
    sanity-check against the actual content before cutting; a pause for
    emphasis is not the same as dead air."""
    cmd = [
        "ffmpeg", "-i", video_path, "-af",
        f"silencedetect=noise={noise_db}:d={min_duration}",
        "-f", "null", "-",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    lines = result.stderr.splitlines()
    silences = []
    start = None
    for line in lines:
        if "silence_start" in line:
            start = float(line.split("silence_start:")[1].strip())
        elif "silence_end" in line and start is not None:
            # format: "silence_end: 12.34 | silence_duration: 1.23"
            end_part = line.split("silence_end:")[1].strip()
            end = float(end_part.split("|")[0].strip())
            silences.append((round(start, 2), round(end, 2)))
            start = None
    return silences


def get_duration(video_path: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", video_path],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def cut_to_segments(video_path: str, keep_segments: list, output_path: str):
    """Concatenate the given [start, end] segments (seconds, original
    timeline) into a single output, preserving audio sync. Uses the
    filter_complex trim+concat approach (re-encodes) rather than the concat
    demuxer, because re-encoding guarantees clean cuts at arbitrary
    (non-keyframe) timestamps — talking-head footage is rarely cut precisely
    on a keyframe, and stream-copy concat at arbitrary points can produce
    glitches or av-desync at the seams."""
    if not keep_segments:
        raise ValueError("keep_segments is empty — nothing to cut")

    duration = get_duration(video_path)
    for start, end in keep_segments:
        if start < 0 or end > duration + 0.05 or end <= start:
            raise ValueError(
                f"Invalid segment [{start}, {end}] for a video of duration {duration:.2f}s"
            )

    filter_parts = []
    v_labels, a_labels = [], []
    for i, (start, end) in enumerate(keep_segments):
        filter_parts.append(
            f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS[v{i}]"
        )
        filter_parts.append(
            f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS[a{i}]"
        )
        v_labels.append(f"[v{i}]")
        a_labels.append(f"[a{i}]")

    n = len(keep_segments)
    concat_inputs = "".join(f"{v}{a}" for v, a in zip(v_labels, a_labels))
    filter_parts.append(f"{concat_inputs}concat=n={n}:v=1:a=1[outv][outa]")
    filter_complex = ";".join(filter_parts)

    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", "[outa]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
        output_path,
    ]
    subprocess.run(cmd, check=True)

    kept_duration = sum(e - s for s, e in keep_segments)
    print(f"Cut {video_path} ({duration:.1f}s) -> {output_path} ({kept_duration:.1f}s), "
          f"{n} segment(s)")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)

    p_detect = sub.add_parser("detect", help="List candidate silence/dead-air windows")
    p_detect.add_argument("--video", required=True)
    p_detect.add_argument("--noise-db", default="-30dB")
    p_detect.add_argument("--min-duration", type=float, default=0.6)

    p_cut = sub.add_parser("cut", help="Cut to the given keep-segments and concatenate")
    p_cut.add_argument("--video", required=True)
    p_cut.add_argument("--keep", required=True,
                        help='JSON list of [start,end] pairs in seconds, e.g. \'[[0,4.2],[6.8,22.1]]\'')
    p_cut.add_argument("--output", required=True)

    args = p.parse_args()

    if args.command == "detect":
        duration = get_duration(args.video)
        silences = detect_silence(args.video, args.noise_db, args.min_duration)
        print(f"Video duration: {duration:.2f}s")
        if not silences:
            print("No silence windows found at this threshold.")
        for s, e in silences:
            print(f"  candidate gap: {s:.2f}s -> {e:.2f}s  (duration {e - s:.2f}s)")
        print(
            "\nThese are candidates only — check what's actually being said "
            "around each before deciding to cut. A dramatic pause is not dead air."
        )
    elif args.command == "cut":
        keep_segments = json.loads(args.keep)
        cut_to_segments(args.video, keep_segments, args.output)


if __name__ == "__main__":
    main()
