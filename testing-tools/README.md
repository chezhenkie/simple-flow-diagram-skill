# Testing tools

The static checker and the bar harness guard the skill payload; the page validator checks the demo. Run them from the repository root or by absolute path.

```sh
python testing-tools/check.py        # 357 static checks, prints failures only
python testing-tools/check.py -v     # same run, prints every PASS line
node testing-tools/harness.js        # bar script against a fake DOM
```

`check.py` covers ASCII and LF endings, the top bar markup and order, menu classes, the theme table and the default token blocks, the inline scripts, the index shell and its glyphs, grid geometry, split rows, up to two side cards and their dashes, text budgets, the page validator, SKILL.md, the style manual, the changelog, README links and images, node syntax, and the harness itself. It reads files relative to the repository root, so any working directory is fine.

`harness.js` reads the two inline scripts from `agent-skill/demo.html`, loads them into a small fake DOM and checks the initial mode, OS preference following, menu rows, theme picking, per-mode memory, print tokens, the switch thumb reset, and the theme state written into and read from page links. It needs no other file, so a fresh clone can run it alone. `check.py` runs it automatically, so a separate call is only needed when debugging the bar.

`testing-tools/validate.py` is the page validator. It is a maintainer tool and does not ship with the payload. `check.py` runs it on the demo page, requires a clean exit, then breaks a card position and requires a failure.

Artifacts, if any, go to `testing-tools/.artifacts`, which is ignored by git. Both tool files are required to be ASCII with LF endings.

The checker asserts that `docs/index.html` is byte-identical to `agent-skill/demo.html` and that the `:root` and dark token blocks match the first theme of each mode, so a theme or default change means updating the table, the blocks, the README name lists, and the `DARK` and `LIGHT` lists in both tool files.
