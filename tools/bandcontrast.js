// Light-band contrast probe (section bands, Oct 2026), Playwright on the built site.
//
//   python3 build.py && (python3 -m http.server 8765 --directory public --bind 127.0.0.1 &) \
//     && NODE_PATH="$(npm root -g)" node tools/bandcontrast.js public
//
// For every cream or white band (.omni-band--cream / --white, site/site.css) on
// every built page, walks the visible text nodes, composites the computed text
// colour over the nearest painted ancestor background (translucent ones are
// blended over the band) and reports anything under 3:1. It is how the
// hard-coded white text in the shared omni-who block, the --white-as-background
// chart cards on outcomes and the navy table headers were found. Expected
// residue: the seven "0" labels on outcomes' scroll-drawn bar segments.
const fs = require('fs');
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const pub = process.argv[2]; const files = fs.readdirSync(pub).filter(f => f.endsWith('.html')).sort();
  const browser = await chromium.launch(); const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.route(/hubspot|googletagmanager|clarity|calendly|fonts\./, r => r.abort());
  let total = 0;
  for (const f of files) {
    await page.goto('http://127.0.0.1:8765/' + f, { waitUntil: 'domcontentloaded' });
    const res = await page.evaluate(() => {
      const lum = ([r, g, b]) => { const c = [r, g, b].map(v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }); return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]; };
      const parse = s => { const m = s.match(/[\d.]+/g) || []; return [+m[0], +m[1], +m[2], m.length > 3 ? +m[3] : 1]; };
      const blend = (fg, bg) => fg.slice(0, 3).map((v, i) => Math.round(v * fg[3] + bg[i] * (1 - fg[3])));
      const out = []; let n = 0;
      for (const band of document.querySelectorAll('.omni-band--cream,.omni-band--white')) {
        const bg = parse(getComputedStyle(band).backgroundColor);
        const walker = document.createTreeWalker(band, NodeFilter.SHOW_TEXT);
        const seen = new Set(); let t;
        while ((t = walker.nextNode())) {
          if (!t.textContent.trim()) continue; const el = t.parentElement; if (!el || seen.has(el)) continue; seen.add(el);
          const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden' || el.closest('[hidden],details:not([open]) > :not(summary)')) continue;
          const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
          // nearest painted ancestor background inside the band
          let p = el, back = bg; while (p && p !== band) { const b = parse(getComputedStyle(p).backgroundColor); if (b[3] > .5) { back = b[3] > .98 ? b : blend(b, bg).concat([1]); break; } p = p.parentElement; }
          const fg = blend(parse(cs.color), back); const L1 = lum(fg), L2 = lum(back); const cr = (Math.max(L1, L2) + .05) / (Math.min(L1, L2) + .05);
          n++; if (cr < 3) out.push({ sel: el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : ''), text: t.textContent.trim().slice(0, 40), cr: +cr.toFixed(2), color: cs.color });
        }
      }
      return { n, out };
    });
    if (res.out.length) { total += res.out.length; const by = {}; res.out.forEach(o => { by[o.sel] = by[o.sel] || { c: 0, ex: o }; by[o.sel].c++; });
      console.log(`${f}: ${res.out.length}/${res.n} low-contrast`); Object.entries(by).slice(0, 8).forEach(([k, v]) => console.log(`    ${v.c}x ${k}  cr=${v.ex.cr} ${v.ex.color}  "${v.ex.text}"`)); }
  }
  console.log('TOTAL low-contrast text nodes in light bands:', total); await browser.close();
})();
