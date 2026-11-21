// Ask OmniFit widget: each hand-off the server can return draws its button.
//   NODE_PATH="$(npm root -g)" node tools/widgettest.js      (after python3 build.py)
// Serves public/ locally, answers /api/ask itself (GET {ok:true}; POST a fixed
// reply with the hand-off under test) and drives the real widget in Chromium.
// Why it exists (Nov 21 2026): the unit tests cover the server, which returned
// "first_visit" correctly while the widget's own whitelist dropped it, so the
// First Visit button never drew. Only a browser sees that.
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const PUB = path.resolve(__dirname, '..', 'public');
const WANT = {
  first_visit: { text: 'Book Your First Visit', href: 'https://calendly.com/nemezio-omnifittraining/recovery-session-first-visit-assessment-in-home', cls: 'oa-btn oa-btn--gold', target: '_blank' },
  book: { text: 'Book a Consultation', href: 'https://calendly.com/nemezio-omnifittraining/45min', cls: 'oa-btn oa-btn--gold', target: '_blank' },
  fit_check: { text: 'Take the Fit Check', href: '/fit-check', cls: 'oa-btn oa-btn--outline', target: null },
};
const srv = http.createServer((req, res) => {
  const p = decodeURIComponent(req.url.split('?')[0]);
  let f = path.join(PUB, p === '/' ? 'index.html' : p);
  if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) f = path.join(PUB, p + '.html');
  if (!fs.existsSync(f)) { res.statusCode = 404; return res.end('not found'); }
  res.setHeader('Content-Type', { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript' }[path.extname(f)] || 'application/octet-stream');
  res.end(fs.readFileSync(f));
});
(async () => {
  await new Promise((r) => srv.listen(0, '127.0.0.1', r));
  const base = `http://127.0.0.1:${srv.address().port}`;
  const browser = await chromium.launch();
  let failed = 0;
  const cases = Object.keys(WANT).map((h) => [h, h]).concat([['unknown_value', null]]);
  for (const [handoff, expect] of cases) {
    const page = await (await browser.newContext({ viewport: { width: 1280, height: 900 } })).newPage();
    await page.route('**/*', (r) => {
      const u = r.request().url();
      if (u.includes('/api/ask')) {
        const body = r.request().method() === 'GET' ? { ok: true } : { reply: 'Test reply.', handoff, sessionId: 'abcdef12-test' };
        return r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(body) });
      }
      return u.startsWith(base) ? r.continue() : r.abort();
    });
    await page.goto(base + '/fascia-stretch-therapy-san-diego', { waitUntil: 'load' });
    await page.waitForSelector('#ask-omnifit .oa-launcher', { state: 'visible', timeout: 15000 });
    await page.click('#ask-omnifit .oa-launcher');
    await page.fill('#oa-input', 'How do I book?');
    await page.keyboard.press('Enter');
    await page.waitForFunction(() => [...document.querySelectorAll('#ask-omnifit .oa-msg--assistant .oa-bubble')].some((b) => b.textContent === 'Test reply.'), null, { timeout: 10000 });
    const got = await page.evaluate(() => [...document.querySelectorAll('#ask-omnifit .oa-ctas a')].map((a) => ({ text: a.textContent, href: a.getAttribute('href'), cls: a.getAttribute('class'), target: a.getAttribute('target') })));
    const want = expect ? [WANT[expect]] : [];
    const ok = JSON.stringify(got) === JSON.stringify(want);
    if (!ok) failed++;
    console.log(`${ok ? 'PASS' : 'FAIL'}  hand-off "${handoff}": ${expect ? got.map((g) => `${g.text} -> ${g.href}`).join(', ') || 'no button' : (got.length ? 'a button drew' : 'no button, as it should be')}`);
    await page.context().close();
  }
  await browser.close(); srv.close();
  console.log(`RESULT: ${failed ? failed + ' FAILED' : 'PASSED'} (${cases.length} hand-offs)`);
  process.exit(failed ? 1 : 0);
})().catch((e) => { console.error('ERROR', e.message.slice(0, 400)); console.log('RESULT: FAILED (did not complete)'); process.exit(1); });
