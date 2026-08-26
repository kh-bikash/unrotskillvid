#!/usr/bin/env python3
"""Map a narration track's speech segments and pauses, and propose scene cuts.

    python scripts/audio-map.py narration.wav --scenes 4 --json out_map.json

Cuts are placed at the MIDPOINT of the longest pauses, so a scene change never lands
mid-sentence. Everything else in the composition hangs off the speech segments between them.

Requires ffmpeg/ffprobe on PATH.
"""

import argparse
import json
import os
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


def map_audio(audio_path, scenes_count=4, noise="-34", min_pause=0.18, json_out=None):
    total = duration_of(audio_path)
    starts, ends = silences(audio_path, noise, min_pause)
    segs = speech_segments(total, starts, ends)
    if not segs:
        print("[WARNING] No speech detected with strict thresholds, retrying with relaxed noise floor (-28dB)...")
        starts, ends = silences(audio_path, "-28", 0.12)
        segs = speech_segments(total, starts, ends)
        if not segs:
            # Fallback evenly split if single continuous track
            segs = [(0.0, total)]

    gaps = [(segs[i][1], segs[i + 1][0]) for i in range(len(segs) - 1)]
    gaps = [(a, b, b - a) for a, b in gaps]

    cuts = []
    scene_plans = []

    if scenes_count > 1:
        need = scenes_count - 1
        if len(gaps) < need:
            # If not enough natural pauses, split by segment boundaries or equal splits
            if segs and len(segs) >= scenes_count:
                step = len(segs) // scenes_count
                cuts = [round(segs[min(i * step, len(segs)-1)][1], 2) for i in range(1, scenes_count)]
            else:
                step = total / scenes_count
                cuts = [round(i * step, 2) for i in range(1, scenes_count)]
        else:
            chosen = sorted(sorted(gaps, key=lambda g: -g[2])[:need], key=lambda g: g[0])
            cuts = [round((a + b) / 2, 2) for a, b, _ in chosen]
            
        bounds = [0.0] + cuts + [round(total, 2)]
        for i in range(len(bounds) - 1):
            a, b = bounds[i], bounds[i + 1]
            inside = [s for s in segs if s[0] >= a - 0.01 and s[1] <= b + 0.01]
            scene_plans.append({
                "scene": i + 1,
                "start": round(a, 2),
                "duration": round(b - a, 2),
                "end": round(b, 2),
                "segments": [{"start": round(s[0], 2), "end": round(s[1], 2), "duration": round(s[1] - s[0], 2)} for s in inside]
            })

    result_data = {
        "audio_file": os.path.basename(audio_path),
        "total_duration": round(total, 2),
        "speech_segments": [{"start": round(s[0], 2), "end": round(s[1], 2), "duration": round(s[1] - s[0], 2)} for s in segs],
        "pauses": [{"start": round(a, 2), "end": round(b, 2), "duration": round(d, 2), "midpoint": round((a + b)/2, 2)} for a, b, d in sorted(gaps, key=lambda g: -g[2])],
        "cut_points": cuts,
        "scenes": scene_plans
    }

    if json_out:
        with open(json_out, "w", encoding="utf-8") as f:
            json.dump(result_data, f, indent=2)
        print(f"[MAP] Cut map saved to {json_out}")

    return result_data


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio", help="Path to narration audio WAV")
    ap.add_argument("--scenes", type=int, default=4, help="Propose cut points for this many scenes (default: 4)")
    ap.add_argument("--noise", default="-34", help="Silence floor in dB (default -34)")
    ap.add_argument("--min-pause", type=float, default=0.18, help="Shortest gap that counts in seconds (default 0.18)")
    ap.add_argument("--json", default=None, help="Save mapping output to JSON file")
    args = ap.parse_args()

    data = map_audio(args.audio, args.scenes, args.noise, args.min_pause, args.json)
    
    print(f"\nAudio File:     {data['audio_file']}")
    print(f"Total Duration: {data['total_duration']:.2f}s (Set root data-duration to this)")
    print(f"Detected {len(data['speech_segments'])} speech segments and {len(data['pauses'])} pauses.\n")

    print("Scene Cut Schedule:")
    for sc in data["scenes"]:
        print(f"  • Scene {sc['scene']}: Start {sc['start']:6.2f}s | Duration {sc['duration']:5.2f}s | End {sc['end']:6.2f}s ({len(sc['segments'])} segments)")
    print()


if __name__ == "__main__":
    main()
