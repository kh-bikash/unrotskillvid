# 🎬 unrotskillvid

<div align="center">

### **AI Video Creation Skill & CLI for High-Retention Vertical Reels & Explainers**

**Turn product demos, screen recordings, SaaS launches, code diffs, or faceless AI concepts into stunning 60fps 9:16 vertical reels with human voiceovers.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green.svg)](https://nodejs.org)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Resolution](https://img.shields.io/badge/Resolution-1080x1920%20(9%3A16)-orange.svg)]()
[![Frame Rate](https://img.shields.io/badge/Frame%20Rate-60fps-purple.svg)]()

[Quick Start](#-quick-start) • [5 Video Styles](#-5-video-styles) • [Human Audio & Gemini TTS](#-human-audio--gemini-tts) • [Non-Tech User Guide](#-non-tech-friendly-guide) • [Claude & Codex Setup](#-claude-code--codex-agent-setup) • [CLI Reference](#-cli-command-reference)

---

</div>

## 🚀 Quick Start

Run the interactive creation wizard directly with `npx` (zero installation needed):

```bash
npx unrotskillvid
```

Or clone the repository and launch:

```bash
git clone https://github.com/kh-bikash/unrotskillvid.git
cd unrotskillvid
npm start
```

---

## 🎨 5 Video Styles

`unrotskillvid` includes 5 pre-built, tested, 60fps vertical reel templates designed for maximum retention across TikTok, Instagram Reels, YouTube Shorts, and X:

| Style | Description | Command | Best For |
|---|---|---|---|
| 📱 **`screen-hero`** | Screen recording hero with smooth virtual camera pans, floating cards, and bottom captions | `npx unrotskillvid init my-reel --type screen-hero` | Product demos, UI walkthroughs, tech news |
| 🚀 **`saas-launch`** | Modern browser mockup, 3-card bento feature grid, glowing stats, and launch CTA | `npx unrotskillvid init my-reel --type saas-launch` | SaaS launches, feature reveals, Product Hunt |
| 💻 **`code-walkthrough`** | Syntax-highlighted code diffs, terminal execution animations, and SWE-bench benchmark bars | `npx unrotskillvid init my-reel --type code-walkthrough` | AI models, developer tools, GitHub repos, PRs |
| ✨ **`faceless-explainer`** | Kinetic typography, glowing badges, 80/20 leverage protocol, and takeaway cards (**no footage needed**) | `npx unrotskillvid init my-reel --type faceless-explainer` | Mental models, storytelling, finance, viral facts |
| ⚔️ **`comparison-vs`** | Head-to-head showdown, 4-row feature matrix table, speed/cost charts, and final verdict | `npx unrotskillvid init my-reel --type comparison-vs` | Model A vs B, tool comparisons, benchmark reviews |

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
npx unrotskillvid map assets/narration.wav --scenes 4 --json assets/audio-map.json
```

Output gives you the exact start and duration timestamps to paste into your `index.html` composition.

---

## 👶 Non-Tech Friendly Guide

You don't need any coding skills to create viral videos with `unrotskillvid`:

1. **Open your terminal** (Terminal on Mac/Linux or PowerShell on Windows).
2. **Type:** `npx unrotskillvid create` and hit Enter.
3. **Follow the on-screen prompts:**
   - Name your video.
   - Pick your favorite video style (1 to 5).
   - Paste what you want the voice to say.
   - Choose a voice.
4. **Done!** The tool will automatically create your video project, record the voiceover, and prepare your 60fps vertical reel.
5. **Render to MP4:**
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
| `npx unrotskillvid` | Launch interactive step-by-step video creator wizard |
| `npx unrotskillvid create` | Launch interactive step-by-step video creator wizard |
| `npx unrotskillvid init <name> [--type <t>]` | Scaffold a new project (`screen-hero`, `saas-launch`, `code-walkthrough`, `faceless-explainer`, `comparison-vs`) |
| `npx unrotskillvid audio <script> [--provider <p>]` | Generate broadcast-quality 48kHz WAV audio |
| `npx unrotskillvid map <audio.wav> [--scenes <n>]` | Analyze speech pauses and calculate cut points |
| `npx unrotskillvid check [dir]` | Run full layout audit, contrast check, and linting |
| `npx unrotskillvid render [dir]` | Render 1080x1920 60fps MP4 video |
| `npx unrotskillvid list-types` | List all 5 video templates with usage guidelines |
| `npx unrotskillvid list-voices` | Display full voice catalog across all TTS providers |

---

## 📁 Repository Structure

```
unrotskillvid/
├── bin/
│   └── cli.js                  # Interactive CLI entrypoint (npx unrotskillvid)
├── scripts/
│   ├── tts.py                  # Multi-provider TTS engine (Gemini, ElevenLabs, OpenAI, Edge)
│   ├── audio-map.py            # Speech pause & cut point analyzer
│   ├── fetch-font.py           # Google Fonts WOFF2 downloader
│   └── content-sheet.py        # Review contact sheet generator
├── templates/
│   ├── screen-hero/            # Product Demo Hero template
│   ├── saas-launch/            # SaaS Product Launch template
│   ├── code-walkthrough/       # Code & Developer Demo template
│   ├── faceless-explainer/     # Viral Faceless Explainer template
│   └── comparison-vs/          # Comparison & VS Battle template
├── references/
│   ├── video-types.md          # Guide to all 5 video styles
│   ├── tts-guide.md            # Complete TTS setup guide
│   ├── workflow.md             # Production lifecycle guide
│   ├── design-law.md           # Visual design and contrast laws
│   ├── camera.md               # Virtual camera movement physics
│   └── audio-cutting.md        # Speech cut placement rules
├── SKILL.md                    # Master AI Skill definition
├── CLAUDE.md                   # Claude Code guidelines
├── AGENTS.md                   # Codex & Agent execution spec
├── package.json                # NPM package & bin config
└── README.md                   # Project documentation
```

---

## 📄 License

MIT License © 2026 [Bikash](https://github.com/kh-bikash). Free to use, modify, and distribute for personal and commercial projects.
