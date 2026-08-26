# Video Types & Template Catalog

`unrotskillvid` comes with 5 pre-built, tested, 60fps vertical reel templates designed for maximum retention across TikTok, Instagram Reels, YouTube Shorts, and X (Twitter).

---

## 1. `screen-hero` (Product Demo & Screen Recording Hero)

**When to use:** You have real screen recording footage, an app UI walkthrough, or a live terminal session, and the footage must carry the credibility.

### Narrative Architecture (4 Scenes)
| Scene | Purpose | Runtime Share | Visual & Audio Register |
|---|---|---|---|
| **1. Hook** | Breakthrough statement + hero badge | 10–15% | Large top-anchored typography + floating character card |
| **2. The Footage** | Screen recording hero | 40–55% | Virtual camera pan/zoom inside stage, bottom caption bar |
| **3. Nuance** | Architecture / limit / data bar | 15–20% | Metric comparison cards with animated gradient progress bars |
| **4. Payoff** | Big stat / outcome + CTA | 20–25% | Centered high-contrast stat card + CTA button pulse |

### Key Design Rules
- The hero footage in Scene 2 is **never cut away from** or broken into multiple `<video>` tags.
- Virtual camera movements (`#camera-rig`) stay gentle if the source footage already has zooming.
- Bottom caption bar updates on speech pauses to guide the viewer.

---

## 2. `saas-launch` (SaaS Product Reveal & Feature Reel)

**When to use:** Launching a new SaaS platform, web app, API service, or major feature update.

### Narrative Architecture (4 Scenes)
| Scene | Purpose | Runtime Share | Visual & Audio Register |
|---|---|---|---|
| **1. Announcement** | "Just Launched" badge + browser preview | 15–20% | macOS-style dark browser mockup with animated URL bar |
| **2. Bento Features** | 3-card bento grid | 35–45% | Staggered cards with glowing neon icon badges |
| **3. Integration Hub** | 4-way integration chips | 20–25% | Supabase, GitHub, Slack, Cloud connector badges |
| **4. Pricing CTA** | $0 trial card + Launch CTA | 15–20% | High-contrast gradient button with scale micro-animations |

---

## 3. `code-walkthrough` (Developer & AI Model Showcase)

**When to use:** Open-source AI releases, GitHub repositories, CLI tools, coding assistants, and technical deep-dives.

### Narrative Architecture (4 Scenes)
| Scene | Purpose | Runtime Share | Visual & Audio Register |
|---|---|---|---|
| **1. Model Specs** | Open-weight badge + spec table | 15–20% | Sparse MoE specs, parameter counts, context length |
| **2. Code Diff** | Syntax-highlighted code diff | 35–45% | Green/red addition/deletion diff bars with tab header |
| **3. Benchmarks** | SWE-bench & HumanEval bars | 20–25% | Live animating percentage progress bars vs Sonnet |
| **4. Quickstart CTA** | `ollama run` terminal box + HuggingFace CTA | 15–20% | One-line terminal copy box + download button |

---

## 4. `faceless-explainer` (Viral Storytelling Reel)

**When to use:** Concepts, productivity mental models, finance advice, tech news, or philosophy — **no screen footage required**.

### Narrative Architecture (4 Scenes)
| Scene | Purpose | Runtime Share | Visual & Audio Register |
|---|---|---|---|
| **1. Curiosity Hook** | Provocative question | 15–20% | Kinetic text with animated accent pop-in + emoji badge |
| **2. The Mistake** | 3 common traps/errors | 30–35% | Numbered red pill list with high-contrast text |
| **3. The Secret** | 3-step framework card | 25–30% | Step 1-2-3 protocol container with sky-blue border glow |
| **4. Golden Rule** | Save & share payoff | 15–20% | Large quote card + "Save this reel" primary CTA |

---

## 5. `comparison-vs` (Head-to-Head Battle & Comparison Reel)

**When to use:** Comparing two models, tools, or frameworks (e.g. Model A vs Model B, Next.js vs Vite, Old Way vs New Way).

### Narrative Architecture (4 Scenes)
| Scene | Purpose | Runtime Share | Visual & Audio Register |
|---|---|---|---|
| **1. The Showdown** | VS badge + side-by-side fighter cards | 15–20% | Red vs Blue glowing cards with central pulsing "VS" badge |
| **2. Feature Matrix** | 4-row checkmark table | 35–40% | Context window, tool accuracy, latency, and open license checks |
| **3. Speed & Cost** | Dual bar charts (+180% faster / -65% cheaper) | 20–25% | Animated bar graphs comparing throughput and price |
| **4. Verdict** | Winner card + discussion prompt | 15–20% | Glowing trophy badge with "Drop your thoughts" CTA |
