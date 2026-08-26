#!/usr/bin/env python3
"""Multi-provider TTS engine for unrotskillvid.

Supports:
- Gemini TTS (Google Gemini Generative Audio API)
- ElevenLabs (Studio-quality voice cloning and neural voices)
- OpenAI TTS (tts-1-hd with realistic human voices)
- Edge-TTS (Free, zero-config neural voices with natural cadence)

Outputs broadcast-quality 48kHz stereo WAV ready for timeline mapping.

Usage:
    python scripts/tts.py "Your voiceover script text goes here." --out assets/narration.wav
    python scripts/tts.py script.txt --provider gemini --voice Aoede --out assets/narration.wav
    python scripts/tts.py script.txt --provider elevenlabs --voice Adam --out assets/narration.wav
    python scripts/tts.py script.txt --provider openai --voice onyx --out assets/narration.wav
    python scripts/tts.py script.txt --provider edge --voice en-US-ChristopherNeural --out assets/narration.wav
"""

import argparse
import asyncio
import base64
import json
import os
import subprocess
import sys
import tempfile
import urllib.request
import urllib.parse
import urllib.error

# Default voices per provider
DEFAULT_VOICES = {
    "gemini": "Puck",  # Options: Puck, Charon, Kore, Fenrir, Aoede
    "elevenlabs": "21m00Tcm4TlvDq8ikWAM",  # Rachel (or custom ID / name)
    "openai": "onyx",  # Options: alloy, echo, fable, onyx, nova, shimmer
    "edge": "en-US-ChristopherNeural",  # Options: en-US-ChristopherNeural, en-US-JennyNeural, en-US-GuyNeural, en-GB-SoniaNeural
}

VOICE_CATALOG = {
    "gemini": [
        {"id": "Puck", "name": "Puck", "gender": "Male", "tone": "Engaging, conversational, crisp tech voice"},
        {"id": "Charon", "name": "Charon", "gender": "Male", "tone": "Deep, authoritative, cinematic narrator"},
        {"id": "Kore", "name": "Kore", "gender": "Female", "tone": "Warm, natural, clear explainer"},
        {"id": "Fenrir", "name": "Fenrir", "gender": "Male", "tone": "Energetic, dynamic, modern launch voice"},
        {"id": "Aoede", "name": "Aoede", "gender": "Female", "tone": "Professional, articulate, polished storyteller"},
    ],
    "elevenlabs": [
        {"id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel", "gender": "Female", "tone": "Calm, conversational, narrative"},
        {"id": "pNInz6obpgDQGcFmaJgB", "name": "Adam", "gender": "Male", "tone": "Dominant, deep, authoritative"},
        {"id": "ErXwobaYiN019PkySvjV", "name": "Antoni", "gender": "Male", "tone": "Friendly, tech explainer"},
        {"id": "TxGEqnHWrfWFTfGW9XjX", "name": "Josh", "gender": "Male", "tone": "Young, energetic, YouTube / Reel style"},
        {"id": "EXAVITQu4vr4xnSDxMaL", "name": "Bella", "gender": "Female", "tone": "Expressive, engaging commercial read"},
    ],
    "openai": [
        {"id": "onyx", "name": "Onyx", "gender": "Male", "tone": "Deep, smooth, authoritative tech reel voice"},
        {"id": "nova", "name": "Nova", "gender": "Female", "tone": "Energetic, friendly, conversational"},
        {"id": "alloy", "name": "Alloy", "gender": "Neutral", "tone": "Balanced, clear, versatile"},
        {"id": "echo", "name": "Echo", "gender": "Male", "tone": "Warm, rounded, podcast tone"},
        {"id": "fable", "name": "Fable", "gender": "British/Neutral", "tone": "Expressive, storytelling cadence"},
        {"id": "shimmer", "name": "Shimmer", "gender": "Female", "tone": "Clear, bright, upbeat"},
    ],
    "edge": [
        {"id": "en-US-ChristopherNeural", "name": "Christopher", "gender": "Male", "tone": "Natural tech narrator, balanced, punchy"},
        {"id": "en-US-JennyNeural", "name": "Jenny", "gender": "Female", "tone": "Bright, confident, modern SaaS voice"},
        {"id": "en-US-GuyNeural", "name": "Guy", "gender": "Male", "tone": "Casual, conversational, relatable"},
        {"id": "en-US-AriaNeural", "name": "Aria", "gender": "Female", "tone": "Articulate, smooth, professional"},
        {"id": "en-GB-SoniaNeural", "name": "Sonia (UK)", "gender": "Female", "tone": "Sophisticated British documentary style"},
        {"id": "en-GB-RyanNeural", "name": "Ryan (UK)", "gender": "Male", "tone": "Energetic British tech explainer"},
    ]
}


def read_script(source: str) -> str:
    """Read script from a file path or use as raw string text."""
    if os.path.exists(source):
        with open(source, "r", encoding="utf-8") as f:
            return f.read().strip()
    return source.strip()


def run_cmd(cmd):
    """Run subprocess command and return result."""
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def convert_to_broadcast_wav(input_audio: str, output_wav: str):
    """Convert any audio format to 48kHz stereo 16-bit PCM WAV using FFmpeg."""
    os.makedirs(os.path.dirname(os.path.abspath(output_wav)), exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-i", input_audio,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-ar", "48000", "-ac", "2",
        output_wav
    ]
    r = run_cmd(cmd)
    if r.returncode != 0:
        # Fallback without loudnorm filter if filter fails
        cmd_fallback = [
            "ffmpeg", "-y", "-i", input_audio,
            "-ar", "48000", "-ac", "2",
            output_wav
        ]
        r2 = run_cmd(cmd_fallback)
        if r2.returncode != 0:
            raise RuntimeError(f"FFmpeg conversion failed:\n{r2.stderr}")


def get_audio_duration(path: str) -> float:
    """Get audio duration in seconds via ffprobe."""
    r = run_cmd([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", path
    ])
    if r.returncode == 0 and r.stdout.strip():
        try:
            return float(r.stdout.strip())
        except ValueError:
            pass
    return 0.0


# -------------------------------------------------------------
# Provider 1: Google Gemini TTS
# -------------------------------------------------------------
def generate_gemini_tts(text: str, voice: str, output_path: str) -> bool:
    """Synthesize speech using Google Gemini API."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("[TTS] GEMINI_API_KEY / GOOGLE_API_KEY not found in environment.")
        return False

    print(f"[TTS] Generating speech with Gemini TTS (Voice: {voice})...")
    
    # Try using google.generativeai if available
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # Try gemini-2.0-flash speech synthesis or direct REST endpoint
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"Please read this narration text aloud with a natural, clear cadence:\n\n{text}"
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "audio/mp3"}
        )
        if hasattr(response, "candidates") and response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "inline_data") and part.inline_data:
                    data = base64.b64decode(part.inline_data.data)
                    with open(output_path, "wb") as f:
                        f.write(data)
                    return True
    except Exception as e:
        print(f"[TTS] Gemini SDK method: {e}. Trying Gemini REST audio endpoint...")

    # Fallback to direct Gemini REST Audio Generation
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [{"text": f"Read aloud naturally: {text}"}]
            }],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {
                    "voiceConfig": {
                        "prebuiltVoiceConfig": {
                            "voiceName": voice
                        }
                    }
                }
            }
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                for p in parts:
                    if "inlineData" in p and "data" in p["inlineData"]:
                        audio_bytes = base64.b64decode(p["inlineData"]["data"])
                        with open(output_path, "wb") as f:
                            f.write(audio_bytes)
                        return True
    except Exception as e:
        print(f"[TTS] Gemini REST failed: {e}")
        
    return False


# -------------------------------------------------------------
# Provider 2: ElevenLabs TTS
# -------------------------------------------------------------
def generate_elevenlabs_tts(text: str, voice: str, output_path: str) -> bool:
    """Synthesize speech using ElevenLabs API."""
    api_key = os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("XI_API_KEY")
    if not api_key:
        print("[TTS] ELEVENLABS_API_KEY not found in environment.")
        return False

    print(f"[TTS] Generating speech with ElevenLabs (Voice: {voice})...")
    
    # Map friendly voice name to Voice ID if known
    voice_id = voice
    for v in VOICE_CATALOG["elevenlabs"]:
        if v["name"].lower() == voice.lower() or v["id"] == voice:
            voice_id = v["id"]
            break

    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.50,
                "similarity_boost": 0.75,
                "style": 0.20,
                "use_speaker_boost": True
            }
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "xi-api-key": api_key,
                "Accept": "audio/mpeg"
            }
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            audio_bytes = resp.read()
            with open(output_path, "wb") as f:
                f.write(audio_bytes)
            return True
    except Exception as e:
        print(f"[TTS] ElevenLabs request failed: {e}")
        return False


# -------------------------------------------------------------
# Provider 3: OpenAI TTS
# -------------------------------------------------------------
def generate_openai_tts(text: str, voice: str, output_path: str) -> bool:
    """Synthesize speech using OpenAI TTS API."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("[TTS] OPENAI_API_KEY not found in environment.")
        return False

    print(f"[TTS] Generating speech with OpenAI TTS (Voice: {voice})...")
    try:
        url = "https://api.openai.com/v1/audio/speech"
        payload = {
            "model": "tts-1-hd",
            "input": text,
            "voice": voice.lower(),
            "response_format": "mp3",
            "speed": 1.05
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            audio_bytes = resp.read()
            with open(output_path, "wb") as f:
                f.write(audio_bytes)
            return True
    except Exception as e:
        print(f"[TTS] OpenAI TTS failed: {e}")
        return False


# -------------------------------------------------------------
# Provider 4: Edge TTS (Free Neural Voices)
# -------------------------------------------------------------
async def generate_edge_tts(text: str, voice: str, rate: str, output_path: str) -> bool:
    """Synthesize speech using Microsoft Edge Neural TTS."""
    print(f"[TTS] Generating speech with Edge Neural TTS (Voice: {voice}, Rate: {rate})...")
    try:
        import edge_tts
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(output_path)
        return True
    except Exception as e:
        print(f"[TTS] Edge-TTS failed: {e}")
        return False


# -------------------------------------------------------------
# Unified Synthesizer
# -------------------------------------------------------------
def synthesize(text: str, provider: str = "auto", voice: str = None, rate: str = "+3%", out_wav: str = "assets/narration.wav"):
    """Synthesize narration script to a 48kHz WAV audio file with auto-fallback."""
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        temp_mp3 = tmp.name

    success = False
    chosen_provider = provider.lower()
    
    # Auto provider resolution
    if chosen_provider == "auto":
        if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
            chosen_provider = "gemini"
        elif os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("XI_API_KEY"):
            chosen_provider = "elevenlabs"
        elif os.environ.get("OPENAI_API_KEY"):
            chosen_provider = "openai"
        else:
            chosen_provider = "edge"

    # Set default voice if not specified
    if not voice:
        voice = DEFAULT_VOICES.get(chosen_provider, "en-US-ChristopherNeural")

    # 1. Try Chosen Provider
    if chosen_provider == "gemini":
        success = generate_gemini_tts(text, voice, temp_mp3)
    elif chosen_provider == "elevenlabs":
        success = generate_elevenlabs_tts(text, voice, temp_mp3)
    elif chosen_provider == "openai":
        success = generate_openai_tts(text, voice, temp_mp3)
    elif chosen_provider == "edge":
        success = asyncio.run(generate_edge_tts(text, voice, rate, temp_mp3))

    # 2. Fallback to Edge-TTS if previous provider failed
    if not success and chosen_provider != "edge":
        print(f"[TTS] Provider '{chosen_provider}' was unable to synthesize audio.")
        print("[TTS] Seamlessly falling back to free high-quality Edge Neural TTS (Christopher)...")
        fallback_voice = "en-US-ChristopherNeural"
        success = asyncio.run(generate_edge_tts(text, fallback_voice, rate, temp_mp3))
        chosen_provider = "edge"
        voice = fallback_voice

    if not success or not os.path.exists(temp_mp3) or os.path.getsize(temp_mp3) == 0:
        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)
        raise RuntimeError("TTS generation failed across all providers. Check your internet connection or API keys.")

    # 3. Post-process to 48kHz stereo WAV with loudness mastering
    print("[TTS] Mastering audio: 48kHz stereo, broadcast loudness normalization...")
    convert_to_broadcast_wav(temp_mp3, out_wav)
    
    # Save a copy as narration_raw.mp3 in the same directory for convenience
    raw_mp3_path = os.path.join(os.path.dirname(os.path.abspath(out_wav)), "narration_raw.mp3")
    try:
        import shutil
        shutil.copy2(temp_mp3, raw_mp3_path)
    except Exception:
        pass

    if os.path.exists(temp_mp3):
        os.remove(temp_mp3)

    duration = get_audio_duration(out_wav)
    
    # Write metadata json
    meta_path = os.path.join(os.path.dirname(os.path.abspath(out_wav)), "audio-meta.json")
    meta_info = {
        "audio_file": os.path.basename(out_wav),
        "duration_seconds": round(duration, 2),
        "provider": chosen_provider,
        "voice": voice,
        "sample_rate": 48000,
        "channels": 2,
        "script_length_chars": len(text),
        "word_count": len(text.split())
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_info, f, indent=2)

    print(f"\n[TTS] Success! High-fidelity narration audio generated at: {out_wav}")
    print(f"[TTS] Duration: {duration:.2f}s | Provider: {chosen_provider} | Voice: {voice}")
    print(f"[TTS] Metadata written to: {meta_path}\n")
    return out_wav, duration, chosen_provider, voice


def list_voices():
    """Print formatted catalog of all available voices across all providers."""
    print("\n" + "=" * 75)
    print(" UNROTSKILLVID — VOICE & TTS CATALOG")
    print("=" * 75)
    
    for provider, voices in VOICE_CATALOG.items():
        print(f"\n[{provider.upper()} TTS]")
        if provider == "gemini":
            print(" Requires: GEMINI_API_KEY or GOOGLE_API_KEY (or auto fallback)")
        elif provider == "elevenlabs":
            print(" Requires: ELEVENLABS_API_KEY / XI_API_KEY")
        elif provider == "openai":
            print(" Requires: OPENAI_API_KEY")
        elif provider == "edge":
            print(" Free & Built-in (No API key required, neural quality)")
            
        print("-" * 75)
        for v in voices:
            print(f"  • {v['name']:<18} ID: {v['id']:<26} [{v['gender']}] - {v['tone']}")
    print("\n" + "=" * 75 + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("script", nargs="?", default="", help="Script text string or path to a .txt / .md script file")
    parser.add_argument("--provider", choices=["auto", "gemini", "elevenlabs", "openai", "edge"], default="auto",
                        help="TTS Provider (default: auto)")
    parser.add_argument("--voice", default="", help="Voice name or ID")
    parser.add_argument("--rate", default="+3%", help="Speaking rate offset for Edge-TTS (default: +3%%)")
    parser.add_argument("--out", default="assets/narration.wav", help="Output WAV path (default: assets/narration.wav)")
    parser.add_argument("--list-voices", action="store_true", help="List all available voices and exit")

    args = parser.parse_args()

    if args.list_voices:
        list_voices()
        sys.exit(0)

    if not args.script:
        parser.print_help()
        sys.exit(1)

    text = read_script(args.script)
    if not text:
        sys.exit("Error: Empty script text provided.")

    synthesize(
        text=text,
        provider=args.provider,
        voice=args.voice if args.voice else None,
        rate=args.rate,
        out_wav=args.out
    )


if __name__ == "__main__":
    main()
