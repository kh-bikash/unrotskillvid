# Master Production Workflow

`unrotskillvid` is a self-contained AI video authoring skill and CLI engine.

---

## 1. Project Initialization
Scaffold any of the 5 pre-built video templates:
```bash
npx unrotskillvid init "my-reel" --type screen-hero
# or: saas-launch, code-walkthrough, faceless-explainer, comparison-vs
```

---

## 2. Voiceover & Audio Mapping
Generate human narration using Gemini TTS, ElevenLabs, OpenAI, or Edge:
```bash
python scripts/tts.py "Your script text" --provider gemini --out videos/my-reel/assets/narration.wav
```
Map pause midpoints to sync timeline cuts with speech:
```bash
python scripts/audio-map.py videos/my-reel/assets/narration.wav --scenes 4 --json videos/my-reel/assets/audio-map.json
```

---

## 3. Composition Authoring
- Sub-compositions in `compositions/scene1.html`, `scene2.html`, etc.
- Root timeline in `index.html` orchestrates scene durations matching `audio-map.json`.
- Continuous narration audio placed at `#root` with `data-start="0"` and `data-duration="<total>"`.

---

## 4. Live Preview & Checking
Start live hot-reloading dev server:
```bash
cd videos/my-reel
npm run dev
```

Run comprehensive layout, motion, contrast, and runtime audit:
```bash
npx unrotskillvid check videos/my-reel
```

---

## 5. Review Content Sheet
Generate contact sheet showing motion states and voiceover captions:
```bash
python scripts/content-sheet.py --frames videos/my-reel/snapshots/frames \
                               --spec videos/my-reel/sheet.json \
                               --out videos/my-reel/snapshots/content-sheet.jpg
```

---

## 6. High-Fidelity 60fps MP4 Render
Render to broadcast-ready 1080x1920 MP4:
```bash
npx unrotskillvid render videos/my-reel
```
