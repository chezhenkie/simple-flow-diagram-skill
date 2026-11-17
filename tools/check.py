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
         "agent-skill/demo.html", "docs/index.html", "CHANGELOG.md", "LICENSE",
         "agent-skill/references/style-manual.md", "tools/check.py", "tools/harness.js"]
for f in files:
    b = read(f)
    check(all(x <= 126 and (x >= 32 or x in (9, 10)) for x in b), f + " ascii")
    check(b"\r" not in b, f + " lf only")

check(not os.path.exists("agent-skill/references/palettes.html"), "palette sheet removed")

demo = text("agent-skill/demo.html")
tpl = text("agent-skill/template.html")
skill = text("agent-skill/SKILL.md")
man = text("agent-skill/references/style-manual.md")
cl = text("CHANGELOG.md")
rd = text("README.md")
pages = text("docs/index.html")

# Page structure
check(demo.count("<h1") == 1, "demo one h1")
check(demo.count('<p class="sub">') == 1, "demo one sub")
check(demo.count("<footer") == 1, "demo one footer")
check(pages == demo, "pages demo matches demo")
check(re.search(r'<html[^>]*data-theme="light"[^>]*data-print="off"', demo[:200]),
      "demo initial state attributes")
check(len(re.findall(r"<section>", demo)) == 3, "demo three bare sections")
check(not re.search(r"<section[^>]+>", demo), "no section attributes")
check('<span class="meta">' not in demo, "no palette meta labels")

# Top bar markup
tb_m = re.search(r'<div id="tb".*?\n</div>', demo, re.S)
tb = tb_m.group(0) if tb_m else ""
check(bool(tb), "demo top bar")
order = [tb.find(x) for x in ('id="print"', 'id="mode"', 'id="dark-theme"', 'id="light-theme"')]
check(all(v >= 0 for v in order) and order == sorted(order), "bar order print, mode, dark, light")
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
check(tb.count("<svg") == 3 and len(re.findall(r'<svg[^>]*aria-hidden="true"', tb)) == 3,
      "bar three icons")
check(">dark theme</button>" in tb and ">light theme</button>" in tb, "theme button text")
theme_btns = re.findall(r'<button class="tb-btn fold".*?</button>', tb, re.S)
check(len(theme_btns) == 2 and all("<svg" not in b for b in theme_btns), "no icons in theme buttons")
check(re.sub(r"<[^>]+>", "", tb).split() == ["print", "friendly", "dark", "theme", "light", "theme"],
      "bar visible text")

# Bar and menu CSS
check(re.search(r"#tb\s*\{[^}]*position:\s*fixed", demo) is not None, "bar fixed")
check(re.search(r"#tb\s*\{[^}]*height:\s*24px", demo) is not None, "bar 24 px")
check(re.search(r"#tb\s*\{[^}]*justify-content:\s*flex-end", demo) is not None, "bar right aligned")
check(re.search(r"#tb\s*\{[^}]*font:\s*10px/1", demo) is not None, "bar 10 px font")
check(re.search(r"#tb\s*\{[^}]*background:\s*var\(--page-bg\)", demo) is not None,
      "bar page background")
tb_css = re.search(r"#tb\s*\{.*?\}", demo, re.S).group(0)
check("border-bottom" not in tb_css, "bar no divider")
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
check(".tb-btn.on { background: var(--tb-ink); color: var(--page-bg);" in demo, "print active fill")
check(not re.search(r'<svg\b[^>]*\s(?:width|height)="', demo), "no fixed svg size")
check(re.search(r"h2\s*\{[^}]*background:\s*var\(--accent\);[^}]*color:\s*var\(--pill-ink\)", demo)
      is not None, "pill uses accent and contrast ink")

# Print rules
ps = demo.find("@media print")
pe = demo.find("</style>", ps)
pblock = demo[ps:pe] if ps >= 0 and pe > ps else ""
check("#tb { display: none; }" in pblock, "print hides bar")
check("@page { margin: 12mm; }" in pblock, "print page margin")
check("break-inside: avoid" in pblock, "print break rule")
check("print-color-adjust: exact" in pblock, "print color adjust")
check("background: #ffffff !important" in pblock and "color: #000000 !important" in pblock,
      "print white page")
check("h2 { background: #e6e6e6 !important; color: #000000 !important; border-color: #000000 !important; }"
      in pblock, "print pill in media")
check('html[data-print="on"] h2 { background: #e6e6e6 !important; color: #000000 !important;'
      ' border-color: #000000 !important; }' in demo, "print toggle pill style")
check(".card, .tag { fill: #ffffff !important; stroke: #9a9a9a !important; }" in pblock,
      "print card fill")
check(".t { fill: #000000 !important; }" in pblock, "print title ink")
check(".d, .cap, .side { fill: #333333 !important; }" in pblock, "print muted ink")
check(".arrow-a { stroke: #000000 !important; }" in pblock, "print accent arrow")

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
DARK = ["ayu", "catppuccin", "github", "nightowl", "solarized", "vercel"]
LIGHT = ["cursor", "monokai", "orng", "synthwave84", "tokyonight", "vercel"]
check(list(themes.get("dark", {})) == DARK, "six dark themes in order")
check(list(themes.get("light", {})) == LIGHT, "six light themes in order")
for mode in ("dark", "light"):
    for name, t in themes.get(mode, {}).items():
        check(sorted(t) == ["accent", "bg", "card", "ink", "line", "muted"],
              "%s %s six tokens" % (mode, name))
        check(all(re.match(r"^#[0-9A-F]{6}$", v) for v in t.values()),
              "%s %s uppercase hex" % (mode, name))

# Default token blocks match the first theme of each mode
root_css = re.search(r":root\s*\{(.*?)\}", demo, re.S).group(1)
dark_css = re.search(r'html\[data-theme="dark"\]\s*\{(.*?)\}', demo, re.S).group(1)
cur = themes.get("light", {}).get("cursor", {})
ayu = themes.get("dark", {}).get("ayu", {})
for key, var in (("bg", "page-bg"), ("card", "card"), ("ink", "ink"),
                 ("muted", "muted"), ("line", "line"), ("accent", "accent")):
    check(one_hex(root_css, var) == cur.get(key, "").lower(), "cursor default " + var)
    check(one_hex(dark_css, var) == ayu.get(key, "").lower(), "ayu default " + var)
check("--mint" not in demo and "--page-mint" not in demo, "no mint token")
check(".diagram" not in demo, "no per-section palette class")
check(not re.search(r'\.d\d\s*\{', demo), "no palette slot rules")

# Scripts and assets
check(not re.search(r'<script[^>]+src=|<link\b|@import|https?://', demo), "no external assets")
check("localStorage" not in demo and "sessionStorage" not in demo, "no storage")
check("setAttribute('data-theme'" in scripts[0], "head sets theme")
for fn in ("function applyTheme", "function applyPrint", "function buildMenu",
           "function syncMenus", "function closeMenus", "function inkOn",
           "function setMode", "function setPrint"):
    check(fn in script, "bar script has " + fn[9:])
check("--pill-ink" in script and "inkOn(t.accent)" in script, "pill ink derived")
check("=== 'light' ? '#FFFFFF'" in script, "light pill ink white")
check("'--thumb': mode === 'dark' ? '#2E2E2E' : '#CBCBCB'" in script,
      "theme sets switch thumb per mode")
check("menuitemradio" in script, "menu rows are menuitemradio")
check("prefers-color-scheme" in scripts[0] and "prefers-color-scheme" in script, "os preference read")
check("if (!manual)" in script, "os follow until manual")
check("setMode(savedMode" in script, "print restores saved mode")

# Template
check(tpl.count("<h1") == 1 and tpl.count('<p class="sub">') == 1 and tpl.count("<footer") == 1,
      "template page copy slots")
check("<section" not in tpl and tpl.count("<svg") == 3, "template no diagrams")
check("Diagram slot:" in tpl, "template diagram slot")
check(re.search(r'<div id="tb".*?\n</div>', tpl, re.S).group(0) == tb,
      "template bar matches demo")
check(re.findall(r"<script>(.*?)</script>", tpl, re.S) == scripts, "template scripts match demo")
check(re.search(r"<style>(.*?)</style>", tpl, re.S).group(1)
      == re.search(r"<style>(.*?)</style>", demo, re.S).group(1), "template styles match demo")
check(not re.search(r'<script[^>]+src=|<link\b|@import|https?://', tpl), "template no external assets")

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
check(len(ids) == 6 and len(set(ids)) == 6, "six unique marker ids")
check(set(re.findall(r"url\(#([^)]+)\)", demo)) <= set(ids), "marker refs resolve")
check(not hexes(re.sub(r"<script>.*?</script>", "", demo.split("<body>")[1].split("<footer>")[0])),
      "no hex colors in body markup")

for n, body in enumerate(sections):
    tag = "d%d" % (n + 1)
    m = re.search(r"<svg\b.*?</svg>", body, re.S)
    if not m:
        check(False, tag + " svg present")
        continue
    root = ET.fromstring(m.group(0))
    rects = root.findall("rect")
    mains = [r for r in rects if r.get("class") in ("card", "focus") and r.get("x") == "300"]
    focus = [r for r in mains if r.get("class") == "focus"]
    check(len(mains) >= 2, tag + " main cards")
    check(len(focus) == 1, tag + " one focus")
    check(all(r.get("width") == "470" and r.get("height") == "70" for r in mains),
          tag + " main card size")
    ys = sorted(int(r.get("y")) for r in mains)
    check(ys == [30 + 108 * i for i in range(len(ys))], tag + " card pitch")
    tags = [r for r in rects if r.get("class") == "tag"]
    tag_y = int(tags[0].get("y")) if tags else -1
    check(len(tags) == 1 and tags[0].get("x") == "300" and tags[0].get("width") == "470"
          and tags[0].get("height") == "26", tag + " tag size")
    check(tag_y == ys[-1] + 98, tag + " tag position")
    check(root.get("viewBox") == "0 0 1040 %d" % (tag_y + 32), tag + " viewBox height")

    sides = [r for r in rects if r.get("class") == "card" and r.get("x") != "300"]
    check(len(sides) == 1, tag + " one side card")
    for r in sides:
        x, w, h = r.get("x"), r.get("width"), r.get("height")
        check(x in ("40", "800") and ((x == "40" and w == "210") or (x == "800" and w == "220"))
              and h in ("70", "90", "100"), tag + " side card size")
        check(int(r.get("y")) in ys, tag + " side card row")

    lines = [l for l in root.findall("line") if l.get("class") in ("arrow", "arrow-a")]
    expected = [(y + 70, y + 98) for y in ys[:-1]]
    check(sorted((int(l.get("y1")), int(l.get("y2"))) for l in lines) == expected,
          tag + " arrow geometry")
    check(all(l.get("x1") == "535" and l.get("x2") == "535" for l in lines),
          tag + " arrows on spine")
    accents = [l for l in lines if l.get("class") == "arrow-a"]
    check(1 <= len(accents) <= 2, tag + " accent connectors")

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
    check(len(dashes) == len(sides), tag + " dash per side card")

    texts = root.findall("text")
    caps = [t for t in texts if t.get("class") == "cap"]
    check(all(t.get("x") == "549" for t in caps), tag + " captions at x 549")
    check(sorted(int(t.get("y")) for t in caps) == [y + 88 for y in ys[:-1]], tag + " caption rows")

    for t in texts:
        s = t.text or ""
        c = t.get("class")
        if c == "t":
            check(len(s) <= 24, tag + " title budget " + repr(s))
        elif c == "d":
            lim = {"318": 65, "56": 26, "816": 28}.get(t.get("x"))
            check(lim is not None and len(s) <= lim, tag + " desc budget " + repr(s))
        elif c == "cap":
            check(len(s) <= 42, tag + " caption budget " + repr(s))
        elif c == "side":
            if int(t.get("y")) == tag_y + 17:
                check(len(s) <= 78, tag + " tag budget " + repr(s))
            else:
                check(len(s) <= 28, tag + " branch label budget " + repr(s))

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
check(lines[1].startswith("name: simple-flow-diagram-skill"), "skill name")
desc_m = re.search(r'description:\s*"(.*)"', skill)
check(desc_m is not None and 1 <= len(desc_m.group(1)) <= 1024, "skill description length")
check(desc_m is not None and "token efficiency" in desc_m.group(1), "skill description goal")
for link in re.findall(r"\]\(([^)]+)\)", skill):
    check(os.path.isfile(os.path.join("agent-skill", link)), "skill link " + link)
check("demo.html" in skill and "template.html" in skill and "references/style-manual.md" in skill,
      "skill file map")
check("palettes.html" not in skill, "skill no palette sheet")
low = skill.lower()
check("token efficiency" in low and "minimal token use" in low and "speed." in low,
      "skill goals")
check("## Goals" in skill, "skill goals section")
check("no external javascript" in low and "no javascript" not in low, "skill script rule")
check("six dark names and six light names" in low, "skill theme count")
check("print toggle labelled `print friendly`" in low, "skill print label")
check("dark theme` and `light theme` foldouts" in low or "`dark theme` and `light theme`" in low,
      "skill foldout labels")
check("sections carry no class" in low, "skill no section colors")
check("print theme" in low, "skill print mention")
check("head with h2 pill" in low, "skill section head")
check("ascii only" in low, "skill ascii rule")
check("diagram body in manual section 10" in low, "skill diagram body")

# Manual
check("## 3. Theme" in man, "manual theme section")
check("## 10. Diagram body" in man, "manual diagram body")
check("## 11. Validation" in man, "manual validation")
check("## 13. Top bar and modes" in man, "manual top bar section")
check("demo.html" in man and "template.html" in man, "manual file references")
check("Inline scripts limited" in man, "manual inline script rule")
check("one or more `<section>` blocks" in man, "manual section count")
check('<section class="diagram' not in man and "<section>\n  <div class=\"head\">" in man,
      "manual plain section body")
check("palette pair" not in man.lower(), "manual no palette pairs")
check("--mint" not in man and "P0" not in man, "manual no mint or P0")
check("`#e6e6e6` pill with black text and a black border" in man, "manual print pill")
check("auto width, 18 px high" in man, "manual print button size")
check("68 px minimum width" in man, "manual theme button size")
check("role=\"menu\"" in man and "menuitemradio" in man, "manual menu markup")
check("Escape closes a foldout" in man, "manual escape close")
check("Each mode remembers its own theme" in man, "manual mode memory")
check("The agent does not pick, mix or author colors" in man, "manual color rule")
check("| `.meta` |" not in man, "manual no meta type")
check("70-high side card" in man, "manual side baselines")
check(man.count("```") % 2 == 0, "manual fences balanced")
for name in DARK + LIGHT:
    if name != "vercel":
        check("`" + name + "`" in man, "manual names " + name)

# Changelog
versions = re.findall(r"^## (\d+\.\d+\.\d+)$", cl, re.M)
check(versions == ["0.6.0", "0.5.0", "0.4.0", "0.3.0", "0.2.0", "0.1.0"],
      "changelog versions newest first")
check(not re.search(r"\b(19|20)\d\d\b", cl), "changelog no dates")
check(not re.search(r"\bv\d+\.\d+", cl), "changelog bare versions")
check("theme" in cl.lower() and "foldout" in cl.lower(), "changelog theme wording")

# README
check("## Page controls" in rd, "readme page controls")
rimgs = [a or b for a, b in re.findall(r'!\[[^\]]*\]\(([^)]+)\)|<img[^>]+src="([^"]+)"', rd)]
check(len(rimgs) == 6 and all(os.path.isfile(x) for x in rimgs), "readme images")
check(rd.count('width="280"') == 3, "readme sample thumbnails")
check(rd.count('width="244"') == 3, "readme closeup sizes")
check("docs/bar-dark.png" in rd and "docs/bar-light.png" in rd
      and "docs/bar-print-friendly.png" in rd, "readme bar closeups")
check("docs/demo-dark.png" in rd and "docs/demo-print-friendly.png" in rd, "readme demo states")
check("https://chezhenkie.github.io/simple-flow-diagram-skill/" in rd, "readme live demo link")
check("<table>" in rd and "CLICK HERE TO OPEN THE LIVE, GITHUB-HOSTED DEMO PAGE" in rd,
      "readme live demo box")
check("@simple-flow-diagram-skill" in rd and "$simple-flow-diagram-skill" in rd
      and rd.count("/skill:simple-flow-diagram-skill") == 2, "readme skill invocations")
check("~/.agents/skills" in rd and "~/.pi/agent/skills" in rd
      and "~/.omp/agent/skills" in rd and ".opencode/skills" in rd, "readme agent install paths")
check("simple-flow-diagram-skill/agent-skill" in rd, "readme install payload")
check("Windows" not in rd and "PowerShell" not in rd and "%USERPROFILE%" not in rd,
      "readme no os specifics")
check("palettes.html" not in rd and "palette pair" not in rd, "readme no palette sheet")
check("dark theme" in rd and "light theme" in rd, "readme theme foldouts")
check("minimal token use" in rd.lower() and "## Cost and speed" in rd, "readme cost section")
check("a few hundred tokens" in rd, "readme token figure")
check("written part stays small" in man, "manual cost note")

# Script syntax and behavior
artifacts = os.path.join("tools", ".artifacts")
os.makedirs(artifacts, exist_ok=True)
for old in os.listdir(artifacts):
    if re.match(r"s\d\.js$", old):
        os.remove(os.path.join(artifacts, old))
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
    r = subprocess.run([node, os.path.join("tools", "harness.js")], capture_output=True, text=True)
    check(r.returncode == 0, "bar behavior harness")
    if r.returncode != 0:
        print(r.stdout.strip()[:800])

print("checks:", count, "failures:", len(fails))
sys.exit(1 if fails else 0)
