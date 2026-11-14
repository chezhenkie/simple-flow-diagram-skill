# Flow diagram style manual

Specsheet for hand-written, single-file flow diagrams. One vertical main path, optional side blocks, muted palette, light and dark from the OS preference, no dependencies.

## 1. File contract

- One `.html` file per topic, named `<topic>-flow.html`.
- UTF-8, printable ASCII only. No typographic quotes, dashes, arrows or bullets.
- No JavaScript, no external CSS, fonts, images or icon sets. Must open from `file://`.
- Light and dark themes from `prefers-color-scheme`.
- One `<main>` wrapper, max width 1080 px, centered.
- One `<h1>`, one `.sub`, one or two `<section>` blocks, one `<footer>`.
- SVG scales with the page; no fixed pixel width or height attributes.

## 2. Page order

```
h1              page title, 22px
p.sub           one sentence naming the whole path, 13px
section
  h2            pill label, "subject: outcome"
  p.note        one or two sentences with the driving rule
  svg           the diagram, viewBox 0 0 1040 H
section         optional second diagram, same shape
footer          shared infrastructure or invariant, 1-2 sentences
```

## 3. Palette

| token | light | dark | use |
|---|---|---|---|
| `--bg` | `#dfe4ee` | `#161b24` | page background |
| `--card` | `#fdfdfd` | `#262626` | card and tag fill |
| `--ink` | `#14181c` | `#e6ebef` | titles |
| `--muted` | `#546374` | `#93a2b3` | descriptions, captions, footer, connectors |
| `--line` | `#c9c9c9` | `#424242` | borders |
| `--accent` | `#0f766e` | `#4fd1c5` | focus border, action arrow |
| `--mint` | `#46755c` | `#46755c` | section pill only |

Rules:

- Accent marks the focus card and the active edge of the path. Keep accent connectors to one or two per diagram.
- Mint is fixed across themes. The pill keeps white text.
- All SVG fills and strokes use classes backed by `var(--...)`, never hardcoded colors, so the dark theme follows without a second stylesheet.

## 4. Type scale

| class | px | weight | use |
|---|---|---|---|
| h1 | 22 | 400 | page title |
| `.sub` | 13 | 400 | page subtitle |
| h2 | 16 | 400 | section pill, white on mint |
| `.note` | 13 | 400 | instruction above the diagram |
| `.t` | 14.5 | 600 | card title |
| `.d` | 12.5 | 400 | card description |
| `.cap` | 11.5 | 400 | arrow caption |
| `.side` | 11.5 | 400 | side card text, tag text |
| footer | 12 | 400 | page footer |

Body font stack: `"Segoe UI", system-ui, -apple-system, sans-serif`, 15px/1.45. Width budgets below leave at least 10 percent headroom for wider fallback fonts. A size change invalidates the budgets; re-measure before writing.

## 5. Grid

All coordinates are integers in a `1040 x H` viewBox.

| element | x | width | notes |
|---|---|---|---|
| main column | 300 | 470 | center line at 535 |
| side card, left | 40 | 210 | text at x+16 |
| side card, right | 800 | 220 | text at x+16, 20 px right margin |
| main text | 318 | to 752 | card padding 18 |
| caption lane | 549 | to 790 | 14 px right of the spine |
| tag | 300 | 470 | same width as the main column |

Vertical rhythm:

```
card top        y = 30 + 108 * n
card height     70 main, 70 / 90 / 100 side
gap between     38
arrow between   y+70 to y+98 (28 long)
caption         y+88 (x 549)
tag             last card top + 98
viewBox height  tag y + 32
```

Examples: six main cards put the last top at 570, the tag at 668 and the viewBox height at 700. Two cards give a tag at 236 and a 268-high viewBox.

Card baselines:

- 70-high card: title `y+30`, description `y+50`. One description line only.
- 90/100-high side card: title `y+26`, lines `y+44`, `y+59`, `y+74`.
- Tag text: `y+17`.

Do not change the 108 pitch per card. If a card needs more text, cut the text or split the step. If the diagram needs more than seven cards, split it into two sections.

## 6. Card anatomy

A card is a `<rect class="card">` or `<rect class="focus">` with `rx="3"`, plus:

- `.t`: 1 to 4 words, sentence case, name of the actor or stage. No verbs in title case, no punctuation.
- `.d`: concrete mechanism. Use the real flags, endpoints, file names, frame sizes, buffer counts. No marketing, no restatement of the title, no trailing period.
- Main cards carry one description line. Side cards carry two or three.
- `focus` marks the component that does the work or coordinates the branch. One per diagram.

Text limits, measured at the sizes above:

| element | usable px | practical characters | budget |
|---|---|---|---|
| main description | 434 | 72 | 65 |
| side description, 220 card | 186 | 31 | 28 |
| side description, 210 card | 176 | 29 | 26 |
| card title, 220 card | 204 | 28 | 24 |
| arrow caption | 241 | 44 | 42 |
| tag line | 434 | 86 | 78 |

SVG text does not wrap. An overlong line runs into the border. Count characters before writing.

## 7. Connectors

Solid arrows connect consecutive main cards. Caption states the condition, protocol or payload that crosses the boundary. The caption does not repeat either card title.

```html
<line class="arrow" x1="535" y1="100" x2="535" y2="128" marker-end="url(#flowHead)"/>
<text class="cap" x="549" y="118">first http(s) link wins</text>
```

- `arrow`: 1.4 stroke, `--muted`.
- `arrow-a`: 1.6 stroke, `--accent`, marks the action into or out of the focus card. One or two per diagram.
- `dash`: 1.2 stroke, 5 4 dasharray, `--muted`. Optional channels and alternate branches only.
- Line and arrowhead are separate objects. The color of the marker path lives in `<defs>` and does not follow the line class, so pair them explicitly: `arrow` with the plain marker, `arrow-a` with the accent marker.
- Marker ids must be unique per page. Prefix by section: `vidHead`, `sumHead`.

Marker definition, once per color per diagram:

```html
<defs>
  <marker id="flowHead" viewBox="0 0 10 10" refX="9" refY="5"
          markerWidth="7" markerHeight="7" orient="auto">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--muted)"/>
  </marker>
  <marker id="flowHeadA" viewBox="0 0 10 10" refX="9" refY="5"
          markerWidth="7" markerHeight="7" orient="auto">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--accent)"/>
  </marker>
</defs>
```

## 8. Branch patterns

Side input, dashed into the main column:

```html
<path class="dash" d="M 250 173 H 290" marker-end="url(#flowHead)"/>
```

Side output, dashed out of the main column:

```html
<path class="dash" d="M 770 399 H 796" marker-end="url(#flowHead)"/>
```

Exit branch with no return (for example a missing prerequisite):

```html
<path class="dash" d="M 300 173 H 254" marker-end="url(#flowHead)"/>
```

Fallback that rejoins a lower card:

```html
<path class="dash" d="M 910 454 V 605 H 780" marker-end="url(#flowHead)"/>
<text class="side" x="845" y="596">sound only</text>
```

Rules:

- Dash means optional, alternate or side channel. Solid means the main path.
- Route around cards, never through them. Use the lanes outside x=300 and x=770.
- A side card sits on the row it touches, or 20 px lower if it is 90-100 high.
- No crossing lines. If two branches would cross, move one side block to the other lane or reorder the rows.
- Labels stay at least 10 px from a card border.

## 9. Section copy

- h2 pattern: `subject: outcome`, lowercase, for example `video download: url to file`.
- Note: the rule that drives the diagram, not a walkthrough of every box.
- Tag strip: the invariant or the verdict shape, one line. Example: `one run ends in one verdict: finished, failed rc, or stopped by escape`.
- Footer: what both diagrams share, or the one guarantee that holds across paths.
- Plain technical English. No sales words, no slogans, no "not X but Y" contrasts, no meta commentary.
- Keys and literal input render in straight single quotes: 's', '0', 'ready'.

## 10. Full skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>topic flow</title>
<style>
  :root {
    --bg: #dfe4ee;
    --card: #fdfdfd;
    --ink: #14181c;
    --muted: #546374;
    --line: #c9c9c9;
    --accent: #0f766e;
    --mint: #46755c;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #161b24;
      --card: #262626;
      --ink: #e6ebef;
      --muted: #93a2b3;
      --line: #424242;
      --accent: #4fd1c5;
    }
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    font: 15px/1.45 "Segoe UI", system-ui, -apple-system, sans-serif;
  }
  main { max-width: 1080px; margin: 0 auto; padding: 36px 20px 60px; }
  h1 { font-size: 22px; margin: 0 0 4px; letter-spacing: 0.2px; }
  .sub { color: var(--muted); font-size: 13px; margin: 0 0 32px; }
  section { margin: 0 0 42px; }
  h2 { display: inline-flex; align-items: center; height: 28px; padding: 0 12px;
       font-size: 16px; margin: 0 0 10px; background: var(--mint); color: #fff;
       border: 1px solid #335742; border-radius: 3px; }
  section + section h2 { margin-top: 8px; }
  .note { color: var(--muted); font-size: 13px; margin: 0 0 16px; }
  svg { display: block; width: 100%; height: auto; }
  .card { fill: var(--card); stroke: var(--line); stroke-width: 1.2; }
  .focus { fill: var(--card); stroke: var(--accent); stroke-width: 1.4; }
  .t { fill: var(--ink); font-size: 14.5px; font-weight: 600; }
  .d { fill: var(--muted); font-size: 12.5px; }
  .cap { fill: var(--muted); font-size: 11.5px; }
  .side { fill: var(--muted); font-size: 11.5px; }
  .arrow { stroke: var(--muted); stroke-width: 1.4; fill: none; }
  .arrow-a { stroke: var(--accent); stroke-width: 1.6; fill: none; }
  .dash { stroke: var(--muted); stroke-width: 1.2; fill: none; stroke-dasharray: 5 4; }
  .tag { fill: var(--card); stroke: var(--line); stroke-width: 1; }
  footer { color: var(--muted); font-size: 12px; border-top: 1px solid var(--line); padding-top: 12px; }
</style>
</head>
<body>
<main>

  <h1>topic flow</h1>
  <p class="sub">One sentence naming the path and the process that owns it.</p>

  <section>
    <h2>main path: start to finish</h2>
    <p class="note">The rule that drives the diagram, in one or two sentences.</p>
    <svg viewBox="0 0 1040 268" role="img" aria-label="Start and work cards with one side channel">
      <defs>
        <marker id="flowHead" viewBox="0 0 10 10" refX="9" refY="5"
                markerWidth="7" markerHeight="7" orient="auto">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--muted)"/>
        </marker>
        <marker id="flowHeadA" viewBox="0 0 10 10" refX="9" refY="5"
                markerWidth="7" markerHeight="7" orient="auto">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--accent)"/>
        </marker>
      </defs>

      <rect class="card" x="300" y="30" width="470" height="70" rx="3"/>
      <text class="t" x="318" y="60">Start</text>
      <text class="d" x="318" y="80">what arrives, and from where</text>

      <rect class="focus" x="300" y="138" width="470" height="70" rx="3"/>
      <text class="t" x="318" y="168">Work</text>
      <text class="d" x="318" y="188">the mechanism: flags, files, endpoints</text>

      <line class="arrow-a" x1="535" y1="100" x2="535" y2="128" marker-end="url(#flowHeadA)"/>
      <text class="cap" x="549" y="118">condition or payload</text>

      <rect class="card" x="40" y="138" width="210" height="70" rx="3"/>
      <text class="t" x="56" y="164">Side note</text>
      <text class="d" x="56" y="182">an optional channel,</text>
      <text class="d" x="56" y="197">kept to two lines</text>
      <path class="dash" d="M 250 173 H 290" marker-end="url(#flowHead)"/>

      <rect class="tag" x="300" y="236" width="470" height="26" rx="3"/>
      <text class="side" x="318" y="253">the invariant stated in one line</text>
    </svg>
  </section>

  <footer>What both paths share, or the guarantee that always holds.</footer>

</main>
</body>
</html>
```

## 11. Validation

Run before delivery:

```python
import re, sys, xml.etree.ElementTree as ET

path = sys.argv[1]
raw = open(path, "rb").read()
bad = [i for i, b in enumerate(raw) if b > 126 or (b < 32 and b not in (9, 10, 13))]
assert not bad, bad[:10]
text = raw.decode("ascii")
svgs = re.findall(r"<svg.*?</svg>", text, re.S)
assert svgs, "no svg found"
for svg in svgs:
    ET.fromstring(svg)
print("ok", len(svgs), "svg", len(raw), "bytes")
```

Visual checks:

- Open the file at 100 percent zoom. Toggle the OS or browser color scheme and confirm both themes.
- Narrow the window to 800 px. The SVG scales; no text may touch a border or another card.
- Confirm no caption crosses x=790 and no side text crosses its card edge.
- Confirm one accent card and one accent arrow per diagram.
- Confirm every marker id referenced by a line exists, and ids are unique across the page.

## 12. Checklist

- [ ] ASCII only, straight quotes, hyphen for dashes.
- [ ] One h1, one sub, one footer.
- [ ] h2 pill reads `subject: outcome`.
- [ ] Main column at x=300, width 470, pitch 108, height 70.
- [ ] Card title at +30, description at +50 for 70-high cards.
- [ ] Arrow 28 long, caption at y+88, x=549.
- [ ] Tag at last card top + 98, viewBox height = tag y + 32.
- [ ] Descriptions carry real flags, files and limits.
- [ ] One focus card, at most two accent connectors, dash only for side channels.
- [ ] Marker ids unique, fills set in `defs`.
- [ ] `role="img"` and a full `aria-label` on each SVG.
- [ ] Light and dark checked in a browser.
- [ ] Python validation passes.
