# 🎬 unrotskillvid

<div align="center">

### **1-Line AI Video Creation Skill & CLI for 60fps Vertical Reels**

**Turn any prompt or idea into a complete, structured 60fps 9:16 vertical reel with natural human voiceover in one single command.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green.svg)](https://nodejs.org)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Resolution](https://img.shields.io/badge/Resolution-1080x1920%20(9%3A16)-orange.svg)]()
[![Frame Rate](https://img.shields.io/badge/Frame%20Rate-60fps-purple.svg)]()

---

</div>

## 🚀 1-Line Quick Start

Just run `npx unrotskillvid` with your prompt:

```bash
npx unrotskillvid "Make a SaaS launch reel for an AI coding assistant"
```

**That's it! In that single command, the skill automatically:**
1. ✍️ **Writes the script** and breaks down the topic into structured visual scenes.
2. 🎙️ **Synthesizes 48kHz human voiceover audio** (Gemini TTS / Edge Neural TTS).
3. 🎯 **Aligns scene cuts** to speech pauses so transitions never cut mid-sentence.
4. 🎨 **Builds 60fps GSAP/HTML5 compositions** with responsive typography, badges, and cards.
5. 🎬 **Renders the finished 1080x1920 MP4 video**.

---

## ⚡ 1-Line Examples

```bash
# 1. SaaS product launches:
npx unrotskillvid "Make a SaaS launch reel for an AI coding assistant"

# 2. Viral explainers & mental models:
npx unrotskillvid "Explain the 80/20 rule in productivity"

# 3. Developer & AI model breakdowns:
npx unrotskillvid "Showcase GLM-4.6 open-weight coding model with SWE-bench scores"

# 4. With Google Gemini TTS human voiceover:
npx unrotskillvid "Showcase Supabase Auth launch" --provider gemini --voice Puck
```

Or launch the interactive prompt wizard:

```bash
npx unrotskillvid
```

---

## 🎙️ Human Voiceover Options

`unrotskillvid` supports 4 TTS providers with automatic fallback:

| Provider | Setup | Default Voice | Tone |
|---|---|---|---|
| 🟢 **Edge Neural TTS** | **Free & Built-in (Zero config)** | `en-US-ChristopherNeural` | Natural tech narrator, punchy & crisp |
| 🔵 **Google Gemini TTS** | `export GEMINI_API_KEY="..."` | `Puck` | Conversational, realistic human inflection |
| 🟣 **ElevenLabs** | `export ELEVENLABS_API_KEY="..."` | `Adam` / `Rachel` | Studio-grade voice cloning |
| ⚪ **OpenAI TTS** | `export OPENAI_API_KEY="..."` | `onyx` | Deep, smooth tech reel voice |

List all available voices:
```bash
npx unrotskillvid list-voices
```

---

## 🤖 Claude Code & Codex Agent Setup

`unrotskillvid` is fully optimized as an AI skill for Claude Code, Codex, Antigravity, Cursor, and Windsurf.

### For Claude Code:
Include `CLAUDE.md` and `SKILL.md` in your project workspace. Claude Code will execute `unrotskillvid` commands when prompted:
> *"Create a vertical reel about our new AI feature with Gemini TTS voiceover."*

### For Codex & OpenAI Agents:
Refer to `AGENTS.md` and `SKILL.md` for 1-command deterministic execution.

---

## 🛠️ CLI Command Reference

| Command | Description |
|---|---|
| `npx unrotskillvid "<prompt>"` | **1-Line execution**: Writes script, generates audio, builds scenes, renders MP4 |
| `npx unrotskillvid` | Interactive step-by-step video creator wizard |
| `npx unrotskillvid list-voices` | Display full voice catalog across all TTS providers |
| `npx unrotskillvid list-types` | List available visual styles |
| `npx unrotskillvid render [dir]` | Render existing project directory to 60fps MP4 |

---

## 📄 License

MIT License © 2026 [Bikash](https://github.com/kh-bikash). Free to use, modify, and distribute for personal and commercial projects.
