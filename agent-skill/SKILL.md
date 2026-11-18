---
name: simple-flow-diagram-skill
description: "Build a flow diagram as one standalone HTML page: one vertical main path, optional side channels, and a fixed top bar with nine themes, light/dark switching and a print view already wired up. Built for speed and token efficiency: the template carries every repeated decision, so the agent writes only the cards and captions in one pass, and output stays consistent and short. Use when asked for a process flow, request path, pipeline, decision flow, state or lifecycle flow, or to restyle an existing flow diagram to this style."
license: MIT
---

# Simple flow diagram

One self-contained `.html` page per topic, or one page with several diagrams. Start from [template.html](template.html): the layout, the themes, the mode switch and the print view are already in it.

## Goals

- Minimal token use. Copy the shell, the theme table and the scripts; write only the page copy and the diagram cards.
- Speed. One pass, no colour or layout decisions, no second draft.
- Consistency. The same grid and the same nine themes on every run, from any model.

Do not choose colors or restyle controls; the page follows whichever theme the reader picks.

The full contract lives in [style-manual.md](style-manual.md). [demo.html](demo.html) is the same shell with four filled diagrams.

## Workflow

1. Read `style-manual.md` before writing; sections 5 to 10 carry every number the page needs. Copy `template.html` to `<topic>-flow.html` in the workspace root unless the user or project rules name another folder. Copy the shell as it is: read only the marked diagram slot, not the whole file. Replace the title, subtitle and footer, then insert diagram sections at the slot. `demo.html` is optional reference, not required reading.
2. Keep the page shell as it is: head script, token block, top bar, bar script and print rules. Change only the page copy and the diagram bodies.
3. Write the page in this order: top bar, h1, p.sub, one or more sections (head with h2 pill, p.note, svg), footer. Use the diagram body in manual section 10.
4. Keep the grid: viewBox `0 0 1040 H`, main column x=300 width=470, card top `30 + 108n`, card height 70, arrow 28, caption x=549 at y+88. The tag is optional at last card top + 98 with a viewBox of `tag + 32`, or none with a viewBox of last top + 102. Up to seven main cards; the tag and side boxes do not count. Side boxes are fixed at 210 wide on x=40 and 220 wide on x=800. A decision may fork into two 222 cards at x=300 and x=548, with arrows at 411 and 659 and captions at 425 and 673.
5. Fill text within the budgets: 65 characters per main line, 28 or 26 per split or side line, card title 24, caption 42 or 18 on a split, tag line 78. A 70-high card takes two lines, a 90/100-high side card three.
6. Mark one focus card and zero to two accent connectors per diagram. Solid for the main path, dashed for side channels, dotted for returns.
7. Run `python validate.py <topic>-flow.html` and fix every failure. Then check both modes, both theme foldouts and the print preview at 100 percent. Open the page in the local browser when it is done; if it is already open from an earlier pass, do not open another window or tab, and let the user refresh.
8. After the user has viewed the page, ask whether the diagram file can be deleted. Do not delete it unasked.

## Themes and modes

- One theme covers the page and every diagram on it. Sections carry no class, no token block and no color of their own.
- The reader picks the theme: five dark names and four light names in the two foldouts, each mode remembering its own pick.
- The mode switch chooses light or dark and starts from the OS preference. Print is a separate toggle with fixed values.
- Never hardcode a fill or stroke outside the template's classes and `var(--...)` tokens.

## Hard rules

- ASCII only. Straight quotes, hyphen for dash, no arrows, bullets or other Unicode.
- One `h1`, one `.sub`, one footer per page.
- Inline scripts are limited to the head mode script and the bar script. No external JavaScript, CSS, fonts, images or icon sets. Must open from `file://`.
- Top bar: fixed, 24 px high, right aligned, page background fill, no divider. Print toggle labelled `print friendly`, mode switch, then the `dark theme` and `light theme` foldouts. Native buttons, keyboard operable, labeled.
- Colors only through `var(--...)`. Tokens live on `:root`; the print override comes last.
- Marker ids unique per page, prefixed by section. Pair each line class with the matching arrowhead.
- Open a finished page in the local browser. If it is already open from an earlier pass, do not open another window or tab; the user refreshes.

## Files

- `style-manual.md`: file contract, theme rules, type scale, grid, card anatomy, connectors, branch and loop patterns, diagram body, validation, checklist, top bar rules.
- `validate.py`: page validator; run it after the draft and after every edit.
- `template.html`: page shell to copy; theme table, top bar, print rules and one marked diagram slot, no diagram content.
- `demo.html`: filled reference page with the bar, one card payment diagram and the print theme.

## Limits

More than seven main cards: split into two sections. Text that does not fit the budgets: cut it or split the step. Do not invent fills, sizes or spacing outside the manual.
