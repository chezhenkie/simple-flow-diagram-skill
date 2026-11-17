# Tools

Two checks guard the skill payload. Run them from the repository root or by absolute path.

```sh
python tools/check.py        # 324 static checks, prints failures only
python tools/check.py -v     # same run, prints every PASS line
node tools/harness.js        # bar script against a fake DOM
```

`check.py` covers ASCII and LF endings, the top bar markup and order, menu classes, the theme table and the default token blocks, the inline scripts, grid geometry, text budgets, SKILL.md, the style manual, the changelog, README links and images, node syntax, and the harness itself. It reads files relative to the repository root, so any working directory is fine.

`harness.js` loads the bar script into a small fake DOM and checks the initial mode, OS preference following, menu rows, theme picking, per-mode memory, print tokens, and the switch thumb reset. `check.py` runs it automatically, so a separate call is only needed when debugging the bar.

Artifacts, if any, go to `tools/.artifacts`, which is ignored by git. Both files are required to be ASCII with LF endings.

The checker asserts that `docs/index.html` is byte-identical to `agent-skill/demo.html` and that the `:root` and dark token blocks match the first theme of each mode, so a theme or default change means updating the table, the blocks, the README name lists, and the `DARK` and `LIGHT` lists in both tool files.
