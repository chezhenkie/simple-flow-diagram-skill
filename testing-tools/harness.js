'use strict';
var fs = require('fs');
var path = require('path');

function El(attrs) {
  var el = {
    attrs: Object.assign({}, attrs || {}),
    classes: {},
    handlers: {},
    children: [],
    style: {
      props: {},
      setProperty: function (k, v) { this.props[k] = String(v); }
    },
    textContent: '',
    setAttribute: function (k, v) { el.attrs[k] = String(v); },
    getAttribute: function (k) { return k in el.attrs ? el.attrs[k] : null; },
    addEventListener: function (k, fn) { el.handlers[k] = fn; },
    appendChild: function (child) { el.children.push(child); },
    focus: function () { el.focused = true; },
    click: function () {
      if (el.handlers.click) el.handlers.click({ stopPropagation: function () {}, target: el });
    },
    classList: {
      add: function (n) { el.classes[n] = true; },
      remove: function (n) { delete el.classes[n]; },
      toggle: function (n, on) { el.classes[n] = !!on; },
      contains: function (n) { return !!el.classes[n]; }
    }
  };
  return el;
}

function makeContext(osDark, search) {
  var root = El({ 'data-theme': 'light', 'data-print': 'off' });
  var mode = El({ 'aria-checked': 'true' });
  var print = El({ 'aria-pressed': 'false' });
  var darkBtn = El({ 'aria-expanded': 'false' });
  var lightBtn = El({ 'aria-expanded': 'false' });
  var darkMenu = El({});
  var lightMenu = El({});
  mode.classes.on = true;
  var byId = {
    mode: mode, print: print,
    'dark-theme': darkBtn, 'light-theme': lightBtn,
    'dark-menu': darkMenu, 'light-menu': lightMenu
  };
  var mq = {
    matches: osDark,
    handlers: {},
    addEventListener: function (k, fn) { this.handlers[k] = fn; },
    addListener: function (fn) { this.handlers.change = fn; },
    set: function (v) {
      this.matches = v;
      if (this.handlers.change) this.handlers.change({ matches: v });
    }
  };
  var link = El({ href: 'other-page.html' });
  var docLink = El({ href: 'notes.md' });
  var document = {
    documentElement: root,
    handlers: {},
    getElementById: function (id) { return byId[id] || null; },
    createElement: function () { return El({}); },
    querySelectorAll: function () { return [link, docLink]; },
    addEventListener: function (k, fn) { document.handlers[k] = fn; }
  };
  var window = {
    matchMedia: function () { return mq; },
    location: { search: search || '' }
  };
  return {
    root: root, mode: mode, print: print, darkBtn: darkBtn, lightBtn: lightBtn,
    darkMenu: darkMenu, lightMenu: lightMenu, mq: mq, document: document, window: window,
    link: link, docLink: docLink,
    bg: function () { return root.style.props['--page-bg']; }
  };
}

function pageScripts() {
  var html = fs.readFileSync(path.join(__dirname, '..', 'agent-skill', 'demo.html'), 'utf8');
  var out = [], re = /<script>([\s\S]*?)<\/script>/g, m;
  while ((m = re.exec(html))) out.push(m[1]);
  if (out.length !== 2) throw new Error('expected two inline scripts, found ' + out.length);
  return out;
}

var code = pageScripts().join('\n');

function run(ctx) {
  global.window = ctx.window;
  global.document = ctx.document;
  (0, eval)(code);
}

var failures = 0;
function ok(value, label) {
  if (!value) {
    failures++;
    console.log('FAIL ' + label);
  }
}

function names(el) {
  return el.children.map(function (c) { return c.textContent; }).join(',');
}

var DARK = 'github,harbor,solarized,oledblack,ayu';
var LIGHT = 'vercel,tokyonight,cursor,orng';

var c = makeContext(false);
run(c);
ok(c.root.getAttribute('data-theme') === 'light', 'initial light theme');
ok(c.mode.getAttribute('aria-checked') === 'true', 'initial light aria');
ok(c.mode.classList.contains('on') === true, 'initial light thumb');
ok(c.bg() === '#E1E2E7', 'initial vercel background');
ok(names(c.darkMenu) === DARK, 'dark menu names');
ok(names(c.lightMenu) === LIGHT, 'light menu names');
ok(c.darkMenu.children[0].getAttribute('aria-checked') === 'true', 'dark default github marked');
ok(c.darkMenu.children[4].getAttribute('aria-checked') === 'false', 'ayu not marked by default');
ok(c.lightMenu.children[0].getAttribute('aria-checked') === 'true', 'light default vercel marked');
ok(c.lightMenu.children[1].getAttribute('aria-checked') === 'false', 'tokyonight not marked by default');
ok(c.link.getAttribute('href') === 'other-page.html?mode=light&dark=github&light=vercel',
   'link carries the initial picks');
ok(c.docLink.getAttribute('href') === 'notes.md', 'non-page links untouched');

c.mq.set(true);
ok(c.root.getAttribute('data-theme') === 'dark', 'os change to dark');
ok(c.mode.getAttribute('aria-checked') === 'false', 'os dark aria');
ok(c.bg() === '#0D1117', 'os dark uses github');
c.mq.set(false);
ok(c.bg() === '#E1E2E7', 'os back to vercel');

c.darkBtn.click();
ok(c.darkMenu.classList.contains('open') === true, 'dark menu opens');
ok(c.darkBtn.getAttribute('aria-expanded') === 'true', 'dark button expanded');
ok(c.darkMenu.children[0].focused === true, 'menu opens on the marked row');
c.document.activeElement = c.darkMenu.children[0];
c.darkMenu.handlers.keydown.call(c.darkMenu, { key: 'ArrowDown', preventDefault: function () {} });
ok(c.darkMenu.children[1].focused === true, 'arrow down moves one row');
c.document.activeElement = c.darkMenu.children[1];
c.darkMenu.handlers.keydown.call(c.darkMenu, { key: 'End', preventDefault: function () {} });
ok(c.darkMenu.children[c.darkMenu.children.length - 1].focused === true, 'End moves to the last row');
c.document.handlers.keydown.call(c.document, { key: 'Escape' });
ok(c.darkMenu.classList.contains('open') === false, 'escape closes the menu');
ok(c.darkBtn.focused === true, 'escape returns focus to the theme button');

c.darkBtn.click();
c.darkMenu.children[0].click();
ok(c.root.getAttribute('data-theme') === 'dark', 'pick github switches to dark');
ok(c.bg() === '#0D1117', 'github background applied');
ok(c.darkMenu.children[0].getAttribute('aria-checked') === 'true', 'github marked');
ok(c.darkMenu.children[4].getAttribute('aria-checked') === 'false', 'ayu unmarked');
ok(c.darkMenu.classList.contains('open') === false, 'menu closes after pick');
ok(c.darkBtn.getAttribute('aria-expanded') === 'false', 'button collapsed after pick');

c.mode.click();
ok(c.bg() === '#E1E2E7', 'mode switch returns to vercel');
c.lightBtn.click();
c.lightMenu.children[1].click();
ok(c.root.style.props['--line'] === '#6B7280', 'tokyonight light line applied');
ok(c.link.getAttribute('href') === 'other-page.html?mode=light&dark=github&light=tokyonight',
   'link follows a theme pick');
c.mode.click();
ok(c.bg() === '#0D1117', 'github remembered across mode switch');
c.mq.set(true);
c.mq.set(false);
ok(c.root.getAttribute('data-theme') === 'dark', 'os ignored after manual toggle');

c.print.click();
ok(c.root.getAttribute('data-print') === 'on', 'print on');
ok(c.print.getAttribute('aria-pressed') === 'true', 'print aria on');
ok(c.bg() === 'var(--print-bg)', 'print white page');
ok(c.root.style.props['--muted'] === 'var(--print-muted)', 'print muted aliases the palette');
ok(c.root.style.props['--thumb'] === '#CBCBCB', 'print light thumb');
c.print.click();
ok(c.root.getAttribute('data-print') === 'off', 'print off');
ok(c.bg() === '#0D1117', 'print off restores github');
ok(c.root.style.props['--thumb'] === '#2E2E2E', 'print off restores dark thumb');
ok(c.root.style.props['--thumb-line'] === '#777777', 'print off restores dark thumb line');
ok(c.print.getAttribute('aria-pressed') === 'false', 'print aria off');

c.darkBtn.click();
c.darkMenu.children[4].click();
ok(c.bg() === '#0B0E14', 'ayu selected again');

var d = makeContext(true);
run(d);
ok(d.root.getAttribute('data-theme') === 'dark', 'initial os dark theme');
ok(d.bg() === '#0D1117', 'initial os dark github');
ok(d.mode.getAttribute('aria-checked') === 'false', 'initial os dark aria');
ok(d.print.getAttribute('aria-pressed') === 'false', 'initial print off');
d.mq.set(false);
ok(d.root.getAttribute('data-theme') === 'light', 'os follow before manual');
ok(d.bg() === '#E1E2E7', 'os light vercel');

var g = makeContext(false);
run(g);
g.lightBtn.click();
g.lightMenu.children[1].click();
ok(g.root.getAttribute('data-theme') === 'light', 'theme pick stays light');
ok(g.root.style.props['--line'] === '#6B7280', 'tokyonight line after pick');
g.mq.set(true);
ok(g.root.getAttribute('data-theme') === 'light', 'theme pick stops os follow');
ok(g.root.style.props['--line'] === '#6B7280', 'theme pick survives os change');

var p = makeContext(false, '?mode=dark&dark=ayu&light=cursor');
run(p);
ok(p.root.getAttribute('data-theme') === 'dark', 'link mode read on load');
ok(p.bg() === '#0B0E14', 'link dark pick applied');
ok(p.darkMenu.children[4].getAttribute('aria-checked') === 'true', 'link dark pick marked');
ok(p.lightMenu.children[2].getAttribute('aria-checked') === 'true', 'link light pick marked');
ok(p.link.getAttribute('href') === 'other-page.html?mode=dark&dark=ayu&light=cursor',
   'link state carried onward');
ok(!('change' in p.mq.handlers), 'no os listener when the link carries the mode');
p.mq.set(false);
ok(p.root.getAttribute('data-theme') === 'dark', 'link state survives an os change');

if (failures) {
  console.log('harness failures: ' + failures);
  process.exit(1);
}
console.log('harness ok');
