---
name: unrotskillvid
description: >
  Autonomous dynamic AI video creation skill and NPX CLI tool. Generates complete, structured 9:16
  vertical reels (1080x1920 60fps) and explainer videos from a single prompt with any number of scenes
  (2 to 7+ scenes dynamically determined by narrative depth), realistic human voiceovers (Gemini TTS,
  Edge TTS, ElevenLabs, OpenAI), speech-pause synchronization, custom GSAP compositions, and 60fps rendering.
---

# Unrot Skill Video (`unrotskillvid`)

An **autonomous, dynamic multi-scene AI video creation engine** and NPX tool for 9:16 vertical reels (1080x1920, 60fps) with realistic human audio and intelligent scene structuring.

---

## ⚡ 1-Prompt Dynamic Video Generation

`unrotskillvid` dynamically calculates the optimal number of scenes (2 to 7+ scenes) based on your prompt:

```bash
# Dynamic scene generation (AI automatically determines 2 to 7 scenes)
npx unrotskillvid generate "Make a SaaS launch reel for an AI coding assistant"

# Explicit scene count (e.g. 3-scene fast teaser or 5-scene deep dive)
npx unrotskillvid generate "5 step protocol to scale your engineering team" --scenes 5 --render

# With Google Gemini TTS human voiceover
npx unrotskillvid generate "Showcase Supabase Auth launch" --provider gemini --voice Puck --render
```

---

## 🎭 Dynamic Scene Layout Engine

Every scene receives a tailored, high-polish visual structure with GSAP animations:

- **`hook-card`**: Headline typography, animated category badges, floating glass cards.
- **`bento-grid`**: Staggered bento feature cards with glowing icon badges and bottom captions.
- **`steps` / `protocol`**: Numbered 1-2-3 framework cards with glowing accent borders.
- **`metrics` / `benchmarks`**: Live animated percentage progress bars and stat callouts.
- **`code` / `terminal`**: macOS editor windows with syntax-highlighted diff additions/deletions.
- **`payoff` / `cta`**: High-impact stat counters and pulsing action buttons.

---

## 🎙️ Human Voiceover & TTS Engine (Gemini TTS, Edge, ElevenLabs, OpenAI)

Generate 48kHz broadcast-quality voiceovers:

```bash
# Gemini TTS (Google GenAI Natural Human Audio)
python scripts/tts.py "Your narration script here" --provider gemini --voice Puck --out assets/narration.wav

# Edge Neural TTS (Free, built-in, instant high quality)
python scripts/tts.py "Your narration script here" --provider edge --voice en-US-ChristopherNeural --out assets/narration.wav

# ElevenLabs TTS (Studio voice cloning)
python scripts/tts.py "Your narration script here" --provider elevenlabs --voice Adam --out assets/narration.wav

# OpenAI TTS (tts-1-hd)
python scripts/tts.py "Your narration script here" --provider openai --voice onyx --out assets/narration.wav
```

List all available voices:
```bash
npx unrotskillvid list-voices
```

---

## 🎯 Speech-Synced Timeline Mapping

**Every cut lands on a real speech pause:**

```bash
python scripts/audio-map.py assets/narration.wav --scenes <N> --json assets/audio-map.json
```

Cuts are calculated at the midpoint of speech pauses so visual scene changes never land awkwardly mid-sentence.

---

## 👶 Interactive Creation Wizard

For non-technical users:

```bash
npx unrotskillvid create
```
Guides you through entering a prompt, choosing an optional scene count (3 to 6 or auto), selecting a voice, and creating the video.

---

## 🛠️ Verification & Rendering

```bash
# Validate compositions & contrast
npx unrotskillvid check videos/my-reel

# Render 60fps MP4
npx unrotskillvid render videos/my-reel
```
