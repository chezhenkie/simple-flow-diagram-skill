# Simple flow diagram

An agent skill that turns a process into a flow diagram on a single HTML page. Open the file in any browser: one main path from start to finish, optional branches on the side, and a top bar for light, dark and print views. No setup, external files or network access.

## Samples

Click a sample to open the full-size PNG.

| Light | Dark | Print friendly |
|:---:|:---:|:---:|
| [<img src="docs/demo-light.png" width="280" alt="Demo page in light mode">](docs/demo-light.png) | [<img src="docs/demo-dark.png" width="280" alt="Demo page in dark mode">](docs/demo-dark.png) | [<img src="docs/demo-print-friendly.png" width="280" alt="Demo page with print friendly on">](docs/demo-print-friendly.png) |
| Three flows, one page background | Same layout, dark palette pairs | White page, print palette |

## Page controls

Two controls sit at the top right. Both are native buttons and work with Tab, Enter and Space.

`print friendly` previews the paper theme on screen: white page, black text and the print palette on every diagram. The bar is hidden in the browser print preview. Switching it off restores the mode that was active before.

The mode switch selects light or dark. The page starts from the OS preference and follows OS changes until the switch is clicked.

<img src="docs/bar-dark.png" width="244" alt="Top bar in dark mode">

Dark mode: moon selected, print off.

<img src="docs/bar-light.png" width="244" alt="Top bar in light mode">

Light mode: sun selected, print off.

<img src="docs/bar-print-friendly.png" width="244" alt="Top bar with print friendly on">

Print friendly on: the print control fills, the light/dark selection stays unchanged.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Agent entry point, workflow and hard rules |
| `template.html` | Page shell to copy; marked diagram slot |
| `demo.html` | Filled reference page with three diagrams |
| `references/style-manual.md` | Grid, type scale, card anatomy, connectors, validation |
| `references/palettes.html` | Palette catalog for both modes and print |
| `tests/` | Static and bar behavior checks |
| `CHANGELOG.md` | Version history |

## Install

Clone the repository into the skills folder for your agent. Keep the folder name `simple-flow-diagram-skill`; it must match the `name` in `SKILL.md`. `~` is your home directory. If your shell does not expand it, use the full path.

| Agent | All projects | One project |
|---|---|---|
| OpenCode | `~/.config/opencode/skills` | `.opencode/skills` |
| Codex | `~/.agents/skills` | `.agents/skills` |
| Pi | `~/.pi/agent/skills` | `.pi/skills` |
| OMP | `~/.omp/agent/skills` | `.omp/skills` |

Replace `<skills-dir>` with the path for your agent and scope:

```sh
git clone https://github.com/chezhenkie/simple-flow-diagram-skill.git "<skills-dir>/simple-flow-diagram-skill"
```

Codex scans `.agents/skills` from the current folder up to the repository root. Pi and OMP scan one level under `skills/`. Restart the agent if the skill does not appear.

## Use

Ask for a flow diagram in this style. The agent reads `SKILL.md`, copies `template.html`, fills the page copy and inserts one section per diagram. The diagram body in `references/style-manual.md` section 10 is the starting block.

Example request: `Draw the request path as a flow diagram in the house style.`

## Check

Run from the repo root:

```sh
python tests/check.py
```

The script validates ASCII and LF endings, palette tokens, SVG geometry, template and demo parity, and the bar state machine. Python 3 and Node are required.

## Limits

- One main path per diagram, up to seven cards. Split longer flows into sections.
- Light mode uses light palettes; dark mode uses dark palettes. Mix pairs for contrast.
- ASCII only, inline SVG, no external assets.
- Text budgets are fixed; cut text or split the step when it does not fit.

## License

MIT
