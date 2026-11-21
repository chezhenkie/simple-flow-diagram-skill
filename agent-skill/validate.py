#!/usr/bin/env python3
"""Check a finished page against the flow diagram contract.

Usage: python validate.py <page>-flow.html [-v]

Reads the page and `template.html` beside it. Prints one line per
failure, then a count. Exit code 1 on any failure, 0 on a clean page.

The shell (style block and both inline scripts) is compared with
template.html beside this file, so a page that edited the shell fails.
"""

import re
import sys

SVG = re.compile(r"<svg\b([^>]*)>(.*?)</svg>", re.S)
RECT = re.compile(r"<rect\b([^>]*)>", re.S)
TEXT = re.compile(r"<text\b([^>]*)>(.*?)</text>", re.S)
LINE = re.compile(r"<line\b([^>]*)>", re.S)
PATH = re.compile(r"<path\b([^>]*)>", re.S)
MARKER = re.compile(r"<marker\b([^>]*)>", re.S)
ATTR = re.compile(r'([a-zA-Z0-9-]+)="([^"]*)"')
STYLE = re.compile(r"<style>(.*?)</style>", re.S)
SCRIPTS = re.compile(r"<script>(.*?)</script>", re.S)

MAIN_X = {300: (470, 222), 548: (222,)}
SPLIT_X = {300, 548}
SIDE_W = {40: 210, 800: 220}
LANES_L = {226, 206, 186, 166}
LANES_R = {824, 844, 864, 884}
PITCH = 108
TOP = 30
HEIGHT = 70
TAG_H = 26
GAP = 28
CAPTION_DY = 88

fails = []
count = 0


def check(ok, name, page=None):
    global count
    count += 1
    if not ok:
        fails.append(name if page is None else "%s: %s" % (page, name))


def attrs(s):
    return dict(ATTR.findall(s))


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def budget(card_w, what):
    if what == "title":
        return 24
    if card_w == 470:
        return 65
    if card_w == 220:
        return 28
    if card_w in (210, 222):
        return 28 if card_w == 222 else 26
    return 24


def side_indent(x):
    return 16 if x in SIDE_W else 18


def strip_comments(s):
    return re.sub(r"<!--.*?-->", "", s, flags=re.S)


def page_checks(raw, body, text):
    check(all(ord(c) < 128 for c in text), "ascii only")
    check("\r" not in text, "lf endings", "file")
    b = re.sub(r"<[^>]+>", "", body)
    check(b.count("<") == 0, "no unclosed tags", "file")
    check(len(re.findall(r"<h1\b", body)) == 1, "one h1")
    check(len(re.findall(r'class="sub"', body)) == 1, "one subtitle")
    check(len(re.findall(r"<footer\b", body)) == 1, "one footer")
    check(len(re.findall(r"<main\b", body)) == 1, "one main")
    check(not re.search(r"<script[^>]+src=|<link\b|@import", body), "no external assets")
    check(not re.search(r"https?://", body), "no network urls")
    check("localStorage" not in body and "sessionStorage" not in body, "no storage")
    check(len(re.findall(r"<script>", body)) == 2, "two inline scripts")
    check(not re.search(r"<svg\b[^>]*\s(?:width|height)=\"", body), "no fixed svg size")
    check("var THEMES" in body, "theme table present")
    table = text[text.find("var THEMES"):]
    dark = table[table.find("dark: {"):table.find("light: {")]
    light = table[table.find("light: {"):table.find("var chosen")]
    dark_names = re.findall(r"^\s{8}([a-z]+):\s*\{", dark, re.M)
    light_names = re.findall(r"^\s{8}([a-z]+):\s*\{", light, re.M)
    check(len(dark_names) == 5, "five dark themes")
    check(len(light_names) == 4, "four light themes")
    check("monokai" not in dark + light, "monokai removed")
    check(re.search(r"var chosen = \{ dark: '(\w+)', light: '(\w+)' \}", table) is not None,
          "default picks declared")
    for key in ("--page-bg", "--page-ink", "--accent", "--card", "--line", "--muted"):
        check(key in text[:text.find("</style>")], "token " + key)
    check('id="print"' in body and 'id="mode"' in body, "print and mode controls")
    check(body.find('id="print"') < body.find('id="mode"') < body.find('id="dark-theme"')
          < body.find('id="light-theme"'), "bar control order")
    check(re.search(r'id="mode"[^>]*role="switch"', body) is not None, "mode is a switch")
    check(len(re.findall(r'role="menu"', body)) == 2, "two menus")
    check(body.count('aria-haspopup="true"') == 2, "foldout popups declared")
    check(body.count('aria-controls="') == 2, "foldouts point at menus")


def shell_checks(page_style, page_scripts):
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    tpl = os.path.join(here, "template.html")
    if not os.path.isfile(tpl):
        return
    src = open(tpl, encoding="ascii").read()
    ts = STYLE.search(src)
    tscripts = SCRIPTS.findall(src)
    check(ts is not None and page_style.strip() == ts.group(1).strip(), "shell style unchanged")
    check(len(page_scripts) == len(tscripts), "shell script count")
    for i, s in enumerate(page_scripts):
        if i < len(tscripts):
            check(s.strip() == tscripts[i].strip(), "shell script %d unchanged" % (i + 1))


def svg_checks(head, inner, tag):
    a = attrs(head)
    box = a.get("viewBox", "").split()
    check(len(box) == 4 and box[0] == "0" and box[1] == "0" and box[2] == "1040",
          "viewBox is 1040 wide", tag)
    height = num(box[3]) if len(box) == 4 else None
    check(a.get("role") == "img", "role img", tag)
    check(bool((a.get("aria-label") or "").strip()), "aria-label", tag)
    check(re.search(r"\bfill=\"#|\bstroke=\"#|\bfill=\"rgb|\bstroke=\"rgb", inner) is None,
          "no hardcoded colors", tag)

    rects = [attrs(m.group(1)) for m in RECT.finditer(inner)]
    markers = [attrs(m.group(1)).get("id") for m in MARKER.finditer(inner)]
    texts = [dict(attrs(m.group(1)), body=m.group(2).strip()) for m in TEXT.finditer(inner)]
    lines = [attrs(m.group(1)) for m in LINE.finditer(inner)]
    paths = [attrs(m.group(1)) for m in PATH.finditer(inner)]

    cards, tagbox = [], None
    for r in rects:
        cls = r.get("class", "")
        x, y = num(r.get("x")), num(r.get("y"))
        w, h = num(r.get("width")), num(r.get("height"))
        if cls == "tag":
            tagbox = (x, y, w, h)
            check((x, w, h) == (300, 470, TAG_H), "tag at 300, 470 wide, 26 high", tag)
            check(r.get("rx") == "3", "tag corners rx 3", tag)
            continue
        check(cls in ("card", "focus"), "rect class card or focus", tag)
        check(r.get("rx") == "3", "card corners rx 3", tag)
        if w in (470, 222):
            check(x in MAIN_X and w in MAIN_X[x], "main or split card width at x=%s w=%s" % (x, w), tag)
        else:
            check(x in SIDE_W and SIDE_W[x] == w, "side card width", tag)
        cards.append((cls, x, y, w, h))

    main = [c for c in cards if c[3] in (470, 222)]
    side = [c for c in cards if c[3] in (210, 220)]
    rows = sorted({c[2] for c in main})
    check(1 <= len(rows) <= 7, "one to seven main rows", tag)
    for i, y in enumerate(rows):
        check(y == TOP + PITCH * i, "main row %d at %d" % (i + 1, TOP + PITCH * i), tag)
    for cls, x, y, w, h in main:
        check(h == HEIGHT, "main card 70 high", tag)
        check(y in rows, "main card on a row", tag)
    for y in rows:
        at = [c for c in main if c[2] == y]
        if len(at) == 2:
            check({c[1] for c in at} == SPLIT_X and all(c[3] == 222 for c in at),
                  "split row 222 at 300 and 548", tag)
        else:
            check(len(at) == 1 and at[0][3] == 470, "one 470 card per row", tag)
    for cls, x, y, w, h in side:
        check(h in (70, 90, 100), "side height 70, 90 or 100", tag)
        check(any(y == TOP + PITCH * i or y == TOP + PITCH * i + 20 for i in range(8)),
              "side box on a row or 20 lower", tag)
    check(sum(1 for c in cards if c[0] == "focus") == 1, "one focus card", tag)

    if tagbox:
        last = rows[-1] + 98
        check(tagbox[1] == last, "tag at last card top + 98", tag)
        check(height == tagbox[1] + 32, "viewBox height tag y + 32", tag)
    else:
        check(height == rows[-1] + 102, "viewBox height last top + 102", tag)

    # Text inside cards.
    used = set()
    for i, t in enumerate(texts):
        cls = t.get("class")
        x, y = num(t.get("x")), num(t.get("y"))
        body = t["body"]
        if cls == "side":
            if tagbox and abs(x - (tagbox[0] + 18)) < 0.01 and abs(y - (tagbox[1] + 17)) < 0.01:
                check(len(body) <= 78, "tag line 78 characters", tag)
                used.add(i)
            continue
        if cls == "cap":
            continue
        host = None
        for c in cards:
            if c[1] <= x <= c[1] + c[3] and c[2] <= y <= c[2] + c[4]:
                host = c
                break
        check(host is not None, "text %r inside a card" % body[:20], tag)
        if host is None:
            continue
        used.add(i)
        cls_, hx, hy, hw, hh = host
        check(x == hx + side_indent(hx), "text indent", tag)
        dy = y - hy
        if cls == "t":
            check(dy == 26, "title at y+26", tag)
            check(len(body) <= 24, "title 24 characters", tag)
        elif cls == "d":
            check(dy in (44, 59, 74), "description at y+44, +59 or +74", tag)
            check(not (dy == 74 and hw not in (210, 220)), "third line on side cards only", tag)
            check(len(body) <= budget(hw, "desc"), "description budget on %d card" % hw, tag)
        else:
            check(False, "text class t/d/side/cap only", tag)

    # Every card needs a title, and no card carries more description lines than rows allow.
    for c in cards:
        n_t = sum(1 for i, t in enumerate(texts)
                  if i in used and t.get("class") == "t"
                  and c[1] <= num(t.get("x")) <= c[1] + c[3]
                  and c[2] <= num(t.get("y")) <= c[2] + c[4])
        check(n_t == 1, "one title on the card at y=%s" % c[2], tag)

    # Arrows between rows.
    def spine(cx, gap_top):
        hit = 0
        for l in lines:
            if num(l.get("x1")) == cx and num(l.get("x2")) == cx:
                if abs(num(l.get("y1")) - gap_top) < 0.01 and abs(num(l.get("y2")) - (gap_top + GAP)) < 0.01:
                    hit += 1 if l.get("marker-end") else 0
        for p in paths:
            d = (p.get("d") or "").strip()
            if p.get("class") not in ("arrow", "arrow-a", "dash", "loop"):
                continue
            if re.match(r"M %s %s H" % (cx, gap_top), d) and p.get("marker-end"):
                hit += 1
        return hit

    for i in range(len(rows) - 1):
        gap_top = rows[i] + HEIGHT
        below = [c for c in main if c[2] == rows[i + 1]]
        xs = [411, 659] if len(below) == 2 else [535]
        for cx in xs:
            check(spine(cx, gap_top) == 1, "one arrow at x=%d over y=%d" % (cx, gap_top), tag)

    # Captions sit on the caption lane of their arrow.
    for i in range(len(rows) - 1):
        gap_top = rows[i] + HEIGHT
        below = [c for c in main if c[2] == rows[i + 1]]
        xs = [425, 673] if len(below) == 2 else [549]
        for cx in xs:
            hit = [t for t in texts
                   if t.get("class") == "cap" and num(t.get("x")) == cx
                   and num(t.get("y")) == gap_top + CAPTION_DY - HEIGHT]
            check(len(hit) == 1, "one caption at x=%d over y=%d" % (cx, gap_top), tag)
            for t in hit:
                check(len(t["body"]) <= (18 if cx in (425, 673) else 42),
                      "caption budget at x=%d" % cx, tag)

    # Accent connectors, loops and markers.
    check(0 <= sum(1 for l in lines if l.get("class") == "arrow-a")
          + sum(1 for p in paths if p.get("class") == "arrow-a") <= 2,
          "zero to two accent connectors", tag)
    for p in paths:
        if p.get("class") != "loop":
            continue
        d = (p.get("d") or "").strip()
        m = re.match(r"M (300|770) (\d+) H (\d+) V (\d+) H (300|770)$", d)
        check(m is not None, "loop is four segments", tag)
        if not m:
            continue
        x1, y1, lane, y2, x5 = map(float, m.groups())
        check(num(m.group(3)) in LANES_L | LANES_R, "loop on a lane", tag)
        left = num(m.group(3)) in LANES_L
        check((left and x1 == 300 and x5 == 300) or (not left and x1 == 770 and x5 == 770),
              "loop leaves the card edge on its lane side", tag)
        check(y2 < y1, "loop runs upward", tag)
        start = [c for c in main if (c[1] if left else c[1] + c[3]) == x1
                 and num(m.group(2)) in (c[2] + 20, c[2] + 35, c[2] + c[4] - 20)]
        end = [c for c in main if (c[1] if left else c[1] + c[3]) == x5
               and num(m.group(4)) in (c[2] + 20, c[2] + 35, c[2] + c[4] - 20)]
        check(bool(start), "loop leaves at a side mark", tag)
        check(bool(end), "loop enters at a side mark", tag)
    for t in texts:
        if t.get("class") == "side" and tagbox and num(t.get("y")) != tagbox[1] + 17:
            check(len(t["body"]) <= 12, "loop or side label 12 characters", tag)

    check(len(markers) == len(set(markers)), "marker ids unique per diagram", tag)
    for el in lines + paths:
        ref = el.get("marker-end") or ""
        if ref.startswith("url(#"):
            check(ref[5:-1] in markers, "marker %s defined" % ref, tag)
    return markers


def main(argv):
    verbose = "-v" in argv
    args = [a for a in argv[1:] if not a.startswith("-")]
    if not args:
        print("usage: python validate.py <page>.html [-v]")
        return 2
    path = args[0]
    raw = open(path, "rb").read()
    text = raw.decode("ascii", "replace")
    body = strip_comments(text)

    page_checks(raw, body, text)
    style = STYLE.search(body)
    shell_checks(style.group(1) if style else "", SCRIPTS.findall(body))

    sections = re.findall(r"<section>(.*?)</section>", body, re.S)
    check(len(sections) >= 1, "at least one section")
    seen = []
    for i, sec in enumerate(sections):
        tag = "section %d" % (i + 1)
        check('class="head"' in sec, "head block", tag)
        h2 = re.search(r"<h2>(.*?)</h2>", sec, re.S)
        check(h2 is not None, "h2 title", tag)
        if h2:
            check(re.search(r":\s\S", h2.group(1)) is not None, "h2 reads subject: outcome", tag)
        check('class="note"' in sec, "note above the diagram", tag)
        m = SVG.search(sec)
        check(m is not None, "one svg", tag)
        if m:
            check(len(re.findall(r"<svg\b", sec)) == 1, "only one svg per section", tag)
            seen += svg_checks(m.group(1), m.group(2), tag)
    for mid in seen:
        check(seen.count(mid) == 1, "marker id %s unique on the page" % mid, "page")

    print("validated %s" % path)
    if verbose:
        print("checks: %d" % count)
    for f in fails:
        print("FAIL " + f)
    print("checks: %d failures: %d" % (count, len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
