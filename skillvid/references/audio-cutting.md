# Cutting to the narration

The single highest-leverage thing in this genre. A reel whose cuts land inside the speaker's
own pauses reads as edited; one whose cuts land mid-clause reads as a slideshow with audio
stuck on top. The difference is usually 1–3 seconds per cut, and it is invisible in a
storyboard — you only hear it.

## Get the map

```bash
python <SKILL_DIR>/scripts/audio-map.py narration.wav --scenes 4
```

Under the hood:

```bash
ffmpeg -hide_banner -i narration.wav -af "silencedetect=noise=-34dB:d=0.18" -f null -
```

- `noise=-34dB` — the floor. Raise toward `-30dB` for a noisy or roomy recording, lower toward
  `-40dB` for a clean studio VO. If you get one giant segment, the floor is too low.
- `d=0.18` — the shortest gap that counts. Below ~0.15 you start catching gaps between words;
  above ~0.3 you miss the breaths that make good caption-swap points.

Prefer `hyperframes transcribe` when whisper-cpp is available — word timings let you hit a
single spoken word (a highlight sweep landing exactly on "talk" is worth the setup). Silence
detection is the fallback that never needs installing, and it is enough for scene cuts.

## Choose cut points

1. Rank the pauses by duration. The longest ones are the sentence boundaries the writer meant.
2. Take as many as you need scene boundaries, in time order.
3. Cut at the **midpoint** of each chosen pause, not at its start or end. Starting the next
   scene while the tail of the last word is still ringing sounds clipped; waiting for the pause
   to fully end leaves a hole.
4. Everything else — caption swaps, camera legs, element entrances — hangs off the *speech
   segments* between those cuts, in scene-local time.

## Use the small pauses too

The short breaths inside a long sentence are where a caption should change. Swapping copy
mid-clause is jarring; swapping it in a 0.2s breath is invisible. Map them once and reuse:

```
scene-local = absolute - scene_start
```

Write the scene-local narration into a comment at the top of each composition's `<script>`.
Every timing in that file should be justifiable against those numbers, and the next person to
open the file can check your work without re-measuring.

## Length consequences

Honest cuts change scene durations, and the footage scene usually loses time. Decide
deliberately which end of the clip to drop and **tell the user which and why**. Landing on the
clip's own closing beat as the narration's final clause finishes is usually worth more than
keeping its opening — but it is the user's call, so surface it rather than burying it.

## Verify

The audio's real duration is rarely the round number in the brief. Check it:

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 narration.wav
```

Set the root composition's `data-duration` from that, and confirm the last scene ends at or
just after the final speech segment — never before it.
