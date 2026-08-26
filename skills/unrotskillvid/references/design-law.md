# Design law

A working starting point plus the parts that hold regardless of palette.

## Who it has to work for

Both audiences in the same frame. Every idea appears twice: once as **plain English** in the
type, once as a **thing you can see**. The real footage carries credibility for practitioners;
the copy and shapes carry meaning for everyone else. A frame that only lands for one of the two
is not finished.

## Banned — reads as "for insiders only"

These are what make a tech reel feel closed. They are the difference between a video your
mother can follow and one only your team can:

- Monospace type anywhere. The single biggest tell.
- Terminal windows with real chrome, prompts, carets, code lines, file paths, diffs.
- `SESSION A` / `AGENT_01` labels, registration marks, index counters, tick rows.
- Jargon in the copy. Say **chat, job, note, finishes, picks it up, passes along** — not
  session, middleware, context window, handoff, token.
- Hard 0px corners and hairline grids.

The exception is the footage itself. Real recordings are allowed to look like what they are —
that is the point of showing them. Everything you draw around them is not.

## Characters, not diagrams

Represent the product's own surfaces as **friendly card characters**, reused across every
scene, rather than drawing a new diagram per idea:

- Rounded dark card with a soft border and shadow.
- Title bar: two or three muted dots, **the product's own mark** as the card's badge, then its
  name in the label weight.
- Body: abstract rounded bars for content, plus **one line of real plain English**. Never real
  code, never a prompt caret.

The bars keep it friendly — unmistakably an app window without asking anyone to read one. The
mark on every card makes it the character's face. A new idea gets an existing mark in a new
arrangement, never a new mark.

## Heading discipline

**Do not put a pill + headline + subhead stack on every frame.** That rhythm is what makes a
piece feel like a slide template. Give each scene its own verbal register:

| Scene       | Treatment                                                     |
| ----------- | ------------------------------------------------------------- |
| Hook        | one large statement, top of frame — the only top-anchored one |
| Footage     | no heading at all; one short caption **below** the clip       |
| Nuance      | illustration first; statement + one line at the **bottom**    |
| Payoff      | diagram first; closing statement at the bottom                |

## Type

- **One family, two extremes.** Statement weight and body weight, nothing in between doing
  hierarchy work.
- **Cap statements at 700.** Heavier turns every frame into a poster and fights the footage.
  Contrast comes from size, not weight.
- Statements 60–110px, body 24–33px at 1.45, labels 21–29px. Nothing below 21px — this plays
  small in a feed.
- Sentence case. Uppercase plus letterspacing reads as shouting and ages badly.

## Colour

A warm near-black beats a neutral `#000` — tint the background toward the accent hue. Then:

- One accent, used scarcely: one accent object per frame so the eye always knows where to go.
- **Check the accent as text against the background.** A mid-tone accent that passes on dark
  often fails on light — on a light canvas it may be legal only as a *fill* carrying dark text.
  Run the contrast numbers before designing around it, not after `check` fails.
- If the product mark is the accent colour, it disappears on an accent fill. Put a dark disc
  behind it, or make the container a dark disc with an accent ring.
- Shadows do not read on dark. Every raised surface gets a border plus a deep black shadow;
  accent objects get a soft accent glow instead.
- Depth from one large **radial** accent glow per frame. Never a full-screen linear gradient —
  it bands visibly under H.264.

## Push the polish on scenes 1, 3, 4

The footage carries scene 2; the three scenes around it are drawn from nothing, and "one glow
and a card" reads thin next to real video. Layer 2–4 of these per scene, all with slow ambient
motion — a static decorative feels like a bug, not a choice:

- A second, smaller glow off-axis from the primary one, dimmer, to break the single-light-source
  flatness.
- Ghost type: one theme word from the script, 3–8% opacity, oversized, drifting slower than
  everything in front of it — never another card character, and never monospace.
- One or two thin accent rules, animated as a slow pulse — not the static engineering-grid look
  banned above.
- A thin inner highlight stroke (1px, ~10–15% white) on a card's top edge, on top of its outer
  border — that's what reads as a physical lit surface instead of a flat rectangle.
- Fine grain/noise overlay across the whole frame, low opacity — kills the flat-vector look
  H.264 exposes on large single-color fields.

Keep every one of these off the footage band itself (`The footage is never treated`, below), and
keep the accent count rule: decoratives extend depth, they do not add a second accent hue.

## Working dark palette

Proven on a warm-orange brand; retune the hue for another:

```
background   #16120F   warm near-black
fg           #F7F2EB   16.7:1
muted        #A79C91   6.9:1
surface      #241E19   panels, chips
line         #3B332B   borders, tracks
accent       #D97757   6.0:1 on background — legal as text here
window       #1F1915   card body
windowBar    #2C251F   card title bar
windowText   #E8DED4   13.1:1 on the card
band         #0F0C0A   behind the footage
```

## The footage is never treated

Framing, rounding, and motion only. No grade, no filter, no overlay on top of it, and text
never sits over it — it lives above and below. If someone asks to make the footage "pop", the
answer is a bigger band or a closer camera, not a LUT. See `/media-use` →
`references/media-treatments.md` before touching pixels.
