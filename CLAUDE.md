# CLAUDE.md — Unrot Skill Video (`unrotskillvid`)

Welcome to **`unrotskillvid`**, the AI Video Creation Skill & CLI tool for high-retention 9:16 vertical reels and explainer videos with dynamic scene counts (2 to 7+ scenes).

## Claude Code Quick Commands

```bash
# 1. Autonomous Dynamic Video Generation (Auto scene count)
node bin/cli.js generate "Create a viral explainer about autonomous AI agents" --render

# 2. Specific Scene Count (e.g. 3-scene fast teaser or 5-scene deep dive)
node bin/cli.js generate "5 step protocol to scale your engineering team" --scenes 5 --render

# 3. Interactive Video Wizard
node bin/cli.js create

# 4. Generate Human Audio (Gemini TTS / Edge / ElevenLabs / OpenAI)
python scripts/tts.py "Your narration text" --provider gemini --out videos/my-video/assets/narration.wav

# 5. Map Speech Cuts for N Scenes
python scripts/audio-map.py videos/my-video/assets/narration.wav --scenes 5 --json videos/my-video/assets/audio-map.json

# 6. Start Live Hot-Reload Preview Server
cd videos/my-video && npm run dev

# 7. Run Full Layout & Contrast Check
node bin/cli.js check videos/my-video

# 8. Render 60fps Vertical MP4
node bin/cli.js render videos/my-video
```

## Dynamic Scene Layout Engine

The engine dynamically formats each scene based on narrative intent:
- `hook-card`: Headline, animated category badge, glass card.
- `bento-grid`: Staggered bento feature cards with glowing icon badges.
- `steps`: Numbered 1-2-3 framework cards with glowing accent borders.
- `metrics`: Live animated percentage progress bars and stat callouts.
- `code`: Editor window with syntax-highlighted diff additions/deletions.
- `payoff`: High-impact stat counters and pulsing action buttons.
