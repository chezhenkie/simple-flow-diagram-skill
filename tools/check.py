import os, re, shutil, subprocess, sys
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


def pal_tokens(css):
    return {k: v.lower() for k, v in re.findall(
        r"--(bg|card|ink|muted|line|accent)\s*:\s*(#[0-9a-fA-F]{6})", css)}


def one_hex(css, name):
    m = re.search(r"--" + re.escape(name) + r"\s*:\s*(#[0-9a-fA-F]{6})", css)
    return m.group(1).lower() if m else None


files = ["README.md", "agent-skill/SKILL.md", "agent-skill/template.html",
         "agent-skill/demo.html", "docs/index.html", "CHANGELOG.md", "LICENSE",
         "agent-skill/references/style-manual.md", "agent-skill/references/palettes.html",
         "tools/check.py", "tools/harness.js"]
for f in files:
    b = read(f)
    check(all(x <= 126 and (x >= 32 or x in (9, 10)) for x in b), f + " ascii")
    check(b"\r" not in b, f + " lf only")

demo = text("agent-skill/demo.html")
tpl = text("agent-skill/template.html")
skill = text("agent-skill/SKILL.md")
man = text("agent-skill/references/style-manual.md")
cl = text("CHANGELOG.md")
cat = text("agent-skill/references/palettes.html")
rd = text("README.md")

# Page structure
check(demo.count("<h1") == 1, "demo one h1")
check(demo.count('<p class="sub">') == 1, "demo one sub")
check(demo.count("<footer") == 1, "demo one footer")
check(text("docs/index.html") == demo, "pages demo matches demo")
check(re.search(r'<html[^>]*data-theme="light"[^>]*data-print="off"', demo[:200]),
      "demo initial state attributes")

# Top bar
tb_m = re.search(r'<div id="tb".*?</div>', demo, re.S)
tb = tb_m.group(0) if tb_m else ""
check(bool(tb), "demo top bar")
check(tb.index('id="print"') < tb.index('id="mode"') if 'id="print"' in tb and 'id="mode"' in tb else False,
      "bar order print then mode")
check(re.search(r'<button class="tb-btn" id="print"[^>]*aria-pressed="false"', tb) is not None,
      "print control")
check(re.search(r'<button class="toggle on" id="mode"[^>]*role="switch"[^>]*aria-checked="true"', tb) is not None,
      "mode switch")
for bid in ("print", "mode"):
    m = re.search(r'<button[^>]*id="%s"[^>]*>' % bid, tb)
    tag = m.group(0) if m else ""
    check('aria-label="' in tag and 'title="' in tag, "bar label " + bid)
check(tb.count("<svg") == 3 and len(re.findall(r'<svg[^>]*aria-hidden="true"', tb)) == 3,
      "bar three icons")
check(re.sub(r"<[^>]+>", "", tb).strip() == "print friendly", "bar label text")
check(re.search(r'<button class="tb-btn" id="print".*?</button>', tb, re.S).group(0).find("print friendly") >= 0,
      "print label inside button")

# Bar and print CSS
check(re.search(r'#tb\s*\{[^}]*position:\s*fixed', demo) is not None, "bar fixed")
check(re.search(r'#tb\s*\{[^}]*height:\s*24px', demo) is not None, "bar 24 px")
check(re.search(r'#tb\s*\{[^}]*justify-content:\s*flex-end', demo) is not None, "bar right aligned")
check(re.search(r'#tb\s*\{[^}]*font:\s*10px/1', demo) is not None, "bar 10 px font")
check(re.search(r'\.tb-btn\s*\{[^}]*height:\s*18px', demo) is not None
      and re.search(r'\.tb-btn\s*\{[^}]*padding:\s*0 6px', demo) is not None
      and re.search(r'\.tb-btn\s*\{[^}]*gap:\s*4px', demo) is not None
      and "width: 27px" not in demo, "print button auto width")
check(re.search(r'#tb\s*\{[^}]*background:\s*var\(--page-bg\)', demo) is not None,
      "bar page background")
tb_css = re.search(r"#tb\s*\{.*?\}", demo, re.S).group(0)
check("border-bottom" not in tb_css, "bar no divider")
check("--tb-bg" not in demo, "bar no fill token")
check(re.search(r'\.toggle\s*\{[^}]*width:\s*44px;[^}]*height:\s*20px', demo) is not None,
      "mode switch 44 x 20")
check(re.search(r'\.toggle-thumb\s*\{[^}]*width:\s*16px;[^}]*height:\s*16px', demo) is not None,
      "mode thumb 16 x 16")
check(".toggle .ico-l { left: 7px;" in demo and ".toggle .ico-r { right: 8px;" in demo,
      "switch icons centered")
check(".tb-btn.on { background: var(--tb-ink); color: var(--page-bg);" in demo, "print active fill")
check(not re.search(r'<svg\b[^>]*\s(?:width|height)="', demo), "no fixed svg size")

# Print rules
ps = demo.find("@media print")
pe = demo.find("</style>", ps)
pblock = demo[ps:pe] if ps >= 0 and pe > ps else ""
check("#tb { display: none; }" in pblock, "print hides bar")
check(":root { --page-mint: #e6e6e6; }" in pblock, "print mint override")
check("html h2 { color: #000000; border-color: #000000; }" in pblock, "print pill text and border")
check("html[data-print=\"on\"] h2 { background: #e6e6e6; color: #000000; border-color: #000000; }" in demo,
      "print toggle pill style")
check("html { --page-mint" not in pblock, "print mint specificity")
check("html[data-theme] .diagram" in pblock, "print repeats P0")
check("@page { margin: 12mm; }" in pblock, "print page margin")
check("break-inside: avoid" in pblock, "print break rule")
check("print-color-adjust: exact" in pblock, "print color adjust")
check(demo.index('html[data-theme="dark"] .d1') < demo.index('html[data-print="on"] .diagram'),
      "print override after themes")

# Scripts and assets
check(not re.search(r'<script[^>]+src=|<link\b|@import|https?://', demo), "no external assets")
check("localStorage" not in demo and "sessionStorage" not in demo, "no storage")
check(demo.count("<script") == 2, "two inline scripts")
scripts = re.findall(r"<script>(.*?)</script>", demo, re.S)
check(len(scripts) == 2, "two script bodies")
check("setAttribute('data-theme'" in scripts[0], "head sets theme")
check("classList.toggle('on'" in scripts[1], "mode thumb sync")
check("setMode(savedMode" in scripts[1] and "savedMode" in scripts[1], "print mode restore")
check("if (!manual)" in scripts[1] and "manual" in scripts[1], "os follow until manual")

# Template
check(tpl.count("<h1") == 1 and tpl.count('<p class="sub">') == 1 and tpl.count("<footer") == 1,
      "template page copy slots")
check("<section" not in tpl and tpl.count("<svg") == 3, "template no diagrams")
check("Diagram slot:" in tpl and "d3 L4/D5" in tpl, "template diagram slot")
check(re.search(r'<div id="tb".*?</div>', tpl, re.S).group(0) == tb, "template bar matches demo")
check(re.findall(r"<script>(.*?)</script>", tpl, re.S) == scripts, "template scripts match demo")
check(re.search(r"<style>(.*?)</style>", tpl, re.S).group(1)
      == re.search(r"<style>(.*?)</style>", demo, re.S).group(1), "template styles match demo")
check(not re.search(r'<script[^>]+src=|<link\b|@import|https?://', tpl), "template no external assets")

# Palette catalog
need = ["L1", "L2", "L3", "L4", "D1", "D2", "D3", "D4", "D5", "P0"]
pal = {}
for m in re.finditer(r"\.p(L1|L2|L3|L4|D1|D2|D3|D4|D5|P0)\s*\{([^}]*)\}", cat):
    pal.setdefault(m.group(1), {}).update(pal_tokens(m.group(2)))
check(set(pal) >= set(need), "catalog palettes present")
keys = {"bg", "card", "ink", "muted", "line", "accent"}
check(all(keys <= set(pal.get(k, {})) for k in need), "catalog tokens complete")


def scope(theme, cls):
    m = re.search(r'html\[data-theme="%s"\]\s+\.%s\s*\{([^}]*)\}' % (theme, cls), demo)
    return pal_tokens(m.group(1)) if m else {}


root_m = re.search(r":root\s*\{(.*?)\}", demo, re.S)
dark_m = re.search(r'html\[data-theme="dark"\]\s*\{(.*?)\}', demo, re.S)
root_css = root_m.group(1) if root_m else ""
dark_css = dark_m.group(1) if dark_m else ""
check(one_hex(root_css, "page-bg") == pal["L1"]["bg"], "light page background L1")
check(one_hex(dark_css, "page-bg") == pal["D1"]["bg"], "dark page background D1")

# Sections and palette pairs
pair_map = {"d1": ("L2", "D3"), "d2": ("L3", "D2"), "d3": ("L4", "D5")}
sections = re.findall(r'<section class="diagram (d\d)">(.*?)</section>', demo, re.S)
check(len(sections) == 3, "demo three diagrams")
check('<span class="meta">' not in demo, "no palette meta labels")
pairs = []
for cls, body in sections:
    lp, dp = pair_map.get(cls, (None, None))
    pairs.append((lp, dp))
    check((lp, dp) in {("L1", "D1"), ("L2", "D3"), ("L3", "D2"), ("L4", "D5")},
          cls + " allowed pair " + str(lp) + "/" + str(dp))
    check(scope("light", cls) == {k: v for k, v in pal.get(lp, {}).items() if k != "bg"},
          cls + " light tokens " + str(lp))
    check(scope("dark", cls) == {k: v for k, v in pal.get(dp, {}).items() if k != "bg"},
          cls + " dark tokens " + str(dp))
    check("--page-bg" not in body, cls + " no page tint")
check(len(set(pairs)) == 3, "three distinct pairs")

# P0 overrides
po_m = re.search(r'html\[data-print="on"\]\s+\.diagram\s*\{([^}]*)\}', demo)
po = pal_tokens(po_m.group(1)) if po_m else {}
p0 = {k: pal["P0"][k] for k in ("card", "ink", "muted", "line", "accent")} if "P0" in pal else {}
check(po == p0, "print toggle P0 tokens")
pm_m = re.search(r"html\[data-theme\]\s+\.diagram\s*\{([^}]*)\}", pblock)
pm = pal_tokens(pm_m.group(1)) if pm_m else {}
check(pm == p0, "print media P0 tokens")

# SVGs and markers
svgs = re.findall(r"<svg\b.*?</svg>", demo, re.S)
check(len(svgs) == 6, "demo six inline svgs")
for i, s in enumerate(svgs):
    try:
        ET.fromstring(s)
        ok = True
    except Exception:
        ok = False
    check(ok, "svg %d parses" % i)
diagrams = [s for s in svgs if re.search(r'viewBox="0 0 1040 \d+"', s)]
check(len(diagrams) == 3, "three diagram svgs")
ids = re.findall(r'<marker id="([^"]+)"', demo)
check(len(ids) == 6 and len(set(ids)) == 6, "six unique marker ids")
check(set(re.findall(r"url\(#([^)]+)\)", demo)) <= set(ids), "marker refs resolve")

# Geometry and text budgets
for cls, body in sections:
    m = re.search(r"<svg\b.*?</svg>", body, re.S)
    if not m:
        check(False, cls + " svg present")
        continue
    root = ET.fromstring(m.group(0))
    rects = root.findall("rect")
    mains = [r for r in rects if r.get("class") in ("card", "focus") and r.get("x") == "300"]
    focus = [r for r in mains if r.get("class") == "focus"]
    check(len(mains) >= 2, cls + " main cards")
    check(len(focus) == 1, cls + " one focus")
    check(all(r.get("width") == "470" and r.get("height") == "70" for r in mains),
          cls + " main card size")
    ys = sorted(int(r.get("y")) for r in mains)
    check(ys == [30 + 108 * i for i in range(len(ys))], cls + " card pitch")
    tags = [r for r in rects if r.get("class") == "tag"]
    tag_y = int(tags[0].get("y")) if tags else -1
    check(len(tags) == 1 and tags[0].get("x") == "300" and tags[0].get("width") == "470"
          and tags[0].get("height") == "26", cls + " tag size")
    check(tag_y == ys[-1] + 98, cls + " tag position")
    check(root.get("viewBox") == "0 0 1040 %d" % (tag_y + 32), cls + " viewBox height")

    sides = [r for r in rects if r.get("class") == "card" and r.get("x") != "300"]
    check(len(sides) == 1, cls + " one side card")
    for r in sides:
        x, w, h = r.get("x"), r.get("width"), r.get("height")
        check(x in ("40", "800") and ((x == "40" and w == "210") or (x == "800" and w == "220"))
              and h in ("70", "90", "100"), cls + " side card size")
        check(int(r.get("y")) in ys, cls + " side card row")

    lines = [l for l in root.findall("line") if l.get("class") in ("arrow", "arrow-a")]
    expected = [(y + 70, y + 98) for y in ys[:-1]]
    check(sorted((int(l.get("y1")), int(l.get("y2"))) for l in lines) == expected,
          cls + " arrow geometry")
    check(all(l.get("x1") == "535" and l.get("x2") == "535" for l in lines),
          cls + " arrows on spine")
    accents = [l for l in lines if l.get("class") == "arrow-a"]
    check(1 <= len(accents) <= 2, cls + " accent connectors")

    fills = {}
    for mk in root.findall(".//marker"):
        p = mk.find("path")
        fills[mk.get("id")] = p.get("fill") if p is not None else None
    check(len(fills) == 2 and len(set(fills.values())) == 2, cls + " two marker fills")
    for l in lines:
        ref = re.search(r"url\(#([^)]+)\)", l.get("marker-end") or "")
        want = "var(--accent)" if l.get("class") == "arrow-a" else "var(--muted)"
        check(ref is not None and fills.get(ref.group(1)) == want, cls + " marker pair")

    dashes = [p for p in root.findall("path") if p.get("class") == "dash"]
    check(len(dashes) == len(sides), cls + " dash per side card")

    texts = root.findall("text")
    caps = [t for t in texts if t.get("class") == "cap"]
    check(all(t.get("x") == "549" for t in caps), cls + " captions at x 549")
    check(sorted(int(t.get("y")) for t in caps) == [y + 88 for y in ys[:-1]],
          cls + " caption rows")

    for t in texts:
        s = t.text or ""
        c = t.get("class")
        n = len(s)
        if c == "t":
            check(n <= 24, cls + " title budget " + repr(s))
        elif c == "d":
            lim = {"318": 65, "56": 26, "816": 28}.get(t.get("x"))
            check(lim is not None and n <= lim, cls + " desc budget " + repr(s))
        elif c == "cap":
            check(n <= 42, cls + " caption budget " + repr(s))
        elif c == "side":
            if int(t.get("y")) == tag_y + 17:
                check(n <= 78, cls + " tag budget " + repr(s))
            else:
                check(n <= 28, cls + " branch label budget " + repr(s))

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
for link in re.findall(r"\]\(([^)]+)\)", skill):
    check(os.path.isfile(os.path.join("agent-skill", link)), "skill link " + link)
check("demo.html" in skill and "template.html" in skill and "references/style-manual.md" in skill,
      "skill file map")
low = skill.lower()
check("no external javascript" in low and "no javascript" not in low, "skill script rule")
check("light mode uses light palettes only" in low, "skill modes")
check("one or more sections" in low, "skill section count")
check("print toggle, then light/dark switch" in low, "skill bar order")
check("print toggle labelled `print friendly`" in low, "skill print label")
check("p0 pill is light grey with black text" in low, "skill print pill")
check("head with h2 pill" in low, "skill section head")
check("ascii only" in low, "skill ascii rule")
check("diagram body in manual section 10" in low, "skill diagram body")

# Manual
check("no javascript" not in man.lower(), "manual no full js ban")
check("demo.html" in man, "manual demo reference")
check("template.html" in man, "manual template reference")
check("## 13. Top bar and modes" in man, "manual top bar section")
check("Inline scripts limited" in man, "manual inline script rule")
check("one common page background per page" in man.lower(), "manual common background")
check("one or more `<section>` blocks" in man, "manual section count")
check("## 10. Diagram body" in man, "manual diagram body")
check('<div class="head">' in man and '<span class="meta">' not in man, "manual section head")
check('<section class="diagram d1">' in man, "manual d1 slot")
check("| `.meta` |" not in man, "manual no meta type")
check("Full skeleton" not in man, "manual no stale skeleton")
check("A diagram's `--bg` token applies only" not in man, "manual no stale bg rule")
check("70-high side card" in man, "manual side baselines")
check("tag and branch labels" in man, "manual side class use")
check("print uses a light grey pill with black text and a black border" in man, "manual print pill")
check("auto width, 18 px high" in man, "manual print button size")
check("print toggle shows `print friendly`" in man, "manual print label")
check(man.count("```") % 2 == 0, "manual fences balanced")

# Changelog
versions = re.findall(r"^## (\d+\.\d+\.\d+)$", cl, re.M)
check(versions == ["0.5.0", "0.4.0", "0.3.0", "0.2.0", "0.1.0"], "changelog versions newest first")
check(not re.search(r"\b(19|20)\d\d\b", cl), "changelog no dates")
check(not re.search(r"\bv\d+\.\d+", cl), "changelog bare versions")
check("inline bar scripts" in cl, "changelog script wording")
check("print friendly" in cl and "light grey pill" in cl, "changelog print wording")

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
check("Windows" not in rd and "PowerShell" not in rd and "%USERPROFILE%" not in rd, "readme no os specifics")

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
    hp = os.path.join("tools", "harness.js")
    r = subprocess.run([node, hp], capture_output=True, text=True)
    check(r.returncode == 0, "bar behavior harness")
    if r.returncode != 0:
        print(r.stdout.strip()[:500])

# Print pill in the catalog
check(re.search(r"\.pP0\s*\{\s*--mint:\s*#e6e6e6;\s*\}", cat) is not None, "catalog P0 pill fill")
check(re.search(r"\.pP0 \.pill\s*\{[^}]*color:\s*#000;[^}]*border-color:\s*#000;", cat) is not None,
      "catalog P0 pill text and border")
check("P0 prints the pill light grey with black text" in cat, "catalog P0 note")
check("light grey pill with black text and a black border" in cat, "catalog P0 page note")

print("checks:", count, "failures:", len(fails))
sys.exit(1 if fails else 0)
