#!/usr/bin/env python3
"""Map a narration track's speech segments and pauses, and propose scene cuts.

    python audio-map.py narration.wav --scenes 4

Cuts are placed at the MIDPOINT of the longest pauses, so a scene change never lands
mid-sentence. Everything else in the composition hangs off the speech segments between them.

Requires ffmpeg/ffprobe on PATH. Prefer `hyperframes transcribe` when whisper-cpp is installed
(word-level timings are better); this is the fallback that always works.
"""

import argparse
import re
import subprocess
import sys


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def duration_of(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", path])
    if r.returncode != 0:
        sys.exit(f"ffprobe failed on {path}:\n{r.stderr.strip()}")
    return float(r.stdout.strip())


def silences(path, noise, min_dur):
    r = run(["ffmpeg", "-hide_banner", "-i", path,
             "-af", f"silencedetect=noise={noise}dB:d={min_dur}", "-f", "null", "-"])
    text = r.stderr + r.stdout
    starts = [float(m) for m in re.findall(r"silence_start:\s*(-?[\d.]+)", text)]
    ends = [float(m) for m in re.findall(r"silence_end:\s*([\d.]+)", text)]
    return sorted(starts), sorted(ends)


def speech_segments(total, starts, ends):
    """Invert the silence list into [start, end] speech spans."""
    marks = []
    for s in starts:
        marks.append(("start", max(0.0, s)))
    for e in ends:
        marks.append(("end", e))
    marks.sort(key=lambda m: m[1])

    segments, cursor, silent = [], 0.0, False
    for kind, t in marks:
        if kind == "start" and not silent:
            if t - cursor > 0.05:
                segments.append((cursor, t))
            silent = True
        elif kind == "end":
            cursor, silent = t, False
    if not silent and total - cursor > 0.05:
        segments.append((cursor, total))
    return segments


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio")
    ap.add_argument("--scenes", type=int, default=0,
                    help="propose cut points for this many scenes (needs scenes-1 pauses)")
    ap.add_argument("--noise", default="-34", help="silence floor in dB (default -34)")
    ap.add_argument("--min-pause", type=float, default=0.18,
                    help="shortest gap that counts, seconds (default 0.18)")
    args = ap.parse_args()

    total = duration_of(args.audio)
    starts, ends = silences(args.audio, args.noise, args.min_pause)
    segs = speech_segments(total, starts, ends)
    if not segs:
        sys.exit("No speech detected — try raising --noise (e.g. -30) or lowering --min-pause.")

    print(f"\nAudio       {args.audio}")
    print(f"Duration    {total:.2f}s   (set the root composition's data-duration from this)")
    print(f"Detected at noise={args.noise}dB  min-pause={args.min_pause}s\n")

    print("Speech segments")
    for i, (a, b) in enumerate(segs, 1):
        print(f"  {i:2d}.  {a:6.2f} - {b:6.2f}   ({b - a:5.2f}s)")

    gaps = [(segs[i][1], segs[i + 1][0]) for i in range(len(segs) - 1)]
    gaps = [(a, b, b - a) for a, b in gaps]
    print("\nPauses, longest first")
    for a, b, d in sorted(gaps, key=lambda g: -g[2]):
        print(f"       {a:6.2f} - {b:6.2f}   ({d:4.2f}s)   midpoint {((a + b) / 2):6.2f}")

    if args.scenes > 1:
        need = args.scenes - 1
        if len(gaps) < need:
            sys.exit(f"\nOnly {len(gaps)} pauses found; {args.scenes} scenes needs {need}.")
        chosen = sorted(sorted(gaps, key=lambda g: -g[2])[:need], key=lambda g: g[0])
        cuts = [round((a + b) / 2, 2) for a, b, _ in chosen]
        bounds = [0.0] + cuts + [round(total, 2)]
        print(f"\nProposed cut plan for {args.scenes} scenes")
        print("  cuts at  " + " | ".join(f"{c:.2f}" for c in cuts))
        for i in range(len(bounds) - 1):
            a, b = bounds[i], bounds[i + 1]
            inside = [s for s in segs if s[0] >= a - 0.01 and s[1] <= b + 0.01]
            print(f"  scene {i + 1}   start {a:6.2f}   duration {b - a:5.2f}"
                  f"   ({len(inside)} speech segment{'s' if len(inside) != 1 else ''})")
        print("\n  Scene-local time = absolute - scene start. Put the segments for each scene")
        print("  in a comment at the top of its composition and justify every timing against them.")
    print()


if __name__ == "__main__":
    main()
