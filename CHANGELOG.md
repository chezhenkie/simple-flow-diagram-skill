# Changelog

## 0.4.0

### New features

#### All platforms

* Added `template.html`: page shell with the top bar, token blocks, print rules and a marked diagram slot, no diagram content.
* Added `README.md` and `docs/` screenshots: demo page in light, dark and print states, plus closeups of both page controls.
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
