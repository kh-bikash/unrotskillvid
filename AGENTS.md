# AGENTS.md — Agent & Codex Guidelines for `unrotskillvid`

This document defines the agent execution model for generating, customizing, and rendering dynamic vertical reels and explainer videos using `unrotskillvid`.

## Overview

`unrotskillvid` autonomously transforms any prompt, script, or footage into a 1080x1920 60fps vertical reel with any number of structured scenes (2 to 7+ scenes) and human-quality TTS audio (Gemini TTS, ElevenLabs, OpenAI, Edge-TTS).

## Autonomous 1-Command Execution

When the user asks to create a video from a prompt or topic:
```bash
python scripts/generate-reel.py "<user_prompt>" [--scenes <N>] [--provider <auto|gemini|edge|elevenlabs|openai>] --render
```

## Step-by-Step Agent Execution Checklist

1. **Synthesize & Scaffold**:
   Run `node bin/cli.js generate "<prompt>" [--scenes <N>]`
   Dynamically determines optimal scene count (e.g. 3, 4, 5, or 6 scenes) or accepts explicit count.

2. **Generate Narration Audio**:
   Synthesizes 48kHz audio into `assets/narration.wav`:
   `python scripts/tts.py "<script_content>" --provider <auto|gemini|elevenlabs|openai|edge> --out <project>/assets/narration.wav`

3. **Calculate Pause-Aligned Timeline**:
   Run `python scripts/audio-map.py <project>/assets/narration.wav --scenes <N> --json <project>/assets/audio-map.json`
   Extracts cut points and synchronizes scene `data-start` and `data-duration` in `<project>/index.html`.

4. **Verify Compositions**:
   Run `node bin/cli.js check <project>` to ensure layout, contrast, and motion rules pass.

5. **Render Video**:
   Run `node bin/cli.js render <project>` to produce the final MP4.
