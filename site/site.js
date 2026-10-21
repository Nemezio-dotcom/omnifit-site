/* OmniFit Performance - shared site script (source: site/site.js).
   The footer year script from pages/footer.html is appended by build.py. */
(function () {
  /* ---- Announcement bar: dismiss for this browser session ---- */
  var bar = document.getElementById('site-announce');
  var KEY = 'omni-announce-dismissed';
  if (bar) {
    try { if (sessionStorage.getItem(KEY) === '1') bar.hidden = true; } catch (e) {}
    var close = bar.querySelector('.site-announce__close');
    if (close) close.addEventListener('click', function () {
      bar.hidden = true;
      try { sessionStorage.setItem(KEY, '1'); } catch (e) {}
    });
  }

  /* ---- Header / primary nav ---- */
  var header = document.getElementById('site-header');
  var toggle = document.querySelector('.site-nav-toggle');
  var nav = document.getElementById('site-nav');
  if (!header || !toggle || !nav) return;

  function mobile() { return window.matchMedia('(max-width: 1099px)').matches; }

  function closeMenus(except) {
    nav.querySelectorAll('.has-menu.is-open').forEach(function (li) {
      if (li !== except) {
        li.classList.remove('is-open');
        var t = li.querySelector('.site-nav__trigger');
        if (t) t.setAttribute('aria-expanded', 'false');
      }
    });
  }

  function setDrawer(open) {
    if (open) {
      /* Drawer starts under the header, wherever the header currently sits. */
      nav.style.top = Math.max(0, Math.round(header.getBoundingClientRect().bottom)) + 'px';
      nav.classList.add('is-open');
      document.body.classList.add('site-nav-open');
    } else {
      nav.classList.remove('is-open');
      nav.style.top = '';
      document.body.classList.remove('site-nav-open');
      closeMenus();
    }
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }

  toggle.addEventListener('click', function () {
    setDrawer(!nav.classList.contains('is-open'));
  });

  /* Dropdowns: tap/click toggles (hover is handled in CSS on pointer devices). */
  nav.querySelectorAll('.site-nav__trigger').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var li = btn.parentNode;
      var open = !li.classList.contains('is-open');
      closeMenus(li);
      li.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  document.addEventListener('click', function (e) {
    if (!nav.contains(e.target) && !toggle.contains(e.target)) closeMenus();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (nav.classList.contains('is-open')) setDrawer(false);
    else closeMenus();
  });

  window.addEventListener('resize', function () {
    if (!mobile() && nav.classList.contains('is-open')) setDrawer(false);
  });
})();

/* ---- Measurement (CANON MEASUREMENT; DEPLOY.md "Measurement") ----
   Every event on the site is sent from here, by delegated listeners and the
   page's data attributes; no page carries a tracking script. window.gtag
   exists only when the site-wide header loaded GA4 (production hostnames,
   or localhost with ?omnifit-track=prod); anywhere else each event is
   logged to the console as "[omnifit-track] <event> <params>".
   Events and params:
     book_consultation_click  any link to calendly.com
                              cta_location, cta_label (text, max 60), cta_position
                              (nav | hero | body | footer | sticky, nearest landmark)
     phone_click / email_click  tel: / mailto: links   cta_location
     generate_lead            HubSpot onFormSubmitted  form_location
     fit_check_start          first answer selected    (no params)
     fit_check_complete       result shown             fit_result (pass | hold),
                              fit_setting (recommended Dial setting, pass only).
                              Individual answers are NEVER sent.
     rates_section_view       /training-rates-san-diego, once per section
                              section (rt-foundation | rt-program | rt-sessions | rt-reset)
     rates_chooser_result     /training-rates-san-diego, each new chooser result
                              format (studio | inhome | virtual), frequency
                              (1x | 2x | 3x | async), couples (true | false),
                              offer (foundation | program | reset)
   cta_location / form_location is the page slug ("home" for /). */
(function () {
  function track(name, params) {
    if (typeof window.gtag === 'function') {
      window.gtag('event', name, params);
    } else {
      try { console.log('[omnifit-track] ' + name + ' ' + JSON.stringify(params)); } catch (e) {}
    }
  }

  var slug = location.pathname.replace(/\/+$/, '').replace(/^\//, '') || 'home';

  function closest(el, sel) {
    return el && el.closest ? el.closest(sel) : null;
  }

  /* Nearest landmark, innermost first. data-cta-position on the link or an
     ancestor overrides the detection. */
  function position(el) {
    var o = closest(el, '[data-cta-position]');
    if (o) return o.getAttribute('data-cta-position');
    if (closest(el, '[class*="sticky"]')) return 'sticky';
    if (closest(el, 'footer')) return 'footer';
    if (closest(el, '#site-header, #site-announce')) return 'nav';
    if (closest(el, '[class*="hero"]')) return 'hero';
    return 'body';
  }

  function label(el) {
    return (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 60);
  }

  function linkHost(a) {
    try { return new URL(a.getAttribute('href'), location.href).hostname.toLowerCase(); } catch (e) { return ''; }
  }

  /* Clicks: Calendly, tel:, mailto: */
  document.addEventListener('click', function (e) {
    var a = closest(e.target, 'a[href]');
    if (!a) return;
    var href = (a.getAttribute('href') || '').trim();
    if (/^tel:/i.test(href)) { track('phone_click', { cta_location: slug }); return; }
    if (/^mailto:/i.test(href)) { track('email_click', { cta_location: slug }); return; }
    var host = linkHost(a);
    if (host === 'calendly.com' || /\.calendly\.com$/.test(host)) {
      track('book_consultation_click', { cta_location: slug, cta_label: label(a), cta_position: position(a) });
    }
  });

  /* HubSpot form submitted (the embed posts a message to the top window). */
  window.addEventListener('message', function (e) {
    var d = e.data;
    if (d && typeof d === 'object' && d.type === 'hsFormCallback' && d.eventName === 'onFormSubmitted') {
      track('generate_lead', { form_location: slug });
    }
  });

  /* Fit Check (pages/fit-check.html, #of-fit). Start = the first answer
     button clicked; complete = the #result section revealed, which the page
     marks with data-fit-result and, on a pass, data-fit-setting. A retake
     that reaches a new result counts as a new start and a new completion. */
  var fit = document.getElementById('of-fit');
  if (fit) {
    var started = false;
    fit.addEventListener('click', function (e) {
      if (!started && closest(e.target, '.opt')) {
        started = true;
        track('fit_check_start', {});
      }
    });
    var result = fit.querySelector('#result');
    if (result && 'MutationObserver' in window) {
      new MutationObserver(function () {
        if (result.hidden) return;
        var verdict = result.getAttribute('data-fit-result');
        if (verdict !== 'pass' && verdict !== 'hold') return;
        var params = { fit_result: verdict };
        if (verdict === 'pass' && result.getAttribute('data-fit-setting')) {
          params.fit_setting = result.getAttribute('data-fit-setting');
        }
        started = false;
        track('fit_check_complete', params);
      }).observe(result, { attributes: true, attributeFilter: ['hidden'] });
    }
  }

  /* Rates page chooser (#rt-ch-result). The page script writes the result's
     params as data attributes and then a new data-ch-key, once per new
     result; an empty key is the "choose both steps" prompt and sends nothing. */
  var chooser = document.getElementById('rt-ch-result');
  if (chooser && 'MutationObserver' in window) {
    new MutationObserver(function () {
      if (!chooser.getAttribute('data-ch-key')) return;
      track('rates_chooser_result', {
        format: chooser.getAttribute('data-ch-format'),
        frequency: chooser.getAttribute('data-ch-frequency'),
        couples: chooser.getAttribute('data-ch-couples') === 'true',
        offer: chooser.getAttribute('data-ch-offer')
      });
    }).observe(chooser, { attributes: true, attributeFilter: ['data-ch-key'] });
  }

  /* Rates page: each ladder section the first time it scrolls into view.
     Each id is on the section's <details>, closed by default, so the summary
     (the section's H2) entering the viewport is the signal, open or not.
     rootMargin trims 20% off the bottom of the viewport, so a section counts
     once its top edge is a fifth of the way up the screen (or its bottom
     edge has entered it), whatever the section's own height. */
  if (slug === 'training-rates-san-diego' && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        track('rates_section_view', { section: en.target.id });
      });
    }, { rootMargin: '0px 0px -20% 0px', threshold: 0 });
    ['rt-foundation', 'rt-program', 'rt-sessions', 'rt-reset'].forEach(function (id) {
      var el = document.getElementById(id);
      if (el) io.observe(el);
    });
  }
})();

/* ---- Expandable sections (<details id="...">, rates page V16) ----
   A link to #id, or a URL hash, that targets a closed <details> (or anything
   inside one) opens it, and every closed <details> around it. The click
   listener runs in the capture phase, so the section is open before any
   page script measures where to scroll. */
(function () {
  function open(id) {
    var el = null;
    try { el = id && document.getElementById(decodeURIComponent(id)); } catch (e) { return; }
    var hidden = false;
    for (var d = el; d; d = d.parentElement) {
      if (d.tagName === 'DETAILS' && !d.open) { d.open = true; if (d !== el) hidden = true; }
    }
    return hidden ? el : null; /* the target was inside a closed section */
  }
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href*="#"]') : null;
    if (!a) return;
    var u;
    try { u = new URL(a.getAttribute('href'), location.href); } catch (err) { return; }
    if (u.hash && u.origin === location.origin && u.pathname === location.pathname) open(u.hash.slice(1));
  }, true);
  function fromHash() {
    var el = location.hash && open(location.hash.slice(1));
    if (el && el.scrollIntoView) el.scrollIntoView();
  }
  window.addEventListener('hashchange', fromHash);
  fromHash();
})();

/* ---- Scrollable tables: reachable by keyboard ----
   A table (or its wrapper) that scrolls sideways (phones, and the hidden
   tables on /outcomes once expanded) gets tabindex="0", role="region" and a label from
   the table caption or the nearest heading above it, so keyboard users can
   focus it and scroll with the arrow keys (WCAG 2.1.1). Wrappers that do not
   overflow are left alone, so desktop gets no extra tab stops. */
(function () {
  function label(el) {
    var cap = el.querySelector('caption');
    if (cap && cap.textContent.trim()) return cap.textContent.trim();
    var n = el;
    while (n && n !== document.body) {
      var p = n.previousElementSibling;
      while (p) {
        if (/^H[1-6]$/.test(p.tagName)) return p.textContent.trim();
        var h = p.querySelectorAll ? p.querySelectorAll('h1,h2,h3,h4,h5,h6') : [];
        if (h.length) return h[h.length - 1].textContent.trim();
        p = p.previousElementSibling;
      }
      n = n.parentElement;
    }
    return 'Table';
  }
  function scan() {
    /* real tables, and the div-grid "tables" some pages use (.bc-table, .of-table) */
    document.querySelectorAll('main table, main [class$="-table"], main [class*="-table "]').forEach(function (t) {
      var el = t;
      while (el && el.tagName !== 'MAIN') {
        var ox = getComputedStyle(el).overflowX;
        if (ox === 'auto' || ox === 'scroll') break;
        el = el.parentElement;
      }
      if (!el || el.tagName === 'MAIN') return;
      var scrolls = el.scrollWidth > el.clientWidth + 1;
      if (scrolls && !el.hasAttribute('tabindex')) {
        el.setAttribute('tabindex', '0');
        el.setAttribute('role', 'region');
        el.setAttribute('aria-label', label(el) + ' (scrollable table)');
        el.setAttribute('data-omni-scroll', '');
      } else if (!scrolls && el.hasAttribute('data-omni-scroll')) {
        el.removeAttribute('tabindex'); el.removeAttribute('role');
        el.removeAttribute('aria-label'); el.removeAttribute('data-omni-scroll');
      }
    });
  }
  var timer;
  function later() { clearTimeout(timer); timer = setTimeout(scan, 150); }
  scan();
  window.addEventListener('load', scan);
  window.addEventListener('resize', later);
  document.addEventListener('click', function (e) {
    if (e.target && e.target.closest && e.target.closest('button,summary')) later();
  });
  document.addEventListener('toggle', later, true);
})();
