import os
import math
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def create_hero_demo(output_path="videos/glm-46-reel/assets/demo.mp4", duration=19.0, fps=30):
    width, height = 1920, 1080
    total_frames = int(duration * fps)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    temp_raw = output_path.replace(".mp4", "_raw.mp4")
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_raw, fourcc, fps, (width, height))
    
    try:
        font_mono_bold = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 22)
        font_mono = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 19)
        font_mono_sm = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 16)
        font_ui = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 20)
        font_ui_bold = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
        font_ui_sm = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16)
    except:
        font_mono_bold = font_mono = font_mono_sm = font_ui = font_ui_bold = font_ui_sm = ImageFont.load_default()

    for frame_idx in range(total_frames):
        t = frame_idx / fps
        img = Image.new("RGB", (width, height), color="#0D0F16")
        draw = ImageDraw.Draw(img)
        
        # 1. Top Window Bar
        draw.rectangle([0, 0, width, 48], fill="#151824")
        draw.line([0, 48, width, 48], fill="#262B3D", width=1)
        
        # macOS Window dots
        draw.ellipse([24, 18, 36, 30], fill="#EF4444")
        draw.ellipse([46, 18, 58, 30], fill="#F59E0B")
        draw.ellipse([68, 18, 80, 30], fill="#10B981")
        
        # Window Center Title
        title_text = "GLM-4.6 (355B MoE) · Claude Code & Cline Autonomous Environment"
        draw.text((width // 2 - 270, 14), title_text, fill="#94A3B8", font=font_ui)
        
        # 2. Left Sidebar: File Tree & Active Specs
        sidebar_w = 320
        draw.rectangle([0, 49, sidebar_w, height - 36], fill="#11131C")
        draw.line([sidebar_w, 49, sidebar_w, height - 36], fill="#262B3D", width=1)
        
        draw.text((24, 66), "PROJECT EXPLORER", fill="#64748B", font=font_ui_bold)
        
        files = [
            ("📁 zhipu-glm46-agent", "#94A3B8"),
            ("  📁 src/moe", "#94A3B8"),
            ("    📄 router_top2.py", "#38BDF8"),
            ("    📄 kv_cache_sparse.py", "#FF6B35"),
            ("    📄 expert_pool_32b.py", "#94A3B8"),
            ("  📁 benchmarks", "#94A3B8"),
            ("    📄 swe_bench_verified.py", "#34D399"),
            ("    📄 cc_bench_eval.ts", "#F59E0B"),
            ("  📁 agent_runtime", "#94A3B8"),
            ("    📄 tool_invoker.rs", "#C084FC"),
            ("📄 config.yaml (200k tokens)", "#94A3B8"),
        ]
        
        y_f = 105
        for fname, col in files:
            draw.text((24, y_f), fname, fill=col, font=font_mono)
            y_f += 30
            
        # Model Specs Card in Sidebar Bottom
        draw.rectangle([16, height - 190, sidebar_w - 16, height - 52], fill="#171B28", outline="#2F364E", width=1)
        draw.text((28, height - 180), "ACTIVE CONTEXT: 194,800 / 200k", fill="#F1F5F9", font=font_ui_sm)
        
        p = min(1.0, 0.45 + 0.52 * (1.0 - math.exp(-t * 0.35)))
        draw.rectangle([28, height - 152, sidebar_w - 28, height - 138], fill="#252B3E")
        draw.rectangle([28, height - 152, 28 + int((sidebar_w - 56) * p), height - 138], fill="#FF6B35")
        
        draw.text((28, height - 128), "Params: 32B Active / 355B Total", fill="#38BDF8", font=font_mono_sm)
        draw.text((28, height - 104), "Cache Hit: 94.2% (30% Token Save)", fill="#10B981", font=font_mono_sm)
        draw.text((28, height - 80), "License: MIT Open Weight", fill="#E2E8F0", font=font_mono_sm)

        # 3. Center Editor Panel (Code View)
        editor_w = 840
        draw.rectangle([sidebar_w + 1, 49, sidebar_w + 1 + editor_w, height - 36], fill="#0D0F16")
        draw.line([sidebar_w + 1 + editor_w, 49, sidebar_w + 1 + editor_w, height - 36], fill="#262B3D", width=1)
        
        # Tabs
        draw.rectangle([sidebar_w + 1, 49, sidebar_w + 240, 92], fill="#1B1F2D")
        draw.text((sidebar_w + 24, 60), "kv_cache_sparse.py", fill="#F8FAFC", font=font_ui)
        draw.rectangle([sidebar_w + 241, 49, sidebar_w + 480, 92], fill="#11131C")
        draw.text((sidebar_w + 264, 60), "router_top2.py", fill="#64748B", font=font_ui)
        
        code_lines = [
            ("import torch", "#C084FC"),
            ("from zai.moe import GLM46Router, SparseAttention", "#C084FC"),
            ("", "#FFFFFF"),
            ("@torch.compile(mode='max-autotune')", "#34D399"),
            ("class DynamicMoEBlock(torch.nn.Module):", "#38BDF8"),
            ("    def __init__(self, d_model=8192, n_experts=8):", "#E2E8F0"),
            ("        super().__init__()", "#94A3B8"),
            ("        self.router = GLM46Router(top_k=2, active_params='32B')", "#FF6B35"),
            ("        self.context_len = 200_000 # 200k Token Window", "#F59E0B"),
            ("", "#FFFFFF"),
            ("    def forward(self, hidden_states: torch.Tensor):", "#38BDF8"),
            ("        # Dynamic Top-2 routing with 30% lower token footprint", "#64748B"),
            ("        routing_weights, selected_experts = self.router(hidden_states)", "#E2E8F0"),
            ("        return self.expert_pool(hidden_states, routing_weights)", "#38BDF8"),
            ("", "#FFFFFF"),
            ("    # SWE-Bench Verified patch: resolves issue #402", "#34D399"),
            ("    def evict_kv_cache(self, threshold=0.92):", "#38BDF8"),
            ("        return self.sparse_cache.evict_redundant_tokens(threshold)", "#34D399")
        ]
        
        y_c = 110
        revealed_lines = min(len(code_lines), int(t * 1.8) + 8)
        for i in range(revealed_lines):
            line_str, col = code_lines[i]
            draw.text((sidebar_w + 16, y_c), f"{i+1:2d}", fill="#475569", font=font_mono)
            draw.text((sidebar_w + 56, y_c), line_str, fill=col, font=font_mono)
            y_c += 28

        # 4. Right Side: Interactive Agent Console (Terminal & Tool Calling)
        term_x = sidebar_w + 1 + editor_w + 1
        draw.rectangle([term_x, 49, width, height - 36], fill="#0A0C11")
        
        # Terminal Header
        draw.rectangle([term_x, 49, width, 92], fill="#131620")
        draw.text((term_x + 20, 60), "CLAUDE CODE / CLINE AGENT TERMINAL", fill="#FF6B35", font=font_ui_bold)
        
        logs = [
            (0.5, "🤖 [GLM-4.6] Initializing agent on SWE-Bench Verified...", "#38BDF8"),
            (2.5, "⚡ Ingested 194,800 tokens of codebase context (0.9s)", "#34D399"),
            (5.0, "→ TOOL: grep_search('sparse_cache.evict_redundant_tokens')", "#FBBF24"),
            (7.5, "  Matched 3 occurrences across src/moe/kv_cache_sparse.py", "#94A3B8"),
            (10.0, "→ TOOL: multi_replace_file_content('kv_cache_sparse.py')", "#FBBF24"),
            (12.5, "✓ Applied 14-line AST-verified patch cleanly", "#34D399"),
            (14.5, "→ TOOL: run_command('pytest tests/test_swe_bench_moe.py')", "#FBBF24"),
            (16.5, "  [TEST] 18/18 tests PASSED in 1.24s (100% accuracy)", "#10B981"),
            (17.5, "🏆 SWE-Bench Verified: 68.1% | CC-Bench Win Rate: 48.6%", "#FF6B35"),
        ]
        
        y_t = 110
        for log_t, text, col in logs:
            if t >= log_t:
                draw.text((term_x + 20, y_t), text, fill=col, font=font_mono_bold if col == "#FF6B35" else font_mono)
                y_t += 36

        # Terminal Blinking cursor
        if int(t * 2) % 2 == 0:
            draw.rectangle([term_x + 20, y_t + 4, term_x + 32, y_t + 24], fill="#FF6B35")

        # 5. Bottom Status Bar
        draw.rectangle([0, height - 36, width, height], fill="#151824")
        draw.text((24, height - 28), "⚡ Zhipu AI · GLM-4.6 (355B MoE) · 200k Context · SWE-Bench Verified: 68.1% · MIT License", fill="#94A3B8", font=font_ui_sm)
        draw.text((width - 290, height - 28), "🟢 Parity with Claude Sonnet 4", fill="#10B981", font=font_ui_sm)
        
        frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)
        
    out.release()
    
    # Re-encode with ffmpeg: -g 30 -keyint_min 30 ensures a keyframe every second for flawless seeks
    import subprocess
    subprocess.run([
        "ffmpeg", "-y", "-i", temp_raw,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-g", "30", "-keyint_min", "30", "-movflags", "+faststart",
        output_path
    ], check=True)
    
    if os.path.exists(temp_raw):
        os.remove(temp_raw)
    print("New high-accuracy hero demo video generated at", output_path)

if __name__ == "__main__":
    create_hero_demo()
