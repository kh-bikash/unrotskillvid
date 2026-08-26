# Inherited workflow — the parts of a general HyperFrames run this skill owns itself

`/unrot-tutorial` is self-contained: it does **not** load `/general-video`. Everything a generic
HyperFrames authoring run would have supplied — brief handling, run shape, the build stage order,
scene dispatch, and the closing gates — lives here.

It still reads the **domain** skills (`/hyperframes-core`, `/hyperframes-creative`,
`/hyperframes-animation`, `/hyperframes-registry`, `/media-use`, `/figma`). Those are shared
capability skills, not workflows, and they are the source of truth for the composition contract,
motion recipes, and media resolution. Independence means no workflow skill sits above this one.

---

## 1. Cross-cutting source adapters

- **Media.** For any audio, image, icon, logo, voice, grade, LUT, treatment/effect, caption, or
  media operation, load `/media-use` and follow `../media-use/references/resolve.md` (resolve,
  adopt, reuse) and `../media-use/references/setup-providers.md` (providers, auth). Vague footage
  feedback ("looks flat", "make it retro") and named styles go through
  `../media-use/references/media-treatments.md` before editing — do not improvise a supported
  media effect with ad-hoc CSS/SVG filters or opacity.

  Before the first authenticated provider action, run `npx hyperframes auth status` and relay its
  output verbatim. If signed out: a collaborative run waits for sign-in or an explicit offline
  choice; an autonomous run states the status and continues through an available offline provider.
  Surface a blocker when no offline provider can satisfy a required capability. Adopting a local
  file the user already gave you needs no auth gate.

- **Figma.** If any input is a `figma.com` URL, run `/figma` first and build from its exported
  assets, tokens, or frames. Do not call the raw Figma connector directly — that skips SVG
  sanitization, media provenance, and brand-token binding.

---

## 2. Start from project state

Apply the **first** matching row. Do not evaluate lower rows.

| State                                                      | Action                                                                                                    |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Specific edit to an existing project                       | Make the edit, preserve existing project decisions, rerun the affected checks. Do not reopen discovery.    |
| `BRIEF.md` exists                                          | Read it. If `workflow:` names a different workflow, load that skill and hand over. Ask no brief questions. |
| No brief, but `hyperframes.json` or `STORYBOARD.md` exists | Resume from files and recorded preferences. Backfill `BRIEF.md` only from known facts.                     |
| Fresh creation                                             | Confirm the brief (below), scaffold, then build.                                                           |

### Scaffold

Pick a kebab-case directory name from the brief and scaffold **before** writing the brief
(`init` refuses a non-empty directory):

```bash
npx hyperframes init "videos/<project>" --non-interactive --example=blank --skill=unrot-tutorial
```

Then write `BRIEF.md` at the project root — the directory containing `hyperframes.json`.

### `BRIEF.md` shape

YAML frontmatter of confirmed, normalized fields, then prose sections. Minimum for this genre:

```markdown
---
workflow: unrot-tutorial
flow: automation # automation | companion
storyboard: yes # yes | no
message: "One sentence — the ONE thing this reel must land"
aspect: 1080x1920
language: en
length: 45s
---

## Intent

What the reel is, for whom, why now. Tone in the user's own words.

## Assets

- assets/demo.mp4 — the screen recording; it is scene 2's hero.
- assets/narration.wav — the voiceover; its pauses decide every cut.

## Customizations

Capabilities the user opted into, and bespoke asks, one line each.

## Notes

Constraints, references, things to avoid.
```

Record only the **preference-backed** subset as cross-project memory —
`destination`, `aspect`, `language`, `flow`, `storyboard`, `voice`, `style_preset` — with:

```bash
node <MEDIA_DIR>/scripts/prefs.mjs record --hyperframes <PROJECT_ROOT>
```

`<MEDIA_DIR>` is the installed `/media-use` skill directory. Never record an inferred default.
`message`, `length`, `audience`, `angle` describe this video, not the user — frontmatter only.

`BRIEF.md` stays the run's truth. A mid-run confirmed change rewrites the field as it happens; an
accepted capability or adopted asset lands as one line in the matching body section. A decision
that lives only in chat is a decision resume never sees.

---

## 3. Run shape

| Field          | Meaning                               | Effect                                                                             |
| -------------- | ------------------------------------- | ---------------------------------------------------------------------------------- |
| `flow`         | Who drives                            | `automation`: choose and execute the route. `companion`: co-create in conversation. |
| `storyboard`   | Whether the board is a review surface | `yes`: run plan and sketch review. `no`: build without the board.                  |
| derived `mode` | How checkpoint gates behave           | Derived from the two above. Never ask the user to name a mode.                      |

Do not invent synonyms for these states. A "just build it" signal arrives as
`flow: automation`, `storyboard: no`.

For `flow: automation`, state the chosen route in one line in the first progress update.

### Companion flow

When `flow: companion`:

- Reconcile accepted `## Assets` and `## Customizations` with what is actually on disk. Finish
  accepted work still pending; leave completed work alone; never re-offer an accepted capability
  as if it were new.
- **Arrive as the director, not the contractor.** The first plan is the ceiling treatment: the
  four-scene arc, the design spec, each scene's motion treatment cited by name, the camera plan
  for the clip, the transitions, the audio identity (music and sound marks, or deliberate
  silence), the user's footage placed, and a designed open and close. One line each on what a
  layer adds; flag the expensive ones (render time, sign-in, billing) as you name them. The user
  trims a treatment down — they should not have to assemble one approval by approval.
- **The ceiling belongs to the concept, not the toolbox.** Every layer must serve the brief's
  `message`. A treatment that would dress any reel the same way is decoration. Craft rises to the
  ceiling; content never grows past what was asked.
- Read `../hyperframes/references/capability-menu.md` before offering a capability, and offer one
  or two traced at material the user is already looking at. Never dump the catalogue.
- Record an accepted capability in `BRIEF.md` immediately.
- Keep every storyboard, validation, content-sheet, and render-approval gate. Companion changes
  who steers, not what quality requires.

---

## 4. Load knowledge before the stage that needs it

Mandatory when the condition matches. Recollection does not substitute — progressive disclosure
only saves context when the reference is actually loaded.

| Condition                                                | Read before acting                                                                                       |
| -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Any composition HTML or scene layout                     | `/hyperframes-core`, plus `references/determinism-rules.md` for its layout contract                      |
| Any visual treatment decision                            | `/hyperframes-creative` → `references/house-style.md`, `references/video-composition.md`                  |
| Any motion, animation, or scene transition               | `/hyperframes-animation`; follow its routing to the matching rules, blueprints, or transition references  |
| The clip's camera move                                   | this skill's `references/camera.md` — before writing any of it                                            |
| Any typography decision                                  | `/hyperframes-creative` → `references/typography.md`, then this skill's § Fonts                          |
| `storyboard: yes`                                        | `../hyperframes-core/references/storyboard-format.md` and `../hyperframes-core/references/review-loop.md` |
| Any media asset or operation (narration, BGM, SFX, grade) | `/media-use`; for framework playback also `/hyperframes-core` → `references/variables-and-media.md`       |
| Multi-scene assembly                                     | `../hyperframes-core/references/production-loop.md`                                                       |
| A design spec exists, before final approval              | `/hyperframes-creative` → `references/design-adherence.md`                                                |
| Installing or wiring a registry block                    | `/hyperframes-registry`                                                                                   |

---

## 5. Build stage order

Dependency order. Skip a stage only when its input is absent.

1. **Map the audio.** Always first — see SKILL.md § 1. Every cut is placed against real speech.
2. **Plan.** The four-scene shape, the viewer arc, the duration driver, and each scene's motion
   citation: a blueprint id from `/hyperframes-animation` → `blueprints-index.md` when one fits,
   or the named rules it composes from `rules-index.md` when none does. Motion names come from
   those indexes — never invented. Record the plan as the dispatch artifact: one `## Frame N`
   block per scene in `STORYBOARD.md` with `status: outline`, a declared `src:`, the citation, and
   the beat text — **even when `storyboard: no`.** The block is the dispatch unit; the board is
   only the review surface.
3. **Review the plan when requested.** `storyboard: yes` → run the review loop over those blocks.
   `storyboard: no` → continue without opening the board.
4. **Resolve dependencies.** Install registry blocks before parallel work. Stage the user's
   footage and narration, adopt existing media, resolve only what the brief requires. Audio is
   already done at stage 1 because its timings drive duration.
5. **Build scenes.** Implement each scene at its most visible moment first — the confirmed
   wireframe, when one exists, is that end state and must not be redrawn — then animate from its
   cited blueprint or rules, reading the full recipe body
   (`/hyperframes-animation` → `blueprints/<id>.md`, `rules/<id>.md`) before writing motion.

   **Build this genre inline.** Four scenes is far below the scale where fan-out pays for itself
   — authoring packets and warming fresh worker contexts costs real minutes and tokens
   (measured elsewhere: 5 short scenes ≈ 9 min inline vs ≈ 21 min packetized). Build them one
   after another in this context. Only if a run grows well past the four-scene shape does
   dispatch become worth it; then give each worker 2–3 scenes, spawn all workers in a single
   wave, and follow `../hyperframes-core/references/subagent-dispatch.md` with
   `../hyperframes-core/references/frame-worker-core.md` as the worker role.
6. **Assemble.** Mount scenes, the clip, transitions, captions, and audio using the production
   loop. Real voice duration overrides every estimate.
7. **Verify.** `npx hyperframes lint` for fast feedback after the first HTML pass and after
   structural changes. `npx hyperframes check` at the final gate — it reruns lint internally, so
   do not run a redundant standalone lint right before it. Inspect midpoint snapshots for
   sub-compositions and review the animation map for multi-scene work.
8. **Content sheet.** SKILL.md § 7. The user approves it before render.
9. **Final approval.** Open the final Studio preview only after checks pass. Ask whether to render
   or revise. Render only after approval.

---

## 6. Gates that always apply

### Keep scope exact

Build what the user asked for. A captioned clip is not a captioned clip plus a music bed and an
outro card. Offer additions before adding them.

### Establish design before HTML

Resolve the design source in this order: `frame.md` → `design.md` → `DESIGN.md`. The first file
found is brand truth.

When no design spec exists, complete all four before writing composition HTML:

1. Ground the visual identity in `house-style.md` and `video-composition.md`.
2. Write one sentence naming the concept angle.
3. Choose an embeddable font pairing from `/hyperframes-creative` → `references/typography.md`. Do
   not assume an unbundled display font exists in cloud rendering.
4. Define the focal element, edge anchors, supporting detail, and background treatment.

Then hold it against this skill's `references/design-law.md`, which overrides generic house style
where the two differ — it is written for footage-led vertical reels.

For a named style or mood, read `/hyperframes-creative` → `references/visual-styles.md`. When the
user needs to choose visually and no shipped preset fits, use `references/design-picker.md` there.

### Preserve the composition contract

Timed elements carry `class="clip"` with `data-start`, `data-duration`, `data-track-index`. The
root and relevant ancestors are sized. Each composition registers exactly one paused, seek-safe
timeline on `window.__timelines`. Rendering is deterministic — no render-time network fetches, no
clocks, no unseeded randomness.

### Borrow other genres safely

When a beat resembles a shipped workflow's, borrow its story shape and taste as an example — run
`npx hyperframes skills update <workflow-name>` first — but not its private scripts, pipeline
state, or directory contract. The build stays owned by this skill.

---

## 7. Done

A run is complete only when:

- the requested scope is implemented;
- for `flow: companion`, the **treatment** is delivered, not just the scope: every scene's cited
  blueprint or rules realized, the audio identity present (or the silence chosen and said), the
  open and close designed rather than defaulted;
- `npx hyperframes check` passes, including its built-in lint stage;
- design adherence is reviewed against `/hyperframes-creative` → `references/design-adherence.md`
  when a design spec exists;
- contrast findings are resolved;
- layout errors are fixed rather than waived — waive only with `data-layout-allow-*` where the
  layering is genuinely intentional (stacked crossfade states, a camera world overflowing its band);
- sub-composition snapshots are inspected when applicable;
- the content sheet is produced and approved;
- the animation map (`hyperframes-animation/scripts/animation-map.mjs`) is reviewed;
- an autonomous handoff includes an inspected contact or content sheet using scene midpoints;
- the handoff names the final preview or rendered artifact and reports the **actual** duration;
- the user approved the final Studio preview before render;
- the rendered file is verified — `ffprobe` **and** frames pulled back out of the finished file. A
  successful exit code is not proof the picture is right.

After final approval, offer once to freeze the run as a recipe
(`../hyperframes-core/references/review-loop.md` § 4).
