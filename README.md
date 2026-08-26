# 🎬 unrotskillvid

<div align="center">

### **AI Video Creation Skill & CLI for High-Retention Vertical Reels & Explainers**

**Turn any prompt or topic into a complete 60fps 9:16 vertical reel with structured scenes (2 to 7+ scenes) and natural human voiceovers in a single command.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green.svg)](https://nodejs.org)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Resolution](https://img.shields.io/badge/Resolution-1080x1920%20(9%3A16)-orange.svg)]()
[![Frame Rate](https://img.shields.io/badge/Frame%20Rate-60fps-purple.svg)]()

[Dynamic Scene Generation](#-dynamic-scene-generation) • [Human Audio & Gemini TTS](#-human-audio--gemini-tts) • [Scene Layout Styles](#-scene-layout-styles) • [Non-Tech User Guide](#-non-tech-friendly-guide) • [Claude & Codex Setup](#-claude-code--codex-agent-setup) • [CLI Reference](#-cli-command-reference)

---

</div>

## ⚡ Dynamic Scene Generation

`unrotskillvid` is not locked to a fixed scene count. It intelligently analyzes your prompt and builds the ideal number of structured scenes (2 to 7+ scenes):

```bash
# Auto scene calculation (AI decides 2-7 scenes based on depth)
npx unrotskillvid generate "Make a SaaS launch reel for an AI coding assistant"

# Fast 3-scene teaser
npx unrotskillvid generate "Announce our new vector database update" --scenes 3 --render

# In-depth 5-scene framework or tutorial
npx unrotskillvid generate "5 step protocol to scale your engineering team" --scenes 5 --render

# With Google Gemini TTS human voiceover
npx unrotskillvid generate "Showcase Supabase Auth launch" --provider gemini --voice Puck --render
```

Or launch the interactive wizard:

```bash
npx unrotskillvid
```

---

## 🎭 Scene Layout Styles

Every generated scene receives a structured, high-polish visual layout with GSAP animations:

| Layout Type | Description | Best For |
|---|---|---|
| 🪝 **`hook-card`** | Punchy headline, glowing badge, and floating glass character card | Opening hook statements |
| 🍱 **`bento-grid`** | Staggered 3-card bento grid with neon icons and bottom caption | Feature highlights & capabilities |
| 📋 **`steps` / `protocol`** | Numbered 1-2-3 framework card with glowing accent border | Actionable steps & protocols |
| 📊 **`metrics`** | Live animating percentage progress bars and stat tags | Benchmarks & performance data |
| 💻 **`code`** | macOS editor window with syntax-highlighted diff additions/deletions | Developer demos & refactors |
| 🏆 **`payoff`** | Big stat counter (e.g. 10x / 68.1%) and pulsing action button | Final verdict & call to action |

---

## 🎙️ Human Audio & Gemini TTS

Generate realistic, natural human voiceovers with broadcast-standard 48kHz stereo mastering:

### 1. Google Gemini TTS
Natural inflection and expressive tone:
```bash
# Set your API key
export GEMINI_API_KEY="your-gemini-api-key"

# Generate voiceover (Voices: Puck, Charon, Kore, Fenrir, Aoede)
npx unrotskillvid audio "Your voiceover script here" --provider gemini --voice Puck --out assets/narration.wav
```

### 2. Edge Neural TTS (Free & Built-in — Zero Setup!)
Free, ultra-natural neural voices with no API key required:
```bash
npx unrotskillvid audio "Your voiceover script here" --provider edge --voice en-US-ChristopherNeural --out assets/narration.wav
```

### 3. ElevenLabs & OpenAI TTS
```bash
# ElevenLabs (Voices: Rachel, Adam, Antoni, Josh, Bella)
npx unrotskillvid audio "Script" --provider elevenlabs --voice Adam --out assets/narration.wav

# OpenAI tts-1-hd (Voices: onyx, nova, alloy, echo, fable, shimmer)
npx unrotskillvid audio "Script" --provider openai --voice onyx --out assets/narration.wav
```

List all available voices anytime:
```bash
npx unrotskillvid list-voices
```

---

## 🎯 Speech-Synced Timeline Cuts

Visual cuts should **always** land on natural speech pauses, never mid-sentence:

```bash
npx unrotskillvid map assets/narration.wav --scenes 5 --json assets/audio-map.json
```

Output gives you the exact start and duration timestamps for all $N$ scenes to paste into your `index.html` composition.

---

## 👶 Non-Tech Friendly Guide

You don't need any coding skills to create viral videos with `unrotskillvid`:

1. **Open your terminal** (Terminal on Mac/Linux or PowerShell on Windows).
2. **Type:** `npx unrotskillvid generate "Your video idea or topic"` and hit Enter.
3. **Done!** The tool will automatically break down the topic into structured scenes, write the script, record the voiceover, sync visual transitions to speech pauses, and prepare your 60fps vertical reel.
4. **Render to MP4:**
   ```bash
   npx unrotskillvid render videos/my-video
   ```

---

## 🤖 Claude Code & Codex Agent Setup

`unrotskillvid` is fully optimized as an AI skill for Claude Code, Codex, Antigravity, Cursor, and Windsurf.

### For Claude Code:
Include `CLAUDE.md` and `SKILL.md` in your project workspace. Claude Code will automatically detect the skill and execute `unrotskillvid` commands when you prompt:
> *"Create a 9:16 vertical reel about our new AI feature with Gemini TTS voiceover."*

### For Codex & OpenAI Agents:
Refer to `AGENTS.md` and `SKILL.md` for deterministic step execution, pause synchronization, and automated 60fps rendering.

---

## 🛠️ CLI Command Reference

| Command | Description |
|---|---|
| `npx unrotskillvid generate "<prompt>" [--scenes <n>] [--render]` | Autonomous dynamic prompt-to-video generation end-to-end |
| `npx unrotskillvid create` | Launch interactive step-by-step video creator wizard |
| `npx unrotskillvid init <name> [--type <t>]` | Scaffold a new project template |
| `npx unrotskillvid audio <script> [--provider <p>]` | Generate broadcast-quality 48kHz WAV audio |
| `npx unrotskillvid map <audio.wav> [--scenes <n>]` | Analyze speech pauses and calculate cut points |
| `npx unrotskillvid check [dir]` | Run full layout audit, contrast check, and linting |
| `npx unrotskillvid render [dir]` | Render 1080x1920 60fps MP4 video |
| `npx unrotskillvid list-types` | List available video styles |
| `npx unrotskillvid list-voices` | Display full voice catalog across all TTS providers |

---

## 📄 License

MIT License © 2026 [Bikash](https://github.com/kh-bikash). Free to use, modify, and distribute for personal and commercial projects.
