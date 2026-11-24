# Simple flow diagram

An agent skill that turns a process into a flow diagram on one HTML page. Every run produces a spec based formatted diagram. Layout, themes, the light and dark switch and the print view are fixed in the template, so the agent writes the cards and the captions and nothing else. Consistent results every time with token economy in mind. An index shell lists a folder of finished pages and documents, with the same bar and small inline SVG glyphs.

The nine themes start from well-known programmer palettes. Text, color, border, muted, accent and the section outline are tuned until each one reads in light, dark and print. The light themes have been specially tuned to prevent glare.

## Themes

Nine themes ship in the template: five dark and four light. Dark: github, harbor, solarized, oledblack, ayu. Light: vercel, tokyonight, cursor, orng. The page opens on theme dependent on OS light/dark mode. The two foldouts switch themes, each mode keeping its own pick. Every color on the page comes from the chosen theme, so a diagram carries no palette of its own.

The 1.4.0 palette pass raises the weak borders and accents. Four mark pairs keep a small shortfall under simulation and are accepted deviations: vercel accent on page, tokyonight accent on card, and the tokyonight and orng checked labels. They affect emphasis and a menu label, not the diagram structure.

## Token cost and consistency

- Fixed cost: one read of the manual and the shell, then the cards. The page shell, the theme table, the bar script and the print rules are copied as they are, so a second diagram on the page adds no shell work.
- Written part: the title, the subtitle, the sections and the footer; a one-diagram page is a few hundred tokens of new text. The shell is read once and copied, not written.
- Consistency: every run uses the same grid and one of nine fixed themes, so pages from different models look the same, toolbar included.
- Verification: no per-page browser pass. The shell is checked once in the repository; the agent checks the written cards against the manual by reading and opens the page once for you. No screenshots, no PDFs, no theme-by-theme renders.
- Measure: context cost is one number, the prompt of the current turn, new input plus cached prefix, as the agent UI shows it. It is not the sum of cache reads across turns.
- Scope: one self-contained file that opens from disk, with no build step, network access or assets.

## Sample page

| Light | Dark | Print friendly |
|:---:|:---:|:---:|
| [<img src="docs/demo-light.png" width="280" alt="Demo page in light mode">](https://chezhenkie.github.io/simple-flow-diagram-skill/demo.html) | [<img src="docs/demo-dark.png" width="280" alt="Demo page in dark mode">](https://chezhenkie.github.io/simple-flow-diagram-skill/demo.html) | [<img src="docs/demo-print-friendly.png" width="280" alt="Demo page with print friendly on">](https://chezhenkie.github.io/simple-flow-diagram-skill/demo.html) |
| Demo, vercel light | Same page, github dark | White page, print tokens |

<table>
  <tr>
    <td><a href="https://chezhenkie.github.io/simple-flow-diagram-skill/demo.html">CLICK HERE TO OPEN THE LIVE, GITHUB-HOSTED DEMO PAGE</a></td>
  </tr>
</table>

## Page controls

Four controls sit at the top right. All are native buttons and work with Tab, Enter and Space.

`print friendly` previews the paper theme on screen: white page, black text and the print tokens on every diagram. The bar is hidden in the browser print preview. Switching it off restores theme that was active before.

The mode switch selects light or dark. The page starts from the OS preference and follows OS changes until the switch is clicked.

`dark theme` and `light theme` open a foldout with five dark names or four light names. Dark: github, harbor, solarized, oledblack, ayu. Light: vercel, tokyonight, cursor, orng. Picking a name applies it to the page and every diagram on it, and switches to that mode. Each mode keeps its own pick, so the switch flips between the two.

<img src="docs/bar-dark.png" width="400" alt="Top bar in dark mode">

Dark mode: github theme, print off.

<img src="docs/bar-light.png" width="400" alt="Top bar in light mode">

Light mode: vercel theme, print off.

<img src="docs/bar-print-friendly.png" width="400" alt="Top bar with print friendly on">

Print friendly on: the print control fills, the mode and theme stay unchanged.

## Several pages

A folder with several diagram pages and text documents can open on one index page. `agent-skill/index.html` is the second shell: a title, one or more groups of link cards, and an optional table of documents. Each card carries a small inline SVG glyph, so the index loads no assets either. The project index is live at https://chezhenkie.github.io/simple-flow-diagram-skill/.

The bar writes the mode and both theme picks into every local `.html` link and reads them on load. A page opened from the index keeps the theme; print stays a preview and does not travel. This is link state, not storage.

The payload is five files. A diagram page copied from an older template still works but ignores the query until its bar script is updated.

## Install

The skill payload is five files in `agent-skill/`. Clone the repository, then copy that folder into the skills folder for your agent and name the copy `simple-flow-diagram-skill`. The folder name must match the `name` in `SKILL.md`.

```sh
git clone https://github.com/chezhenkie/simple-flow-diagram-skill.git
```

| Agent | All projects | One project |
|---|---|---|
| OpenCode | `~/.config/opencode/skills` | `.opencode/skills` |
| Codex | `~/.agents/skills` | `.agents/skills` |
| Pi | `~/.pi/agent/skills` | `.pi/skills` |
| OMP | `~/.omp/agent/skills` | `.omp/skills` |

Copy `simple-flow-diagram-skill/agent-skill` to the path from the table as `simple-flow-diagram-skill`. `~` is your home directory. If your shell does not expand it, use the full path.

Codex scans `.agents/skills` from the current folder up to the repository root. Pi and OMP scan one level under `skills/`. Restart the agent if the skill does not appear.

## Use

Ask for a flow diagram in this style. The agent reads `agent-skill/SKILL.md`, copies `agent-skill/template.html`, fills the page copy and inserts one section per diagram. The diagram body in `agent-skill/style-manual.md` section 10 is the starting block.

For an index of several pages and documents, the agent copies `agent-skill/index.html` and fills the link cards and the documents table; manual section 14 covers the glyph rules and the budgets.

### Call the skill

| Agent | Invocation |
|---|---|
| OpenCode | `@simple-flow-diagram-skill` |
| Codex | `$simple-flow-diagram-skill` |
| Pi | `/skill:simple-flow-diagram-skill` |
| OMP | `/skill:simple-flow-diagram-skill` |

Codex also lists installed skills with `/skills`.

Example request: `Draw the request path as a flow diagram in the house style.`

## Files

| File | Purpose |
|---|---|
| `agent-skill/SKILL.md` | Agent entry point, workflow and hard rules |
| `agent-skill/template.html` | Page shell to copy; marked diagram slot |
| `agent-skill/index.html` | Index shell to copy; link cards with inline glyphs and a documents table |
| `agent-skill/demo.html` | Filled reference page: card payment flow with a side channel, a split and a return |
| `agent-skill/style-manual.md` | Theme rules, grid, type scale, card anatomy, connectors, validation |
| `testing-tools/` | Static checks, page validator and bar behavior checks |
| `docs/` | GitHub Pages index, demo copy and screenshots |
| `color-vision-audit.md` | Colour vision audit of the nine themes |
| `CHANGELOG.md` | Version history |

## Check

Run from the repo root:

```sh
python testing-tools/check.py
```

The script checks ASCII and LF endings, the theme table, SVG geometry, template and demo parity and the page validator on the demo, and runs the bar state machine. Python 3 and Node are required.

## Limits

- One main path per diagram, up to seven rows. A decision may fork into two cards on one row. Split longer flows into sections.
- One theme per page and no colors of the agent's own. The reader picks from nine installed themes. The pick travels in the links, so an index and its pages open on the same one.
- ASCII only, inline SVG, no external assets.
- Text budgets are fixed; cut text or split the step when it does not fit.
- An index lists pages; it is not a dashboard and carries no counts or status.

## License

MIT
