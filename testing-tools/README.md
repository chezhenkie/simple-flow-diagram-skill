# Testing tools

Three tools check the repository: a static checker, a toolbar test that runs the page script without a browser, and a page validator. Run them from the repository root or by absolute path.

```sh
python testing-tools/check.py        # 417 static checks, prints failures only
python testing-tools/check.py -v     # same run, prints every PASS line
node testing-tools/harness.js        # toolbar script against a fake page
```

`check.py` covers ASCII and LF endings, the toolbar markup and order, menu classes, the theme table and the default color blocks, the inline scripts, the index page and its glyphs, the filled pages index and its entries, grid geometry, split rows, up to two side cards and their dashes, text budgets, the page validator, SKILL.md, the style manual, the changelog, README links and images, node syntax, and the toolbar test. It reads files relative to the repository root, so any working directory is fine.

`harness.js` reads the two inline scripts from `agent-skill/demo.html`, runs them against a small fake DOM and checks the initial mode, OS preference following, menu rows, theme picking, per-mode memory, print colors, the switch thumb reset, the brightness and saturation adjustment with its clamping, and the theme state written into and read from page links. It needs no other file, so a fresh clone can run it alone. `check.py` runs it too, so a separate call is only needed when debugging the toolbar.

`testing-tools/validate.py` is the page validator. It stays in the repository and is not part of the installed skill. `check.py` runs it on the demo page and requires a clean exit, then moves a card off the grid and requires a failure.

The checker writes its probe files to `testing-tools/.artifacts` and removes the folder when the run is clean; a failed run keeps them for inspection. The folder is ignored by git. The tool files are ASCII with LF endings.

The checker asserts that `docs/demo.html` is byte-identical to `agent-skill/demo.html`, that `docs/index.html` is a filled copy of the index page with working links, and that the `:root` and dark color blocks match the first theme of each mode, so a theme or default change means updating the table, the blocks, the README name lists, and the `DARK` and `LIGHT` lists in both tool files.
