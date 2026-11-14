---
name: simple-flow-diagram-skill
description: "Build flow diagrams as one standalone HTML file in a fixed house style: one vertical main path, optional side channels, muted palette, light and dark themes, no JavaScript or external assets. Use when asked for a process flow, request path, pipeline, decision flow, state or lifecycle flow, or to restyle an existing flow diagram to this style."
license: MIT
---

# Simple flow diagram

Produce one self-contained `.html` page per flow diagram. The full contract lives in [references/style-manual.md](references/style-manual.md); the ten color sets and token table live in [references/palettes.html](references/palettes.html).

## Workflow

1. Read `references/style-manual.md` before writing. Open `references/palettes.html` only when you need a palette pair.
2. Pick the palette. Default is L1 light with D1 dark. Copy the light row into `:root` and the dark row into the `prefers-color-scheme: dark` block, keep the seven token names.
3. Write the page in this order: h1, p.sub, one or two sections (h2 pill, p.note, svg), footer. Use the skeleton in manual section 10.
4. Keep the grid: viewBox `0 0 1040 H`, main column x=300 width=470, card top `30 + 108n`, card height 70, arrow 28, caption x=549 at y+88, tag at last card top + 98, viewBox height tag + 32.
5. Fill text within the budgets: main description 65 characters, side description 28 or 26, card title 24, caption 42, tag line 78.
6. Mark one focus card and at most two accent connectors. Solid for the main path, dash for side channels.
7. Run the section 11 validator on the finished file.
8. Check 100 percent zoom in both color schemes and at 800 px width before delivery.

## Hard rules

- ASCII only. Straight quotes, hyphen for dash, no arrows, bullets or other Unicode.
- One `h1`, one `.sub`, one footer per page.
- No JavaScript, no external CSS, fonts, images or icon sets. Must open from `file://`.
- Colors only through `var(--...)`. SVG fills and strokes use classes.
- Marker ids unique per page, prefixed by section. Pair each line class with the matching arrowhead.
- `--muted` drives text and plain connectors, `--line` drives borders, `--accent` the focus card and active edge, `--mint` the section pill.

## Files

- `references/style-manual.md`: file contract, grid, type scale, card anatomy, connectors, branch patterns, skeleton, validation, checklist.
- `references/palettes.html`: palettes L1 to L4, D1 to D5, P0 print, token table, contrast figures.

## Limits

More than seven cards: split into two sections. Text that does not fit the budgets: cut it or split the step. Do not invent fills, sizes or spacing outside the manual.
