# A camera over the footage

The clip is on screen for half the reel. Static, it reads as a screenshot with audio. The fix
is a virtual camera — but the failure mode is worse than no camera at all, so read this before
writing any of it.

## Check the source first

**Most edited demo clips already contain camera moves.** They zoom to whatever is being
demonstrated and pull back between beats. Find out before you plan yours:

```bash
for t in 0.5 3 6 9 12 15; do
  ffmpeg -v error -ss $t -i clip.mp4 -frames:v 1 -vf scale=400:-1 -y /tmp/src-$t.png
done
```

Look at them. If the framing changes between samples, the source has its own camera and **your
layer must stay gentle** — the two transforms compose, and a long pan of yours stacked on a
zoom of the source's throws the subject clean off the edge. That is the mistake this file
exists to prevent.

| Source clip                  | Your camera                                          |
| ---------------------------- | ---------------------------------------------------- |
| Static screen recording      | Free — push to 1.5–1.7×, pan the full legal range    |
| Has its own zooms/pans       | Gentle — 1.2–1.35×, short symmetrical drift only     |

## The mechanism

`hyperframes-animation` → `rules/viewport-change.md`. One `.world` wrapper around the video,
one `cam` object, one writer. Read the rule; the essentials:

```html
<div id="band">                      <!-- overflow:hidden, background = the clip's own dark -->
  <div id="world" data-layout-allow-overflow>   <!-- transform-origin: 50% 50% -->
    <video class="clip" ... muted playsinline></video>   <!-- inset:0, object-fit:cover -->
  </div>
</div>
```

```js
const cam = { s: 1, x: 0, y: 0 };
const apply = () => { world.style.transform =
  `translate(${cam.x}px, ${cam.y}px) scale(${cam.s})`; };
apply();                                    // seed frame 0
tl.fromTo(cam, FROM, { ...TO, onUpdate: apply, immediateRender: false }, at);
```

Use `fromTo` with explicit from-states on every leg so seeking is correct in both directions,
and `immediateRender: false` on every leg after the first.

## The two inequalities

The world must never expose an edge. For a band `W × H`:

```
|x| ≤ (W/2)(s − 1)        |y| ≤ (H/2)(s − 1)
```

At `s = 1` the pan budget is zero — the wide pose is always `x: 0, y: 0`. Every pose you invent
gets checked against both before you write it, and re-checked after any change to band size or
scale. Put the numbers in a comment next to the pose constants.

The corollary that surprises people: **you usually cannot centre a subject that sits off to one
side.** Centring an object whose offset from band centre is `d` needs `s ≥ (W/2)/((W/2) − d)`. A
panel a third of the way across a band (`d` = one-sixth of the band width) already needs `s ≥
1.5×`; a panel a sixth of the way across (`d` = a third of the band width) needs `s ≥ 3×` — a
zoom that crops far more than it gains. Accept off-centre framing instead.

## Band geometry

Full-bleed width, and pick the height from what the clip can afford:

```
cover_scale = max(W / src_w, H / src_h)
visible_src_width = W / cover_scale
```

Choose `H` so `visible_src_width` still contains the subject. For a 2400×1260 two-panel
recording whose panels span 6%–94% of the width, a 1080×650 band lands the visible range at
6.4%–93.6% — essentially lossless. Push the band to 700 and it starts eating the panel.

A taller band makes the recording read bigger, which is usually what "show the video clearly"
means. It is bounded by that crop, not by taste.

## Pacing the legs

Motivate every move by the narration underneath it. A typical shape over a 12s hold:

- brief wide beat so the viewer sees the whole thing exists
- drift toward the first subject while it is being named
- hold while its line is spoken
- one slow travel to the second subject, on the clause about handing over
- hold
- pull back on the closing clause

Keep scale locked through a lateral travel so it reads as a pan, not a second zoom. Under ~1s a
move teleports; over ~4s it drags.

## Verify at six or more times

A pose that frames well at one instant can overshoot at another, because the source is moving
too. Never judge from a single snapshot:

```bash
hyperframes snapshot --at 4.2,6.5,9.2,11.5,13.5,15.5 --output snapshots/probe
```

Read the contact sheet. You are looking for dead space creeping in at either edge — that is the
overshoot signature. Fix it by shortening the pan, not by chasing it with an offset.
