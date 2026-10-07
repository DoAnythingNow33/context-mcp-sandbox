# DoAnythingNow — Brand Reference

## Visual Identity

**Feel**: Freedom + future nostalgia. The sense that what's possible is bigger than what's been, and that moving toward it is the point.

---

## Colour

| Role | Hex | Notes |
|---|---|---|
| Primary / background | `#0875D4` | DoAnythingNow blue — the default background on ALL slides, carousels, and pitch decks |
| Dark variant | `#0660B0` | Use on alternating slides or sections for depth without breaking the palette |
| Light variant | `#1A88E8` | Reserved for glows, gradients, and hover states — a step brighter than primary, not a background swap |
| White | `#FFFFFF` | All headline text, primary copy |
| White 70% | `rgba(255,255,255,0.70)` | Body copy, subtext |
| White 40% | `rgba(255,255,255,0.40)` | Labels, slide numbers, secondary metadata |
| White 15% | `rgba(255,255,255,0.15)` | Card borders, image borders |
| White 8% | `rgba(255,255,255,0.08)` | Card backgrounds, pill backgrounds |

**Rule**: Blue is always the background. White is always the text. Never invert this. Never put white backgrounds behind content blocks — use the opacity scale above for contrast instead.

---

## Typography

| Role | Font | Weight | Size | Letter-spacing | Notes |
|---|---|---|---|---|---|
| Display / H1 | **Koulen** | 400 (only weight) | `clamp(60px, 8.5vw, 116px)` | `0.01em` | All slide headlines, big stats |
| H2 / Section headline | **Koulen** | 400 | `clamp(40px, 5.5vw, 80px)` | `0.01em` | Sub-headlines within slides |
| Pillar / card title | **Koulen** | 400 | `22px` | `0.02em` | Labels inside cards/pillars |
| Stat value | **Koulen** | 400 | `34–36px` | `0.01em` | Numbers, metrics |
| Body / subtext | **Oswald** | 300 | `clamp(14px, 1.7vw, 18px)` | `0.02em` | All paragraph copy |
| Label / eyebrow | **Oswald** | 400 | `10–11px` | `0.30–0.35em` | Section labels, always uppercase |
| Slide number / meta | **Oswald** | 400 | `11px` | `0.18em` | Chrome UI, always uppercase |
| Tag / pill text | **Oswald** | 400 | `10–12px` | `0.12–0.14em` | Tags, badges, uppercase |

Load order: Koulen first, Oswald second.
```html
<link href="https://fonts.googleapis.com/css2?family=Koulen&family=Oswald:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

**Rules:**
- Koulen for everything that needs to land hard: headlines, stats, names, pillar titles
- Oswald for everything that needs to be read: body, labels, metadata
- Line height on Koulen headlines: `0.92–0.95` — tight, no air
- Never use system fonts for display text

---

## Logo

**File**: `ops/content/DANlogo.png`

The logo is white text ("DOANYTHINGNOW.") with a blue running figure. On the blue background the figure blends — this is intentional, an embossed effect.

Usage in decks:
- **Cover slide**: Large, centred above the headline. Height `42px`.
- **Fixed chrome**: Top-left of every slide at `height: 28px`, `opacity: 0.95`.
- **Closing slide**: Centred below contact details at `height: 32px`, `opacity: 0.7`.
- Never on a white or dark background — blue only.

---

## Pitch Deck / Carousel System

### Slide structure

Every deck follows this 7-slide arc:

| Slide | Role | Background | Key element |
|---|---|---|---|
| 1 | Cover | `#0875D4` | Logo + big Koulen headline + one-line sub |
| 2 | The Challenge | `#0660B0` | Big stat headline + body copy |
| 3 | The Product / Proof | `#0875D4` | Split layout: text left, full-bleed image right |
| 4 | The Audience | `#0875D4` | 4 image cards in corners + text centre |
| 5 | The Creator / Partner | `#0660B0` | Photo left + stats + detail right |
| 6 | The Role / Strategy | `#0875D4` | Headline + 3-column pillar grid |
| 7 | The Ask / Close | `#0660B0` | Centred headline + contact + logo |

### Chrome (fixed UI on every slide)

```css
/* Logo — top left */
position: fixed; top: 18px; left: 28px; height: 28px; z-index: 100;

/* Slide number — top right */
font-family: 'Oswald'; font-size: 11px; letter-spacing: 0.18em;
color: rgba(255,255,255,0.2); text-transform: uppercase;

/* Nav dots — bottom centre */
width: 6px; height: 6px; border-radius: 50%;
background: rgba(255,255,255,0.2); /* inactive */
background: #FFFFFF; transform: scale(1.5); /* active */

/* Arrow buttons — left/right centre */
opacity: 0.35; /* resting */ opacity: 1; /* hover */
```

### Slide transition

```css
opacity: 0; transform: translateX(56px); /* default */
opacity: 1; transform: translateX(0);    /* active — 0.5s cubic-bezier(0.22,1,0.36,1) */
opacity: 0; transform: translateX(-56px); /* exit — 0.38s ease */
```

---

## Component Patterns

### Label / Eyebrow
```css
font-family: 'Oswald'; font-size: 10px; font-weight: 400;
letter-spacing: 0.35em; text-transform: uppercase;
color: rgba(255,255,255,0.70); display: block; margin-bottom: 20px;
```

### Big stat (Slide 2 style)
```css
font-family: 'Koulen'; font-size: clamp(70px, 10vw, 130px);
color: #FFFFFF; line-height: 0.9; letter-spacing: 0.01em;
/* Dimmed words: color: rgba(255,255,255,0.70) */
```

### Split layout (Slide 3 style)
- Left panel: `flex: 1`, `max-width: 500px`, `padding: 80px 60px`, text content
- Right panel: `flex: 1`, full-bleed image with `object-fit: cover`
- Left-to-right gradient on image edge: `linear-gradient(to right, #0875D4 0%, transparent 30%)` — prevents hard cut

### 4-corner image cards (Slide 4 style)
```css
.photo { width: 230px; height: 265px; border-radius: 10px; overflow: hidden;
         border: 3px solid rgba(255,255,255,0.18);
         box-shadow: 0 12px 40px rgba(0,0,0,0.35); position: absolute; }

.tl { top: 52px;    left: 48px;   transform: rotate(-4deg); }
.tr { top: 52px;    right: 48px;  transform: rotate(3.5deg); }
.bl { bottom: 52px; left: 48px;   transform: rotate(3deg); }
.br { bottom: 52px; right: 48px;  transform: rotate(-3.5deg); }
```
Text sits centred, `z-index: 2`, `max-width: 480px`.
Alternate rotations: outer cards lean away from centre, inner cards lean in.

### Creator / profile card (Slide 5 style)
- Photo: `width: 300px; height: 370px; border-radius: 12px`
- Handle badge overlaid bottom-left: frosted glass (`background: rgba(255,255,255,0.15); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.25)`)
- Stats row: Koulen `34px` value + Oswald `10px` uppercase key
- Live indicator pill: `border: 1px solid rgba(255,255,255,0.40)` + pulsing white dot

### 3-pillar grid (Slide 6 style)
```css
.pillar { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);
          border-radius: 10px; padding: 24px; }
/* Number: Oswald 10px, 0.25em spacing, 40% white */
/* Title: Koulen 22px */
/* Body: Oswald 13px, 300 weight, 70% white */
```

### Tags
```css
padding: 6–7px 14–18px; border-radius: 100px;
border: 1px solid rgba(255,255,255,0.18); /* default */
border: 1px solid #FFFFFF;                /* hot/active */
font-family: 'Oswald'; font-size: 10–11px; letter-spacing: 0.14em; text-transform: uppercase;
color: rgba(255,255,255,0.5); /* default */
color: #FFFFFF;                /* hot/active */
```

### Rule divider (Cover slide, under the sub-line)
```css
width: 40px; height: 2px; background: #FFFFFF; opacity: 0.4; margin: 0 auto;
```
A single short underline — not a full-width rule. Signals "end of cover block," used once per deck.

### Feature list (dot bullets — Slide 3 style)
```css
.feature-list { list-style: none; display: flex; flex-direction: column; gap: 18px; }
.feature-list li { display: flex; align-items: flex-start; gap: 14px;
                    font-family: 'Oswald'; font-size: 15px; font-weight: 300;
                    color: rgba(255,255,255,0.7); line-height: 1.55; }
.f-dot { width: 6px; height: 6px; min-width: 6px; border-radius: 50%;
         background: #FFFFFF; margin-top: 8px; opacity: 0.6; }
/* bold the load-bearing phrase inside each item: <strong> → color: #FFFFFF; font-weight: 500 */
```
Never use native `<ul>` markers — always a custom dot, sized and dimmed exactly as above.

### Sleevenote watermark (when presenting for Sleevenote)
```css
position: fixed; bottom: 58px; right: 32px; opacity: 0.15; z-index: 100;
img { height: 20px; border-radius: 2px; }
```

---

## Deck Engine (interactive HTML mechanics)

This is the reusable navigation skeleton behind the Sleevenote pitch deck — the deck that landed a free product. Reuse it wholesale for any future pitch/carousel deck; don't rebuild it from scratch.

**Structure**: one `.deck` container holding N `.slide` divs (`position: absolute; inset: 0`), each `display: flex; align-items: center; justify-content: center`. Only one slide has `.active` at a time.

**Transition**: entering slide goes `opacity:0; transform: translateX(56px)` → `.active` animates to `opacity:1; translateX(0)` over `0.5s cubic-bezier(0.22,1,0.36,1)`. The outgoing slide gets `.exit` (`opacity:0; translateX(-56px)`, `0.38s ease`) and is cleared after a 420ms timeout.

**Chrome present on every slide** (fixed position, `z-index: 100`, outside the `.slide` elements so it persists across transitions):
- Logo top-left (`.dan-logo-chrome`)
- Slide counter top-right, format `01 / 07` (zero-padded, updated on every `goTo`)
- Prev/left and next/right arrow buttons, centered vertically, `opacity: 0.35` resting → `1` on hover
- Nav dots bottom-center, one per slide, active dot scales `1.5` and goes full white

**Navigation JS** (`goTo(next)`):
- Guards: ignore if `animating`, if `next === current`, or if `next` is out of bounds — no wraparound
- Sets `animating = true`, adds `.exit` to current + removes `.active`, adds `.active` to next, clears `.exit` after 420ms
- Wired to: arrow clicks, dot clicks, `ArrowRight`/`ArrowDown`/`Space` (next) and `ArrowLeft`/`ArrowUp` (prev) keydowns, and touch swipe (threshold 50px on `touchstart`/`touchend` delta)

**Client watermark** (when pitching on behalf of a client's product): fixed bottom-right, `opacity: 0.2`, logo height `20px` — present but deliberately unobtrusive.

Copy the `<script>` block and chrome markup verbatim from `visual/sleevenote-pitch/index.html` when starting a new deck; only the per-slide content and slide count change.

---

## Copy Voice (for slide copy)

- **Koulen headlines are statements, not slogans.** Say the thing directly. "The hard part is done." not "Unleashing the future of music."
- **Labels set context, headlines deliver.** Label: "The challenge" → Headline: "Great product. Small team. One gap."
- **Body copy is Oswald 300** — it should breathe. Two to four sentences max per slide. No bullet points in body paragraphs.
- **Honest over impressive.** "I don't have all the answers but I'll work hard with you" lands harder than "proven track record of community growth."
- No em-dash deluge. No triplet chanting. No inspirational pivots to humanity. See global writing rules.

---

## File locations

| Asset | Path |
|---|---|
| Logo (PNG) | `ops/content/DANlogo.png` |
| Pitch deck template | `visual/sleevenote-pitch/index.html` — reference for structure, CSS, and the deck engine JS |
| Brand reference | `ops/content/brand.md` (this file) |
| Writing voice | `ops/content/writing-dna.md` |

---

## Always Load With

`ops/content/writing-dna.md` — voice is inseparable from visual identity.
`ops/content/website-rebrand-brief.md` — page structure and conversion paths for the three tracks.

---

## Brand Tracks

Three expressions of the same identity — same colour, type, and feel, different tone:

| Track | Tone | Primary CTA |
|---|---|---|
| **DoAnythingNow** (hub) | Philosophical, orienting | Explore |
| **AI Workflows** | Efficient, clear, systems | Book AI Clarity Call |
| **Reality Architects** | Deep, becoming, architectural | Join the community |
