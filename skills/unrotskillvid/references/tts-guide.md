# Human-like TTS Voice Engine Guide

`unrotskillvid` supports 4 industry-leading Text-To-Speech providers with automatic fallback and broadcast-standard 48kHz stereo mastering.

---

## 1. Google Gemini TTS (Natural Conversational Voice)

Gemini's audio generation models deliver natural cadence, realistic human inflection, and dynamic tone.

### Setup
Set your Gemini API key in your environment:
```bash
# Windows PowerShell
$env:GEMINI_API_KEY = "your-api-key-here"

# Mac / Linux / Bash
export GEMINI_API_KEY="your-api-key-here"
```

### Supported Voices
- `Puck` — Crisp, conversational, engaging male tech voice (Default)
- `Charon` — Deep, authoritative, cinematic male narrator
- `Kore` — Warm, natural, clear female explainer
- `Fenrir` — Energetic, dynamic, modern launch voice
- `Aoede` — Articulate, polished female storyteller

### CLI Command
```bash
npx unrotskillvid audio "Script text here" --provider gemini --voice Puck --out assets/narration.wav
```

---

## 2. Microsoft Edge Neural TTS (Free, Zero Config)

Free, built-in, and requires **no API keys**. Uses state-of-the-art neural models.

### Recommended Voices
- `en-US-ChristopherNeural` — Balanced, punchy American tech narrator (Default)
- `en-US-JennyNeural` — Bright, confident, modern SaaS commercial voice
- `en-US-GuyNeural` — Casual, conversational, relatable male voice
- `en-US-AriaNeural` — Articulate, smooth, professional female voice
- `en-GB-SoniaNeural` — Sophisticated British documentary voice
- `en-GB-RyanNeural` — Energetic British tech explainer

### CLI Command
```bash
npx unrotskillvid audio "Script text here" --provider edge --voice en-US-ChristopherNeural --out assets/narration.wav
```

---

## 3. ElevenLabs TTS (Studio-Quality Voice Cloning)

Studio-grade fidelity and emotional depth.

### Setup
```bash
export ELEVENLABS_API_KEY="your-elevenlabs-api-key"
```

### Supported Voices
- `Rachel` (`21m00Tcm4TlvDq8ikWAM`) — Calm, narrative, conversational
- `Adam` (`pNInz6obpgDQGcFmaJgB`) — Deep, dominant, authoritative
- `Antoni` (`ErXwobaYiN019PkySvjV`) — Friendly, tech explainer
- `Josh` (`TxGEqnHWrfWFTfGW9XjX`) — Young, high-energy YouTube/Reels tone
- `Bella` (`EXAVITQu4vr4xnSDxMaL`) — Expressive commercial read

---

## 4. OpenAI TTS (tts-1-hd)

Clear, expressive, and studio-mastered.

### Setup
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

### Supported Voices
- `onyx` — Deep, smooth, authoritative tech reel voice (Default)
- `nova` — Energetic, friendly, conversational female voice
- `alloy` — Neutral, balanced, versatile
- `echo` — Warm, rounded, podcast tone
- `fable` — Expressive British storytelling voice
- `shimmer` — Bright, upbeat female voice

---

## Audio Post-Processing Pipeline

Every generated audio file automatically undergoes FFmpeg post-processing:
1. **Loudness Normalization:** `loudnorm=I=-16:TP=-1.5:LRA=11` (EBU R128 standard for mobile vertical video platforms).
2. **Resampling:** Resampled to 48,000 Hz, 2-channel 16-bit PCM WAV.
3. **Metadata Indexing:** Saves `audio-meta.json` with duration, word count, sample rate, and provider info.
