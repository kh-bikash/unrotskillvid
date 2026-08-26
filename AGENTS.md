# AGENTS.md — Agent & Codex Guidelines for `unrotskillvid`

This document defines the agent execution model for generating, customizing, and rendering vertical reels and explainer videos using `unrotskillvid`.

## Overview

`unrotskillvid` generates 1080x1920 60fps vertical reels using HTML5/GSAP compositions with human-quality TTS audio (Gemini TTS, ElevenLabs, OpenAI, Edge-TTS).

## Agent Execution Checklist

1. **Scaffold Project**:
   Run `node bin/cli.js init <project-name> --type <template-type>`
   Templates: `screen-hero`, `saas-launch`, `code-walkthrough`, `faceless-explainer`, `comparison-vs`.

2. **Generate Narration Audio**:
   Synthesize script into `assets/narration.wav`:
   `python scripts/tts.py "<script_content>" --provider <auto|gemini|elevenlabs|openai|edge> --out <project>/assets/narration.wav`

3. **Calculate Pause-Aligned Timeline**:
   Run `python scripts/audio-map.py <project>/assets/narration.wav --scenes 4 --json <project>/assets/audio-map.json`
   Extract cut points and set scene `data-start` and `data-duration` attributes in `<project>/index.html`.

4. **Verify Compositions**:
   Run `node bin/cli.js check <project>` to ensure layout, contrast, and motion rules pass.

5. **Render Video**:
   Run `node bin/cli.js render <project>` to produce the final MP4.
