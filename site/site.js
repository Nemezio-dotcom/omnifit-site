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

  function mobile() { return window.matchMedia('(max-width: 1023px)').matches; }

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
