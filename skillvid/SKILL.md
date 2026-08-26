---
name: unrotskillvid
description: >
  Build high-retention vertical reels (9:16) and explainer videos with natural human audio
  (Gemini TTS, ElevenLabs, OpenAI, Edge-TTS) and 5 distinct video styles: screen-hero, saas-launch,
  code-walkthrough, faceless-explainer, and comparison-vs. Self-contained AI video generation skill
  and NPX CLI tool. Use for "make a reel about this feature", "turn this demo/code into a tutorial reel",
  "create a faceless explainer", "generate SaaS launch video", or any vertical video creation request.
---

# Unrot Skill Video (`unrotskillvid`)

A complete, self-contained AI video creation engine and NPX tool for vertical reels (1080x1920, 60fps) with realistic human audio and 5 versatile video templates.

---

## 5 Video Styles & Presets

| Style | Command | Best For |
|---|---|---|
| 📱 **`screen-hero`** | `npx unrotskillvid init my-reel --type screen-hero` | Real screen recordings, demo clips with virtual camera pan/zoom |
| 🚀 **`saas-launch`** | `npx unrotskillvid init my-reel --type saas-launch` | SaaS product reveals, browser mockups, bento grids, pricing CTAs |
| 💻 **`code-walkthrough`** | `npx unrotskillvid init my-reel --type code-walkthrough` | AI models, GitHub repos, code diffs, SWE-bench performance graphs |
| ✨ **`faceless-explainer`** | `npx unrotskillvid init my-reel --type faceless-explainer` | Viral storytelling, mental models, finance (no footage required) |
| ⚖️ **`comparison-vs`** | `npx unrotskillvid init my-reel --type comparison-vs` | Head-to-head battles, feature matrices, benchmark charts, verdicts |

---

## Voiceover & TTS Engine (Gemini TTS, ElevenLabs, OpenAI, Edge)

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

## 1. Speech-Synced Audio Timeline Mapping

**Always map cuts to natural speech pauses before timing scenes:**

```bash
python scripts/audio-map.py assets/narration.wav --scenes 4 --json assets/audio-map.json
```

Cuts are placed at the midpoint of speech pauses, ensuring visual transitions never land awkwardly mid-sentence.

---

## 2. Interactive Creation Wizard

For non-technical users and automated generation:

```bash
npx unrotskillvid create
```
The wizard guides you through choosing a style, writing/pasting a script, selecting a voice, generating audio, mapping timeline cuts, and setting up the live preview.

---

## 3. Composition Rules & Design Law

- **Typography:** Embedded WOFF2 fonts only (`Geist`, `Inter`, etc.) via `scripts/fetch-font.py`. Statements capped at 700 weight.
- **Ambient Glows:** Use radial gradients (`radial-gradient(circle, ...)`) to avoid H.264 banding.
- **Timing & Visibility:** Every animated element requires `class="clip"`, `data-start`, and `data-duration`.
- **GSAP Timelines:** Paused timelines registered on `window.__timelines[compositionId]`.
- **Layout Compliance:** Run `npx unrotskillvid check` before rendering.

---

## 4. Verification & Rendering

```bash
# Validate compositions & contrast
npx unrotskillvid check videos/my-reel

# Generate contact review sheet
python scripts/content-sheet.py --frames snapshots/frames --spec sheet.json --out snapshots/content-sheet.jpg

# Render 60fps MP4
npx unrotskillvid render videos/my-reel
```
