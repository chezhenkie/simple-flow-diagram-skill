# Flow diagram style manual

Specsheet for hand-written, single-file flow diagrams with a small top bar for mode, theme and print. One vertical main path, optional side blocks, one theme for the page, no external dependencies.

The shell is copied, not rebuilt. This manual exists so the written part stays small and predictable: a fixed grid, a fixed type scale, fixed themes, and text budgets that fit on the first pass.

## 1. File contract

- One `.html` file per topic, named `<topic>-flow.html`, copied from `template.html`.
- UTF-8, printable ASCII only. No typographic quotes, dashes, arrows or bullets.
- Inline scripts limited to the top bar and its initial mode. No external CSS, fonts, images or icon sets. Must open from `file://`.
- Light and dark mode from the top bar switch, initial state from `prefers-color-scheme`. Two foldouts pick the theme for each mode. The print theme is a separate toggle.
- One `<main>` wrapper, max width 1080 px, centered.
- One `<h1>`, one `.sub`, one or more `<section>` blocks, one `<footer>`.
- SVG scales with the page; no fixed pixel width or height attributes.

## 2. Page order

```
div#tb          fixed 24px bar: print toggle, mode switch, dark theme, light theme
h1              page title, 22px
p.sub           one sentence naming the whole path, 13px
section
  div.head      h2 pill
  p.note        one or two sentences with the driving rule
  svg           the diagram, viewBox 0 0 1040 H
section         optional further diagrams, same shape
footer          shared infrastructure or invariant, 1-2 sentences
```

## 3. Theme

The page carries one theme, and every diagram on it follows that theme. A theme is six values:

| value | role |
|---|---|
| `bg` | page background |
| `card` | card and tag fill |
| `ink` | page text, card titles |
| `muted` | descriptions, captions, connectors, footer, bar ink |
| `line` | card and tag borders, bar lines |
| `accent` | section pill outline, focus border, action arrow |

Nine themes ship in the template: five dark and four light. Dark: `github`, `monochrome`, `ayu`, `nightowl`, `solarized`. Light: `vercel`, `tokyonight`, `cursor`, `orng`. Light opens on `vercel`, dark on `github`.

Rules:

- The agent does not pick, mix or author colors. The list is fixed and the theme script in `template.html` sets the six values as CSS custom properties.
- A diagram carries no colors of its own. No class on a section, no per-section token block, no inline `fill` or `stroke` with a color value.
- The pill is transparent with a 2 px accent outline and takes the page ink for its text, in both modes. No theme fills the title box, so it never competes with the diagram.
- One theme per page. Two diagrams side by side use the same tokens; contrast comes from layout and copy.
- Print is a separate state with fixed tokens: white page, black ink, `#333333` muted, `#9a9a9a` line, black accent, and the same transparent pill with a 2 px black outline and black text.

## 4. Type scale

| class | px | weight | use |
|---|---|---|---|
| h1 | 22 | 400 | page title |
| `.sub` | 13 | 400 | page subtitle |
| h2 | 16 | 600 | section pill, transparent with a 2 px accent outline and page ink text (black outline in print) |
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
| split card, left | 300 | 222 | text at 318 |
| split card, right | 548 | 222 | text at 566 |
| side card, left | 40 | 210 | text at x+16, 10 px left margin |
| side card, right | 800 | 220 | text at x+16, 20 px right margin |
| main text | 318 | to 752 | card padding 18 |
| caption lane | 549 | to 790 | 14 px right of the spine |
| split caption | 425, 673 | 18 characters | one per branch, 14 px right of its arrow |
| tag | 300 | 470 | same width as the main column |

Vertical rhythm:

```
card top        y = 30 + 108 * n
card height     70 main, 70 / 90 / 100 side
split row       two 222 cards at x 300 and x 548, 26 gap
gap between     38
arrow between   y+70 to y+98 (28 long)
caption         y+88 (x 549)
tag             last card top + 98, optional
viewBox height  tag y + 32, or last card top + 102 without a tag
```

A split row replaces the main card on that row; the parent above and any merged card below stay 470 wide.

Examples: six main cards put the last top at 570, the tag at 668 and the viewBox height at 700. Two cards give a tag at 236 and a 268-high viewBox; the same two cards without a tag end at 232.

Side marks are measured from a card or side box top, where `h` is the height:

| mark | y | use |
|---|---|---|
| `hi` | top + 20 | loopback exit on the lower card |
| `mid` | top + h/2 | side channel stub |
| `lo` | top + h - 20 | loopback entry on the upper card |

A 70-high card puts the marks at 20, 35 and 50. A 90-high side box at 20, 45 and 70; a 100-high box at 20, 50 and 80.

Card baselines:

- 70-high card: title `y+26`, up to two description lines at `y+44` and `y+59`.
- 90/100-high side card: title `y+26`, up to three description lines at `y+44`, `y+59`, `y+74`.
- Tag text: `y+17`.

Do not change the 108 pitch per card. If a card needs more text, cut the text or split the step. A diagram carries up to seven main cards; the tag and the side boxes do not count toward that limit. If the path needs more than seven main cards, split it into two sections.

## 6. Card anatomy

A card is a `<rect class="card">` or `<rect class="focus">` with `rx="3"`, plus:

- `.t`: 1 to 4 words, sentence case, name of the actor or stage. No verbs in title case, no punctuation.
- `.d`: concrete mechanism. Use the real flags, endpoints, file names, frame sizes, buffer counts. No marketing, no restatement of the title, no trailing period.
- A 70-high card carries up to two description lines. A 90/100-high side card carries up to three.
- `focus` marks the component that does the work or coordinates the branch. One per diagram.

Text limits, measured at the sizes above and applied per line:

| element | usable px | practical characters | budget |
|---|---|---|---|
| main description | 434 | 72 | 65 |
| split description, 222 card | 186 | 31 | 28 |
| side description, 220 card | 186 | 31 | 28 |
| side description, 210 card | 176 | 29 | 26 |
| card title, 220 or 222 card | 204 | 28 | 24 |
| arrow caption | 241 | 44 | 42 |
| split caption | 113 | 20 | 18 |
| tag line | 434 | 86 | 78 |

SVG text does not wrap. An overlong line runs into the border. Count characters before writing.

## 7. Connectors

Solid arrows connect consecutive main cards. Caption states the condition, protocol or payload that crosses the boundary. The caption does not repeat either card title.

```html
<line class="arrow" x1="535" y1="100" x2="535" y2="128" marker-end="url(#flowHead)"/>
<text class="cap" x="549" y="118">first http(s) link wins</text>
```

Three line styles: solid, dashed and dotted. A solid line is the main path, a dashed line is a side channel or alternate branch, a dotted line is a return.

| class | look | use |
|---|---|---|
| `arrow` | solid, 1.4, `--muted` | main path between cards |
| `arrow-a` | solid, 1.6, `--accent` | action into or out of the focus card, zero to two per diagram |
| `dash` | dashed, 5 bar with a 4 gap, 1.2, `--muted` | side channel or alternate branch |
| `loop` | dotted, round 1.6, 6 apart, `--muted` | return edge |
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

## 8. Branch and loop patterns

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

Loopback, a later card feeding an earlier one. Four lanes per side, 24 px inside the side box edge and 20 px apart: left 226, 206, 186, 166; right 824, 844, 864, 884. The spine runs under the side box band.

```html
<path class="loop" d="M 300 266 H 226 V 80 H 300" marker-end="url(#flowHead)"/>
```

That is card 3 (top 246) back to card 1 (top 30): out of the lower card at `hi` 266, up lane 1, into the upper card at `lo` 80. The spine covers only the rows between the cards and disappears under a side box if one sits on them.

Rules:

- A dashed line means optional, alternate or side channel, a dotted line means a return, and a solid line is the main path.
- Route around cards, never across them. A loop spine is the one line that may pass under a side box, and only by paint order.
- A side card sits on the row it touches, or 20 px lower if it is 90-100 high.
- No crossing lines. If two branches would cross, move one side block to the other lane or reorder the rows.
- Labels stay at least 10 px from a card border.
- A loopback runs upward only. A forward jump is an alternate branch and stays `dash`.
- Lane 1 carries the shortest span, lane 2 the next, and so on. Spans must be nested or disjoint, never partly overlapping, so loop spines never cross each other.
- A loopback joins main cards only. By default it leaves the lower card at `hi` and enters the upper card at `lo`. `mid` belongs to a side stub on that edge, so a loop stays off `mid` where a stub exists. Two connectors on one edge take different marks.
- The two rows a loopback joins must be free of a side box on that side, otherwise the connector starts under the box. A box on one side rules that side out; use the other side when its rows are free too. A spine may pass at most one side box.
- Write the loop path before the first card rect, so the spine passes under the boxes.
- One loopback per lane, so at most four per side. More than two per diagram usually reads better as two sections.
- A loopback label is optional. If used, it names the returning payload or condition in up to 12 characters, sits in the row gap nearest the arrowhead, 6 px from the spine, and never over a card.

Split row, a decision card forking into two cards on the next row:

```html
<line class="arrow" x1="411" y1="208" x2="411" y2="236" marker-end="url(#flowHead)"/>
<text class="cap" x="425" y="226">musl target</text>
<line class="arrow" x1="659" y1="208" x2="659" y2="236" marker-end="url(#flowHead)"/>
<text class="cap" x="673" y="226">msvc target</text>

<rect class="card" x="300" y="246" width="222" height="70" rx="3"/>
<text class="t" x="318" y="276">Linux</text>
<text class="d" x="318" y="296">x86_64-unknown-linux-musl</text>

<rect class="card" x="548" y="246" width="222" height="70" rx="3"/>
<text class="t" x="566" y="276">Windows</text>
<text class="d" x="566" y="296">x86_64-pc-windows-msvc</text>
```

Two arrows leave the parent bottom at the card centres, 411 and 659, and enter the children at the same x. A merge back into a 470 card uses the same two positions. No fork bar, no elbows.

Split rules:

- The single column stays the default. Use a split only where a decision produces two named outcomes, and make the decision card the focus.
- A split is a branch, not a parallel path: both children leave the same row, and each is a normal card with a title and up to two description lines.
- Both children take 28 characters of description, the same 186 px usable width as a 220 side card. Text sits at 318 and 566.
- Captions sit at 425 and 673 and take 18 characters, so each ends clear of the other and inside x=790.
- The inner edges at 522 and 548 carry no connector. A loop attaches to a split card at its outer edge, x=300 or x=770, at a free mark.
- A side box may sit on a split row, one per side. The left box feeds the left card and the right box the right card.
- Split arrows stay muted. They take the accent only when the focus card is the decision and one branch is the main action.

## 9. Section copy

- h2 pattern: `subject: outcome`, lowercase, for example `video download: url to file`.
- Note: the rule that drives the diagram, not a walkthrough of every box.
- Tag strip: the invariant or the verdict shape, one line. Example: `one run ends in one verdict: finished, failed rc, or stopped by escape`.
- Footer: what both diagrams share, or the one guarantee that holds across paths.
- Plain technical English. No sales words, no slogans, no "not X but Y" contrasts, no meta commentary.
- Keys and literal input render in straight single quotes: 's', '0', 'ready'.

## 10. Diagram body

Copy the page shell from `template.html`: theme tokens, top bar, theme script, bar script and print rules. The block below is one section body to place at the template's diagram slot; repeat it for each diagram. No class on the section: the theme colours every diagram on the page.

```html
<section>
  <div class="head">
    <h2>main path: start to finish</h2>
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
    <text class="t" x="318" y="56">Start</text>
    <text class="d" x="318" y="74">what arrives, and from where</text>

    <rect class="focus" x="300" y="138" width="470" height="70" rx="3"/>
    <text class="t" x="318" y="164">Work</text>
    <text class="d" x="318" y="182">the mechanism: flags, files, endpoints</text>

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

For a decision, replace one row with a split row: two 222 cards at x=300 and x=548, two arrows at 411 and 659, captions at 425 and 673 of 18 characters. Section 8 holds the rules.

## 11. Validation

Run the validator before delivery:

```
python validate.py <topic>-flow.html
```

It reads the page and `template.html` beside it, then prints one line per failure and a final count. Exit code 1 means the page is not ready. It covers:

- File shape: ASCII, LF endings, one h1, one subtitle, one footer, one main, two inline scripts, no external files or network URLs.
- Shell: the style block and both scripts are byte-equal to `template.html`, so an edited shell fails.
- Page: the bar controls in order, the mode switch as a switch, two menus, five dark and four light theme names, the six tokens, the default picks.
- Sections: head block, `subject: outcome` title, note, one svg, `role="img"` and an aria-label.
- Geometry: 1040-wide viewBox, main rows at `30 + 108n` up to seven, 70-high cards, 222 split cards at 300 and 548, side boxes at 210 and 220, one focus card.
- Arrows and captions: one spine arrow over each row gap at 535 or 411 and 659, a caption on the lane at y+88, caption budgets.
- Text: title at y+26, description lines at y+44, +59 and +74, the per-line budgets, one title per card, tag text at y+17.
- Tag and height: tag at last card top + 98 with a `tag + 32` viewBox, or the no-tag height of the last top + 102.
- Connectors: zero to two accent connectors, loops on a lane, upward, leaving and entering at side marks, unique marker ids, every marker defined.
- Colors: no hex or rgb fill or stroke in the markup.

The demo page passes 245 checks. Checks that the validator cannot make, because they need eyes, follow below.

- Open the file at 100 percent zoom. Switch between light and dark, open both theme foldouts and pick one theme from each. Every diagram must follow the theme, with no diagram keeping its own colors.
- Toggle print mode and confirm the print preview: white page, outlined pills, print cards.
- Operate both bar controls with the keyboard and confirm the focus ring and state change. In an open foldout, the arrow keys and Home and End move between rows, and Escape closes it and returns focus to its button.
- Confirm the bar is hidden in the print preview and every diagram renders in the print tokens.
- If a width check is needed, shrink the window until the bar is 360 px wide and confirm the four controls still fit on one line.
- Confirm no caption crosses x=790 and no side text crosses its card edge.
- Confirm a split row: two arrows land on the card centres, each caption sits in its own half, and no connector meets an inner edge.
- Confirm each loopback leaves and enters a main card at a free mark, never on a side stub, and that no loop connector starts under a side box.
- Confirm round loop dots read apart from side dashes (5 4).
- Confirm one focus card and at most two accent connectors per diagram.
- Confirm every marker id referenced by a line exists, and ids are unique across the page.

## 12. Checklist

- [ ] ASCII only, straight quotes, hyphen for dashes.
- [ ] One h1, one sub, one footer.
- [ ] h2 pill reads `subject: outcome`.
- [ ] Main column at x=300, width 470, or a split row of two 222 cards at x=300 and x=548; pitch 108, height 70.
- [ ] Card title at +26, description lines at +44 and +59.
- [ ] Arrow 28 long, caption at y+88, x=549, or x=425 and x=673 on a split row.
- [ ] Tag optional at last card top + 98; viewBox height = tag y + 32, or last card top + 102 without a tag.
- [ ] Up to seven main cards; tag and side boxes do not count.
- [ ] Side boxes fixed: 210 wide at x=40, 220 wide at x=800.
- [ ] Descriptions carry real flags, files and limits.
- [ ] One focus card, zero to two accent connectors, dash only for side channels.
- [ ] Loopbacks use a lane (226/206/186/166 left, 824/844/864/884 right), enter and leave at a free mark, and the path sits before the cards.
- [ ] Return edges use `loop`, side channels use `dash`.
- [ ] Marker ids unique, fills set in `defs`.
- [ ] `role="img"` and a full `aria-label` on each SVG.
- [ ] Light and dark checked in a browser.
- [ ] `python validate.py <topic>-flow.html` exits 0.
- [ ] Top bar present: 24 px, print toggle, mode switch, dark theme and light theme foldouts, keyboard operable.
- [ ] One theme for the page; no section class, no per-diagram colors.
- [ ] Print toggle forces the print tokens and hides the bar in the print preview.
- [ ] Inline scripts limited to the bar; no external files.

## 13. Top bar and modes

`demo.html` is the reference implementation. Copy its bar, token blocks and scripts; do not invent a second control style.

Bar:

- Fixed, 24 px high, right aligned, 28 px inset at both ends, 10 px UI font. Fill is `var(--page-bg)` with no bottom divider, so the controls sit directly on the page.
- Print toggle: auto width, 18 px high, printer icon plus the label `print friendly`, `aria-pressed`. Active fill uses the bar ink.
- Mode switch: 44 x 20 px, moon left and sun right, 16 px thumb, `aria-checked` true in light mode.
- Dark theme and light theme: text label plus a solid downward caret, 18 px high, same border as the print toggle, 68 px minimum width, each with a foldout below it. No icons.
- A foldout lists the theme names for its mode, one row per name, `role="menu"` with `menuitemradio` rows and the current theme marked `aria-checked`. Picking a name applies it and switches to that mode.
- All controls are native `<button>` elements, so Enter and Space work without key handlers. Opening a foldout focuses its checked row, the arrow keys move between rows, Home and End jump to the ends, and Escape closes the foldout, returns focus to its button and also closes on a click outside.

State:

- `html[data-theme="light"]` or `html[data-theme="dark"]` selects the mode, and with it which theme list applies.
- Each mode remembers its own theme. The mode switch flips between the two picks.
- `html[data-print="on"]` forces the print tokens on a white page. It does not change `data-theme`; switching it off restores the mode that was active before.
- Initial mode comes from `prefers-color-scheme`; OS changes are followed until the mode switch or a theme pick is used. No storage.

Token scope:

- Every colour token lives on `:root`: `--page-bg`, `--page-ink`, `--page-muted`, `--page-line`, `--card`, `--ink`, `--muted`, `--line`, `--accent`, `--pick-ink`, the print palette (`--print-bg`, `--print-ink`, `--print-muted`, `--print-line`) and the bar tokens. The switch thumb is written by the theme script.
- The theme script writes the six theme values and the derived menu pick ink to `:root` whenever the mode or theme changes. `--pick-ink` is the text on the filled accent row in the theme foldout; the section pill uses `--page-ink` over a transparent fill.
- Print writes its own fixed values to `:root`, so it wins over the theme without a cascade trick.

Scripts:

- One inline script in the head sets the initial `data-theme` before paint.
- One inline script before `</body>` holds the theme table, builds both foldouts, applies the theme and follows OS changes until the user toggles.

Print:

- `@page` margin 12 mm, exact color adjust, `break-inside: avoid` per section.
- `@media print` hides the bar, removes the page cap, drops the dark color scheme and forces the print palette through the tokens, so paper output is print-themed even when the toggle was never clicked. The pill keeps the transparent fill with a black outline and black text.
- The 250 ms colour transitions stop under `prefers-reduced-motion: reduce`.
- Print mode on screen keeps the bar visible; only the print preview hides it.
