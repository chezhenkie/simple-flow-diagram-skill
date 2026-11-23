# Changelog

## 1.5.0

### New features

#### All platforms

* An index shell joins the payload: `agent-skill/index.html`, a title, groups of link cards and an optional documents table. Each card carries a small inline SVG glyph drawn with the theme tokens.
* The bar carries the mode and both theme picks in every local `.html` link, so a page opened from the index keeps the chosen theme. The head script reads the mode before paint. No storage.
* The workflow keeps the browser out of the loop: the shell is checked once in the repository, the written part is checked by reading, and the page is opened once for the user. No screenshots, no PDFs, no per-theme renders.
* Manual section 14 is a separate chapter for index pages; the payload is five files.

## 1.4.0

### Changes

#### All platforms

* The palette pass raises the weak accent and line values. Github accent and line, harbor line, solarized accent and line, oledblack line, vercel accent, tokyonight line, cursor accent and line, and orng line change.
* Solarized and vercel accents sit between their original and fully passing values; tokyonight and orng accents are unchanged. Four mark pairs keep a small shortfall under deuteranopia and are accepted deviations; the manual and the colour audit record them.
* The colour audit carries the clamp, line-on-page and scoped-loss corrections, the 1.4.0 values and the accepted deviations.

## 1.3.7

### Changes

#### All platforms

* The page validator leaves the skill payload for `testing-tools/validate.py`. The payload is four files, needs no Python 3 and no longer reads the 14.6 KB source.
* `SKILL.md` step 7 and manual section 11 check the page against the manual and the browser instead of a command; the checker keeps the mechanical page check for the demo and an off-grid probe.
* The checker enforces the payload: `agent-skill/` holds four files, no executable, and neither the skill nor the manual names a runtime. 312 checks.
* The colour vision audit of the nine themes is added at `color-vision-audit.md`.

## 1.3.6

### New features

#### All platforms

* The focus card carries a 2 px accent border instead of 1.4, so the marking does not rely on colour alone. The manual states the width.

## 1.3.5

### New features

#### All platforms

* The dark foldout gains harbor: a navy page, dark grey cards and a teal accent, taken from the dark palette of an existing page.
* Monochrome is renamed oledblack. Its six values are unchanged.
* Nightowl is removed. Dark order: github, harbor, solarized, oledblack, ayu.

## 1.3.4

### New features

#### All platforms

* The README and the skill goals put the same result first: every run uses the same grid, the same toolbar and one of nine fixed themes. The cost section states the read it takes, the manual and the shell once, then the cards.
* The skill description and goals say repeatable, small written part and one pass. The checker follows the new wording.

## 1.3.3

### New features

#### All platforms

* The style manual is 17.6 KB against 23.6 KB, with the same numbers and rules: the theme value table, the type scale table, the repeated validator coverage and the long checklist are now short prose or short lists.
* The split example in the manual places the title at y+26 and the description at y+44, matching the card grid and the validator; the old block used the retired y+30 baseline.

## 1.3.2

### New features

#### All platforms

* The demo page is one long diagram: a card payment flow from the Pay press to the receipt, with a fraud side channel, a two-card decision split, a return lane and a tag line.
* The samples are rebuilt from that page: three 900 x 806 shots of the whole page, footer included.
* The checker follows the new demo: one section, one diagram, two marker ids, a split-row check that looks at every section, and the validator count read from the manual instead of hardcoded, at 313 checks. The demo passes 245.

## 1.3.1

### New features

#### All platforms

* The checker accepts two side cards, one per side, and one or two dashes per box, so it matches the manual's side-card contract. A two-box fixture with three dashes passes; the same page with one dash fails.
* The switch thumb pairs live in one table read by the theme and print paths, and the print palette is defined once in `:root`, aliased by `@media print` and by the print toggle. The values are typed once.
* The bar menus take the keyboard: opening a foldout focuses its checked row, the arrow keys and Home and End move between rows, and Escape closes it and returns focus to its button. The focus ring stays inside the viewport, print drops the dark color scheme, and a `prefers-reduced-motion` rule stops the 250 ms transitions.
* The checker follows the new shell: 394 checks.

## 1.3.0

### New features

#### All platforms

* Page validator: `python validate.py <topic>-flow.html` ships in the payload and checks the file shape, the shell copy, the bar, the section structure, the grid, arrows and captions, text budgets, tag and height, connectors, lanes and marker ids. The demo page passes 460 checks with exit code 0.
* Contract decisions reach the manual and the skill: side boxes fixed at 210 and 220, optional tag with a no-tag height of last card top + 102, up to seven main cards excluding the tag and side boxes, zero to two accent connectors, the loopback label convention, and a 360 px bar check in place of the 800 px window step.
* The skill names the validator in step 7 and reads only the diagram slot and manual sections 5 to 10, so a page costs no more tokens than before.
* Manual section 11 is the validator description; the inline Python block is gone.
* The bar harness reads both inline scripts from `demo.html`, so a fresh clone runs it without `check.py`.
* The checker runs the validator on the demo, compares its count with the manual and requires a failure on an off-grid card: 381 checks.

## 1.2.0

### New features

#### All platforms

* Readability is the first theme rule. The nine themes were retuned for contrast in light, dark and print, and the theme set was checked in the browser.
* The section title is an outline in every theme and in print: transparent fill, a 2 px accent border and page ink text, so no theme dominates the page with a filled block. The README intro states the palette work and the light theme handling.
* Pill text is black or white by measured contrast: vercel and cursor take black, tokyonight and orng keep white.
* Light theme inks darkened: vercel `#B81F1F` (4.99:1), tokyonight `#2655C2` (5.14:1), orng `#A63D1A` (4.91:1).
* Nightowl outline `#9B6FD0` and accent `#27A65C`; solarized muted text `#8FA5AA`.
* A theme pick stops OS preference following; the harness covers the case.
* A diagram may use zero accent connectors.
* The checker follows the contrast threshold and the zero-accent rule: 370 checks.

## 1.1.0

### New features

#### All platforms

* All 70-high cards share one text grid: title at `y+26`, description lines at `y+44` and `y+59`. Main, focus and split cards now carry two description lines like side cards, with no taller box, and titles align across the main column and the side lanes.
* Text budgets apply per line: 65 characters on a main line, 28 on a split line, 28 or 26 on a side line. A 90/100-high side card takes a third line at `y+74`.
* The checker accepts the shared baselines and two-line cards: 370 checks.
* Checks moved to `testing-tools/`; run `python testing-tools/check.py`.
* README sample shots are recropped to the first two sections and the bar closeups display at 400 px.

## 1.0.0

### New features

#### All platforms

* Split row: a decision card forks into two 222 px cards at x=300 and x=548, with arrows at 411 and 659 and captions at 425 and 673. A merge returns on the same two positions.
* Loopback returns use four lanes per side, 24 px inside the side box at a 20 px pitch, drawn as round dots so a return reads apart from a side dash.
* Three line styles are named: solid for the main path, dashed for a side channel or alternate branch, dotted for a return.
* Nine themes: monokai is gone and the light foldout lists four names. Light opens on vercel and dark on github; `:root` mirrors vercel and the dark block mirrors github.
* Vercel accent retuned to `#E8A020` and tokyonight muted text to `#474F60`.
* Top bar carries a 28 px inset at both ends.
* `demo.html` adds a package section with the split row, and the docs section returns a rejected draft to Draft. Section order is request, package, video, docs.
* `SKILL.md` opens a finished page in the local browser and keeps a second window closed when the page is already open.
* The checker covers split rows and per-boundary arrows and captions: 370 checks.
* Regenerated all six screenshots.

## 0.7.0

### New features

#### All platforms

* Ten themes, retuned for contrast and ordered by mode. Dark: github, monochrome, ayu, nightowl, solarized. Light: tokyonight, vercel, cursor, monokai, orng.
* Defaults are github for dark and tokyonight for light. The page opens in light mode on tokyonight.
* Removed catppuccin and synthwave84. Dark vercel becomes monochrome.
* Style manual moved to `agent-skill/style-manual.md`, beside `SKILL.md`. `references/` is gone.
* `SKILL.md` saves new pages to the workspace root unless the project rules name another folder, and asks before deleting a diagram the user has seen.
* README gains a Themes section naming all ten themes and a cost and speed section. Install instructions are OS neutral.
* Added `tools/README.md`. The checker and bar harness cover the new theme table, the defaults and the print tokens: 321 checks.
* Bar controls polished: wider print toggle with visible label, raised button text, per-mode switch thumb colors.
* Regenerated all six screenshots from the current files.

## 0.6.0

### New features

#### All platforms

* Themes replace palette pairs. Twelve built-in themes: ayu, catppuccin, github, nightowl, solarized and vercel for dark; cursor, monokai, orng, synthwave84, tokyonight and vercel for light.
* Two foldout controls in the top bar, `dark theme` and `light theme`, each listing the six names for its mode. Picking one applies it and switches mode; each mode keeps its own pick.
* One theme covers the page and every diagram on it. Sections carry no class and no colors of their own.
* The agent no longer chooses colors. The page shell and the theme table are fixed, so a diagram costs only the cards, captions and notes.
* Removed the palette catalog and its per-section tokens.
* Rewritten checker and bar harness for the theme table, the foldouts, and print tokens on `:root`.

## 0.5.0

### New features

#### All platforms

* Moved the skill payload to `agent-skill/`: `SKILL.md`, `template.html`, `demo.html` and `references/`.
* Moved the validator and bar harness to `tools/`; run `python tools/check.py`.
* Added the public GitHub Pages demo and linked it from the README.
* Added per-agent install and invocation instructions for OpenCode, Codex, Pi and OMP.

## 0.4.0

### New features

#### All platforms

* Added `template.html`: page shell with the top bar, token blocks, print rules and a marked diagram slot, no diagram content.
* Added `README.md` and `docs/` screenshots: demo page in light, dark and print states, plus closeups of both page controls.
* Moved the validator and bar harness to `tests/`; run `python tests/check.py` from the repo root.
* Top bar uses the page background with no divider; controls sit directly on the page.
* Skill workflow and style manual start from the template; `demo.html` remains the filled reference page.

## 0.3.0

### New features

#### All platforms

* Added a fixed 24 px top bar with a light/dark switch and a separate print theme toggle labelled `print friendly`.
* Multi-diagram pages share one page background and may mix palette pairs; dark mode uses dark palettes only and light mode light palettes only.
* Added `demo.html` as the reference shell with three diagrams, both modes and the print theme.
* Print theme uses a white page, P0 diagrams and a light grey pill with black text and a black border.
* Skill and style manual updated: inline bar scripts, no external assets, print override rules.

## 0.2.0

### New features

#### All platforms

* Packaged as an agent skill: root `SKILL.md` with name, description and license frontmatter, workflow and hard rules.
* Style manual and palette sheet moved to `references/` and linked one level deep from the skill file.

## 0.1.0

### New features

#### All platforms

* Style manual for single-file flow diagrams: file contract, 1040-wide grid, card anatomy, text budgets, connector and branch patterns, skeleton and validation checklist.
* Palette sheet with four light palettes, five dark palettes and one print palette, each rendering the same sample diagram.
* Token table with page, card, ink, muted, line, accent and pill values per palette, plus contrast figures.
