# Requirements

A diagram page is one HTML file and runs in a browser with no server, network or build step. The behaviour contract is `agent-skill/style-manual.md`; this page covers what a host and the repository checks need.

## Host

- A current browser with CSS custom properties, `color-scheme`, `prefers-color-scheme`, `matchMedia`, inline SVG and the History API. The Navigation API improves the back button state and is optional; without it the button falls back to `history.length`.
- The page opens from `file://` or a static HTTP host. It fetches nothing: the styles, the SVG, the scripts and the nine themes are inline.
- An HTTP host must pass the query string to the page, because every local link carries the mode and both theme names. A host that drops or rewrites the query opens each page on the OS mode and the default picks.
- A UI sans-serif font. The page asks for Segoe UI, then system-ui, then -apple-system, then the browser default; Segoe UI is not required.
- A viewport of any width. The diagram scales with the column, and below 680 px the toolbar wraps to two rows. No minimum resolution.
- No storage. The page writes no cookies or localStorage; mode, theme and slider state live in the URL and page memory.
- An embedded page needs an HTML host that can frame it, with the diagram in the host's folder or below, because a `file://` page frames only its own tree. The iframe height is set from the viewBox.

## Print

- The browser print dialog. The page sets a 12 mm margin, hides the toolbar and prints in its fixed light palette regardless of the chosen mode.
- Card, tag and arrow colours are SVG fills and strokes, so the result does not depend on the browser's background graphics option.

## Skill

- Five files: `SKILL.md`, `template.html`, `index.html`, `demo.html` and `style-manual.md`, copied as one folder named `simpleflow`. The folder name must match `name` in `SKILL.md`.
- An agent that loads skills from a folder, reads those files and writes `.html` in the workspace. Building a page needs no install script, package, compiler or network access.
- One clone or release zip to obtain the files; after that the skill runs offline.
- Index pages and embedded pages add no dependency beyond the same five files and a browser.

## Verification

- Python 3 for `testing-tools/check.py` and `testing-tools/validate.py`, standard library only.
- Node on `PATH` for `testing-tools/harness.js`, which `check.py` runs as part of its pass. No npm package or browser driver.
- A writable checkout: the checker writes probe files to `testing-tools/.artifacts` and removes the folder when the run is clean; a failed run keeps them for inspection.
- A browser on the machine where the page is read; the workflow opens the page once. The checks take no screenshots, make no PDFs and render no theme separately.
- Run from the repository root with `python testing-tools/check.py`. Failures print as FAIL lines, and the exit status is non-zero.
