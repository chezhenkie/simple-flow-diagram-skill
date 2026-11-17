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

function makeContext(osDark) {
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
  var document = {
    documentElement: root,
    handlers: {},
    getElementById: function (id) { return byId[id] || null; },
    createElement: function () { return El({}); },
    addEventListener: function (k, fn) { document.handlers[k] = fn; }
  };
  var window = { matchMedia: function () { return mq; } };
  return {
    root: root, mode: mode, print: print, darkBtn: darkBtn, lightBtn: lightBtn,
    darkMenu: darkMenu, lightMenu: lightMenu, mq: mq, document: document, window: window,
    bg: function () { return root.style.props['--page-bg']; }
  };
}

function run(ctx) {
  global.window = ctx.window;
  global.document = ctx.document;
  var code = fs.readFileSync(path.join(__dirname, '.artifacts', 's0.js'), 'utf8') + '\n' +
             fs.readFileSync(path.join(__dirname, '.artifacts', 's1.js'), 'utf8');
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

var DARK = 'github,monochrome,ayu,nightowl,solarized';
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
ok(c.darkMenu.children[2].getAttribute('aria-checked') === 'false', 'ayu not marked by default');
ok(c.lightMenu.children[0].getAttribute('aria-checked') === 'true', 'light default vercel marked');
ok(c.lightMenu.children[1].getAttribute('aria-checked') === 'false', 'tokyonight not marked by default');

c.mq.set(true);
ok(c.root.getAttribute('data-theme') === 'dark', 'os change to dark');
ok(c.mode.getAttribute('aria-checked') === 'false', 'os dark aria');
ok(c.bg() === '#0D1117', 'os dark uses github');
c.mq.set(false);
ok(c.bg() === '#E1E2E7', 'os back to vercel');

c.darkBtn.click();
ok(c.darkMenu.classList.contains('open') === true, 'dark menu opens');
ok(c.darkBtn.getAttribute('aria-expanded') === 'true', 'dark button expanded');
c.darkBtn.click();
ok(c.darkMenu.classList.contains('open') === false, 'dark menu closes');

c.darkBtn.click();
c.darkMenu.children[0].click();
ok(c.root.getAttribute('data-theme') === 'dark', 'pick github switches to dark');
ok(c.bg() === '#0D1117', 'github background applied');
ok(c.darkMenu.children[0].getAttribute('aria-checked') === 'true', 'github marked');
ok(c.darkMenu.children[2].getAttribute('aria-checked') === 'false', 'ayu unmarked');
ok(c.darkMenu.classList.contains('open') === false, 'menu closes after pick');
ok(c.darkBtn.getAttribute('aria-expanded') === 'false', 'button collapsed after pick');

c.mode.click();
ok(c.bg() === '#E1E2E7', 'mode switch returns to vercel');
c.lightBtn.click();
c.lightMenu.children[1].click();
ok(c.root.style.props['--line'] === '#737A8C', 'tokyonight light line applied');
c.mode.click();
ok(c.bg() === '#0D1117', 'github remembered across mode switch');
c.mq.set(true);
c.mq.set(false);
ok(c.root.getAttribute('data-theme') === 'dark', 'os ignored after manual toggle');

c.print.click();
ok(c.root.getAttribute('data-print') === 'on', 'print on');
ok(c.print.getAttribute('aria-pressed') === 'true', 'print aria on');
ok(c.bg() === '#FFFFFF', 'print white page');
ok(c.root.style.props['--muted'] === '#333333', 'print muted token');
c.print.click();
ok(c.root.getAttribute('data-print') === 'off', 'print off');
ok(c.bg() === '#0D1117', 'print off restores github');
ok(c.root.style.props['--thumb'] === '#2E2E2E', 'print off restores dark thumb');
ok(c.root.style.props['--thumb-line'] === '#777777', 'print off restores dark thumb line');
ok(c.print.getAttribute('aria-pressed') === 'false', 'print aria off');

c.darkBtn.click();
c.darkMenu.children[2].click();
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

if (failures) {
  console.log('harness failures: ' + failures);
  process.exit(1);
}
console.log('harness ok');
