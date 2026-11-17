# Changelog

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
