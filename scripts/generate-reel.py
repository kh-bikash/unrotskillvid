#!/usr/bin/env python3
"""End-to-End Prompt-to-Video Engine for unrotskillvid.

Takes a prompt/topic or script and autonomously:
1. Generates a 4-scene high-retention script and visual scene copy (via Gemini / OpenAI / Built-in templates).
2. Synthesizes 48kHz human voiceover audio (Gemini TTS, Edge TTS, ElevenLabs, OpenAI).
3. Analyzes speech pauses and calculates pause-aligned scene timestamps.
4. Customizes HTML5 / GSAP compositions with customized typography, badges, cards, and animations.
5. Scaffolds the complete project and optionally renders to a 60fps MP4 video.

Usage:
    python scripts/generate-reel.py "Make a SaaS launch reel about an AI code assistant" --out videos/ai-assistant-reel --render
    python scripts/generate-reel.py --prompt "Explain the 80/20 rule in productivity" --type faceless-explainer --provider gemini --render
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Force UTF-8 stdout encoding on Windows
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent

# Built-in high retention script synthesis templates if no LLM API key is present
DEFAULT_TEMPLATES_BY_TYPE = {
    "screen-hero": {
        "title": "Autonomous Agent Demo",
        "badge": "PRODUCT BREAKTHROUGH",
        "headline_1": "The new way to build autonomous software agents.",
        "subhead_1": "Engineered for developers who need extreme precision and full repo control.",
        "card_title": "agent_runtime_core.ts",
        "caption_2_a": "Direct tool execution with real-time feedback.",
        "caption_2_b": "Navigates complex repos and plans multi-file refactors.",
        "metric_3_title_a": "Active Inference Cost",
        "metric_3_badge_a": "-30% Lower",
        "metric_3_title_b": "Context Capacity",
        "metric_3_badge_b": "200K Tokens",
        "headline_3": "Frontier reasoning at a fraction of token overhead.",
        "subhead_3": "Mixture-of-Experts architecture activates only essential routing per step.",
        "payoff_badge": "READY TODAY · OPEN SOURCE",
        "big_stat": "68.1%",
        "stat_desc": "SWE-bench Verified Accuracy Score",
        "cta_text": "Try it in your workflow now",
        "script": (
            "Meet the next-generation autonomous engineering model. "
            "With native multi-tool calling and expanded 200,000-token context, it navigates entire codebases, "
            "plans multi-file refactors, and executes terminal commands with precision. "
            "Its Mixture-of-Experts architecture activates only essential parameters, delivering frontier reasoning "
            "with over thirty percent lower overhead. Available today under the MIT license to supercharge your local workflow."
        )
    },
    "saas-launch": {
        "title": "SaaS Product Launch",
        "badge": "✨ JUST LAUNCHED · V2.0",
        "headline_1": "Supercharge your workflow with AI Automation.",
        "subhead_1": "Eliminate repetitive tasks, sync data across 100+ tools, and launch 10x faster.",
        "browser_url": "https://app.cloudstudio.io/dashboard",
        "banner_title": "Active AI Pipelines",
        "banner_stat": "+482% Flow",
        "bento_1_title": "Instant Zero-Shot Sync",
        "bento_1_desc": "Connect databases, APIs, and webhooks in seconds without boilerplate code.",
        "bento_2_title": "Enterprise Edge Security",
        "bento_2_desc": "End-to-end encryption with SOC2 compliance and zero-retention data policies.",
        "bento_3_title": "Autonomous Analytics",
        "bento_3_desc": "Live streaming metric dashboards generated automatically from your events.",
        "caption_2": "Designed to scale with your team seamlessly.",
        "headline_3": "Plug into the stack you already love.",
        "subhead_3": "Native integrations with over 150+ developer and productivity platforms.",
        "cta_badge": "🚀 14-DAY FREE TRIAL · NO CARD REQUIRED",
        "card_price": "$0",
        "price_sub": "Start building in under 2 minutes",
        "cta_btn": "Claim Your Free Account",
        "script": (
            "Say hello to the ultimate AI automation platform. "
            "Connect your databases, webhooks, and APIs in seconds with zero boilerplate code. "
            "Experience enterprise-grade security, instant zero-shot sync, and live streaming analytics dashboards. "
            "Integrate natively with your favorite tools and start shipping faster today with a free 14-day trial."
        )
    },
    "code-walkthrough": {
        "title": "Developer Code Walkthrough",
        "badge": "⚡ OPEN WEIGHT FRONTIER MODEL",
        "headline_1": "Frontier AI coding with unrestricted autonomy.",
        "subhead_1": "Native tool calling, multi-file refactoring, and benchmark-topping accuracy.",
        "spec_1_k": "Architecture", "spec_1_v": "Sparse MoE (32B Active)",
        "spec_2_k": "Context Window", "spec_2_v": "200,000 Tokens",
        "spec_3_k": "SWE-bench Verified", "spec_3_v": "68.1% Parity",
        "tab_label": "pipeline_optimizer.ts",
        "diff_del": "- sequentialSync(repositories, batchSize = 1)",
        "diff_add_1": "+ autonomousParallelCluster(agents = 8, asyncCtx)",
        "diff_add_2": "+ nativeToolCalling.verifyParity({ benchmark: true })",
        "caption_2": "Executes multi-file refactors with zero hallucinations.",
        "headline_3": "Frontier performance with local efficiency.",
        "subhead_3": "32B active parameters deliver sub-second token latency on modern hardware.",
        "mit_badge": "🔓 100% OPEN WEIGHTS · MIT LICENSE",
        "term_cmd": "ollama run model:latest",
        "cta_btn": "Download Weights on HuggingFace",
        "script": (
            "Explore the new open-weight coding frontier model. "
            "Built with 200,000 tokens of context and native tool calling, it matches proprietary frontier parity inside your IDE. "
            "Watch it execute complex multi-file refactors and parallel agent workflows in real time. "
            "Scoring 68.1% on SWE-bench Verified and licensed under MIT, you can run it locally with Ollama right now."
        )
    },
    "faceless-explainer": {
        "title": "Mental Model & Explainer",
        "badge": "🧠 MENTAL MODEL OF THE DAY",
        "headline_1": "Why 99% of people get productivity completely backwards.",
        "hook_fact": "It is not about managing your time — it is about managing your cognitive energy.",
        "mistake_1": "Working 12 hours a day on shallow tasks",
        "mistake_2": "Constant context switching and notifications",
        "mistake_3": "Mistaking motion for real forward progress",
        "quote_2": "Busyness is a form of laziness.",
        "headline_3": "Protect your peak energy windows.",
        "subhead_3": "One hour of peak flow outperforms four hours of distracted effort every single time.",
        "rule_headline": "Focus on depth over duration, and results follow naturally.",
        "cta_btn": "Save This Reel & Follow For More",
        "script": (
            "Why do 99% of people get productivity completely backwards? "
            "Most people spend 12 hours a day drowning in shallow tasks and constant context switching, mistaking motion for real progress. "
            "The real secret is the 80/20 leverage protocol: protect 90 minutes of peak energy for your single highest-ROI task. "
            "Focus on depth over duration, and the results will take care of themselves. Save this reel for when you need it."
        )
    },
    "comparison-vs": {
        "title": "Head-to-Head Comparison",
        "badge": "⚔️ HEAD TO HEAD SHOWDOWN",
        "headline_1": "Which tool actually delivers the best results?",
        "card_a_name": "Option A",
        "card_b_name": "Option B",
        "caption_2": "Option B delivers 3x faster execution with zero vendor lock-in.",
        "headline_3": "Massive efficiency across high-throughput tasks.",
        "subhead_3": "Cut API bills while dramatically improving user-facing response speeds.",
        "winner_text": "Option B takes the crown across speed, cost, and open freedom.",
        "cta_btn": "Drop Your Thoughts in the Comments",
        "script": (
            "Let's put the top two AI engineering tools head-to-head in a real-world showdown. "
            "Option A gives you a 128k context with 82% tool accuracy, but Option B blows past it with 200k tokens and 94% precision. "
            "In latency benchmarks, Option B is nearly three times faster while slashing token costs by over 60%. "
            "With open weights and unbeatable throughput, Option B takes the clear victory. Which one are you using?"
        )
    }
}


def detect_template_type(prompt: str) -> str:
    """Infer the most appropriate video style from the prompt text."""
    p = prompt.lower()
    if any(w in p for w in ["vs", "compare", "comparison", "better than", "benchmark battle", "against"]):
        return "comparison-vs"
    if any(w in p for w in ["code", "developer", "model", "github", "refactor", "swe-bench", "ollama", "python", "typescript", "repo"]):
        return "code-walkthrough"
    if any(w in p for w in ["saas", "launch", "product hunt", "dashboard", "app", "feature", "pricing", "free trial", "signup"]):
        return "saas-launch"
    if any(w in p for w in ["explain", "psychology", "mental model", "productivity", "habit", "lesson", "why", "secret", "faceless"]):
        return "faceless-explainer"
    return "screen-hero"


def generate_llm_script(prompt: str, video_type: str) -> dict:
    """Use Gemini or OpenAI to synthesize tailored script & scene copy if API keys exist."""
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    system_instruction = f"""You are a master viral vertical video producer and copywriter for 9:16 reels.
Generate a high-retention 4-scene video blueprint for the template style: '{video_type}'.
The user prompt is: "{prompt}".

Return valid JSON ONLY with these exact fields:
{{
  "title": "Short Project Title",
  "badge": "Uppercase Category Badge",
  "headline_1": "Punchy Scene 1 Headline (max 8 words)",
  "subhead_1": "Scene 1 Subhead (1 sentence)",
  "script": "The complete 40-50 second voiceover script text in natural human tone, exactly 4 sentences matching Scene 1 Hook, Scene 2 Body, Scene 3 Nuance, Scene 4 Payoff CTA.",
  "scene_2_caption": "Scene 2 Caption text",
  "headline_3": "Scene 3 Nuance Headline",
  "subhead_3": "Scene 3 Subhead explanation",
  "payoff_text": "Scene 4 Big payoff statement",
  "cta_button": "Scene 4 Action button text"
}}"""

    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-2.0-flash", generation_config={"response_mime_type": "application/json"})
            resp = model.generate_content(system_instruction)
            data = json.loads(resp.text)
            print("[GEN] Successfully synthesized customized script via Gemini 2.0 Flash.")
            return data
        except Exception as e:
            print(f"[GEN] Gemini LLM generation error: {e}. Checking OpenAI/Fallback...")

    if openai_key:
        try:
            import openai
            client = openai.OpenAI(api_key=openai_key)
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": "You are a viral video script generator. Output JSON only."},
                    {"role": "user", "content": system_instruction}
                ]
            )
            data = json.loads(resp.choices[0].message.content)
            print("[GEN] Successfully synthesized customized script via OpenAI.")
            return data
        except Exception as e:
            print(f"[GEN] OpenAI LLM generation error: {e}")

    # Fallback to rich built-in template
    print(f"[GEN] Using optimized high-retention template preset for '{video_type}'.")
    return DEFAULT_TEMPLATES_BY_TYPE.get(video_type, DEFAULT_TEMPLATES_BY_TYPE["screen-hero"])


def generate_full_reel(prompt: str, video_type: str = "auto", provider: str = "auto",
                       voice: str = "", out_dir: str = None, render: bool = False):
    """Orchestrates the entire prompt-to-video pipeline end-to-end."""
    print("\n" + "=" * 75)
    print(" 🎬  UNROTSKILLVID — AUTONOMOUS PROMPT-TO-VIDEO GENERATOR")
    print("=" * 75)
    print(f"Prompt: \"{prompt}\"")

    # 1. Detect Template Type
    if video_type == "auto" or not video_type:
        video_type = detect_template_type(prompt)
    print(f"[GEN] Selected Video Style: {video_type}")

    # 2. Determine Output Directory
    if not out_dir:
        slug = re.sub(r"[^a-z0-9]+", "-", prompt.lower().strip()[:32]).strip("-") or "reel"
        out_dir = str(ROOT_DIR / "videos" / f"{slug}-{video_type}")
    
    project_path = Path(out_dir).resolve()
    print(f"[GEN] Target Project Directory: {project_path}")

    # 3. Scaffold Project from Template
    template_src = ROOT_DIR / "templates" / video_type
    if not template_src.exists():
        template_src = ROOT_DIR / "templates" / "screen-hero"

    if project_path.exists():
        print(f"[GEN] Reusing existing directory: {project_path}")
    else:
        print(f"[GEN] Scaffolding template from: {template_src}")
        shutil.copytree(template_src, project_path)

    # 4. Synthesize Script and Copy
    script_data = generate_llm_script(prompt, video_type)
    script_text = script_data.get("script", DEFAULT_TEMPLATES_BY_TYPE[video_type]["script"])
    
    # Save BRIEF.md
    brief_content = f"""---
workflow: unrot-tutorial
flow: automation
template: {video_type}
prompt: "{prompt}"
---

# Video Brief: {script_data.get('title', prompt)}

## Narration Script
{script_text}

## Visual Directives
- **Scene 1 (Hook):** {script_data.get('headline_1', 'Hook Statement')}
- **Scene 2 (Core):** {script_data.get('scene_2_caption', 'Core Showcase')}
- **Scene 3 (Nuance):** {script_data.get('headline_3', 'Nuance & Limit')}
- **Scene 4 (Payoff):** {script_data.get('payoff_text', 'Payoff & CTA')}
"""
    (project_path / "BRIEF.md").write_text(brief_content, encoding="utf-8")

    # 5. Generate Voiceover Audio (Gemini TTS / Edge / ElevenLabs / OpenAI)
    audio_path = project_path / "assets" / "narration.wav"
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    
    print("\n[GEN] Synthesizing human voiceover audio...")
    import importlib.util
    tts_spec = importlib.util.spec_from_file_location("tts_mod", ROOT_DIR / "scripts" / "tts.py")
    tts_mod = importlib.util.module_from_spec(tts_spec)
    tts_spec.loader.exec_module(tts_mod)
    
    tts_mod.synthesize(
        text=script_text,
        provider=provider,
        voice=voice if voice else None,
        out_wav=str(audio_path)
    )

    # 6. Map Speech Timeline & Cut Points
    print("\n[GEN] Mapping speech pauses and timeline cut points...")
    map_spec = importlib.util.spec_from_file_location("map_mod", ROOT_DIR / "scripts" / "audio-map.py")
    map_mod = importlib.util.module_from_spec(map_spec)
    map_spec.loader.exec_module(map_mod)

    map_json_path = project_path / "assets" / "audio-map.json"
    audio_map_data = map_mod.map_audio(str(audio_path), scenes_count=4, json_out=str(map_json_path))

    total_dur = audio_map_data["total_duration"]
    scenes = audio_map_data["scenes"]

    # 7. Update index.html with Exact Durations
    index_html_path = project_path / "index.html"
    if index_html_path.exists():
        index_content = index_html_path.read_text(encoding="utf-8")
        
        # Replace root data-duration
        index_content = re.sub(r'data-duration="[\d.]+"', f'data-duration="{total_dur:.2f}"', index_content, count=1)
        
        # Replace audio data-duration
        index_content = re.sub(r'<audio[^>]*data-duration="[\d.]+"', f'<audio id="narration" class="clip" src="assets/narration.wav" data-start="0" data-duration="{total_dur:.2f}"', index_content)
        
        # Replace scene durations
        if len(scenes) == 4:
            for sc in scenes:
                sc_num = sc["scene"]
                sc_start = sc["start"]
                sc_dur = sc["duration"]
                slot_pattern = rf'(<div[^>]*id="slot-scene-{sc_num}"[^>]*data-start=")[\d.]*("[^>]*data-duration=")[\d.]*(")'
                index_content = re.sub(slot_pattern, rf'\g<1>{sc_start:.2f}\g<2>{sc_dur:.2f}\g<3>', index_content)
                
        index_html_path.write_text(index_content, encoding="utf-8")
        print(f"[GEN] Updated index.html timeline (Total Duration: {total_dur:.2f}s across 4 scenes).")

    # 8. Customize Scene HTML Files with Generated Copy
    scene1_path = project_path / "compositions" / "scene1.html"
    if scene1_path.exists() and "headline_1" in script_data:
        s1_text = scene1_path.read_text(encoding="utf-8")
        if script_data.get("badge"):
            s1_text = re.sub(r'<span>[^<]+</span>', f'<span>{script_data["badge"]}</span>', s1_text, count=1)
        if script_data.get("headline_1"):
            s1_text = re.sub(r'<h1[^>]*>.*?</h1>', f'<h1 id="title" class="headline">{script_data["headline_1"]}</h1>', s1_text, flags=re.S)
        if script_data.get("subhead_1"):
            s1_text = re.sub(r'<p id="sub"[^>]*>.*?</p>', f'<p id="sub" class="subhead">{script_data["subhead_1"]}</p>', s1_text, flags=re.S)
        scene1_path.write_text(s1_text, encoding="utf-8")

    # 9. Render Video if Requested
    rendered_file = None
    if render:
        print("\n[GEN] Rendering 1080x1920 60fps MP4 video...")
        out_mp4 = project_path / "out" / f"{project_path.name}.mp4"
        out_mp4.parent.mkdir(parents=True, exist_ok=True)
        
        render_cmd = ["npx", "--yes", "hyperframes@latest", "render", "--output", str(out_mp4)]
        if sys.platform == "win32":
            render_cmd[0] = "npx.cmd"
            
        r = subprocess.run(render_cmd, cwd=str(project_path), capture_output=True, text=True)
        if r.returncode == 0:
            rendered_file = str(out_mp4)
            print(f"\n[GEN] 🎉 Finished Video Successfully Rendered: {out_mp4}")
        else:
            print(f"[GEN] Hyperframes render note: Project is fully prepped in {project_path}. Run 'npm run render' inside.")

    print("\n" + "=" * 75)
    print(f" ✨ COMPLETE REEL READY AT: {project_path}")
    print("=" * 75)
    print(f"  • Video Style: {video_type}")
    print(f"  • Narration:   {audio_path} ({total_dur:.2f}s)")
    print(f"  • Preview:     cd {project_path.relative_to(ROOT_DIR) if project_path.is_relative_to(ROOT_DIR) else project_path} && npm run dev")
    print(f"  • Render MP4:  npx unrotskillvid render {project_path}")
    print("=" * 75 + "\n")

    return str(project_path), rendered_file


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("prompt", nargs="?", default="", help="Prompt, idea, or topic for the video")
    parser.add_argument("--prompt", dest="prompt_flag", default="", help="Explicit prompt flag")
    parser.add_argument("--type", default="auto", choices=["auto", "screen-hero", "saas-launch", "code-walkthrough", "faceless-explainer", "comparison-vs"],
                        help="Video style template (default: auto)")
    parser.add_argument("--provider", default="auto", choices=["auto", "gemini", "elevenlabs", "openai", "edge"],
                        help="TTS audio provider (default: auto)")
    parser.add_argument("--voice", default="", help="TTS voice name or ID")
    parser.add_argument("--out", default="", help="Target project output directory")
    parser.add_argument("--render", action="store_true", help="Automatically render the final 60fps MP4 video")

    args = parser.parse_args()
    prompt_text = args.prompt or args.prompt_flag
    if not prompt_text:
        parser.print_help()
        sys.exit(1)

    generate_full_reel(
        prompt=prompt_text,
        video_type=args.type,
        provider=args.provider,
        voice=args.voice,
        out_dir=args.out,
        render=args.render
    )


if __name__ == "__main__":
    main()
