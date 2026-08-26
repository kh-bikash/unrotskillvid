---
name: unrotskillvid
description: >
  1-line AI video creation skill. Autonomously transforms any prompt or topic into a complete 1080x1920
  60fps vertical reel with realistic human voiceover (Gemini TTS, Edge TTS, ElevenLabs, OpenAI),
  dynamic structured scenes, pause alignment, and MP4 rendering in a single command.
---

# Unrot Skill Video (`unrotskillvid`)

Turn any prompt or idea into a complete, ready-to-publish 60fps vertical reel with realistic human voiceover in **one single command**:

```bash
npx unrotskillvid "<your prompt or topic>"
```

---

## ⚡ What Happens in that 1 Line:

1. **Prompt Intelligence**: Analyzes the topic, writes a punchy script, and structures the narrative into dynamic visual scenes.
2. **Human Voiceover Synthesis**: Generates 48kHz broadcast-mastered audio using Gemini TTS, Edge Neural TTS, ElevenLabs, or OpenAI TTS.
3. **Speech-Pause Alignment**: Calculates exact speech pauses so visual scene cuts always land on natural pauses rather than mid-sentence.
4. **GSAP Composition Assembly**: Generates responsive, 60fps HTML5/GSAP compositions with typography, glows, and badges.
5. **Video Rendering**: Automatically renders the finished 1080x1920 60fps MP4 video.

---

## 🎬 1-Line Examples

```bash
# 1. SaaS & Product launches:
npx unrotskillvid "Make a SaaS launch reel for an AI coding assistant"

# 2. Viral explainers & mental models:
npx unrotskillvid "Explain the 80/20 rule in productivity"

# 3. Developer & AI model breakdowns:
npx unrotskillvid "Showcase GLM-4.6 open-weight coding model with SWE-bench scores"

# 4. With Google Gemini TTS voiceover:
npx unrotskillvid "Showcase Supabase Auth launch" --provider gemini --voice Puck
```
