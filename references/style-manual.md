# Flow diagram style manual

Specsheet for hand-written, single-file flow diagrams with a small top bar for light/dark and print themes. One vertical main path, optional side blocks, muted palette, no external dependencies.

## 1. File contract

- One `.html` file per topic, named `<topic>-flow.html`.
- UTF-8, printable ASCII only. No typographic quotes, dashes, arrows or bullets.
- Inline scripts limited to the top bar and its initial mode. No external CSS, fonts, images or icon sets. Must open from `file://`.
- Light and dark themes from the top bar switch, initial state from `prefers-color-scheme`. The print theme is a separate toggle.
- One `<main>` wrapper, max width 1080 px, centered.
- One `<h1>`, one `.sub`, one or more `<section>` blocks, one `<footer>`.
- SVG scales with the page; no fixed pixel width or height attributes.

## 2. Page order

```
div#tb          fixed 24px bar: print toggle, light/dark switch
h1              page title, 22px
p.sub           one sentence naming the whole path, 13px
section
  div.head      h2 pill plus optional palette pair label
  p.note        one or two sentences with the driving rule
  svg           the diagram, viewBox 0 0 1040 H
section         optional further diagrams, same shape
footer          shared infrastructure or invariant, 1-2 sentences
```

## 3. Palette

| token | light | dark | use |
|---|---|---|---|
| `--bg` | `#dfe4ee` | `#161b24` | page background (`--page-bg`) |
| `--card` | `#fdfdfd` | `#262626` | card and tag fill |
| `--ink` | `#14181c` | `#e6ebef` | titles |
| `--muted` | `#546374` | `#93a2b3` | descriptions, captions, footer, connectors |
| `--line` | `#c9c9c9` | `#424242` | borders |
| `--accent` | `#0f766e` | `#4fd1c5` | focus border, action arrow |
| `--mint` | `#46755c` | `#46755c` | section pill (`--page-mint`) |

Rules:

- Accent marks the focus card and the active edge of the path. Keep accent connectors to one or two per diagram.
- Mint is fixed across screen themes; print uses a black pill with white text.
- All SVG fills and strokes use classes backed by `var(--...)`, never hardcoded colors, so the dark theme follows without a second stylesheet.
- One common page background per page, set by the mode, not by the individual diagram palettes. Diagram sections carry no page tint; the catalog `--bg` and `--mint` rows map to the page tokens `--page-bg` and `--page-mint`.
- Light mode uses light palettes only; dark mode uses dark palettes only, also when several diagrams share a page. Mix pairs for contrast: L1/D1, L2/D3, L3/D2, L4/D5.
- Print mode overrides every diagram with the P0 tokens and a white page. It is independent of the light/dark switch and restores the previous mode when switched off.

## 4. Type scale

| class | px | weight | use |
|---|---|---|---|
| h1 | 22 | 400 | page title |
| `.sub` | 13 | 400 | page subtitle |
| h2 | 16 | 400 | section pill, white on mint |
| `.meta` | 11 | 400 | palette pair label beside the pill |
| `.note` | 13 | 400 | instruction above the diagram |
| `.t` | 14.5 | 600 | card title |
| `.d` | 12.5 | 400 | card description |
| `.cap` | 11.5 | 400 | arrow caption |
| `.side` | 11.5 | 400 | tag and branch labels |
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

- 70-high main card: title `y+30`, one description line at `y+50`.
- 70-high side card: title `y+26`, up to two description lines at `y+44` and `y+59`.
- 90/100-high side card: title `y+26`, up to three description lines at `y+44`, `y+59`, `y+74`.
- Tag text: `y+17`.

Do not change the 108 pitch per card. If a card needs more text, cut the text or split the step. If the diagram needs more than seven cards, split it into two sections.

## 6. Card anatomy

A card is a `<rect class="card">` or `<rect class="focus">` with `rx="3"`, plus:

- `.t`: 1 to 4 words, sentence case, name of the actor or stage. No verbs in title case, no punctuation.
- `.d`: concrete mechanism. Use the real flags, endpoints, file names, frame sizes, buffer counts. No marketing, no restatement of the title, no trailing period.
- Main cards carry one description line. Side cards carry up to two lines on a 70-high card and up to three on a 90/100-high card.
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

## 10. Diagram body

Copy the page shell from `demo.html`: page tokens, top bar, theme script, bar script and print rules. The block below is one section body to place inside `<main>`. It uses the demo `d1` slot, which carries L2/D3; change the section class and the meta label together when you pick another pair.

```html
<section class="diagram d1">
  <div class="head">
    <h2>main path: start to finish</h2>
    <span class="meta">L2 / D3</span>
  </div>
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

- Open the file at 100 percent zoom. Toggle the bar switch and confirm both themes, then toggle print mode and confirm the print preview.
- Operate both bar controls with the keyboard and confirm the focus ring and state change.
- Confirm the bar is hidden in the print preview and every diagram renders in P0.
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
- [ ] Top bar present: 24 px, print toggle then mode switch, keyboard operable.
- [ ] Every diagram uses a palette from the active family; one common background per page.
- [ ] Print toggle forces P0 and hides the bar in the print preview.
- [ ] Inline scripts limited to the bar; no external files.

## 13. Top bar and modes

`demo.html` is the reference implementation. Copy its bar, token blocks and scripts; do not invent a second control style.

Bar:

- Fixed, 24 px high, right aligned, 10 px UI font, 1 px bottom border.
- Print toggle: 27 x 18 px, printer icon, `aria-pressed`. Active fill uses the bar ink.
- Mode switch: 44 x 20 px, moon left and sun right, 16 px thumb, `aria-checked` true in light mode.
- Both controls are native `<button>` elements, so Enter and Space work without key handlers.
- Labels: `aria-label` and `title` on both; no visible text inside the bar.

State:

- `html[data-theme="light"]` or `html[data-theme="dark"]` selects the common page background and the diagram family.
- `html[data-print="on"]` forces P0 on every diagram and a white page. It does not change `data-theme`.
- Initial mode comes from `prefers-color-scheme`; OS changes are followed until the user toggles. No storage.

Token scope:

- Page tokens live on `:root` and the theme blocks: `--page-bg`, `--page-ink`, `--page-muted`, `--page-line`, `--page-mint`, plus the bar and thumb tokens.
- Diagram tokens live on each section: `--card`, `--ink`, `--muted`, `--line`, `--accent`, set per family under the theme selector.
- The print override comes after the scoped theme blocks, so it wins at equal specificity.

Scripts:

- One inline script in the head sets the initial `data-theme` before paint.
- One inline script before `</body>` wires both buttons and follows OS changes until the user toggles.

Print:

- `@page` margin 12 mm, exact color adjust, `break-inside: avoid` per section.
- `@media print` hides the bar, removes the page cap and repeats the P0 override, so paper output is print-themed even when the toggle was never clicked.
- Print mode on screen keeps the bar visible; only the print preview hides it.
