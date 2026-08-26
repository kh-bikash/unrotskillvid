#!/usr/bin/env python3
"""Autonomous Dynamic Multi-Scene Prompt-to-Video Engine for unrotskillvid.

Features:
- Dynamically determines the optimal number of scenes (2 to 7+ scenes) based on prompt depth.
- Synthesizes a structured multi-scene blueprint with custom visual layouts per scene.
- Generates broadcast-quality 48kHz human voiceover audio (Gemini TTS, Edge, ElevenLabs, OpenAI).
- Maps speech pauses and synchronizes exact scene boundaries.
- Generates tailored HTML5 / GSAP 60fps compositions for every scene.
- Prepares root index.html orchestrator and renders 1080x1920 MP4.

Usage:
    python scripts/generate-reel.py "Create an in-depth 5-step guide on mastering prompt engineering" --render
    python scripts/generate-reel.py "Announce our new Figma AI plugin in a fast 3-scene teaser" --provider gemini --render
"""

import argparse
import importlib.util
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


# -------------------------------------------------------------
# Dynamic Scene Layout HTML Generators
# -------------------------------------------------------------
def render_scene_html(scene_data: dict, scene_index: int, total_scenes: int, theme: str = "dark") -> str:
    """Dynamically generates self-contained GSAP-animated HTML composition for any scene."""
    layout_type = scene_data.get("layout_type", "hook-card")
    title = scene_data.get("headline", "Next-Generation Breakthrough")
    subhead = scene_data.get("subhead", "Engineered for maximum velocity and autonomous execution.")
    badge = scene_data.get("badge", f"STAGE {scene_index:02d} OF {total_scenes:02d}")
    accent_color = scene_data.get("accent_color", "#ff6b35")
    bg_color = scene_data.get("bg_color", "#13100e")

    # Layout 1: Hook / Statement
    if layout_type in ["hook-card", "statement", "hero"]:
        content_body = f"""
        <div id="badge" class="badge">
          <div class="badge-dot"></div>
          <span>{badge}</span>
        </div>
        <h1 id="title" class="headline">{title}</h1>
        <p id="sub" class="subhead">{subhead}</p>
        <div id="main-card" class="card-glass">
          <div class="card-top">
            <div class="dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
            <span class="card-label">{scene_data.get("card_label", "system_overview.ts")}</span>
          </div>
          <div class="card-body">
            <div class="row-highlight">
              <span class="row-key">{scene_data.get("key_label", "Primary Capability")}</span>
              <span class="row-val">{scene_data.get("val_label", "100% Autonomous")}</span>
            </div>
          </div>
        </div>
        """
        timeline_js = """
        tl.from("#badge", { opacity: 0, y: -20, duration: 0.6, ease: "power2.out" }, 0.2)
          .from("#title", { opacity: 0, y: 30, duration: 0.8, ease: "power2.out" }, 0.4)
          .from("#sub", { opacity: 0, y: 20, duration: 0.6, ease: "power2.out" }, 0.7)
          .from("#main-card", { opacity: 0, scale: 0.92, y: 40, duration: 0.8, ease: "back.out(1.3)" }, 1.0)
          .to("#main-card", { y: -10, repeat: 1, yoyo: true, duration: 2.5, ease: "sine.inOut" }, 1.8);
        """

    # Layout 2: Bento Grid / Feature List
    elif layout_type in ["bento-grid", "features", "list"]:
        items = scene_data.get("items", [
            {"icon": "⚡", "title": "Zero-Latency Execution", "desc": "Instant real-time responses without queue delays."},
            {"icon": "🔒", "title": "Enterprise Security", "desc": "End-to-end encrypted with zero retention policies."},
            {"icon": "📊", "title": "Autonomous Analytics", "desc": "Live streaming metrics generated on the fly."}
        ])
        cards_html = ""
        for i, item in enumerate(items, 1):
            cards_html += f"""
            <div id="bento-{i}" class="bento-item">
              <div class="bento-icon">{item.get("icon", "✨")}</div>
              <div class="bento-info">
                <h3 class="bento-title">{item.get("title", f"Feature {i}")}</h3>
                <p class="bento-desc">{item.get("desc", "High performance capability.")}</p>
              </div>
            </div>
            """
        content_body = f"""
        <div id="badge" class="badge"><span>{badge}</span></div>
        <h2 id="title" class="headline-medium">{title}</h2>
        <div class="bento-container">{cards_html}</div>
        <div id="caption-box" class="caption-bar"><p class="cap-text">{subhead}</p></div>
        """
        timeline_js = """
        tl.from("#badge", { opacity: 0, y: -20, duration: 0.5, ease: "power2.out" }, 0.2)
          .from("#title", { opacity: 0, y: 20, duration: 0.6, ease: "power2.out" }, 0.4)
          .from(".bento-item", { opacity: 0, x: -30, stagger: 0.25, duration: 0.6, ease: "power2.out" }, 0.7)
          .from("#caption-box", { opacity: 0, y: 30, duration: 0.6, ease: "back.out(1.2)" }, 1.5);
        """

    # Layout 3: Step-by-Step / Protocol
    elif layout_type in ["steps", "protocol", "framework"]:
        steps = scene_data.get("steps", [
            {"num": "1", "title": "Identify Highest-ROI Needle Mover"},
            {"num": "2", "title": "Protect 90 Minutes of Deep Work"},
            {"num": "3", "title": "Automate or Delegate Ruthlessly"}
        ])
        steps_html = ""
        for s in steps:
            steps_html += f"""
            <div class="step-card">
              <div class="step-num">{s.get("num", "1")}</div>
              <div class="step-text">{s.get("title", "Protocol action item")}</div>
            </div>
            """
        content_body = f"""
        <div class="step-container">
          <div class="protocol-box">
            <div class="proto-badge">{badge}</div>
            <h2 class="proto-title">{title}</h2>
            <div class="steps-list">{steps_html}</div>
          </div>
          <div id="bot-copy" class="bottom-copy">
            <p class="bot-sub">{subhead}</p>
          </div>
        </div>
        """
        timeline_js = """
        tl.from(".protocol-box", { opacity: 0, scale: 0.92, y: 30, duration: 0.8, ease: "back.out(1.3)" }, 0.2)
          .from(".step-card", { opacity: 0, x: -20, stagger: 0.25, duration: 0.6, ease: "power2.out" }, 0.6)
          .from("#bot-copy", { opacity: 0, y: 20, duration: 0.6, ease: "power2.out" }, 1.3);
        """

    # Layout 4: Metrics / Benchmark Graph
    elif layout_type in ["metrics", "benchmarks", "stats"]:
        metrics = scene_data.get("metrics", [
            {"name": "Accuracy Benchmark", "val": "94.2%", "width": "94%"},
            {"name": "Inference Efficiency", "val": "+180% Faster", "width": "85%"}
        ])
        metrics_html = ""
        for idx, m in enumerate(metrics, 1):
            metrics_html += f"""
            <div id="m-{idx}" class="metric-card">
              <div class="metric-top">
                <span class="m-name">{m.get("name", "Metric")}</span>
                <span class="m-val">{m.get("val", "100%")}</span>
              </div>
              <div class="m-track"><div class="m-fill" style="width: {m.get('width', '80%')};"></div></div>
            </div>
            """
        content_body = f"""
        <div id="badge" class="badge"><span>{badge}</span></div>
        <h2 id="title" class="headline-medium">{title}</h2>
        <div class="metric-container">{metrics_html}</div>
        <div id="bot-copy" class="bottom-copy"><p class="bot-sub">{subhead}</p></div>
        """
        timeline_js = """
        tl.from("#badge", { opacity: 0, y: -20, duration: 0.5, ease: "power2.out" }, 0.2)
          .from("#title", { opacity: 0, y: 20, duration: 0.6, ease: "power2.out" }, 0.4)
          .from(".metric-card", { opacity: 0, y: 30, stagger: 0.3, duration: 0.7, ease: "power2.out" }, 0.7)
          .from(".m-fill", { width: "0%", stagger: 0.3, duration: 1.0, ease: "power3.out" }, 0.9)
          .from("#bot-copy", { opacity: 0, y: 20, duration: 0.6, ease: "power2.out" }, 1.5);
        """

    # Layout 5: Code Diff / Terminal Execution
    elif layout_type in ["code", "terminal", "diff"]:
        content_body = f"""
        <div id="badge" class="badge"><span>{badge}</span></div>
        <h2 id="title" class="headline-medium">{title}</h2>
        <div id="editor" class="editor-window">
          <div class="editor-bar">
            <span style="color:#f87171;">●</span>
            <span style="color:#fbbf24;">●</span>
            <span style="color:#34d399;">●</span>
            <span class="tab-title">{scene_data.get("tab_name", "pipeline.ts")}</span>
          </div>
          <div class="diff-lines">
            <div class="line del">{scene_data.get("code_del", "- sequentialExecution(agents = 1)")}</div>
            <div class="line add">{scene_data.get("code_add_1", "+ parallelAutonomousCluster(nodes = 8)")}</div>
            <div class="line add">{scene_data.get("code_add_2", "+ nativeToolCalling.verifyParity()")}</div>
          </div>
        </div>
        <div id="bot-copy" class="bottom-copy"><p class="bot-sub">{subhead}</p></div>
        """
        timeline_js = """
        tl.from("#badge", { opacity: 0, y: -20, duration: 0.5, ease: "power2.out" }, 0.2)
          .from("#title", { opacity: 0, y: 20, duration: 0.6, ease: "power2.out" }, 0.4)
          .from("#editor", { opacity: 0, scale: 0.93, y: 30, duration: 0.8, ease: "back.out(1.3)" }, 0.7)
          .from(".line", { opacity: 0, x: -20, stagger: 0.3, duration: 0.5, ease: "power2.out" }, 1.1)
          .from("#bot-copy", { opacity: 0, y: 20, duration: 0.6, ease: "power2.out" }, 1.7);
        """

    # Layout 6: Final Payoff / CTA
    else:
        content_body = f"""
        <div class="payoff-wrap">
          <div id="badge" class="badge"><span>{badge}</span></div>
          <div id="stat-card" class="payoff-card">
            <div class="stat-highlight">{scene_data.get("stat_highlight", "10x")}</div>
            <div class="stat-label">{title}</div>
          </div>
          <div id="cta-block" class="cta-container">
            <div class="cta-btn">{scene_data.get("cta_text", "Get Started Today")}</div>
            <p class="cta-note">{subhead}</p>
          </div>
        </div>
        """
        timeline_js = """
        tl.from("#badge", { opacity: 0, scale: 0.9, duration: 0.5, ease: "power2.out" }, 0.2)
          .from("#stat-card", { opacity: 0, scale: 0.92, y: 30, duration: 0.8, ease: "back.out(1.3)" }, 0.4)
          .from("#cta-block", { opacity: 0, y: 40, duration: 0.7, ease: "power2.out" }, 0.8)
          .to(".cta-btn", { scale: 1.03, repeat: 1, yoyo: true, duration: 1.5, ease: "sine.inOut" }, 1.5);
        """

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Scene {scene_index}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {{
        font-family: "Geist";
        font-style: normal;
        font-weight: 400;
        src: url(../assets/fonts/geist-400.woff2) format("woff2");
      }}
      @font-face {{
        font-family: "Geist";
        font-style: normal;
        font-weight: 600;
        src: url(../assets/fonts/geist-600.woff2) format("woff2");
      }}
      @font-face {{
        font-family: "Geist";
        font-style: normal;
        font-weight: 700;
        src: url(../assets/fonts/geist-700.woff2) format("woff2");
      }}

      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        width: 1080px;
        height: 1920px;
        background: transparent;
        color: #f7f2eb;
        font-family: "Geist", sans-serif;
        overflow: hidden;
      }}

      .scene-wrap {{
        position: relative;
        width: 1080px;
        height: 1920px;
        padding: 160px 72px 120px 72px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }}

      .badge {{
        display: inline-flex;
        align-items: center;
        gap: 12px;
        padding: 10px 24px;
        background: rgba(255, 107, 53, 0.14);
        border: 1px solid rgba(255, 107, 53, 0.35);
        border-radius: 9999px;
        color: #ff6b35;
        font-size: 24px;
        font-weight: 600;
        width: fit-content;
        margin-bottom: 28px;
      }}
      .badge-dot {{ width: 10px; height: 10px; border-radius: 50%; background: #ff6b35; }}

      .headline {{ font-size: 84px; line-height: 1.08; font-weight: 700; color: #ffffff; margin-bottom: 24px; }}
      .headline-medium {{ font-size: 72px; line-height: 1.12; font-weight: 700; color: #ffffff; margin-bottom: 28px; }}
      .subhead {{ font-size: 32px; line-height: 1.45; color: #a79c91; margin-bottom: 48px; }}

      .card-glass {{
        background: #1f1915;
        border: 1px solid #3b332b;
        border-radius: 32px;
        padding: 40px;
        box-shadow: 0 30px 60px rgba(0,0,0,0.6);
      }}
      .card-top {{ display: flex; align-items: center; gap: 14px; margin-bottom: 24px; }}
      .dots {{ display: flex; gap: 8px; }}
      .dot {{ width: 14px; height: 14px; border-radius: 50%; background: #3b332b; }}
      .card-label {{ font-size: 24px; color: #e8ded4; font-weight: 600; }}
      .row-highlight {{
        display: flex; justify-content: space-between; align-items: center;
        padding: 24px 28px; background: #16120f; border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.05);
      }}
      .row-key {{ font-size: 26px; font-weight: 600; color: #ffffff; }}
      .row-val {{ font-size: 26px; font-weight: 700; color: #ff6b35; }}

      /* Bento */
      .bento-container {{ display: flex; flex-direction: column; gap: 24px; }}
      .bento-item {{
        background: #1f1915; border: 1px solid #3b332b; border-radius: 28px;
        padding: 32px; display: flex; align-items: center; gap: 24px;
      }}
      .bento-icon {{
        width: 64px; height: 64px; border-radius: 18px; background: rgba(255,107,53,0.15);
        display: flex; align-items: center; justify-content: center; font-size: 32px; flex-shrink: 0;
      }}
      .bento-title {{ font-size: 30px; font-weight: 700; color: #ffffff; margin-bottom: 6px; }}
      .bento-desc {{ font-size: 24px; color: #a79c91; line-height: 1.35; }}
      .caption-bar {{
        padding: 24px; background: rgba(31,25,21,0.9); border: 1px solid rgba(255,107,53,0.3);
        border-radius: 20px; text-align: center; font-size: 28px; font-weight: 600; color: #ffffff;
      }}

      /* Steps */
      .step-container {{ display: flex; flex-direction: column; justify-content: space-between; height: 100%; }}
      .protocol-box {{ background: #1f1915; border: 2px solid #ff6b35; border-radius: 36px; padding: 48px; }}
      .proto-badge {{ font-size: 22px; color: #ff6b35; font-weight: 700; margin-bottom: 16px; }}
      .proto-title {{ font-size: 56px; font-weight: 700; color: #ffffff; margin-bottom: 32px; }}
      .steps-list {{ display: flex; flex-direction: column; gap: 20px; }}
      .step-card {{ display: flex; align-items: center; gap: 20px; padding: 18px 0; border-bottom: 1px solid #3b332b; }}
      .step-card:last-child {{ border-bottom: none; }}
      .step-num {{
        width: 48px; height: 48px; border-radius: 50%; background: rgba(255,107,53,0.2);
        color: #ff6b35; display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 700;
      }}
      .step-text {{ font-size: 28px; font-weight: 600; color: #f7f2eb; }}

      /* Metrics */
      .metric-container {{ display: flex; flex-direction: column; gap: 28px; }}
      .metric-card {{ background: #1f1915; border: 1px solid #3b332b; border-radius: 28px; padding: 36px; }}
      .metric-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }}
      .m-name {{ font-size: 28px; font-weight: 600; color: #e8ded4; }}
      .m-val {{ font-size: 30px; font-weight: 700; color: #ff6b35; }}
      .m-track {{ width: 100%; height: 20px; background: #16120f; border-radius: 10px; overflow: hidden; }}
      .m-fill {{ height: 100%; background: linear-gradient(90deg, #ff6b35 0%, #ffa500 100%); border-radius: 10px; }}

      /* Editor */
      .editor-window {{ background: #1f1915; border: 1px solid #3b332b; border-radius: 28px; overflow: hidden; }}
      .editor-bar {{ height: 56px; background: #16120f; display: flex; align-items: center; padding: 0 24px; gap: 10px; }}
      .tab-title {{ font-size: 20px; color: #e8ded4; font-weight: 600; margin-left: 14px; }}
      .diff-lines {{ padding: 36px; display: flex; flex-direction: column; gap: 14px; }}
      .line {{ padding: 16px 20px; border-radius: 12px; font-size: 24px; font-weight: 600; }}
      .del {{ background: rgba(239,68,68,0.15); color: #f87171; }}
      .add {{ background: rgba(16,185,129,0.15); color: #34d399; }}

      /* Payoff */
      .payoff-wrap {{ display: flex; flex-direction: column; justify-content: space-between; height: 100%; }}
      .payoff-card {{ background: #1f1915; border: 1px solid #3b332b; border-radius: 36px; padding: 60px 40px; text-align: center; }}
      .stat-highlight {{ font-size: 110px; font-weight: 700; color: #ff6b35; line-height: 1.0; margin-bottom: 16px; }}
      .stat-label {{ font-size: 34px; font-weight: 700; color: #ffffff; }}
      .cta-container {{ display: flex; flex-direction: column; gap: 20px; }}
      .cta-btn {{
        padding: 32px; background: #ff6b35; border-radius: 24px; color: #ffffff;
        font-size: 34px; font-weight: 700; text-align: center; box-shadow: 0 20px 40px rgba(255,107,53,0.4);
      }}
      .cta-note {{ text-align: center; font-size: 26px; color: #a79c91; }}
      .bottom-copy {{ margin-top: auto; }}
      .bot-sub {{ font-size: 28px; color: #a79c91; line-height: 1.45; }}
    </style>
  </head>
  <body>
    <div id="scene{scene_index}" class="clip" data-start="0" data-duration="10.00">
      <div class="scene-wrap">
        {content_body}
      </div>
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      {timeline_js}
      window.__timelines["scene{scene_index}"] = tl;
    </script>
  </body>
</html>
"""


# -------------------------------------------------------------
# Dynamic LLM Multi-Scene Script Synthesizer
# -------------------------------------------------------------
def synthesize_dynamic_scenes(prompt: str, target_scenes: int = 0) -> dict:
    """Uses LLM (or intelligent heuristic decomposition) to break any prompt into 2 to 7+ structured scenes."""
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    scene_constraint = f"Decide the best number of scenes (between 2 to 6 scenes) to tell this story."
    if target_scenes > 1:
        scene_constraint = f"Break this down into EXACTLY {target_scenes} scenes."

    system_instruction = f"""You are a master viral vertical video producer for 9:16 reels.
The user wants a reel about: "{prompt}".
{scene_constraint}

Return valid JSON ONLY with this structure:
{{
  "title": "Short Title",
  "style": "screen-hero | saas-launch | code-walkthrough | faceless-explainer | comparison-vs",
  "scenes_count": 4,
  "full_script": "Complete narration text where each sentence corresponds sequentially to each scene.",
  "scenes": [
    {{
      "scene_num": 1,
      "layout_type": "hook-card | bento-grid | steps | metrics | code | payoff",
      "badge": "Uppercase Category Badge",
      "headline": "Punchy Main Headline (max 7 words)",
      "subhead": "Supporting sentence / explanation",
      "voiceover_sentence": "The exact voiceover spoken during this scene."
    }}
  ]
}}"""

    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-2.0-flash", generation_config={"response_mime_type": "application/json"})
            resp = model.generate_content(system_instruction)
            data = json.loads(resp.text)
            print(f"[GEN] Synthesized dynamic {len(data.get('scenes', []))}-scene structure via Gemini 2.0 Flash.")
            return data
        except Exception as e:
            print(f"[GEN] Gemini dynamic generation notice: {e}")

    if openai_key:
        try:
            import openai
            client = openai.OpenAI(api_key=openai_key)
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": "You are a master video script generator. Output JSON only."},
                    {"role": "user", "content": system_instruction}
                ]
            )
            data = json.loads(resp.choices[0].message.content)
            print(f"[GEN] Synthesized dynamic {len(data.get('scenes', []))}-scene structure via OpenAI.")
            return data
        except Exception as e:
            print(f"[GEN] OpenAI generation notice: {e}")

    # Smart Heuristic Multi-Scene Decomposition
    count = target_scenes if target_scenes > 1 else 4
    words = prompt.strip().split()
    subject = " ".join(words[:6]) if len(words) >= 6 else prompt

    scenes_list = []
    scripts = []

    # Scene 1: Hook
    s1_vo = f"Introducing {subject} — the breakthrough you have been waiting for."
    scripts.append(s1_vo)
    scenes_list.append({
        "scene_num": 1,
        "layout_type": "hook-card",
        "badge": "MAJOR BREAKTHROUGH",
        "headline": f"Discover {subject}",
        "subhead": "Engineered for speed, precision, and complete autonomy.",
        "voiceover_sentence": s1_vo
    })

    # Middle Scenes
    if count == 3:
        s2_vo = "With direct real-time execution and instant tool calling, you can automate your entire workflow seamlessly."
        scripts.append(s2_vo)
        scenes_list.append({
            "scene_num": 2,
            "layout_type": "bento-grid",
            "badge": "CORE CAPABILITY",
            "headline": "Next-Level Performance",
            "subhead": "Designed to scale with your team effortlessly.",
            "voiceover_sentence": s2_vo
        })
    elif count >= 4:
        s2_vo = "Connect your tools and execute multi-step operations with zero latency and complete precision."
        scripts.append(s2_vo)
        scenes_list.append({
            "scene_num": 2,
            "layout_type": "bento-grid",
            "badge": "ZERO LATENCY",
            "headline": "Autonomous Execution",
            "subhead": "Seamless real-time integration across your entire stack.",
            "voiceover_sentence": s2_vo
        })

        s3_vo = "Experience enterprise-grade efficiency with over thirty percent lower operational overhead."
        scripts.append(s3_vo)
        scenes_list.append({
            "scene_num": 3,
            "layout_type": "metrics",
            "badge": "PROVEN EFFICIENCY",
            "headline": "Frontier-Grade Accuracy",
            "subhead": "Validated benchmarks deliver peak performance without bloat.",
            "voiceover_sentence": s3_vo
        })

    if count >= 5:
        s4_vo = "Follow the simple three-step protocol to deploy this right into your existing production setup."
        scripts.append(s4_vo)
        scenes_list.append({
            "scene_num": 4,
            "layout_type": "steps",
            "badge": "DEPLOYMENT PROTOCOL",
            "headline": "3 Steps to Launch",
            "subhead": "Deploy in under two minutes with zero friction.",
            "voiceover_sentence": s4_vo
        })

    # Final Scene: Payoff
    sf_vo = f"Start using {subject} in your workflow today and take your productivity to the next level."
    scripts.append(sf_vo)
    scenes_list.append({
        "scene_num": len(scenes_list) + 1,
        "layout_type": "payoff",
        "badge": "AVAILABLE NOW",
        "headline": "Supercharge Your Stack",
        "subhead": "Get started today with zero setup required.",
        "stat_highlight": "10x",
        "cta_text": "Try It Free Now",
        "voiceover_sentence": sf_vo
    })

    return {
        "title": subject,
        "style": "saas-launch",
        "scenes_count": len(scenes_list),
        "full_script": " ".join(scripts),
        "scenes": scenes_list
    }


# -------------------------------------------------------------
# Dynamic Reel Assembler
# -------------------------------------------------------------
def generate_dynamic_reel(prompt: str, scenes_count: int = 0, video_type: str = "auto",
                          provider: str = "auto", voice: str = "", out_dir: str = None, render: bool = False):
    print("\n" + "=" * 75)
    print(" 🎬  UNROTSKILLVID — DYNAMIC MULTI-SCENE REEL GENERATOR")
    print("=" * 75)
    print(f"Prompt: \"{prompt}\"")

    # 1. Synthesize Dynamic Scene Blueprint
    blueprint = synthesize_dynamic_scenes(prompt, target_scenes=scenes_count)
    actual_scenes = blueprint.get("scenes", [])
    num_scenes = len(actual_scenes)
    full_script = blueprint.get("full_script", prompt)
    title = blueprint.get("title", prompt)

    print(f"[GEN] Generated {num_scenes}-scene structured blueprint for '{title}'.")

    # 2. Prepare Project Directory
    if not out_dir:
        slug = re.sub(r"[^a-z0-9]+", "-", prompt.lower().strip()[:28]).strip("-") or "dynamic-reel"
        out_dir = str(ROOT_DIR / "videos" / f"{slug}-{num_scenes}s")
    
    project_path = Path(out_dir).resolve()
    project_path.mkdir(parents=True, exist_ok=True)
    comps_dir = project_path / "compositions"
    comps_dir.mkdir(parents=True, exist_ok=True)
    assets_dir = project_path / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    fonts_dir = assets_dir / "fonts"
    fonts_dir.mkdir(parents=True, exist_ok=True)

    # Copy fonts
    src_fonts = ROOT_DIR / "assets" / "fonts"
    if src_fonts.exists():
        for f in src_fonts.glob("*.woff2"):
            shutil.copy2(f, fonts_dir / f.name)

    # 3. Generate Voiceover Audio (Gemini / Edge / ElevenLabs / OpenAI)
    audio_path = assets_dir / "narration.wav"
    print("\n[GEN] Synthesizing 48kHz broadcast narration audio...")
    tts_spec = importlib.util.spec_from_file_location("tts_mod", ROOT_DIR / "scripts" / "tts.py")
    tts_mod = importlib.util.module_from_spec(tts_spec)
    tts_spec.loader.exec_module(tts_mod)
    tts_mod.synthesize(text=full_script, provider=provider, voice=voice if voice else None, out_wav=str(audio_path))

    # 4. Map Speech Cuts for Exact N Scenes
    print(f"\n[GEN] Mapping speech pauses for {num_scenes} scenes...")
    map_spec = importlib.util.spec_from_file_location("map_mod", ROOT_DIR / "scripts" / "audio-map.py")
    map_mod = importlib.util.module_from_spec(map_spec)
    map_spec.loader.exec_module(map_mod)

    map_json_path = assets_dir / "audio-map.json"
    audio_map = map_mod.map_audio(str(audio_path), scenes_count=num_scenes, json_out=str(map_json_path))
    total_dur = audio_map["total_duration"]
    scene_timings = audio_map["scenes"]

    # 5. Generate Every Scene Composition HTML File
    print(f"[GEN] Generating {num_scenes} custom GSAP scene compositions...")
    for idx, sc_data in enumerate(actual_scenes, 1):
        sc_html = render_scene_html(sc_data, idx, num_scenes)
        (comps_dir / f"scene{idx}.html").write_text(sc_html, encoding="utf-8")

    # 6. Generate Master index.html
    slots_html = ""
    for sc_time in scene_timings:
        s_idx = sc_time["scene"]
        s_start = sc_time["start"]
        s_dur = sc_time["duration"]
        slots_html += f"""
      <!-- Scene {s_idx} ({s_start:.2f}s - {s_start + s_dur:.2f}s) -->
      <div
        id="slot-scene-{s_idx}"
        class="clip"
        data-composition-id="scene{s_idx}"
        data-composition-src="compositions/scene{s_idx}.html"
        data-start="{s_start:.2f}"
        data-duration="{s_dur:.2f}"
        data-track-index="1"
        data-width="1080"
        data-height="1920"
      ></div>
"""

    master_index_html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Geist"; font-style: normal; font-weight: 400; src: url(assets/fonts/geist-400.woff2) format("woff2"); }}
      @font-face {{ font-family: "Geist"; font-style: normal; font-weight: 600; src: url(assets/fonts/geist-600.woff2) format("woff2"); }}
      @font-face {{ font-family: "Geist"; font-style: normal; font-weight: 700; src: url(assets/fonts/geist-700.woff2) format("woff2"); }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        margin: 0; width: 1080px; height: 1920px; overflow: hidden;
        background: #13100e; color: #f7f2eb; font-family: "Geist", sans-serif;
      }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #13100e; }}
      .bg-glow {{
        position: absolute; width: 850px; height: 850px; border-radius: 50%;
        background: radial-gradient(circle, rgba(255, 107, 53, 0.14) 0%, rgba(255, 107, 53, 0) 70%);
        pointer-events: none; z-index: 0;
      }}
      #root > div[data-composition-src] {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="{total_dur:.2f}"
      data-width="1080"
      data-height="1920"
    >
      <div class="bg-glow" style="left: 120px; top: 180px;"></div>
      <div class="bg-glow" style="right: -80px; bottom: 280px;"></div>

{slots_html}

      <audio
        id="narration"
        class="clip"
        src="assets/narration.wav"
        data-start="0"
        data-duration="{total_dur:.2f}"
        data-track-index="10"
      ></audio>
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const mainTl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = mainTl;
    </script>
  </body>
</html>
"""
    (project_path / "index.html").write_text(master_index_html, encoding="utf-8")

    # 7. Write Configuration Files (hyperframes.json, meta.json, package.json, BRIEF.md)
    hf_json = {
        "$schema": "https://hyperframes.heygen.com/schema/v1.json",
        "name": project_path.name,
        "version": "1.0.0",
        "main": "index.html",
        "width": 1080,
        "height": 1920,
        "fps": 60,
        "duration": round(total_dur, 2),
        "metadata": { "scenes_count": num_scenes, "theme": "dark" }
    }
    (project_path / "hyperframes.json").write_text(json.dumps(hf_json, indent=2), encoding="utf-8")

    meta_json = { "id": project_path.name, "name": title, "scenes": num_scenes }
    (project_path / "meta.json").write_text(json.dumps(meta_json, indent=2), encoding="utf-8")

    pkg_json = {
        "name": project_path.name,
        "private": True,
        "type": "module",
        "scripts": {
            "dev": "npx --yes hyperframes@latest preview",
            "check": "npx --yes hyperframes@latest check",
            "render": "npx --yes hyperframes@latest render"
        }
    }
    (project_path / "package.json").write_text(json.dumps(pkg_json, indent=2), encoding="utf-8")

    brief_md = f"""---
workflow: unrot-tutorial
scenes_count: {num_scenes}
prompt: "{prompt}"
duration: {total_dur:.2f}s
---

# Video Brief: {title}

## Narration Script
{full_script}

## Scene Breakdown ({num_scenes} Scenes)
"""
    for sc in actual_scenes:
        brief_md += f"- **Scene {sc['scene_num']} ({sc.get('layout_type', 'card')}):** {sc.get('headline', '')} — {sc.get('subhead', '')}\n"
    (project_path / "BRIEF.md").write_text(brief_md, encoding="utf-8")

    # 8. Render Video if Requested
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

    print("\n" + "=" * 75)
    print(f" ✨ DYNAMIC {num_scenes}-SCENE REEL READY AT: {project_path}")
    print("=" * 75)
    print(f"  • Total Scenes:  {num_scenes} structured scenes")
    print(f"  • Narration:     {audio_path} ({total_dur:.2f}s)")
    print(f"  • Live Preview:  cd {project_path.relative_to(ROOT_DIR) if project_path.is_relative_to(ROOT_DIR) else project_path} && npm run dev")
    print(f"  • Render MP4:    npx unrotskillvid render {project_path}")
    print("=" * 75 + "\n")

    return str(project_path), rendered_file


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("prompt", nargs="?", default="", help="Prompt, idea, or topic for the video")
    parser.add_argument("--prompt", dest="prompt_flag", default="", help="Explicit prompt flag")
    parser.add_argument("--scenes", type=int, default=0, help="Number of scenes (default: auto 2-7)")
    parser.add_argument("--type", default="auto", help="Video style hint (default: auto)")
    parser.add_argument("--provider", default="auto", choices=["auto", "gemini", "elevenlabs", "openai", "edge"],
                        help="TTS audio provider (default: auto)")
    parser.add_argument("--voice", default="", help="TTS voice name or ID")
    parser.add_argument("--out", default="", help="Target project output directory")
    parser.add_argument("--render", action="store_true", help="Automatically render final 60fps MP4 video")

    args = parser.parse_args()
    prompt_text = args.prompt or args.prompt_flag
    if not prompt_text:
        parser.print_help()
        sys.exit(1)

    generate_dynamic_reel(
        prompt=prompt_text,
        scenes_count=args.scenes,
        video_type=args.type,
        provider=args.provider,
        voice=args.voice,
        out_dir=args.out,
        render=args.render
    )


if __name__ == "__main__":
    main()
