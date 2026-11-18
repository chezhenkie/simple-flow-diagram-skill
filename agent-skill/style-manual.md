# Flow diagram style manual

Specsheet for hand-written, single-file flow diagrams with a small top bar for mode, theme and print. One vertical main path, optional side blocks, one theme for the page, no external dependencies. The shell is copied, not rebuilt; the written part stays small because the grid, the type scale, the themes and the budgets are fixed.

## 1. File contract

- One `.html` file per topic, `<topic>-flow.html`, copied from `template.html`.
- UTF-8, printable ASCII only. No typographic quotes, dashes, arrows or bullets.
- Inline scripts limited to the top bar and its initial mode. No external CSS, fonts, images or icon sets. Must open from `file://`.
- Light and dark from the bar switch, initial state from `prefers-color-scheme`; two foldouts pick a theme per mode; print is a separate toggle.
- One `<main>` wrapper, max width 1080 px, centered; one `<h1>`, one `.sub`, one or more `<section>` blocks, one `<footer>`. The SVG scales with the page, no fixed width or height attributes.

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

A theme is six values: `bg` page, `card` card and tag fill, `ink` page text and card titles, `muted` descriptions, captions, connectors, footer and bar ink, `line` card and tag borders and bar lines, `accent` pill outline, focus border and action arrow.

Nine themes ship in the template: five dark and four light. Dark: `github`, `monochrome`, `ayu`, `nightowl`, `solarized`. Light: `vercel`, `tokyonight`, `cursor`, `orng`. Light opens on `vercel`, dark on `github`.

- The agent does not pick, mix or author colors. The theme script in `template.html` writes the six values as CSS custom properties.
- A diagram carries no colors of its own: no class on a section, no per-section token block, no inline `fill` or `stroke` with a color value.
- The pill is transparent with a 2 px accent outline and takes the page ink for its text, in both modes. No theme fills the title box.
- One theme per page; two diagrams use the same tokens and contrast comes from layout and copy.
- Print is a separate state with fixed tokens: white page, black ink, `#333333` muted, `#9a9a9a` line, black accent, and the same transparent pill with a 2 px black outline and black text.

## 4. Type scale

Class sizes: h1 22/400, `.sub` 13, h2 16/600, `.note` 13, `.t` 14.5/600, `.d` 12.5, `.cap` 11.5, `.side` 11.5, footer 12. Body stack `"Segoe UI", system-ui, -apple-system, sans-serif`, 15px/1.45. The budgets leave 10 percent headroom for wider fallback fonts; a size change invalidates them.

## 5. Grid

Coordinates are integers in a `1040 x H` viewBox.

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

A split row replaces the main card on that row; the parent above and any merged card below stay 470 wide. Six main cards put the last top at 570, the tag at 668 and the height at 700; two cards put the tag at 236 and the height at 268, or 232 without a tag.

Side marks, from a card or side box top, where `h` is the height:

| mark | y | use |
|---|---|---|
| `hi` | top + 20 | loopback exit on the lower card |
| `mid` | top + h/2 | side channel stub |
| `lo` | top + h - 20 | loopback entry on the upper card |

A 70-high card puts the marks at 20, 35 and 50; a 90-high side box at 20, 45 and 70; a 100-high box at 20, 50 and 80.

Baselines:

- 70-high card: title `y+26`, up to two description lines at `y+44` and `y+59`.
- 90/100-high side card: title `y+26`, up to three description lines at `y+44`, `y+59`, `y+74`.
- Tag text: `y+17`.

Do not change the 108 pitch. If a card needs more text, cut the text or split the step. A diagram carries up to seven main cards; the tag and side boxes do not count, and a longer path becomes two sections.

## 6. Card anatomy

A card is `<rect class="card">` or `<rect class="focus">` with `rx="3"`, plus `.t`: 1 to 4 words, sentence case, the actor or stage, no punctuation and no verbs in title case; and `.d`: the concrete mechanism, with real flags, endpoints, file names, sizes, no marketing, no restatement of the title, no trailing period. A 70-high card takes two description lines, a 90/100-high side card three. `focus` marks the component that does the work or coordinates the branch; one per diagram.

Text limits, per line:

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

SVG text does not wrap; an overlong line runs into the border. Count characters before writing.

## 7. Connectors

Solid arrows connect consecutive main cards. The caption states the condition, protocol or payload that crosses the boundary, and does not repeat either card title.

```html
<line class="arrow" x1="535" y1="100" x2="535" y2="128" marker-end="url(#flowHead)"/>
<text class="cap" x="549" y="118">first http(s) link wins</text>
```

| class | look | use |
|---|---|---|
| `arrow` | solid, 1.4, `--muted` | main path between cards |
| `arrow-a` | solid, 1.6, `--accent` | into or out of the focus card, zero to two per diagram |
| `dash` | dashed, 5 bar with a 4 gap, 1.2, `--muted` | side channel or alternate branch |
| `loop` | dotted, round 1.6, 6 apart, `--muted` | return edge |

Line and arrowhead are separate objects; the marker path carries the color. Pair `arrow` and `dash` with the muted marker, `arrow-a` with the accent marker. Marker ids are unique per page, prefixed by section (`vidHead`, `sumHead`).

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

Side input, dashed into the main column: `<path class="dash" d="M 250 173 H 290" marker-end="url(#flowHead)"/>`

Side output: `<path class="dash" d="M 770 399 H 796" marker-end="url(#flowHead)"/>`

Exit branch with no return, such as a missing prerequisite: `<path class="dash" d="M 300 173 H 254" marker-end="url(#flowHead)"/>`

Fallback that rejoins a lower card: `<path class="dash" d="M 910 454 V 605 H 780" marker-end="url(#flowHead)"/>` with its `.side` label.

Loopback, a later card feeding an earlier one. Four lanes per side, 24 px inside the side box edge and 20 apart: left 226, 206, 186, 166; right 824, 844, 864, 884. The spine runs under the side box band and is written before the first card rect.

```html
<path class="loop" d="M 300 266 H 226 V 80 H 300" marker-end="url(#flowHead)"/>
```

That is card 3 (top 246) back to card 1 (top 30): out at `hi` 266, up lane 1, in at `lo` 80. The spine covers the rows between the cards and disappears under a side box that sits on them.

- Dashed is optional, alternate or side; dotted is a return; solid is the main path. A loopback runs upward only; a forward jump stays `dash`.
- Route around cards, never across them. Only a loop spine passes under a side box, by paint order. Labels stay 10 px from a card border.
- Lane 1 carries the shortest span, lane 2 the next; spans nest or stay disjoint.
- A loopback joins main cards: out of the lower card at `hi`, into the upper at `lo`; `mid` belongs to a side stub. Two connectors on one edge take different marks.
- The joined rows must be free of a side box on that side, and a spine passes at most one box.
- One loopback per lane, at most four per side; more than two per diagram reads better as two sections.
- An optional label names the returning payload in up to 12 characters, in the row gap nearest the arrowhead, 6 px from the spine, never over a card.

Split row, a decision card forking into two cards on the next row:

```html
<line class="arrow" x1="411" y1="208" x2="411" y2="236" marker-end="url(#flowHead)"/>
<text class="cap" x="425" y="226">musl target</text>
<line class="arrow" x1="659" y1="208" x2="659" y2="236" marker-end="url(#flowHead)"/>
<text class="cap" x="673" y="226">msvc target</text>

<rect class="card" x="300" y="246" width="222" height="70" rx="3"/>
<text class="t" x="318" y="272">Linux</text>
<text class="d" x="318" y="290">x86_64-unknown-linux-musl</text>

<rect class="card" x="548" y="246" width="222" height="70" rx="3"/>
<text class="t" x="566" y="272">Windows</text>
<text class="d" x="566" y="290">x86_64-pc-windows-msvc</text>
```

Two arrows leave the parent bottom at the card centres, 411 and 659, and enter the children at the same x. A merge back into a 470 card uses the same positions. No fork bar, no elbows.

- The single column stays the default. A split needs a decision with two named outcomes, and the decision card is the focus.
- Both children leave the same row and are normal cards with a title and up to two description lines.
- Both take 28 characters, the 186 px width of a 220 side card, with text at 318 and 566.
- Captions sit at 425 and 673 and take 18 characters, so each stays inside x=790.
- The inner edges at 522 and 548 carry no connector. A loop attaches at the outer edge, x=300 or x=770, at a free mark.
- A side box may sit on a split row, one per side: the left box feeds the left card, the right box the right card.
- Split arrows stay muted, and take the accent only when the focus card is the decision and one branch is the main action.

## 9. Section copy

- h2 pattern: `subject: outcome`, lowercase, as in `video download: url to file`.
- Note: the rule that drives the diagram, not a walkthrough.
- Tag: the invariant or verdict shape in one line, as in `one run ends in one verdict: finished, failed rc, or stopped by escape`.
- Footer: what the paths share, or the one guarantee that holds across them.
- Plain technical English. No sales words, slogans, "not X but Y" contrasts or meta commentary. Keys and literal input render in straight single quotes: 's', '0', 'ready'.

## 10. Diagram body

Copy the shell from `template.html`: theme tokens, top bar, theme script, bar script and print rules. The block below is one section body for the diagram slot; repeat it per diagram. No class on the section.

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

```
python validate.py <topic>-flow.html
```

It reads the page and `template.html` beside it, prints one line per failure and a final count, and exits 1 when the page is not ready. It covers the file shape, the shell copy byte-equal to `template.html`, the bar and its theme table, the section structure, the geometry (`30 + 108n` rows, split cards, side boxes, one focus card), the arrows and captions, the text baselines and budgets, the tag and viewBox height, the connectors, marker ids and hardcoded colors.

The demo page passes 245 checks. The checks that need eyes:

- Open the file at 100 percent. Switch light and dark, open both foldouts, pick one theme from each; every diagram follows the theme.
- Toggle print and confirm white page, outlined pills and print cards. The bar is hidden in the print preview.
- Operate the bar by keyboard: focus ring, state change, arrows and Home and End in an open foldout, Escape returns focus.
- Confirm no caption crosses x=790, and a split row lands its arrows on the card centres with each caption in its half.
- Confirm each loopback leaves and enters at a free mark, never a side stub, and no loop starts under a side box.
- Confirm one focus card and at most two accent connectors, every marker id referenced and unique.
- If a width check is needed, shrink until the bar is 360 px wide and confirm four controls fit on one line.

## 12. Checklist

- [ ] ASCII only, straight quotes, hyphen for dashes.
- [ ] One h1, one sub, one footer; h2 pill reads `subject: outcome`.
- [ ] Main column x=300 width 470, or two 222 cards at 300 and 548; pitch 108, height 70.
- [ ] Title at +26, descriptions at +44 and +59; tag at last top + 98 and viewBox at tag y + 32, or last top + 102.
- [ ] Up to seven main cards; side boxes 210 at x=40 and 220 at x=800.
- [ ] One focus card, zero to two accent connectors; `dash` for sides, `loop` for returns.
- [ ] Loop lanes at 226/206/186/166 and 824/844/864/884, free marks, path before the cards.
- [ ] Marker ids unique and defined; `role="img"` and an aria-label on each SVG.
- [ ] One theme for the page, no section class, no per-diagram colors; inline scripts bar only.
- [ ] `python validate.py <topic>-flow.html` exits 0, then light and dark checked in a browser.

## 13. Top bar and modes

`demo.html` is the reference implementation. Copy its bar, token blocks and scripts; do not invent a second control style.

- Fixed, 24 px high, right aligned, 28 px inset, fill `var(--page-bg)`, no bottom divider.
- Print toggle: auto width, 18 px high, printer icon plus `print friendly`, `aria-pressed`; active fill is the bar ink.
- Mode switch: 44 x 20 px, moon left, sun right, 16 px thumb, `aria-checked` true in light.
- Theme buttons: text plus a solid caret, 18 px high, 68 px minimum width, a foldout below each.
- A foldout lists its mode's names in `role="menu"` rows with `menuitemradio` and the current name marked `aria-checked`. Picking one applies it and switches mode.
- Native `<button>` controls, so Enter and Space work. Opening a foldout focuses its checked row; arrows move, Home and End jump, Escape closes the foldout and returns focus to its button, a click outside closes it.
- `html[data-theme="light"|"dark"]` selects the mode and its list. Each mode remembers its own theme; the switch flips between the two picks.
- `html[data-print="on"]` forces the print tokens on a white page and leaves `data-theme` alone; off restores the previous mode.
- Initial mode comes from `prefers-color-scheme`, followed until the mode switch or a theme pick. No storage.
- Tokens live on `:root`; the theme script writes the six values and `--pick-ink` on every change, and print writes its fixed values there too, so it wins without a cascade trick.
- One inline head script sets the initial `data-theme` before paint; one script before `</body>` holds the theme table, builds the foldouts, applies the theme and follows OS changes.
