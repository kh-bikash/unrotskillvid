#!/usr/bin/env node

/**
 * UNROTSKILLVID — Next-Generation AI Video Creation Skill & CLI
 * 
 * Build professional vertical reels (9:16) & explainer videos from footage,
 * SaaS launches, code diffs, or faceless AI concepts with realistic human audio
 * (Gemini TTS, ElevenLabs, OpenAI, Edge-TTS).
 */

import { spawn, spawnSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';
import * as readline from 'readline';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

// ANSI Color Helpers
const c = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m',
  orange: '\x1b[38;5;208m',
};

function banner() {
  console.log(`
${c.orange}${c.bright}========================================================================${c.reset}
${c.orange}${c.bright}  🎬  UNROT SKILL VIDEO  —  AI Reel & Explainer Video Generator  🎬${c.reset}
${c.dim}  High-Retention 9:16 Vertical Reels · Human Audio (Gemini TTS) · Multi-Template${c.reset}
${c.orange}${c.bright}========================================================================${c.reset}
`);
}

function promptUser(query) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  return new Promise((resolve) =>
    rl.question(query, (ans) => {
      rl.close();
      resolve(ans.trim());
    })
  );
}

function runCommand(command, args, options = {}) {
  return new Promise((resolve, reject) => {
    let cmd = command;
    let useShell = false;
    if (process.platform === 'win32') {
      if (cmd === 'npx' || cmd === 'npm') {
        cmd = `${cmd}.cmd`;
      }
    }
    const proc = spawn(cmd, args, {
      stdio: 'inherit',
      shell: useShell,
      ...options,
    });
    proc.on('close', (code) => {
      if (code === 0) resolve();
      else reject(new Error(`Command failed with exit code ${code}`));
    });
    proc.on('error', (err) => reject(err));
  });
}

function copyRecursiveSync(src, dest) {
  const exists = fs.existsSync(src);
  const stats = exists && fs.statSync(src);
  const isDirectory = exists && stats.isDirectory();
  if (isDirectory) {
    fs.mkdirSync(dest, { recursive: true });
    fs.readdirSync(src).forEach((childItemName) => {
      copyRecursiveSync(path.join(src, childItemName), path.join(dest, childItemName));
    });
  } else {
    fs.copyFileSync(src, dest);
  }
}

// -------------------------------------------------------------
// Command: list-types
// -------------------------------------------------------------
function listTypes() {
  console.log(`
${c.bright}AVAILABLE VIDEO STYLES & TEMPLATES:${c.reset}

${c.orange}1. screen-hero${c.reset}  (Product Demo & Screen Recording Hero)
   ${c.dim}• 4-scene narrative with virtual camera pan & zoom over real demo footage.${c.reset}
   ${c.dim}• Best for: AI tools, SaaS demos, UI walkthroughs, tech news.${c.reset}

${c.cyan}2. saas-launch${c.reset}  (SaaS Product Reveal & Feature Reel)
   ${c.dim}• Modern browser mockup, bento feature grid, glowing stats, and launch CTA.${c.reset}
   ${c.dim}• Best for: Product Hunt launches, new feature drops, web app promos.${c.reset}

${c.blue}3. code-walkthrough${c.reset}  (Developer & AI Model Showcase)
   ${c.dim}• Code diffs, terminal execution animations, MoE routing, and SWE-bench graphs.${c.reset}
   ${c.dim}• Best for: GitHub repos, LLM releases, developer tooling, PR recaps.${c.reset}

${c.magenta}4. faceless-explainer${c.reset}  (Viral Faceless Storytelling Reel)
   ${c.dim}• Kinetic typography, animated badges, bento cards, and golden takeaways (no footage needed).${c.reset}
   ${c.dim}• Best for: Educational concepts, mental models, finance, viral storytelling.${c.reset}

${c.green}5. comparison-vs${c.reset}  (Head-to-Head Battle & Comparison Reel)
   ${c.dim}• Side-by-side fighter cards, feature matrix table, speed charts, and final verdict.${c.reset}
   ${c.dim}• Best for: Tool vs Tool, Benchmark comparisons, Tech decision guides.${c.reset}
`);
}

// -------------------------------------------------------------
// Command: list-voices
// -------------------------------------------------------------
function listVoices() {
  const pythonScript = path.join(ROOT_DIR, 'scripts', 'tts.py');
  spawnSync('python', [pythonScript, '--list-voices'], { stdio: 'inherit', shell: true });
}

// -------------------------------------------------------------
// Command: init
// -------------------------------------------------------------
function initProject(projectName, type = 'screen-hero', targetDir = 'videos') {
  const validTypes = ['screen-hero', 'saas-launch', 'code-walkthrough', 'faceless-explainer', 'comparison-vs'];
  if (!validTypes.includes(type)) {
    console.error(`${c.red}Error: Unknown video type '${type}'. Available types: ${validTypes.join(', ')}${c.reset}`);
    process.exit(1);
  }

  const projectPath = path.join(process.cwd(), targetDir, projectName);
  if (fs.existsSync(projectPath)) {
    console.error(`${c.red}Error: Directory '${projectPath}' already exists.${c.reset}`);
    process.exit(1);
  }

  const templatePath = path.join(ROOT_DIR, 'templates', type);
  if (!fs.existsSync(templatePath)) {
    console.error(`${c.red}Error: Template '${type}' not found at ${templatePath}${c.reset}`);
    process.exit(1);
  }

  console.log(`${c.bright}Scaffolding new ${c.orange}${type}${c.reset}${c.bright} reel project at: ${c.cyan}${projectPath}${c.reset}...`);
  fs.mkdirSync(projectPath, { recursive: true });
  copyRecursiveSync(templatePath, projectPath);

  // Update meta.json with project name
  const metaFile = path.join(projectPath, 'meta.json');
  if (fs.existsSync(metaFile)) {
    try {
      const meta = JSON.parse(fs.readFileSync(metaFile, 'utf8'));
      meta.name = projectName;
      meta.id = projectName.toLowerCase().replace(/[^a-z0-9]+/g, '-');
      fs.writeFileSync(metaFile, JSON.stringify(meta, null, 2));
    } catch (e) {}
  }

  console.log(`
${c.green}✔ Successfully created '${projectName}' (${type})!${c.reset}

${c.bright}Next Steps:${c.reset}
  1. Generate natural voiceover:
     ${c.cyan}npx unrotskillvid audio "Your narration script here" --out videos/${projectName}/assets/narration.wav${c.reset}
  2. Map speech cuts:
     ${c.cyan}npx unrotskillvid map videos/${projectName}/assets/narration.wav --scenes 4${c.reset}
  3. Preview live in browser:
     ${c.cyan}cd videos/${projectName} && npm run dev${c.reset}
  4. Render 60fps MP4:
     ${c.cyan}npx unrotskillvid render videos/${projectName}${c.reset}
`);
}

// -------------------------------------------------------------
// Command: audio
// -------------------------------------------------------------
async function generateAudio(script, provider = 'auto', voice = '', outPath = 'assets/narration.wav') {
  const pythonScript = path.join(ROOT_DIR, 'scripts', 'tts.py');
  const args = [pythonScript, script, '--provider', provider, '--out', outPath];
  if (voice) {
    args.push('--voice', voice);
  }

  console.log(`${c.bright}Generating human narration audio via TTS...${c.reset}`);
  await runCommand('python', args);
}

// -------------------------------------------------------------
// Command: map
// -------------------------------------------------------------
async function mapAudioTimeline(audioPath, scenes = 4, jsonOut = null) {
  const pythonScript = path.join(ROOT_DIR, 'scripts', 'audio-map.py');
  const args = [pythonScript, audioPath, '--scenes', String(scenes)];
  if (jsonOut) {
    args.push('--json', jsonOut);
  }

  console.log(`${c.bright}Analyzing speech pauses and timeline cut points...${c.reset}`);
  await runCommand('python', args);
}

// -------------------------------------------------------------
// Command: render
// -------------------------------------------------------------
async function renderVideo(projectDir, outMp4 = null) {
  const dir = path.resolve(process.cwd(), projectDir || '.');
  if (!fs.existsSync(path.join(dir, 'index.html'))) {
    console.error(`${c.red}Error: No index.html found in ${dir}. Please specify a valid video project directory.${c.reset}`);
    process.exit(1);
  }

  console.log(`${c.bright}Rendering project at ${c.cyan}${dir}${c.reset}${c.bright} to 1080x1920 60fps MP4...${c.reset}`);
  const renderArgs = ['--yes', 'hyperframes@latest', 'render'];
  if (outMp4) {
    renderArgs.push('--output', outMp4);
  }
  await runCommand('npx', renderArgs, { cwd: dir });
}

async function generateFromPrompt(promptText, scenes = 0, type = 'auto', provider = 'auto', voice = '', outDir = '', render = false) {
  const pythonScript = path.join(ROOT_DIR, 'scripts', 'generate-reel.py');
  const args = [pythonScript, promptText, '--type', type, '--provider', provider];
  if (scenes > 0) args.push('--scenes', String(scenes));
  if (voice) args.push('--voice', voice);
  if (outDir) args.push('--out', outDir);
  if (render) args.push('--render');

  await runCommand('python', args);
}

// -------------------------------------------------------------
// Command: create (Interactive Step-by-Step Wizard)
// -------------------------------------------------------------
async function createWizard() {
  banner();
  console.log(`${c.bright}Welcome to the Unrot Reel Creation Wizard!${c.reset}`);
  console.log(`${c.dim}Let's create your viral reel in a few simple steps.\n${c.reset}`);

  const promptAns = await promptUser(`${c.bright}What is your video about? (Enter a topic or prompt): ${c.reset}`);
  const userPrompt = promptAns.trim() || 'Create a viral tech explainer about autonomous AI agents';

  console.log(`\n${c.bright}2. Choose number of scenes (or let AI decide dynamically):${c.reset}`);
  console.log(`   [0] ${c.white}auto${c.reset}  - AI dynamically calculates optimal scene count`);
  console.log(`   [3] ${c.cyan}3 scenes${c.reset} - Fast teaser / short announcement (15-25s)`);
  console.log(`   [4] ${c.orange}4 scenes${c.reset} - Standard narrative explainer (30-45s)`);
  console.log(`   [5] ${c.blue}5 scenes${c.reset} - Multi-step framework / deep dive (45-60s)`);
  console.log(`   [6] ${c.green}6 scenes${c.reset} - Full comprehensive tutorial (60s+)`);
  const sceneChoice = await promptUser(`${c.bright}Select scenes [0, 3-6] (default 0): ${c.reset}`);
  const scenesCount = parseInt(sceneChoice, 10) || 0;

  console.log(`\n${c.bright}3. Choose your video style (or auto-detect):${c.reset}`);
  console.log(`   [0] ${c.white}auto${c.reset}              - Automatically match best style to your prompt`);
  console.log(`   [1] ${c.orange}screen-hero${c.reset}       - Screen Recording / Product Demo with virtual camera`);
  console.log(`   [2] ${c.cyan}saas-launch${c.reset}       - SaaS Launch / Feature Showcase & Bento Grid`);
  console.log(`   [3] ${c.blue}code-walkthrough${c.reset}  - Developer & AI Model Demo with Code Diffs`);
  console.log(`   [4] ${c.magenta}faceless-explainer${c.reset}- Viral Storytelling Reel (No footage needed)`);
  console.log(`   [5] ${c.green}comparison-vs${c.reset}     - Head-to-Head Comparison & Verdict`);
  const typeChoice = await promptUser(`${c.bright}Select style [0-5] (default 0): ${c.reset}`);
  
  const typeMap = {
    '0': 'auto',
    '1': 'screen-hero',
    '2': 'saas-launch',
    '3': 'code-walkthrough',
    '4': 'faceless-explainer',
    '5': 'comparison-vs',
  };
  const chosenType = typeMap[typeChoice] || 'auto';

  console.log(`\n${c.bright}4. Choose TTS Voice Provider:${c.reset}`);
  console.log(`   [1] ${c.orange}Gemini TTS${c.reset}  (Google Generative AI audio - Natural human voices)`);
  console.log(`   [2] ${c.green}Edge TTS${c.reset}    (Free, zero-config neural voices - Instant high quality)`);
  console.log(`   [3] ${c.magenta}ElevenLabs${c.reset}  (Studio quality voice cloning)`);
  console.log(`   [4] ${c.blue}OpenAI TTS${c.reset}  (tts-1-hd Onyx / Nova)`);
  const provChoice = await promptUser(`Select provider [1-4] (default 2): `);
  const provMap = { '1': 'gemini', '2': 'edge', '3': 'elevenlabs', '4': 'openai' };
  const chosenProvider = provMap[provChoice] || 'edge';

  console.log(`\n${c.bright}🚀 Generating structured video reel from your prompt...${c.reset}\n`);
  await generateFromPrompt(userPrompt, scenesCount, chosenType, chosenProvider, '', '', false);
}

async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  const reservedCommands = [
    'help', '--help', '-h',
    'list-types', 'list-voices',
    'create', 'init', 'audio', 'map', 'render', 'check', 'generate', 'prompt'
  ];

  // 1-LINE EXECUTION: npx unrotskillvid "Your prompt here"
  if (args.length > 0 && !reservedCommands.includes(cmd) && !cmd.startsWith('-')) {
    const promptText = args.filter(a => !a.startsWith('--')).join(' ');
    const render = !args.includes('--no-render');
    const provIdx = args.indexOf('--provider');
    const provider = provIdx !== -1 && args[provIdx + 1] ? args[provIdx + 1] : 'auto';
    const voiceIdx = args.indexOf('--voice');
    const voice = voiceIdx !== -1 && args[voiceIdx + 1] ? args[voiceIdx + 1] : '';
    await generateFromPrompt(promptText, 0, 'auto', provider, voice, '', render);
    return;
  }

  if (cmd === '--help' || cmd === '-h' || cmd === 'help') {
    banner();
    console.log(`
${c.bright}1-LINE USAGE:${c.reset}
  ${c.cyan}npx unrotskillvid "<your prompt or topic>"${c.reset}
  ${c.dim}Takes any prompt, writes the script, generates human voiceover, structures scenes, and renders a 60fps MP4.${c.reset}

${c.bright}EXAMPLES:${c.reset}
  ${c.cyan}npx unrotskillvid "Make a SaaS launch reel for an AI coding assistant"${c.reset}
  ${c.cyan}npx unrotskillvid "Explain the 80/20 rule in productivity"${c.reset}
  ${c.cyan}npx unrotskillvid "Showcase Supabase Auth launch" --provider gemini${c.reset}

${c.bright}MORE COMMANDS:${c.reset}
  ${c.cyan}npx unrotskillvid${c.reset}                             Interactive video creator wizard
  ${c.cyan}npx unrotskillvid list-voices${c.reset}                List all available TTS voices (Gemini, Edge, ElevenLabs, OpenAI)
  ${c.cyan}npx unrotskillvid list-types${c.reset}                 List all visual styles (screen-hero, saas-launch, etc.)
  ${c.cyan}npx unrotskillvid render [dir]${c.reset}                Render existing project to MP4
`);
    return;
  }

  if (cmd === 'generate' || cmd === 'prompt') {
    const promptArgs = args.slice(1).filter(a => !a.startsWith('--'));
    const promptText = promptArgs.join(' ');
    if (!promptText) {
      console.error(`${c.red}Error: Prompt required. Example: npx unrotskillvid "Make a SaaS launch reel"${c.reset}`);
      process.exit(1);
    }
    const scenesIdx = args.indexOf('--scenes');
    const scenes = scenesIdx !== -1 && args[scenesIdx + 1] ? parseInt(args[scenesIdx + 1], 10) : 0;
    const typeIdx = args.indexOf('--type');
    const type = typeIdx !== -1 && args[typeIdx + 1] ? args[typeIdx + 1] : 'auto';
    const provIdx = args.indexOf('--provider');
    const provider = provIdx !== -1 && args[provIdx + 1] ? args[provIdx + 1] : 'auto';
    const voiceIdx = args.indexOf('--voice');
    const voice = voiceIdx !== -1 && args[voiceIdx + 1] ? args[voiceIdx + 1] : '';
    const outIdx = args.indexOf('--out');
    const outDir = outIdx !== -1 && args[outIdx + 1] ? args[outIdx + 1] : '';
    const render = !args.includes('--no-render');
    await generateFromPrompt(promptText, scenes, type, provider, voice, outDir, render);
    return;
  }

  if (cmd === 'list-types') {
    listTypes();
    return;
  }

  if (cmd === 'list-voices') {
    listVoices();
    return;
  }

  if (cmd === 'create') {
    await createWizard();
    return;
  }

  if (cmd === 'init') {
    const name = args[1];
    if (!name) {
      console.error(`${c.red}Error: Project name required. Example: npx unrotskillvid init my-reel --type screen-hero${c.reset}`);
      process.exit(1);
    }
    const typeIdx = args.indexOf('--type');
    const type = typeIdx !== -1 && args[typeIdx + 1] ? args[typeIdx + 1] : 'screen-hero';
    initProject(name, type, 'videos');
    return;
  }

  if (cmd === 'audio') {
    const script = args[1];
    if (!script) {
      console.error(`${c.red}Error: Script text or path required. Example: npx unrotskillvid audio "My script" --provider gemini${c.reset}`);
      process.exit(1);
    }
    const provIdx = args.indexOf('--provider');
    const provider = provIdx !== -1 && args[provIdx + 1] ? args[provIdx + 1] : 'auto';
    const voiceIdx = args.indexOf('--voice');
    const voice = voiceIdx !== -1 && args[voiceIdx + 1] ? args[voiceIdx + 1] : '';
    const outIdx = args.indexOf('--out');
    const outPath = outIdx !== -1 && args[outIdx + 1] ? args[outIdx + 1] : 'assets/narration.wav';
    await generateAudio(script, provider, voice, outPath);
    return;
  }

  if (cmd === 'map') {
    const audioPath = args[1];
    if (!audioPath) {
      console.error(`${c.red}Error: Path to audio.wav required. Example: npx unrotskillvid map assets/narration.wav --scenes 4${c.reset}`);
      process.exit(1);
    }
    const scenesIdx = args.indexOf('--scenes');
    const scenes = scenesIdx !== -1 && args[scenesIdx + 1] ? parseInt(args[scenesIdx + 1], 10) : 4;
    const jsonIdx = args.indexOf('--json');
    const jsonOut = jsonIdx !== -1 && args[jsonIdx + 1] ? args[jsonIdx + 1] : null;
    await mapAudioTimeline(audioPath, scenes, jsonOut);
    return;
  }

  if (cmd === 'render') {
    const projectDir = args[1] && !args[1].startsWith('--') ? args[1] : '.';
    const outIdx = args.indexOf('--out');
    const outMp4 = outIdx !== -1 && args[outIdx + 1] ? args[outIdx + 1] : null;
    await renderVideo(projectDir, outMp4);
    return;
  }

  if (cmd === 'check') {
    const dir = args[1] || '.';
    await runCommand('npx', ['--yes', 'hyperframes@latest', 'check'], { cwd: path.resolve(process.cwd(), dir) });
    return;
  }

  // Fallback
  console.log(`${c.yellow}Unknown command '${cmd}'. Launching creation wizard...${c.reset}\n`);
  await createWizard();
}

main().catch((err) => {
  console.error(`${c.red}\nError: ${err.message}${c.reset}`);
  process.exit(1);
});
