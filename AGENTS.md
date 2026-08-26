# AGENTS.md — Agent & Codex Guidelines for `unrotskillvid`

This document defines the agent execution model for generating vertical reels and explainer videos using `unrotskillvid`.

## 1-Command Autonomous Execution

When the user asks to create a video from a prompt or topic:
```bash
npx unrotskillvid "<user_prompt>"
```

The CLI autonomously writes the script, determines the optimal structured scene count, synthesizes 48kHz human voiceover audio, aligns speech pauses, generates 60fps GSAP compositions, and renders the finished MP4 video.
