# CLAUDE.md — Unrot Skill Video (`unrotskillvid`)

Welcome to **`unrotskillvid`**, the 1-line AI Video Creation Skill & CLI tool for 9:16 vertical reels and explainer videos.

## 1-Line Execution (Everything Handled Automatically)

When the user asks to create a video about any topic:
```bash
npx unrotskillvid "<prompt_or_topic>"
```

### What Happens Automatically:
1. **Script & Scene Structuring**: Writes the script and decomposes the narrative into structured scenes.
2. **Human Voiceover**: Synthesizes 48kHz audio via Gemini TTS or Edge Neural TTS.
3. **Speech-Pause Alignment**: Places scene transitions on real speech pauses.
4. **GSAP Compositions**: Generates 60fps compositions with responsive typography and badges.
5. **Video Rendering**: Automatically renders the finished 1080x1920 MP4 video.

### Examples:
```bash
# General creation:
npx unrotskillvid "Make a SaaS launch reel for an AI coding assistant"

# With Google Gemini TTS voiceover:
npx unrotskillvid "Showcase Supabase Auth launch" --provider gemini --voice Puck
```
