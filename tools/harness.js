'use strict';
var fs = require('fs');
var path = require('path');

function makeEl(initial) {
  var attrs = Object.assign({}, initial || {});
  var classes = {};
  var handlers = {};
  return {
    attrs: attrs,
    classes: classes,
    handlers: handlers,
    setAttribute: function (k, v) { attrs[k] = String(v); },
    getAttribute: function (k) { return k in attrs ? attrs[k] : null; },
    addEventListener: function (k, fn) { handlers[k] = fn; },
    classList: {
      toggle: function (name, on) { classes[name] = !!on; },
      contains: function (name) { return !!classes[name]; }
    },
    click: function () { if (handlers.click) handlers.click(); }
  };
}

function makeContext(osDark) {
  var root = makeEl({ 'data-theme': 'light', 'data-print': 'off' });
  var mode = makeEl({ 'aria-checked': 'true' });
  var print = makeEl({ 'aria-pressed': 'false' });
  mode.classes.on = true;
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
    getElementById: function (id) {
      return id === 'mode' ? mode : (id === 'print' ? print : null);
    }
  };
  var window = {
    matchMedia: function () { return mq; }
  };
  return { root: root, mode: mode, print: print, mq: mq, document: document, window: window };
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

var c = makeContext(false);
run(c);
ok(c.root.getAttribute('data-theme') === 'light', 'initial light theme');
ok(c.mode.getAttribute('aria-checked') === 'true', 'initial light aria');
ok(c.mode.classList.contains('on') === true, 'initial light thumb');

c.mq.set(true);
ok(c.root.getAttribute('data-theme') === 'dark', 'os change to dark');
ok(c.mode.getAttribute('aria-checked') === 'false', 'os dark aria');
ok(c.mode.classList.contains('on') === false, 'os dark thumb');
c.mq.set(false);
ok(c.root.getAttribute('data-theme') === 'light', 'os change back to light');

c.mode.click();
ok(c.root.getAttribute('data-theme') === 'dark', 'click toggles to dark');
ok(c.mode.getAttribute('aria-checked') === 'false', 'click dark aria');
ok(c.mode.classList.contains('on') === false, 'click dark thumb');
c.mq.set(true);
c.mq.set(false);
ok(c.root.getAttribute('data-theme') === 'dark', 'os ignored after manual toggle');

c.print.click();
ok(c.root.getAttribute('data-print') === 'on', 'print on');
ok(c.print.getAttribute('aria-pressed') === 'true', 'print aria on');
ok(c.print.classList.contains('on') === true, 'print fill on');
c.mode.click();
ok(c.root.getAttribute('data-theme') === 'light', 'mode changes while print on');
ok(c.root.getAttribute('data-print') === 'on', 'print stays on');
c.print.click();
ok(c.root.getAttribute('data-print') === 'off', 'print off');
ok(c.print.getAttribute('aria-pressed') === 'false', 'print aria off');
ok(c.print.classList.contains('on') === false, 'print fill off');
ok(c.root.getAttribute('data-theme') === 'dark', 'print off restores saved dark');
ok(c.mode.getAttribute('aria-checked') === 'false', 'restored dark aria');
ok(c.mode.classList.contains('on') === false, 'restored dark thumb');

var d = makeContext(true);
run(d);
ok(d.root.getAttribute('data-theme') === 'dark', 'initial os dark theme');
ok(d.mode.getAttribute('aria-checked') === 'false', 'initial os dark aria');
ok(d.mode.classList.contains('on') === false, 'initial os dark thumb');
ok(d.print.getAttribute('aria-pressed') === 'false', 'initial print off');
d.mq.set(false);
ok(d.root.getAttribute('data-theme') === 'light', 'os follow before manual');

if (failures) {
  console.log('harness failures: ' + failures);
  process.exit(1);
}
console.log('harness ok');
