---
name: unrotskillvid
description: >
  Autonomous end-to-end AI video creation skill and NPX CLI tool. Generates complete 9:16 vertical reels
  (1080x1920 60fps) and explainer videos from a single prompt or script with realistic human voiceovers
  (Gemini TTS, Edge TTS, ElevenLabs, OpenAI) and 5 distinct video styles: screen-hero, saas-launch,
  code-walkthrough, faceless-explainer, and comparison-vs. Handles script writing, audio synthesis,
  pause alignment, GSAP composition generation, and MP4 rendering.
---

# Unrot Skill Video (`unrotskillvid`)

An **autonomous end-to-end AI video creation engine** and NPX tool for 9:16 vertical reels (1080x1920, 60fps) with realistic human audio and 5 versatile video styles.

---

## ⚡ 1-Prompt Video Generation

Provide a prompt or topic, and `unrotskillvid` builds the entire video (script, audio, synced timeline, and compositions) automatically:

```bash
# Autonomous generation from prompt
npx unrotskillvid generate "Make a SaaS launch reel for an AI code assistant"

# With automatic 60fps MP4 rendering
npx unrotskillvid generate "Explain the 80/20 rule in productivity" --type faceless-explainer --render

# With Gemini TTS human audio
npx unrotskillvid generate "Showcase Supabase Auth launch" --provider gemini --voice Puck --render
```

---

## 🎨 5 Video Styles & Presets

| Style | Command | Best For |
|---|---|---|
| 📱 **`screen-hero`** | `npx unrotskillvid generate "..." --type screen-hero` | Real screen recordings, demo clips with virtual camera pan/zoom |
| 🚀 **`saas-launch`** | `npx unrotskillvid generate "..." --type saas-launch` | SaaS product reveals, browser mockups, bento grids, pricing CTAs |
| 💻 **`code-walkthrough`** | `npx unrotskillvid generate "..." --type code-walkthrough` | AI models, GitHub repos, code diffs, SWE-bench performance graphs |
| ✨ **`faceless-explainer`** | `npx unrotskillvid generate "..." --type faceless-explainer` | Viral storytelling, mental models, finance (no footage required) |
| ⚖️ **`comparison-vs`** | `npx unrotskillvid generate "..." --type comparison-vs` | Head-to-head battles, feature matrices, benchmark charts, verdicts |

---

## 🎙️ Voiceover & TTS Engine (Gemini TTS, Edge, ElevenLabs, OpenAI)

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

## 🎯 Speech-Synced Audio Timeline Mapping

**Always map cuts to natural speech pauses before timing scenes:**

```bash
python scripts/audio-map.py assets/narration.wav --scenes 4 --json assets/audio-map.json
```

Cuts are placed at the midpoint of speech pauses, ensuring visual transitions never land awkwardly mid-sentence.

---

## 👶 Interactive Creation Wizard

For non-technical users and automated generation:

```bash
npx unrotskillvid create
```
The wizard guides you through choosing a style, writing/pasting a script, selecting a voice, generating audio, mapping timeline cuts, and setting up the live preview.

---

## 🛠️ Verification & Rendering

```bash
# Validate compositions & contrast
npx unrotskillvid check videos/my-reel

# Generate contact review sheet
python scripts/content-sheet.py --frames snapshots/frames --spec sheet.json --out snapshots/content-sheet.jpg

# Render 60fps MP4
npx unrotskillvid render videos/my-reel
```
