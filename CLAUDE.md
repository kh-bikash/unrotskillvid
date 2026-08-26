# CLAUDE.md — Unrot Skill Video (`unrotskillvid`)

Welcome to **`unrotskillvid`**, the AI Video Creation Skill & CLI tool for high-retention 9:16 vertical reels and explainer videos.

## Claude Code Quick Commands

```bash
# 1. Autonomous Prompt-to-Video Generation (End-to-End)
node bin/cli.js generate "Create a viral explainer about autonomous AI agents" --render

# 2. Interactive Video Wizard
node bin/cli.js create

# 3. Scaffold a Specific Video Style
node bin/cli.js init my-video --type screen-hero
# Available types: screen-hero, saas-launch, code-walkthrough, faceless-explainer, comparison-vs

# 4. Generate Human Audio (Gemini TTS / Edge / ElevenLabs / OpenAI)
python scripts/tts.py "Your narration text" --provider gemini --out videos/my-video/assets/narration.wav

# 5. Map Speech Cuts & Audio Pauses
python scripts/audio-map.py videos/my-video/assets/narration.wav --scenes 4 --json videos/my-video/assets/audio-map.json

# 6. Start Live Hot-Reload Preview Server
cd videos/my-video && npm run dev

# 7. Run Full Layout & Contrast Check
node bin/cli.js check videos/my-video

# 8. Render 60fps Vertical MP4
node bin/cli.js render videos/my-video
```

## Video Template Types

1. **`screen-hero`**: Screen recording / product demo hero reel with virtual camera moves.
2. **`saas-launch`**: SaaS product reveal with browser mockups, bento grids, and launch CTA.
3. **`code-walkthrough`**: Developer & AI model showcase with code diffs, terminal animations, and benchmarks.
4. **`faceless-explainer`**: Viral faceless explainer with kinetic typography & bento cards (no footage needed).
5. **`comparison-vs`**: Side-by-side battle / vs comparison reel with feature matrix & verdict.

## Key Framework Rules

- Every timed element must have `class="clip"`, `data-start`, and `data-duration`.
- GSAP timelines must be paused and attached to `window.__timelines[compName]`.
- Always map real voiceover pauses via `scripts/audio-map.py` before placing scene transitions.
- Use embedded WOFF2 fonts (`assets/fonts/`) to prevent rendering fallbacks.
