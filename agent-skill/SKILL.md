---
name: simple-flow-diagram-skill
description: "Build flow diagrams as one standalone HTML file in a fixed house style: one vertical main path, optional side channels, muted palette pairs, a small top bar with light/dark switch and print theme, no external assets. Use when asked for a process flow, request path, pipeline, decision flow, state or lifecycle flow, or to restyle an existing flow diagram to this style."
license: MIT
---

# Simple flow diagram

Produce one self-contained `.html` page per flow diagram, or one page with several diagrams. Start from [template.html](template.html): the page shell with the top bar, theme tokens, print rules and a marked diagram slot. The full contract lives in [references/style-manual.md](references/style-manual.md). [demo.html](demo.html) shows the same shell with three filled diagrams; [references/palettes.html](references/palettes.html) is a color catalog, not a layout template.

## Workflow

1. Read `references/style-manual.md` before writing. Copy `template.html` to `<topic>-flow.html`. Replace the title, subtitle and footer; insert diagram sections at the marked slot.
2. Choose a light/dark pair per diagram from the palette catalog: L1/D1, L2/D3, L3/D2, L4/D5. Mix pairs on one page for contrast.
3. Keep the top bar and its inline script. Two controls only: print toggle, then light/dark switch.
4. Write the page in this order: top bar, h1, p.sub, one or more sections (head with h2 pill, p.note, svg), footer. Use the diagram body in manual section 10.
5. Keep the grid: viewBox `0 0 1040 H`, main column x=300 width=470, card top `30 + 108n`, card height 70, arrow 28, caption x=549 at y+88, tag at last card top + 98, viewBox height tag + 32.
6. Fill text within the budgets: main description 65 characters, side description 28 or 26, card title 24, caption 42, tag line 78.
7. Mark one focus card and at most two accent connectors per diagram. Solid for the main path, dash for side channels.
8. Run the section 11 validator, check both modes, check the print preview at 100 percent and at 800 px width.

## Modes and palettes

- One common page background per page, set by the mode. Diagrams do not carry their own page tint.
- Light mode uses light palettes only; dark mode uses dark palettes only, also when several diagrams share a page.
- Print is a separate toggle. It forces every diagram to the P0 tokens and a white page, then restores the previous mode when switched off. It does not change the light/dark selection. The P0 pill is light grey with black text.

## Hard rules

- ASCII only. Straight quotes, hyphen for dash, no arrows, bullets or other Unicode.
- One `h1`, one `.sub`, one footer per page.
- Inline scripts are limited to the top bar and its initial mode. No external JavaScript, CSS, fonts, images or icon sets. Must open from `file://`.
- Top bar: fixed, 24 px high, right aligned, page background fill, no divider, print toggle labelled `print friendly`, then mode switch, native buttons, keyboard operable, labeled.
- Colors only through `var(--...)`. Diagram tokens are scoped per section; the print override comes last.
- Marker ids unique per page, prefixed by section. Pair each line class with the matching arrowhead.
- `--muted` drives text and plain connectors, `--line` drives borders, `--accent` the focus card and active edge, `--mint` the section pill.

## Files

- `references/style-manual.md`: file contract, grid, type scale, card anatomy, connectors, branch patterns, diagram body, validation, checklist, top bar rules.
- `references/palettes.html`: palettes L1 to L4, D1 to D5, P0 print, token table, contrast figures.
- `template.html`: page shell to copy; top bar, tokens, print rules and one marked diagram slot, no diagram content.
- `demo.html`: filled reference page with the bar, three diagrams on different palette pairs, and the print theme.

## Limits

More than seven cards: split into two sections. Text that does not fit the budgets: cut it or split the step. Do not invent fills, sizes or spacing outside the manual.
