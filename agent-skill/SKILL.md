---
name: simpleflow
description: "Build a flow diagram as one standalone HTML page: one vertical main path, optional side channels, and a fixed toolbar with nine themes, light/dark switching and a print view already wired up. Built for repeatability: the template carries every repeated decision, so the agent writes only the cards and captions in one pass, and output stays consistent and short. Use when asked for a process flow, request path, pipeline, decision flow, state or lifecycle flow, or to restyle an existing flow diagram to this style. It also builds an index page that lists several diagrams and documents, with small inline SVG glyphs and the same toolbar."
license: MIT
---

# simpleflow diagram

One self-contained `.html` page per topic, or one page with several diagrams. Start from [template.html](template.html): the layout, the themes, the mode switch and the print view are already in it. A folder of finished pages and documents can open on [index.html](index.html), a second template with link cards and a document table.

## Page types

- Diagram page: copy `template.html`; the workflow below applies.
- Index page: copy `index.html`; manual section 14 applies. It lists the diagram pages and documents of one folder, one link card each with a small inline glyph, and keeps the same toolbar, themes and print rules. The mode and both theme names travel in every local page link.
- Embedded page: one finished page can sit inside another HTML page as one iframe placed before the host's closing `</main>`. It keeps its own toolbar and theme, sits in the same folder or below, and takes a height from manual section 14. No second copy.

## Goals

- The same result every run. Copy the template, the theme table and the scripts; the grid, the toolbar and one of nine fixed themes do not change.
- A small written part. Write only the page copy and the diagram cards; the template is copied, not rebuilt.
- One pass. No colour or layout decisions, no second draft.

Do not choose colors or restyle controls; the page follows whichever theme the reader picks.

The full contract lives in [style-manual.md](style-manual.md). [demo.html](demo.html) is the same template with one filled diagram.

## Writing rules

The page copy follows the project's writing rules: the subtitle, the group names, the entry names and descriptions, the document rows and the footer. They hold for this skill, its manual, the README and the changelog.

- Plain professional English: dry, product focused, without owner or user references and without decisions and dates scattered through the text. A header names its subject.
- Short: no big prose, no long explanations, no filler and no bloat.
- No drama, slogans, "X, not Y" contrasts, punchline fragments, superlatives or sales comparisons.
- Never insert a manual line break inside a sentence or a paragraph; text wraps by itself in every viewer. Break only between paragraphs, and in a file wrap only when a line exceeds 500 characters.
- ASCII only, 0x20 to 0x7E plus newline and tab. No em or en dashes, curly quotes, arrows, bullets, box characters or emojis; a dash is a plain hyphen and a quote is straight.

## Workflow

1. Read `style-manual.md` before writing; it carries every number and rule the page needs. Copy `template.html` to `<topic>-flow.html` in the workspace root unless the user or project rules name another folder. Copy the template as it is. Replace the title, subtitle and footer, then insert diagram sections at the marked space. `demo.html` is an optional filled example.
2. Keep the page template as it is: head script, token block, toolbar, toolbar script and print rules. Change only the page copy and the diagram bodies.
3. Fill the copy in two edits. The first replaces the title, h1, p.sub and footer; the second inserts every diagram section at the marked space in order, head with h2 pill, p.note and svg. Use the diagram body in manual section 10. Do not edit one section at a time and do not rewrite the whole page, because edits keep the template byte for byte; a further edit is only for a defect found in the read.
4. Keep the grid: viewBox `0 0 1040 H`, main column x=300 width=470, card top `30 + 108n`, card height 70, arrow 28, caption x=549 at y+88. The tag is optional at last card top + 98 with a viewBox of `tag + 32`, or none with a viewBox of last top + 102. Up to seven main rows; the tag and side boxes do not count. Side boxes are fixed at 210 wide on x=40 and 220 wide on x=800. A decision may fork into two 222 cards at x=300 and x=548, with arrows at 411 and 659 and captions at 425 and 673. A merge back into one 470 card keeps that pair, captions optional.
5. Fill text within the budgets: 65 characters per main line, 28 or 26 per split or side line, card title 24, caption 42 or 18 on a split, tag line 78. Write three characters under each limit, so a read can see the slack. A 70-high card takes two lines, a 90/100-high side card three.
6. Mark one focus card and zero to two accent connectors per diagram. Solid for the main path, dashed for side channels, dotted for returns.
7. Check the written part by reading it once, by eye, against the manual section 12 checklist: page structure, geometry, arrows and captions, text budgets, focus and accents, loop lanes and marker ids. Do not write a checker script, run a separate check tool, or count, grep, diff or hash the page with commands; a check is a read, not a measurement. The template is copied byte for byte and is already checked in the repository, so do not compare the page against it and do not test the toolbar, themes or print. On a page that already holds a diagram, read only the new section and leave the earlier ones alone. A defect found in the read gets one repair edit; a defect that survives that edit is named in the reply to the user, never chased in another pass. Open the page once for the user when it is done; if it is already open from an earlier pass, do not open another window or tab, and let the user refresh.
8. After the user has viewed the page, ask whether the diagram file can be deleted. Do not delete it unasked.

## Themes and modes

- One theme covers the page and every diagram on it. Sections carry no class, no token block and no color of their own.
- The reader picks the theme: five dark names and four light names in the two menus, each mode remembering its own choice.
- The mode switch chooses light or dark and starts from the OS preference. Print is a separate toggle with fixed values.
- A link between pages carries the mode and both theme names, never the six values. Each page resolves the names through its own table, so pages from different projects can share the choice while each keeps its own palette.
- Brightness and saturation sliders adjust the applied palette in seven steps; they never change the saved pick and print ignores them.
- Never hardcode a fill or stroke outside the template's classes and `var(--...)` tokens.

## Hard rules

- ASCII only. Straight quotes, hyphen for dash, no arrows, bullets or other Unicode.
- One `h1`, one `.sub`, one footer per page.
- Inline scripts are limited to the head mode script and the toolbar script. No external JavaScript, CSS, fonts, images or icon sets. Must open from `file://`.
- Toolbar: fixed, 24 px high, right aligned, page background fill, no divider. Print toggle labelled `print friendly`, mode switch, then the `dark theme` and `light theme` menus, then the brightness and saturation sliders. Native controls, keyboard operable, labeled.
- Colors only through `var(--...)`. Tokens live on `:root`; the print override comes last.
- Marker ids unique per page, prefixed by section. Pair each line class with the matching arrowhead.
- Open a finished page once for the user. No screenshots, no PDFs, no theme-by-theme renders; the template is checked in the repository, not on every page.

## Files

- `style-manual.md`: file contract, theme rules, type scale, grid, card anatomy, connectors, branch and loop patterns, diagram body, validation, checklist, toolbar rules, index pages and embeds.
- `template.html`: page template to copy; theme table, toolbar, print rules and one marked space for the diagram, no diagram content.
- `index.html`: index template to copy; grid of link cards with inline glyphs, documents table, same toolbar. Fill the marked copy spaces.
- `demo.html`: filled reference page with the toolbar, one card payment diagram and the print theme.

## Limits

More than seven main rows: split into two sections. Text that does not fit the budgets: cut it or split the step. Do not invent fills, sizes or spacing outside the manual. An index lists pages; it is not a dashboard and carries no counts or status.
