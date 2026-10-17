// Mobile layout audit (CANON LAUNCH DECISIONS item 22), Playwright on the built site.
//
//   python3 build.py && NODE_PATH="$(npm root -g)" node tools/mobileaudit.js [path ...] [--shots DIR]
//
// Serves public/ on a local port and loads each page (default: every built
// page) at 390x900 and 412x900 (isMobile). For each page and width it reports:
//   - document scrollWidth wider than the viewport;
//   - every visible grid item (child of a display:grid element) or element
//     whose class names a card, narrower than 240px ("narrow");
//   - content clipped past the viewport edge. site.css gives <main>
//     overflow-x:clip, so scrollWidth cannot see overflow inside main; an
//     element whose right edge passes the viewport is reported unless a
//     scrollable (auto/scroll) ancestor contains it ("clipped"). Decorative
//     layers marked aria-hidden="true" (the hero's zoomed photo frames) are
//     cropped by design and are not content, so they are not reported.
// Exit 1 when any page has a scrollWidth overflow or a clipped element.
// Narrow items are printed for review (2-up tiles and table cells are narrow
// by design); the caller decides. Re-created in the homepage rebuild run
// (Oct 17 2026) from the method recorded in REPORT.md, item 22.
const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', 'public');
const args = process.argv.slice(2);
const shotsAt = args.indexOf('--shots');
const SHOTS = shotsAt > -1 ? args[shotsAt + 1] : null;
const only = args.filter((a, i) => !a.startsWith('--') && (shotsAt === -1 || i !== shotsAt + 1));
const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml', '.xml': 'text/xml', '.txt': 'text/plain' };

function serve() {
  return new Promise(res => {
    const srv = http.createServer((req, rsp) => {
      let p = decodeURIComponent(req.url.split('?')[0]);
      let f = path.join(ROOT, p);
      if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
      if (!fs.existsSync(f)) { rsp.writeHead(404); rsp.end(); return; }
      rsp.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' });
      fs.createReadStream(f).pipe(rsp);
    }).listen(0, '127.0.0.1', () => res(srv));
  });
}

function pages() {
  if (only.length) return only;
  const out = [];
  (function walk(d, rel) {
    for (const n of fs.readdirSync(d)) {
      const f = path.join(d, n);
      if (fs.statSync(f).isDirectory()) { if (n !== 'assets') walk(f, rel + n + '/'); }
      else if (n === 'index.html') out.push('/' + rel);
    }
  })(ROOT, '');
  return out.sort();
}

(async () => {
  const srv = await serve();
  const base = `http://127.0.0.1:${srv.address().port}`;
  const browser = await chromium.launch({ executablePath: process.env.PW_CHROMIUM || undefined });
  let failed = 0;
  for (const width of [390, 412]) {
    const ctx = await browser.newContext({ viewport: { width, height: 900 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
    const page = await ctx.newPage();
    for (const p of pages()) {
      await page.goto(base + p, { waitUntil: 'load' });
      // reveal everything the scroll-reveal layer hid, so measurements see the final layout
      await page.evaluate(() => { document.querySelectorAll('.omni-rv').forEach(e => e.classList.add('is-in')); });
      await page.waitForTimeout(150);
      const r = await page.evaluate(() => {
        const vw = window.innerWidth;
        const vis = e => { const s = getComputedStyle(e); const b = e.getBoundingClientRect(); return s.display !== 'none' && s.visibility !== 'hidden' && b.width > 0 && b.height > 0; };
        const label = e => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (typeof e.className === 'string' && e.className.trim() ? '.' + e.className.trim().split(/\s+/).join('.') : '');
        const narrow = [], clipped = [];
        for (const e of document.querySelectorAll('main *')) {
          if (!vis(e)) continue;
          const parent = e.parentElement;
          const isCard = (parent && getComputedStyle(parent).display.includes('grid')) || /card/i.test(typeof e.className === 'string' ? e.className : '');
          if (isCard && e.offsetWidth < 240) narrow.push(`${label(e)} ${e.offsetWidth}px`);
          const b = e.getBoundingClientRect();
          if (b.right > vw + 1 && b.width < vw * 3 && !e.closest('[aria-hidden="true"]')) {
            let a = e.parentElement, scroller = false;
            while (a && a !== document.body) { const o = getComputedStyle(a).overflowX; if (o === 'auto' || o === 'scroll') { scroller = true; break; } a = a.parentElement; }
            if (!scroller) clipped.push(`${label(e)} right=${Math.round(b.right)}`);
          }
        }
        return { sw: document.documentElement.scrollWidth, vw, narrow, clipped };
      });
      const bad = r.sw > r.vw || r.clipped.length;
      if (bad) failed++;
      console.log(`${width}  ${p.padEnd(44)} scrollWidth ${r.sw}/${r.vw}  narrow ${r.narrow.length}  clipped ${r.clipped.length}  ${bad ? 'FAIL' : 'ok'}`);
      for (const n of r.narrow) console.log(`        narrow   ${n}`);
      for (const c of r.clipped.slice(0, 12)) console.log(`        clipped  ${c}`);
    }
    if (SHOTS) {
      fs.mkdirSync(SHOTS, { recursive: true });
      await page.goto(base + '/', { waitUntil: 'load' });
      await page.evaluate(() => { document.querySelectorAll('.omni-rv').forEach(e => e.classList.add('is-in')); document.querySelectorAll('#omni-hero .hero-content, #omni-hero .hero-content *').forEach(e => { e.style.animation = 'none'; e.style.opacity = '1'; }); });
      await page.waitForTimeout(400);
      await page.locator('#omni-hero').screenshot({ path: path.join(SHOTS, `home-hero-${width}.png`) });
      await page.locator('#omh-short').screenshot({ path: path.join(SHOTS, `home-in-short-${width}.png`) });
    }
    await ctx.close();
  }
  await browser.close(); srv.close();
  console.log(failed ? `RESULT: FAILED (${failed} page/width with overflow or clipped content)` : 'RESULT: PASSED');
  process.exit(failed ? 1 : 0);
})();
