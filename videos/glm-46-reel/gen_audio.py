import asyncio
import edge_tts
import subprocess
import os

script_text = (
    "Meet GLM-4.6 from Zhipu AI, the 355-billion-parameter open-weight model engineered specifically for agentic AI and software engineering. "
    "With an expanded 200,000-token context window and native tool calling, it achieves direct parity with Claude Sonnet 4 inside environments like Claude Code and Cline. "
    "It navigates entire repositories, plans complex multi-file refactors, and executes terminal commands with precision. "
    "Its Mixture-of-Experts architecture activates only 32 billion parameters per token, delivering frontier-grade reasoning with over thirty percent lower token consumption. "
    "Scoring 68.1% on SWE-bench Verified and available under the MIT license, GLM-4.6 brings unrestricted frontier coding right to your local workflow."
)

async def generate():
    voice = "en-US-ChristopherNeural"
    out_mp3 = "videos/glm-46-reel/assets/narration_raw.mp3"
    out_wav = "videos/glm-46-reel/assets/narration.wav"
    
    os.makedirs("videos/glm-46-reel/assets", exist_ok=True)
    
    communicate = edge_tts.Communicate(script_text, voice, rate="+3%")
    await communicate.save(out_mp3)
    
    subprocess.run([
        "ffmpeg", "-y", "-i", out_mp3,
        "-ar", "48000", "-ac", "2",
        out_wav
    ], check=True)
    print("New narration audio successfully generated at", out_wav)

if __name__ == "__main__":
    asyncio.run(generate())
