# Unrot Skill Video (`unrotskillvid`)

An installable AI-agent skill that turns any prompt, script, product demo, or announcement into a complete, structured 60fps vertical reel with human voiceover.

It works with **Claude Code**, **Codex**, **Cursor**, **GitHub Copilot**, **Windsurf**, **OpenCode**, **Cline**, and many other agents that support the open `SKILL.md` format.

---

## What it does

- **1-Command Video Creation**: Turns any prompt, article, or script into a complete 1080 × 1920 (9:16) 60fps vertical reel in a single step.
- **Intelligent Scene Structuring**: Dynamically structures the narrative into the ideal number of visual scenes (2 to 7+ scenes) based on the topic.
- **Realistic Human Voiceover**: Synthesizes 48kHz broadcast-mastered audio using **Google Gemini TTS**, **Microsoft Edge Neural TTS**, **ElevenLabs**, or **OpenAI TTS**.
- **Speech-Pause Alignment**: Places scene cuts on real speech pauses so transitions never cut mid-sentence.
- **60fps GSAP Compositions**: Builds responsive HTML5/GSAP compositions with typography, glowing badges, glass cards, and bento grids.
- **Render-Ready MP4 Output**: Produces editable HTML compositions, WAV voiceover, review contact sheets, and a rendered 60fps MP4 video.
- **Review-First Architecture**: Stops at review-ready local files and never publishes a post without separate authorization.

---

## Before you start

You need:
- An AI coding agent or IDE agent such as **Claude Code**, **Codex**, **Cursor**, or **GitHub Copilot**.
- [Node.js](https://nodejs.org/) (LTS release) installed on your computer.
- Python 3.10+ and [FFmpeg](https://ffmpeg.org/) installed.
- An internet connection for the one-time installation.

### Check Prerequisites
Open Terminal, PowerShell, or your IDE's terminal and run:
```bash
node --version
python --version
ffmpeg -version
```
If versions are displayed, continue to the next step.

---

## Install the skill

Installation is required only once.

### Recommended: let the installer detect your agent
Copy and run:
```bash
npx --yes skills add kh-bikash/unrotskillvid --skill unrotskillvid --global
```
The installer will show the compatible agents it detects. Select the agent or agents where you want to use the skill, confirm the installation, and then restart those applications.

### Install directly for a specific agent
Use one of these commands if you already know your agent:

| Agent | Command |
|---|---|
| **Claude Code** | `npx --yes skills add kh-bikash/unrotskillvid --skill unrotskillvid --global --agent claude-code --yes` |
| **Codex** | `npx --yes skills add kh-bikash/unrotskillvid --skill unrotskillvid --global --agent codex --yes` |
| **Cursor** | `npx --yes skills add kh-bikash/unrotskillvid --skill unrotskillvid --global --agent cursor --yes` |
| **GitHub Copilot** | `npx --yes skills add kh-bikash/unrotskillvid --skill unrotskillvid --global --agent github-copilot --yes` |
| **Windsurf** | `npx --yes skills add kh-bikash/unrotskillvid --skill unrotskillvid --global --agent windsurf --yes` |
| **OpenCode** | `npx --yes skills add kh-bikash/unrotskillvid --skill unrotskillvid --global --agent opencode --yes` |
| **Cline** | `npx --yes skills add kh-bikash/unrotskillvid --skill unrotskillvid --global --agent cline --yes` |

### Confirm the installation
Run:
```bash
npx --yes skills list --global
```
Look for `unrotskillvid`, then restart your AI agent or IDE.

---

## Use the skill

### Step 1: Open your AI agent
Start Claude Code, Codex, Cursor, Copilot, Windsurf, OpenCode, Cline, or another compatible agent. Open the workspace where you want the video generated.

### Step 2: Provide the topic or footage
Give the agent one or more of the following:
- A prompt or topic idea (e.g. *"Announce our new SaaS feature"*);
- A product demo clip or screen recording (`demo.mp4`);
- A blog post or news announcement URL;
- A voiceover script text.

### Step 3: Invoke the skill

| Agent | How to invoke it |
|---|---|
| **Claude Code** | Type `/unrotskillvid`, or ask Claude to use the skill |
| **Codex** | Type `$unrotskillvid`, use `/skills`, or ask Codex to use the skill |
| **Cursor** | Say `Use the unrotskillvid skill` |
| **GitHub Copilot** | Say `Use the unrotskillvid skill` |
| **Other compatible agents** | Say `Use the unrotskillvid skill` |

Agents may also select the skill automatically when the request asks to create a video, vertical reel, or explainer.

### Step 4: Use this universal prompt

```
Use the unrotskillvid skill. Create a high-retention 9:16 vertical reel about: [PASTE YOUR TOPIC, URL, OR SCRIPT]

Requirements:
- 1080 × 1920 pixels, 60fps
- Structure the narrative into dynamic visual scenes
- Generate natural human voiceover audio (Gemini TTS / Edge TTS)
- Align all visual cuts to natural speech pauses
- Render the finished 60fps MP4 video
- Save everything in output/my-reel
- Do not publish anything
```

### Step 5: Review the files
The agent should:
1. Select the best visual style and outline the scene plan.
2. Synthesize 48kHz natural narration audio.
3. Map speech pause midpoints to sync timeline cuts.
4. Generate the HTML5/GSAP scene compositions.
5. Render the 60fps MP4 video and review contact sheet.
6. Provide clickable links or exact output paths.

**Typical output directory:**
```
output/my-reel/
├── index.html                  # Master timeline composition
├── compositions/               # Scene sub-compositions
│   ├── scene1.html
│   ├── scene2.html
│   └── scene3.html
├── assets/
│   ├── narration.wav           # Mastered 48kHz voiceover
│   └── audio-map.json          # Speech pause cut timestamps
└── out/
    └── my-reel.mp4             # 🎬 60fps broadcast MP4 video
```

---

## ⚡ Direct 1-Line CLI Execution (Without an Agent)

You can also run `unrotskillvid` directly in your terminal without opening an AI agent:

```bash
# 1. Autonomous video generation from a prompt
npx unrotskillvid "Make a SaaS launch reel for an AI coding assistant"

# 2. Viral storytelling explainer (no footage required)
npx unrotskillvid "Explain the 80/20 rule in productivity"

# 3. With Google Gemini TTS human voiceover
npx unrotskillvid "Showcase Supabase Auth launch" --provider gemini --voice Puck
```

---

## 🎨 Template Catalog

| Template | Best for |
|---|---|
| **`screen-hero`** | Product demos & screen recordings with smooth virtual camera pans/zooms |
| **`saas-launch`** | Modern browser mockup, bento feature grid, glowing stats, and launch CTA |
| **`code-walkthrough`** | Syntax-highlighted code diffs, terminal execution, and benchmark graphs |
| **`faceless-explainer`** | Kinetic typography, glowing badges, and takeaway cards (**no footage needed**) |
| **`comparison-vs`** | Head-to-head showdown, feature matrix table, speed charts, and final verdict |

The skill automatically selects the ideal template based on your prompt, or you can specify one directly.

---

## 🔄 Request changes

Continue in the same conversation with your agent. For example:
- *"Make the hook headline punchier and under 6 words."*
- *"Change the voice to Google Gemini Puck."*
- *"Add a 3-card bento grid to Scene 2."*
- *"Make the CTA button pulse faster."*
- *"Rerender the approved version as a 1080x1920 60fps MP4."*

---

## 🔄 Update the skill

Run occasionally to download improvements:
```bash
npx --yes skills update unrotskillvid --global --yes
```
Restart your agent afterward.

## 🗑️ Remove the skill

```bash
npx --yes skills remove unrotskillvid --global --yes
```

---

## 🛠️ Troubleshooting

### `node` or `npx` is not recognized
Install the Node.js LTS release from [nodejs.org](https://nodejs.org/), close the terminal, and reopen it.

### The skill does not appear in your agent
1. Run `npx --yes skills list --global`.
2. Confirm that `unrotskillvid` appears in the list.
3. Restart your AI agent or IDE.
4. Invoke it explicitly using `/unrotskillvid` or `Use the unrotskillvid skill`.

### Voiceover fails or sounds robotic
- Ensure you have an internet connection for TTS synthesis.
- To use Google Gemini TTS, ensure `GEMINI_API_KEY` is set in your environment (`export GEMINI_API_KEY="..."`).
- If no key is set, the tool seamlessly uses free Microsoft Edge Neural TTS with natural human pacing.

---

## 📚 Compatibility references

- [OpenAI: Build skills for ChatGPT and Codex](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/features-overview)
- [Cursor: Agent Skills](https://prod.cursor.com/docs/skills)
- [GitHub Copilot: About agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
- [Skills CLI supported agents](https://github.com/vercel-labs/skills#supported-agents)

---

## 📄 License

MIT License © 2026 [Bikash](https://github.com/kh-bikash). Free to use, modify, and distribute for personal and commercial projects.
