/* Ask OmniFit - on-site AI assistant widget.
   Source: site/assistant.js, copied to public/assets/assistant.js by build.py.
   Loaded lazily by the footer loader after the page has finished loading. It
   asks GET /api/ask first and only draws the launcher when the function
   answers {ok: true}, so until ANTHROPIC_API_KEY and the D1 binding exist the
   widget never appears. Everything is position:fixed: no layout shift. */
(function () {
  'use strict';
  if (window.__askOmniFit) return;
  window.__askOmniFit = true;

  var API = '/api/ask';
  var CALENDLY = 'https://calendly.com/nemezio-omnifittraining/45min';
  var FIT_CHECK = '/fit-check';
  var MAX_CHARS = 600;
  var STORE = 'oa-chat-v1';
  var COPY = {
    launcher: 'Ask OmniFit',
    title: 'Ask OmniFit',
    note: "AI assistant · Answers come from OmniFit's published pricing and policies. Conversations are logged to improve answers. Please don't share medical details.",
    opener: 'I can answer questions about pricing, how programs work, in-home areas, and whether OmniFit fits your situation. What would you like to know?',
    chips: ['What does it cost?', 'Do you train in-home?', 'I have an old injury. Is that okay?', 'How is this different from a gym?'],
    book: 'Book a Consultation',
    fitCheck: 'Take the Fit Check',
    error: 'Something went wrong. You can book a consultation directly.',
    placeholder: 'Ask a question',
    inputLabel: 'Your question',
    send: 'Send',
    close: 'Close Ask OmniFit',
    typing: 'Ask OmniFit is typing'
  };
  var ICON_CHAT = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v8a2.5 2.5 0 0 1-2.5 2.5H10l-4.2 3.6c-.5.4-1.3.1-1.3-.6V16A2.5 2.5 0 0 1 4 13.5z"/><path d="M8 8.5h8M8 11.5h5"/></svg>';
  var ICON_CLOSE = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6L6 18"/></svg>';
  var ICON_SEND = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 12l16-8-6 16-2.5-6.5z"/><path d="M11.5 13.5L20 4"/></svg>';

  function track(name, params) {
    if (typeof window.gtag === 'function') window.gtag('event', name, params || {});
  }

  function load() {
    try { var s = JSON.parse(sessionStorage.getItem(STORE) || 'null'); if (s && Array.isArray(s.messages)) return s; } catch (e) {}
    return null;
  }
  function save() {
    try { sessionStorage.setItem(STORE, JSON.stringify(state)); } catch (e) {}
  }
  function newId() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return 'oa-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 12);
  }

  var state = load() || { sessionId: newId(), messages: [] };
  var root, launcher, panel, log, chips, form, input, sendBtn, busy = false, lastFocus = null;

  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }

  function ctaButtons(handoff) {
    var wrap = el('div', 'oa-ctas');
    if (handoff === 'book') {
      var a = el('a', 'oa-btn oa-btn--gold');
      a.href = CALENDLY; a.target = '_blank'; a.rel = 'noopener'; a.textContent = COPY.book;
      a.addEventListener('click', function () { track('assistant_cta_click', { cta: 'book' }); });
      wrap.appendChild(a);
    } else if (handoff === 'fit_check') {
      var f = el('a', 'oa-btn oa-btn--outline');
      f.href = FIT_CHECK; f.textContent = COPY.fitCheck;
      f.addEventListener('click', function () { track('assistant_cta_click', { cta: 'fit_check' }); });
      wrap.appendChild(f);
    }
    return wrap;
  }

  function bubble(role, text, handoff) {
    var row = el('div', 'oa-msg oa-msg--' + role);
    var b = el('div', 'oa-bubble');
    b.textContent = text;
    row.appendChild(b);
    if (handoff) row.appendChild(ctaButtons(handoff));
    log.appendChild(row);
    log.scrollTop = log.scrollHeight;
    return row;
  }

  function renderLog() {
    log.innerHTML = '';
    bubble('assistant', COPY.opener);
    state.messages.forEach(function (m) { bubble(m.role, m.content, m.role === 'assistant' ? m.handoff : null); });
    chips.hidden = state.messages.length > 0;
  }

  function setBusy(on) {
    busy = on;
    sendBtn.disabled = on;
    input.setAttribute('aria-busy', on ? 'true' : 'false');
  }

  function typing() {
    var row = el('div', 'oa-msg oa-msg--assistant oa-typing');
    row.setAttribute('role', 'status');
    row.innerHTML = '<div class="oa-bubble"><span class="oa-sr">' + COPY.typing + '</span><i></i><i></i><i></i></div>';
    log.appendChild(row);
    log.scrollTop = log.scrollHeight;
    return row;
  }

  function send(text) {
    text = (text || '').trim();
    if (!text || busy) return;
    if (text.length > MAX_CHARS) text = text.slice(0, MAX_CHARS);
    chips.hidden = true;
    state.messages.push({ role: 'user', content: text });
    save();
    bubble('user', text);
    input.value = '';
    autosize();
    track('assistant_message');
    setBusy(true);
    var dots = typing();
    var history = state.messages.map(function (m) { return { role: m.role, content: m.content }; });
    fetch(API, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ messages: history, page: location.pathname, sessionId: state.sessionId })
    }).then(function (res) {
      if (res.status === 503) { teardown(); return null; }
      if (!res.ok) throw new Error('status ' + res.status);
      return res.json();
    }).then(function (data) {
      if (!data) return;
      if (!data.reply) throw new Error('empty');
      var handoff = data.handoff === 'book' || data.handoff === 'fit_check' ? data.handoff : null;
      state.messages.push({ role: 'assistant', content: data.reply, handoff: handoff });
      save();
      dots.remove();
      bubble('assistant', data.reply, handoff);
    }).catch(function () {
      // The failed question stays out of the history sent next time.
      state.messages.pop();
      save();
      dots.remove();
      bubble('assistant', COPY.error, 'book');
    }).then(function () {
      if (root) { setBusy(false); }
    });
  }

  function autosize() {
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 120) + 'px';
  }

  function focusables() {
    return Array.prototype.filter.call(
      panel.querySelectorAll('a[href], button:not([disabled]), textarea, [tabindex]:not([tabindex="-1"])'),
      function (n) { return n.offsetParent !== null || n === document.activeElement; }
    );
  }

  function isSheet() { return window.matchMedia('(max-width: 640px)').matches; }

  function open() {
    if (!panel.hidden) return;
    lastFocus = document.activeElement;
    renderLog();
    panel.hidden = false;
    launcher.setAttribute('aria-expanded', 'true');
    root.classList.add('oa-open');
    if (isSheet()) document.documentElement.classList.add('oa-lock');
    track('assistant_open');
    setTimeout(function () { input.focus(); }, 30);
  }

  function close() {
    if (panel.hidden) return;
    panel.hidden = true;
    launcher.setAttribute('aria-expanded', 'false');
    root.classList.remove('oa-open');
    document.documentElement.classList.remove('oa-lock');
    (launcher || lastFocus).focus();
  }

  function teardown() {
    document.documentElement.classList.remove('oa-lock');
    if (root && root.parentNode) root.parentNode.removeChild(root);
    root = null;
    window.removeEventListener('resize', place);
  }

  // Keep the launcher clear of any fixed bar pinned to the bottom of the
  // viewport (the 4S Ranch mobile Call / Book bar is the one on the site
  // today); the offset is re-read on resize, since those bars are breakpoint-driven.
  function place() {
    if (!root) return;
    var vh = window.innerHeight, off = 0;
    var bars = document.querySelectorAll('[class*="sticky"], [class*="fixed"], [class*="bottom-bar"]');
    for (var i = 0; i < bars.length; i++) {
      var n = bars[i];
      if (root.contains(n)) continue;
      var cs = getComputedStyle(n);
      if (cs.position !== 'fixed' || cs.display === 'none' || cs.visibility === 'hidden') continue;
      var r = n.getBoundingClientRect();
      if (r.height > 0 && r.height < vh / 2 && r.bottom >= vh - 4 && r.top < vh) off = Math.max(off, vh - r.top);
    }
    root.style.setProperty('--oa-offset', Math.round(off) + 'px');
  }

  function build() {
    root = el('div', 'oa-root');
    root.id = 'ask-omnifit';

    launcher = el('button', 'oa-launcher', ICON_CHAT + '<span>' + COPY.launcher + '</span>');
    launcher.type = 'button';
    launcher.setAttribute('aria-haspopup', 'dialog');
    launcher.setAttribute('aria-expanded', 'false');
    launcher.setAttribute('aria-controls', 'oa-panel');
    launcher.addEventListener('click', function () { panel.hidden ? open() : close(); });

    panel = el('div', 'oa-panel');
    panel.id = 'oa-panel';
    panel.hidden = true;
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-modal', 'true');
    panel.setAttribute('aria-labelledby', 'oa-title');
    panel.setAttribute('aria-describedby', 'oa-note');

    var head = el('div', 'oa-head');
    var titles = el('div', 'oa-titles');
    var title = el('p', 'oa-title'); title.id = 'oa-title'; title.textContent = COPY.title;
    var note = el('p', 'oa-note'); note.id = 'oa-note'; note.textContent = COPY.note;
    titles.appendChild(title); titles.appendChild(note);
    var closeBtn = el('button', 'oa-close', ICON_CLOSE);
    closeBtn.type = 'button';
    closeBtn.setAttribute('aria-label', COPY.close);
    closeBtn.addEventListener('click', close);
    head.appendChild(titles); head.appendChild(closeBtn);

    log = el('div', 'oa-log');
    log.setAttribute('role', 'log');
    log.setAttribute('aria-live', 'polite');
    log.setAttribute('aria-label', 'Conversation');
    log.tabIndex = 0;

    chips = el('div', 'oa-chips');
    chips.setAttribute('role', 'group');
    chips.setAttribute('aria-label', 'Suggested questions');
    COPY.chips.forEach(function (c) {
      var b = el('button', 'oa-chip');
      b.type = 'button'; b.textContent = c;
      b.addEventListener('click', function () { send(c); });
      chips.appendChild(b);
    });

    form = el('form', 'oa-form');
    form.noValidate = true;
    var label = el('label', 'oa-sr'); label.htmlFor = 'oa-input'; label.textContent = COPY.inputLabel;
    input = el('textarea', 'oa-input');
    input.id = 'oa-input'; input.rows = 1; input.maxLength = MAX_CHARS;
    input.placeholder = COPY.placeholder;
    input.setAttribute('enterkeyhint', 'send');
    input.addEventListener('input', autosize);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); send(input.value); }
    });
    sendBtn = el('button', 'oa-send', ICON_SEND);
    sendBtn.type = 'submit';
    sendBtn.setAttribute('aria-label', COPY.send);
    form.addEventListener('submit', function (e) { e.preventDefault(); send(input.value); });
    form.appendChild(label); form.appendChild(input); form.appendChild(sendBtn);

    panel.appendChild(head); panel.appendChild(log); panel.appendChild(chips); panel.appendChild(form);

    // Focus trap and Esc while the dialog is open.
    panel.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.preventDefault(); close(); return; }
      if (e.key !== 'Tab') return;
      var f = focusables();
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    root.appendChild(panel);
    root.appendChild(launcher);
    document.body.appendChild(root);
    place();
    window.addEventListener('resize', place);
    setTimeout(place, 1000);
  }

  function start() {
    fetch(API, { method: 'GET', headers: { accept: 'application/json' } })
      .then(function (res) { return res.ok ? res.json() : null; })
      .then(function (data) {
        if (!data || data.ok !== true) return;
        var css = document.createElement('link');
        css.rel = 'stylesheet';
        css.href = '/assets/assistant.css';
        css.onload = build;
        document.head.appendChild(css);
      })
      .catch(function () { /* not configured or offline: stay hidden */ });
  }

  start();
})();
