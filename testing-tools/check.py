import json, os, re, shutil, subprocess, sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

VERBOSE = "-v" in sys.argv
fails = []
count = 0


def check(ok, label):
    global count
    count += 1
    if not ok:
        fails.append(label)
        print("FAIL " + label)
    elif VERBOSE:
        print("PASS " + label)


def read(name):
    return open(name, "rb").read()


def text(name):
    return read(name).decode("ascii")


def hexes(s):
    return {m.lower() for m in re.findall(r"#[0-9a-fA-F]{6}\b", s)}


def one_hex(css, name):
    m = re.search(r"--" + re.escape(name) + r"\s*:\s*(#[0-9a-fA-F]{6})", css)
    return m.group(1).lower() if m else None


files = ["README.md", "agent-skill/SKILL.md", "agent-skill/template.html",
         "agent-skill/demo.html", "agent-skill/index.html", "docs/index.html",
         "docs/demo.html", "docs/SKILL.html", "docs/color-vision-audit.html",
         "docs/context-performance-report.html", "docs/color-vision-audit-comparison.html",
         "docs/embed-sample.html",
         "CHANGELOG.md", "LICENSE",
         "agent-skill/style-manual.md", "testing-tools/check.py", "testing-tools/validate.py",
         "testing-tools/harness.js", "testing-tools/README.md"]
for f in files:
    b = read(f)
    check(all(x <= 126 and (x >= 32 or x in (9, 10)) for x in b), f + " ascii")
    check(b"\r" not in b, f + " lf only")

check(not os.path.exists("agent-skill/palettes.html"), "palette sheet removed")

demo = text("agent-skill/demo.html")
tpl = text("agent-skill/template.html")
idx = text("agent-skill/index.html")
skill = text("agent-skill/SKILL.md")
man = text("agent-skill/style-manual.md")
cl = text("CHANGELOG.md")
rd = text("README.md")
pages = text("docs/demo.html")

# Page structure
check(demo.count("<h1") == 1, "demo one h1")
check(demo.count('<p class="sub">') == 1, "demo one sub")
check(demo.count("<footer") == 1, "demo one footer")
check(pages == demo, "pages demo matches demo")
check(re.search(r'<html[^>]*data-theme="light"[^>]*data-print="off"', demo[:200]),
      "demo initial state attributes")
check(len(re.findall(r"<section>", demo)) == 1, "demo one bare section")
check(not re.search(r"<section[^>]+>", demo), "no section attributes")
check('<span class="meta">' not in demo, "no palette meta labels")

# Top bar markup
tb_m = re.search(r'<div id="tb".*?\n</div>', demo, re.S)
tb = tb_m.group(0) if tb_m else ""
check(bool(tb), "demo top bar")
order = [tb.find(x) for x in ('id="print"', 'id="mode"', 'id="dark-theme"', 'id="light-theme"',
                              'id="brightness"', 'id="saturation"')]
check(all(v >= 0 for v in order) and order == sorted(order),
      "bar order print, mode, dark, light, brightness, saturation")
check(re.search(r'<button class="tb-btn" id="print"[^>]*aria-pressed="false"', tb) is not None,
      "print control")
check(re.search(r'<button class="toggle on" id="mode"[^>]*role="switch"[^>]*aria-checked="true"', tb) is not None,
      "mode switch")
check(re.search(r'<button class="tb-btn fold" id="dark-theme"[^>]*aria-expanded="false"'
                r'[^>]*aria-haspopup="true"[^>]*aria-controls="dark-menu"', tb) is not None,
      "dark theme foldout button")
check(re.search(r'<button class="tb-btn fold" id="light-theme"[^>]*aria-expanded="false"'
                r'[^>]*aria-haspopup="true"[^>]*aria-controls="light-menu"', tb) is not None,
      "light theme foldout button")
check(re.search(r'<div class="menu" id="dark-menu" role="menu" aria-label="Dark theme"></div>', tb) is not None,
      "dark menu empty shell")
check(re.search(r'<div class="menu" id="light-menu" role="menu" aria-label="Light theme"></div>', tb) is not None,
      "light menu empty shell")
for bid in ("print", "mode"):
    m = re.search(r'<button[^>]*id="%s"[^>]*>' % bid, tb)
    tag = m.group(0) if m else ""
    check('aria-label="' in tag and 'title="' in tag, "bar label " + bid)
for bid in ("dark-theme", "light-theme"):
    m = re.search(r'<button[^>]*id="%s"[^>]*>' % bid, tb)
    tag = m.group(0) if m else ""
    check('title="' in tag, "bar title " + bid)
check(tb.count("<svg") == 5 and len(re.findall(r'<svg[^>]*aria-hidden="true"', tb)) == 5,
      "bar five icons")
check(">dark theme</button>" in tb and ">light theme</button>" in tb, "theme button text")
theme_btns = re.findall(r'<button class="tb-btn fold".*?</button>', tb, re.S)
check(len(theme_btns) == 2 and all("<svg" not in b for b in theme_btns), "no icons in theme buttons")
check(re.sub(r"<[^>]+>", "", tb).split() == ["print", "friendly", "dark", "theme", "light", "theme", "0", "0"],
      "bar visible text")
for sid in ("brightness", "saturation"):
    m = re.search(r'<input[^>]*id="%s"[^>]*>' % sid, tb)
    tag = m.group(0) if m else ""
    check('type="range"' in tag and 'min="-3"' in tag and 'max="3"' in tag
          and 'step="1"' in tag and 'value="0"' in tag and 'aria-label="' in tag,
          "slider " + sid)
check(tb.find('id="light-theme"') < tb.find('id="brightness"'), "sliders right of the theme buttons")
check(tb.count('class="sl"') == 2 and tb.count('class="v"') == 2, "two sliders with readouts")

# Bar and menu CSS
check(re.search(r"#tb\s*\{[^}]*position:\s*fixed", demo) is not None, "bar fixed")
check(re.search(r"#tb\s*\{[^}]*height:\s*24px", demo) is not None, "bar 24 px")
check(re.search(r"#tb\s*\{[^}]*justify-content:\s*flex-end", demo) is not None, "bar right aligned")
check(re.search(r"#tb\s*\{[^}]*font:\s*10px/1", demo) is not None, "bar 10 px font")
check(re.search(r"#tb\s*\{[^}]*background:\s*var\(--page-bg\)", demo) is not None,
      "bar page background")
tb_css = re.search(r"#tb\s*\{.*?\}", demo, re.S).group(0)
check("border-bottom" not in tb_css, "bar no divider")
check(re.search(r"#tb\s*\{[^}]*padding:\s*0 28px", demo) is not None, "bar inset")
check(re.search(r"\.tb-btn\s*\{[^}]*height:\s*18px", demo) is not None
      and re.search(r"\.tb-btn\s*\{[^}]*padding:\s*0 6px", demo) is not None
      and re.search(r"\.tb-btn\s*\{[^}]*gap:\s*4px", demo) is not None, "bar button size")
check(re.search(r"\.tb-btn\.fold\s*\{\s*min-width:\s*68px;\s*\}", demo) is not None,
      "theme buttons equal width")
check(re.search(r"\.tb-btn\.fold::after\s*\{[^}]*border-top:\s*4px solid currentColor", demo)
      is not None, "theme button caret")
check(re.search(r"\.menu\s*\{[^}]*position:\s*absolute", demo) is not None, "menu overlay")
check(re.search(r"\.menu\s*\{[^}]*top:\s*21px", demo) is not None, "menu below bar")
check(re.search(r"\.menu\.open\s*\{\s*display:\s*flex;\s*\}", demo) is not None, "menu open state")
check(re.search(r'\.menu button\[aria-checked="true"\]\s*\{[^}]*background:\s*var\(--accent\)', demo)
      is not None, "menu selected uses accent")
check(re.search(r"\.toggle\s*\{[^}]*width:\s*44px;[^}]*height:\s*20px", demo) is not None,
      "mode switch 44 x 20")
check(re.search(r"\.toggle-thumb\s*\{[^}]*width:\s*16px;[^}]*height:\s*16px", demo) is not None,
      "mode thumb 16 x 16")
check(".toggle .ico-l { left: 7px;" in demo and ".toggle .ico-r { right: 8px;" in demo,
      "switch icons centered")
check(re.search(r"\.sl input\[type=range\]\s*\{[^}]*width:\s*48px", demo) is not None,
      "slider 48 px track")
check(re.search(r"\.sl input\[type=range\]::-webkit-slider-thumb\s*\{[^}]*width:\s*10px", demo) is not None,
      "slider 10 px thumb")
check(".tb-btn.on { background: var(--tb-ink); color: var(--page-bg);" in demo, "print active fill")
check(not re.search(r'<svg\b[^>]*\s(?:width|height)="', demo), "no fixed svg size")
check(re.search(r"h2\s*\{[^}]*background:\s*transparent;[^}]*color:\s*var\(--page-ink\);[^}]*border:\s*2px solid var\(--accent\)", demo)
      is not None, "pill is transparent with a 2px accent outline")

# Print rules: one palette in :root, aliased by @media print and by the bar script.
ps = demo.find("@media print {")
pe = demo.find("</style>", ps)
pblock = demo[ps:pe] if ps >= 0 and pe > ps else ""
check("#tb { display: none; }" in pblock, "print hides bar")
check("@page { margin: 12mm; }" in pblock, "print page margin")
check("break-inside: avoid" in pblock, "print break rule")
check("print-color-adjust: exact" in pblock, "print color adjust")
check("color-scheme: light !important;" in pblock, "print color scheme")
check(demo.count("--print-bg: #FFFFFF;") == 1 and demo.count("--print-ink: #000000;") == 1
      and demo.count("--print-muted: #333333;") == 1 and demo.count("--print-line: #9A9A9A;") == 1,
      "one print palette")
check("--page-bg: var(--print-bg) !important;" in pblock
      and "--page-ink: var(--print-ink) !important;" in pblock
      and "--accent: var(--print-ink) !important;" in pblock, "print tokens alias the palette")
check(not re.search(r"#[0-9a-fA-F]{3,6}", pblock), "print block has no literal colors")
check("body { background: var(--page-bg) !important; color: var(--page-ink) !important; }" in pblock,
      "print white page")
check("h2 { background: transparent !important" not in pblock, "print pill uses the base outline")
check(".loop { stroke: var(--muted); stroke-width: 1.6; fill: none; stroke-dasharray: 0.1 6; stroke-linecap: round; }" in demo,
      "loop line style")
check('html[data-print="on"] h2 {' not in demo, "no per-state pill override")
check(".card, .tag { fill: var(--card) !important; stroke: var(--line) !important; }" in pblock,
      "print card fill")
check(".t { fill: var(--ink) !important; }" in pblock, "print title ink")
check(".d, .cap, .side { fill: var(--muted) !important; }" in pblock, "print muted ink")
check(".arrow-a { stroke: var(--accent) !important; }" in pblock, "print accent arrow")
check(".arrow, .dash, .loop { stroke: var(--muted) !important; }" in pblock, "print loop stroke")

# Theme table
scripts = re.findall(r"<script>(.*?)</script>", demo, re.S)
check(len(scripts) == 2, "two inline scripts")
script = scripts[1] if len(scripts) == 2 else ""
i = script.find("var THEMES")
start = script.find("{", i)
depth = 0
end = -1
for pos in range(start, len(script)):
    if script[pos] == "{":
        depth += 1
    elif script[pos] == "}":
        depth -= 1
        if depth == 0:
            end = pos + 1
            break
raw = script[start:end] if i >= 0 and end > 0 else ""
check(bool(raw), "theme table present")
themes = {}
if raw:
    j = re.sub(r"(?<=[{,\s])([a-z][a-z0-9]*)\s*:", r'"\1":', raw).replace("'", '"')
    try:
        themes = json.loads(j)
    except Exception:
        themes = {}
check(set(themes) == {"dark", "light"}, "theme table has two modes")
DARK = ["github", "harbor", "solarized", "oledblack", "ayu"]
LIGHT = ["vercel", "tokyonight", "cursor", "orng"]
check(list(themes.get("dark", {})) == DARK, "five dark themes in order")
check(list(themes.get("light", {})) == LIGHT, "four light themes in order")
for mode in ("dark", "light"):
    for name, t in themes.get(mode, {}).items():
        check(sorted(t) == ["accent", "bg", "card", "ink", "line", "muted"],
              "%s %s six tokens" % (mode, name))
        check(all(re.match(r"^#[0-9A-F]{6}$", v) for v in t.values()),
              "%s %s uppercase hex" % (mode, name))

# Default token blocks match the first theme of each mode
root_css = re.search(r":root\s*\{(.*?)\}", demo, re.S).group(1)
dark_css = re.search(r'html\[data-theme="dark"\]\s*\{(.*?)\}', demo, re.S).group(1)
cur = themes.get("light", {}).get("vercel", {})
ayu = themes.get("dark", {}).get("github", {})
for key, var in (("bg", "page-bg"), ("card", "card"), ("ink", "ink"),
                 ("muted", "muted"), ("line", "line"), ("accent", "accent")):
    check(one_hex(root_css, var) == cur.get(key, "").lower(), "vercel default " + var)
    check(one_hex(dark_css, var) == ayu.get(key, "").lower(), "github default " + var)
check("--mint" not in demo and "--page-mint" not in demo, "no mint token")
check(".diagram" not in demo, "no per-section palette class")
check(not re.search(r'\.d\d\s*\{', demo), "no palette slot rules")

# Scripts and assets
check(not re.search(r'<script[^>]+src=|<link\b|@import|https?://', demo), "no external assets")
check("localStorage" not in demo and "sessionStorage" not in demo, "no storage")
check("setAttribute('data-theme'" in scripts[0], "head sets theme")
for fn in ("function applyTheme", "function applyPrint", "function buildMenu",
           "function syncMenus", "function closeMenus", "function inkOn",
           "function adjustHex", "function syncSliders", "function stepOf",
           "function setMode", "function setPrint"):
    check(fn in script, "bar script has " + fn[9:])
check("--pick-ink" in script and "inkOn(accent)" in script, "menu pick ink derived")
check("0.179" in script, "pill ink contrast threshold")
check("parseInt(el.value, 10)" in script and "Math.max(-3, Math.min(3" in script,
      "slider steps clamped")
check("b * 0.08" in script and "s * 0.15" in script, "slider step factors")
check(script.count("addEventListener('input'") == 2, "both sliders wired")
check(script.count("syncSliders();") == 3, "sliders synced on load and on input")
check("'--thumb': THUMB[mode].bg, '--thumb-line': THUMB[mode].line" in script,
      "theme sets switch thumb per mode")
check(script.count("'#2E2E2E'") == 1 and script.count("'#CBCBCB'") == 1,
      "one switch thumb pair per mode")
check("function menuKey" in script and "ArrowDown" in script and "Home" in script,
      "menu arrow keys")
check("prefers-reduced-motion" in demo, "reduced motion rule")
check("outline-offset: 1px" in demo, "focus ring inside the viewport")
check('html[data-print="on"] { color-scheme: light; }' in demo, "print mode light color scheme")
check("menuitemradio" in script, "menu rows are menuitemradio")
check("prefers-color-scheme" in scripts[0] and "prefers-color-scheme" in script, "os preference read")
check("if (!manual)" in script, "os follow until manual")
check("setMode(savedMode" in script, "print restores saved mode")

# Template
check(tpl.count("<h1") == 1 and tpl.count('<p class="sub">') == 1 and tpl.count("<footer") == 1,
      "template page copy slots")
check("<section" not in tpl and tpl.count("<svg") == 5, "template no diagrams")
check("Diagram slot:" in tpl, "template diagram slot")
check(re.search(r'<div id="tb".*?\n</div>', tpl, re.S).group(0) == tb,
      "template bar matches demo")
check(re.findall(r"<script>(.*?)</script>", tpl, re.S) == scripts, "template scripts match demo")
check(re.search(r"<style>(.*?)</style>", tpl, re.S).group(1)
      == re.search(r"<style>(.*?)</style>", demo, re.S).group(1), "template styles match demo")
check(not re.search(r'<script[^>]+src=|<link\b|@import|https?://', tpl), "template no external assets")

# Index shell: same bar, tokens and scripts, plus link cards and a documents table.
istyles = re.findall(r"<style>(.*?)</style>", idx, re.S)
check(len(istyles) == 2, "index two style blocks")
check(bool(istyles) and istyles[0] == re.search(r"<style>(.*?)</style>", demo, re.S).group(1),
      "index shared style matches demo")
check(len(istyles) == 2 and all(k in istyles[1] for k in (".grid {", ".entry {", ".glyph {", ".docs {")),
      "index grid, entry, glyph and docs styles")
check(re.search(r'<div id="tb".*?\n</div>', idx, re.S).group(0) == tb,
      "index bar matches demo")
check(re.findall(r"<script>(.*?)</script>", idx, re.S) == scripts, "index scripts match demo")
check(idx.count("<h1") == 1 and idx.count('<p class="sub">') == 1 and idx.count("<footer") == 1,
      "index page copy slots")
check("Index copy:" in idx and "Entry:" in idx and "Documents:" in idx, "index marked slots")
check(idx.count('<nav class="grid" aria-label="group label">') == 1, "index one example group")
check(idx.count('class="entry"') == 1 and idx.count('class="glyph"') == 1, "index one example entry")
check(idx.count('class="hot"') == 1, "index one accent glyph path")
check('href="first-page.html"' in idx and 'href="notes.md"' in idx, "index example links")
check(idx.count("<section") == 1 and 'aria-labelledby="documents"' in idx, "index documents section")
check(idx.count('class="docs"') == 1 and ">Document<" in idx and ">Covers<" in idx,
      "index documents table")
check("localStorage" not in idx and "sessionStorage" not in idx, "index no storage")
check(not hexes(idx.split("<body>")[1].split("</main>")[0]), "no hex colors in index body markup")
glyph = re.search(r'<svg class="glyph".*?</svg>', idx, re.S)
check(glyph is not None, "index glyph present")
if glyph:
    try:
        ET.fromstring(glyph.group(0))
        check(True, "index glyph parses")
    except Exception:
        check(False, "index glyph parses")
check(not re.search(r'<script[^>]+src=|<link\b|@import|https?://', idx), "index no external assets")
for fn in ("function readParams", "function pickQuery", "function syncLinks"):
    check(fn in script, "bar script has " + fn[9:])
check("window.location.search" in script and "/[?&]mode=(dark|light)\\b/" in scripts[0],
      "mode read from the link before paint")
check(script.index("var startMode = readParams();") < script.index("buildMenu('dark-menu'"),
      "params read before the menus are built")
check("'?mode=' + (isDark() ? 'dark' : 'light')" in script
      and "'&dark=' + chosen.dark" in script and "'&light=' + chosen.light" in script,
      "link query carries mode and both picks")
check("syncLinks();" in script, "theme change rewrites the links")

# Pages index: the filled index shell served from docs.
live = text("docs/index.html")
lstyle = re.findall(r"<style>(.*?)</style>", live, re.S)
check(len(lstyle) == 2 and lstyle == istyles, "pages index styles match shell")
check(re.findall(r"<script>(.*?)</script>", live, re.S) == scripts, "pages index scripts match shell")
check(live.count("<h1") == 1 and live.count('<p class="sub">') == 0 and live.count("<footer") == 1,
      "pages index copy without subtitle")
check('href="demo.html"' in live and 'href="embed-sample.html"' in live
      and 'src="demo.html"' in text("docs/embed-sample.html"),
      "pages index page links")
for doc in ("SKILL.html", "color-vision-audit.html", "context-performance-report.html"):
    check('href="%s"' % doc in live, "pages index document " + doc)
check(live.count('<nav class="grid" aria-label="sample pages">') == 1
      and live.count('<nav class="grid" aria-label="documents"') == 1, "pages index two groups")
check(live.count('class="entry"') == 3 and live.count('class="glyph"') == 3, "pages index three entries")
check(live.count('class="hot"') == 3, "pages index three accent glyph paths")
check(live.count('class="docs"') == 1 and ">Document<" in live and ">Covers<" in live,
      "pages index documents table")
check("localStorage" not in live and "sessionStorage" not in live, "pages index no storage")
check(not hexes(live.split("<body>")[1].split("</main>")[0]), "pages index no hex colors in body")
check(not re.search(r'<script[^>]+src=|<link\b|@import|https?://', live),
      "pages index no external assets")
for n, s in enumerate(re.findall(r'<svg class="glyph".*?</svg>', live, re.S)):
    try:
        ET.fromstring(s)
        check(True, "pages index glyph %d parses" % n)
    except Exception:
        check(False, "pages index glyph %d parses" % n)

# The two sample pages in docs carry the same shell as the templates.
samp = text("docs/sample-one-diagram.html")
sstyle = re.findall(r"<style>(.*?)</style>", samp, re.S)
check(len(sstyle) == 1
      and sstyle[0] == re.search(r"<style>(.*?)</style>", demo, re.S).group(1),
      "sample page style matches shell")
check(re.findall(r"<script>(.*?)</script>", samp, re.S) == scripts, "sample page scripts match shell")
check(re.search(r'<div id="tb".*?\n</div>', samp, re.S).group(0) == tb,
      "sample page bar matches shell")
check(samp.count("<h1") == 1 and samp.count("<footer") == 1, "sample page structure")

# SVGs, markers, geometry, budgets
svgs = re.findall(r"<svg\b.*?</svg>", demo, re.S)
check(len(svgs) == 6, "demo six inline svgs")
for n, s in enumerate(svgs):
    try:
        ET.fromstring(s)
        ok = True
    except Exception:
        ok = False
    check(ok, "svg %d parses" % n)
sections = [s for s in re.findall(r"<section>(.*?)</section>", demo, re.S)]
ids = re.findall(r'<marker id="([^"]+)"', demo)
check(len(ids) == 2 and len(set(ids)) == 2, "two unique marker ids")
check(set(re.findall(r"url\(#([^)]+)\)", demo)) <= set(ids), "marker refs resolve")
check(not hexes(re.sub(r"<script>.*?</script>", "", demo.split("<body>")[1].split("<footer>")[0])),
      "no hex colors in body markup")

split_seen = False
for n, body in enumerate(sections):
    tag = "d%d" % (n + 1)
    m = re.search(r"<svg\b.*?</svg>", body, re.S)
    if not m:
        check(False, tag + " svg present")
        continue
    root = ET.fromstring(m.group(0))
    rects = root.findall("rect")
    mains = [r for r in rects if r.get("class") in ("card", "focus")
             and r.get("x") in ("300", "548")]
    focus = [r for r in mains if r.get("class") == "focus"]
    check(len(mains) >= 2, tag + " main cards")
    check(len(focus) == 1, tag + " one focus")

    rows = {}
    for r in mains:
        x, y, w = int(r.get("x")), int(r.get("y")), int(r.get("width"))
        rows.setdefault(y, []).append((x, w))
    check(all(int(r.get("height")) == 70 for r in mains), tag + " card height")
    check(all((x, w) in ((300, 470), (300, 222), (548, 222)) for y, cells in rows.items()
              for x, w in cells), tag + " card geometry")
    ys = sorted(rows)
    check(ys == [30 + 108 * i for i in range(len(ys))], tag + " card pitch")
    shapes = []
    for y in ys:
        cells = sorted(rows[y])
        shapes.append(len(cells))
        check(cells in ([(300, 470)], [(300, 222), (548, 222)]),
              tag + " row shape at %d" % y)
    if 2 in shapes:
        split_seen = True

    tags = [r for r in rects if r.get("class") == "tag"]
    tag_y = int(tags[0].get("y")) if tags else -1
    check(len(tags) == 1 and tags[0].get("x") == "300" and tags[0].get("width") == "470"
          and tags[0].get("height") == "26", tag + " tag size")
    check(tag_y == ys[-1] + 98, tag + " tag position")
    check(root.get("viewBox") == "0 0 1040 %d" % (tag_y + 32), tag + " viewBox height")

    sides = [r for r in rects if r.get("class") == "card"
             and r.get("x") not in ("300", "548")]
    check(len(sides) <= 2, tag + " at most two side cards")
    check(len({r.get("x") for r in sides}) == len(sides), tag + " one side card per side")
    for r in sides:
        x, w, h = r.get("x"), r.get("width"), r.get("height")
        check(x in ("40", "800") and ((x == "40" and w == "210") or (x == "800" and w == "220"))
              and h in ("70", "90", "100"), tag + " side card size")
        check(int(r.get("y")) in ys, tag + " side card row")

    # One arrow per boundary, two when either row is split.
    want_arrow, want_cap = [], []
    for i in range(len(ys) - 1):
        split = 2 in (shapes[i], shapes[i + 1])
        for x in ((411, 659) if split else (535,)):
            want_arrow.append((x, x, ys[i] + 70, ys[i] + 98))
        for x in ((425, 673) if split else (549,)):
            want_cap.append((x, ys[i] + 88))

    lines = [l for l in root.findall("line") if l.get("class") in ("arrow", "arrow-a")]
    got = sorted((int(l.get("x1")), int(l.get("x2")), int(l.get("y1")), int(l.get("y2")))
                 for l in lines)
    check(got == sorted(want_arrow), tag + " arrow geometry")
    accents = [l for l in lines if l.get("class") == "arrow-a"]
    check(len(accents) <= 2, tag + " accent connectors")

    fills = {}
    for mk in root.findall(".//marker"):
        p = mk.find("path")
        fills[mk.get("id")] = p.get("fill") if p is not None else None
    check(len(fills) == 2 and len(set(fills.values())) == 2, tag + " two marker fills")
    for l in lines:
        ref = re.search(r"url\(#([^)]+)\)", l.get("marker-end") or "")
        want = "var(--accent)" if l.get("class") == "arrow-a" else "var(--muted)"
        check(ref is not None and fills.get(ref.group(1)) == want, tag + " marker pair")

    dashes = [p for p in root.findall("path") if p.get("class") == "dash"]
    check(len(sides) <= len(dashes) <= 2 * len(sides), tag + " one or two dashes per side card")

    texts = root.findall("text")
    caps = [t for t in texts if t.get("class") == "cap"]
    check(sorted((int(t.get("x")), int(t.get("y"))) for t in caps) == sorted(want_cap),
          tag + " captions at the arrow rows")

    desc = {}
    for r in mains + sides:
        x, y = int(r.get("x")), int(r.get("y"))
        w, h = int(r.get("width")), int(r.get("height"))
        pad = 16 if w in (210, 220) else 18
        lim = {470: 65, 210: 26, 220: 28, 222: 28}[w]
        for dy in (44, 59) + ((74,) if h >= 90 else ()):
            desc[(x + pad, y + dy)] = lim

    for t in texts:
        s = t.text or ""
        c = t.get("class")
        if c == "t":
            check(len(s) <= 24, tag + " title budget " + repr(s))
        elif c == "d":
            x, y = t.get("x"), t.get("y")
            lim = desc.get((int(x), int(y))) if x and y else None
            check(lim is not None and len(s) <= lim, tag + " desc budget " + repr(s))
        elif c == "cap":
            lim = {"549": 42, "425": 18, "673": 18}.get(t.get("x"))
            check(lim is not None and len(s) <= lim, tag + " caption budget " + repr(s))
        elif c == "side":
            if int(t.get("y")) == tag_y + 17:
                check(len(s) <= 78, tag + " tag budget " + repr(s))
            else:
                check(len(s) <= 28, tag + " branch label budget " + repr(s))

check(split_seen, "demo split row")

# Skill
lines = skill.split("\n")
check(lines[0] == "---", "skill frontmatter open")
try:
    fm_end = lines.index("---", 1)
except ValueError:
    fm_end = -1
check(fm_end > 1, "skill frontmatter close")
fields = [l.split(":", 1)[0] for l in lines[1:fm_end] if l and not l.startswith(" ")]
check(fields == ["name", "description", "license"], "skill three fields")
check(lines[1].startswith("name: simpleflow"), "skill name")
desc_m = re.search(r'description:\s*"(.*)"', skill)
check(desc_m is not None and 1 <= len(desc_m.group(1)) <= 1024, "skill description length")
check(desc_m is not None and "repeatability" in desc_m.group(1), "skill description goal")
for link in re.findall(r"\]\(([^)]+)\)", skill):
    check(os.path.isfile(os.path.join("agent-skill", link)), "skill link " + link)
check("demo.html" in skill and "template.html" in skill and "style-manual.md" in skill
      and "index.html" in skill, "skill file map")
check("palettes.html" not in skill, "skill no palette sheet")
low = skill.lower()
check("the same result every run" in low and "small written part" in low and "one pass" in low,
      "skill goals")
check("## Goals" in skill, "skill goals section")
check("no external javascript" in low and "no javascript" not in low, "skill script rule")
check("five dark names and four light names" in low, "skill theme count")
check("print toggle labelled `print friendly`" in low, "skill print label")
check("dark theme` and `light theme` foldouts" in low or "`dark theme` and `light theme`" in low,
      "skill foldout labels")
check("sections carry no class" in low, "skill no section colors")
check("print theme" in low, "skill print mention")
check("head with h2 pill" in low, "skill section head")
check("ascii only" in low, "skill ascii rule")
check("diagram body in manual section 10" in low, "skill diagram body")
check("fill the copy in two edits" in low and "do not edit one section at a time" in low
      and "do not rewrite the whole page" in low, "skill two-edit rule")
check("## Page types" in skill, "skill page types")
check("manual section 14" in skill and "index.html" in skill and "iframe" in skill,
      "skill index chapter and embed")
check("no screenshots" in low and "no pdf" in low, "skill no render pass")
check("by reading" in low and "do not write a checker script" in low, "skill step 7 names the read method")
check("count, grep, diff or hash" in low and "count, grep, diff or hash" in man.lower()
      and "a check is a read, not a measurement" in low, "skill and manual ban command checks")
check("arrows and captions" in low and man.lower().count("arrows and captions") >= 2
      and "one arrow at x=535" in man.lower(), "skill and manual cover arrows and captions")
check("a merge back into" in low and "keeps the same pair" in man.lower()
      and "a merge back into one 470 card keeps the 411 and 659 pair" in man.lower(),
      "skill and manual allow a merge")
check("write three characters under each limit" in low
      and "every line is written three characters under its budget" in man.lower(),
      "skill and manual keep a budget margin")
check("one repair edit" in low and "one repair edit" in man.lower()
      and "named in the reply to the user" in man.lower(), "skill and manual cap repairs")
check(all(k in man for k in ("LF endings", "rx 3", "one title per card", "title 24 on every card",
                             "arrow-a", "four segments and upward", "prefixed by section")),
      "manual checklist covers the validator rules")
check("both modes" not in low, "skill no per-page mode pass")

# Manual
check("## 3. Theme" in man, "manual theme section")
check("## 10. Diagram body" in man, "manual diagram body")
check("Loopback, a later card feeding an earlier one" in man, "manual loopback pattern")
check("226, 206, 186, 166" in man and "824, 844, 864, 884" in man, "manual loop lanes")
check("Split row, a decision card forking into two cards on the next row" in man,
      "manual split pattern")
check("411 and 659" in man, "manual split arrows")
check("425 and 673" in man, "manual split captions")
check("| `hi` | top + 20 |" in man and "| `lo` | top + h - 20 |" in man, "manual side marks")
check("## 11. Validation" in man, "manual validation")
check("## 13. Toolbar and modes" in man, "manual toolbar section")
check("## 14. Index pages" in man and "### Embedding a page" in man, "manual index chapter")
check("copy `index.html` instead of `template.html`" in man, "manual index shell")
check('class="glyph"' in man and "104 x 56" in man, "manual glyph rules")
check("?mode=...&dark=...&light=..." in man, "manual index link query")
check("Two to six entries" in man, "manual index group size")
check("screenshots" in man.lower() and "pdfs" in man.lower(), "manual no render pass")
check("Switch light and dark" not in man, "manual no per-page theme pass")
check("both foldouts opened" not in man, "manual checklist no per-page render")
check("demo.html" in man and "template.html" in man, "manual file references")
check("Inline scripts limited" in man, "manual inline script rule")
check("one or more `<section>` blocks" in man, "manual section count")
check('<section class="diagram' not in man and "<section>\n  <div class=\"head\">" in man,
      "manual plain section body")
check("palette pair" not in man.lower(), "manual no palette pairs")
check("--mint" not in man and "P0" not in man, "manual no mint or P0")
check("transparent with a 2 px accent outline" in man, "manual pill outline")
check("auto width, 18 px high" in man, "manual print button size")
check("68 px minimum width" in man, "manual theme button size")
check("role=\"menu\"" in man and "menuitemradio" in man, "manual menu markup")
check("Escape closes the menu" in man, "manual escape close")
check("Each mode remembers its own theme" in man, "manual mode memory")
check("The agent does not pick, mix or author colors" in man, "manual color rule")
check("| `.meta` |" not in man, "manual no meta type")
check("70-high card: title" in man and "90/100-high side card" in man, "manual card baselines")
check(man.count("```") % 2 == 0, "manual fences balanced")
for name in DARK + LIGHT:
    if name != "vercel":
        check("`" + name + "`" in man, "manual names " + name)

# Page validator
check("800 px" not in man.lower() and "800 px" not in low, "no 800 px check")
check(not os.path.exists("agent-skill/validate.py"), "validator outside the payload")
check(sorted(os.listdir("agent-skill")) == ["SKILL.md", "demo.html", "index.html", "style-manual.md", "template.html"],
      "payload is five files")
check("validate.py" not in skill and "python" not in skill.lower(), "skill free of the validator")
check("validate.py" not in man and "python" not in man.lower(), "manual free of the validator")
r = subprocess.run([sys.executable, "testing-tools/validate.py", "agent-skill/demo.html",
                    "agent-skill/template.html"], capture_output=True, text=True)
check(r.returncode == 0, "validator passes on demo")
vm = re.search(r"checks: (\d+) failures: 0", r.stdout)
check(vm is not None and int(vm.group(1)) >= 200, "validator check count")
broken = "testing-tools/.artifacts/broken.html"
os.makedirs("testing-tools/.artifacts", exist_ok=True)
broken_src = re.sub(r'<rect class="focus" x="300" y="(\d+)"',
                    lambda m: '<rect class="focus" x="300" y="%d"' % (int(m.group(1)) + 4),
                    demo, count=1)
check(broken_src != demo, "off-grid probe built")
open(broken, "w", encoding="ascii", newline="\n").write(broken_src)
r = subprocess.run([sys.executable, "testing-tools/validate.py", broken, "agent-skill/template.html"],
                   capture_output=True, text=True)
check(r.returncode == 1 and "main row" in r.stdout, "validator catches an off-grid card")

# Changelog
versions = re.findall(r"^## (\d+\.\d+\.\d+)$", cl, re.M)
check(versions == ["1.6.0", "1.5.2", "1.5.1", "1.5.0", "1.4.0", "1.3.7", "1.3.6", "1.3.5", "1.3.4", "1.3.3", "1.3.2", "1.3.1", "1.3.0", "1.2.0", "1.1.0", "1.0.0", "0.7.0", "0.6.0", "0.5.0", "0.4.0", "0.3.0", "0.2.0", "0.1.0"],
      "changelog versions newest first")
check(not re.search(r"\b(19|20)\d\d\b", cl), "changelog no dates")
check(not re.search(r"\bv\d+\.\d+", cl), "changelog bare versions")
check("theme" in cl.lower() and "menu" in cl.lower(), "changelog theme wording")

# README
check("## Page controls" in rd, "readme page controls")
rimgs = [a or b for a, b in re.findall(r'!\[[^\]]*\]\(([^)]+)\)|<img[^>]+src="([^"]+)"', rd)]
check(len(rimgs) == 11 and all(os.path.isfile(x) for x in rimgs), "readme images")
check(rd.startswith('<img src="docs/top-toolbar.png"'), "readme opens with the toolbar strip")
check('<img src="docs/top-diagram.png" alt=' in rd.split('\n\n')[0], "readme diagram strip under the bar")
check(rd.count('width="280"') == 4, "readme sample thumbnails")
check(rd.count('width="400"') == 0, "readme closeups unscaled")
check("docs/bar-dark.png" in rd and "docs/bar-light.png" in rd
      and "docs/bar-print-friendly.png" in rd, "readme bar closeups")
check("docs/slider-dark.png" in rd and "docs/slider-light.png" in rd,
      "readme slider closeups")
check("docs/demo-dark.png" in rd and "docs/demo-github.png" in rd
      and "docs/demo-print-friendly.png" in rd, "readme demo states")
check(rd.count('href="https://chezhenkie.github.io/simpleflow-diagram-skill/"') == 4
      and "CLICK IMAGES TO GO TO GITHUB INDEX PAGE WITH SAMPLES AND DOCS" in rd,
      "readme thumbnails and caps link to the live index")
check("The project index is live at https://chezhenkie.github.io/simpleflow-diagram-skill/." in rd,
      "readme live index link")
check("CLICK HERE" not in rd and "<table>" not in rd, "readme no index box")
check("@simpleflow" in rd and "$simpleflow" in rd
      and rd.count("/skill:simpleflow") == 2, "readme skill invocations")
check("~/.agents/skills" in rd and "~/.pi/agent/skills" in rd
      and "~/.omp/agent/skills" in rd and ".opencode/skills" in rd, "readme agent install paths")
check("simpleflow-diagram-skill/agent-skill" in rd and "as `simpleflow`" in rd, "readme install copy")
check("Windows" not in rd and "PowerShell" not in rd and "%USERPROFILE%" not in rd,
      "readme no os specifics")
check("palettes.html" not in rd and "palette pair" not in rd, "readme no palette sheet")
check("dark theme" in rd and "light theme" in rd, "readme theme foldouts")
check("colour-vision impaired" in rd and "a few hundred tokens" in rd and "seven rows" in rd
      and "no extra setup" in rd and "instead of white text" in rd
      and "run, evaluate, compare, edit, repeat" in rd
      and "multiple sub-agent runs" in rd, "readme value bullets")
check("gathers several finished diagrams and documents onto one page" in rd
      and rd.count("- Optional index page:") == 1, "readme index bullet")
check("one of nine fixed themes" in rd and "nine installed themes" in rd, "readme theme count")
check("## Readability and colour vision" in rd
      and "color-vision-audit.html" in rd and "color-vision-audit-comparison.html" in rd
      and "two colour vision and readability documents" in rd,
      "readme colour vision section")
check("## Optional index page" in rd, "readme index section")
check("agent-skill/index.html" in rd, "readme index shell")
check("The skill is five files" in rd and "payload" not in rd, "readme five files")
check("keeps the theme" in rd, "readme theme carry")
check("no screenshots" in rd.lower() and "no pdfs" in rd.lower(), "readme no render pass")
check("a few hundred tokens" in rd, "readme token figure")
check("written part stays small" in man, "manual cost note")

# Script syntax and behavior
artifacts = os.path.join("testing-tools", ".artifacts")
shutil.rmtree(artifacts, ignore_errors=True)
os.makedirs(artifacts)
paths = []
for i, body in enumerate(scripts):
    p = os.path.join(artifacts, "s%d.js" % i)
    open(p, "w", encoding="ascii", newline="\n").write(body)
    paths.append(p)

node = shutil.which("node")
check(node is not None, "node available")
if node:
    for i, p in enumerate(paths):
        r = subprocess.run([node, "--check", p], capture_output=True, text=True)
        check(r.returncode == 0, "script %d syntax" % i)
        if r.returncode != 0:
            print(r.stderr.strip()[:300])
    r = subprocess.run([node, os.path.join("testing-tools", "harness.js")], capture_output=True, text=True)
    check(r.returncode == 0, "bar behavior harness")
    if r.returncode != 0:
        print(r.stdout.strip()[:800])

if not fails:
    shutil.rmtree(artifacts, ignore_errors=True)

print("checks:", count, "failures:", len(fails))
sys.exit(1 if fails else 0)
