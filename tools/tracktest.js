#!/usr/bin/env node
/* Measurement test (CANON MEASUREMENT; DEPLOY.md "Measurement").

   Serves public/ on 127.0.0.1 the way Cloudflare Pages does (/slug ->
   public/slug.html, / -> public/index.html), drives the built site in Chromium and asserts:

     - the production branch runs on the production hostname (mapped to the
       local server with --host-resolver-rules), on localhost only with the
       test override ?omnifit-track=prod, and nowhere else;
     - every event in CANON MEASUREMENT fires with its params (incl. the rates
       chooser's rates_chooser_result, and the rates page's closed sections
       opening from an anchor or a URL hash), as a hit to
       google-analytics.com in production mode and as a "[omnifit-track]"
       console line otherwise;
     - Clarity never loads on /fit-check, and on a non-production host no
       request reaches google-analytics.com, googletagmanager.com or clarity.ms.

   NO HIT REACHES GOOGLE OR MICROSOFT. The request for gtag.js is answered with
   a stub that forwards each gtag('event', ...) to google-analytics.com/g/collect
   in GA4's own shape (en=<event>, ep.<param>=<value>), and every request to
   google-analytics.com, clarity.ms and the HubSpot loaders is intercepted and
   answered locally. Fonts, images and anything else external are blocked.

       python3 build.py
       NODE_PATH="$(npm root -g)" node tools/tracktest.js      # prints the results table

   Needs Node 18+ and the playwright package with Chromium (npm i -g playwright
   && npx playwright install chromium). Exit code 1 if any row fails. */
"use strict";
const http = require("http");
const fs = require("fs");
const path = require("path");

let chromium;
try { ({ chromium } = require("playwright")); } catch (e) {
  console.error("playwright not found: npm i -g playwright && npx playwright install chromium, then run with NODE_PATH=\"$(npm root -g)\"");
  process.exit(2);
}

const ROOT = path.resolve(__dirname, "..");
const PUBLIC = path.join(ROOT, "public");
const GA4 = "G-0K6VLEC2VJ";
const CLARITY = "yzawpvwvdf";
const PROD_HOST = "www.omnifittraining.com";
const PREVIEW_HOST = "preview.omnifit-site.example";
const FLAG = "omnifit-track=prod";

const TYPES = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml",
  ".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp", ".xml": "application/xml", ".txt": "text/plain" };

function serve() {
  return new Promise((resolve) => {
    const srv = http.createServer((req, res) => {
      let p = decodeURIComponent(new URL(req.url, "http://x").pathname);
      if (p.length > 1) p = p.replace(/\/+$/, "");
      const candidates = p === "/" ? [path.join(PUBLIC, "index.html")]
        : [path.join(PUBLIC, p), path.join(PUBLIC, p + ".html")];
      for (const f of candidates) {
        if (f.startsWith(PUBLIC) && fs.existsSync(f) && fs.statSync(f).isFile()) {
          res.writeHead(200, { "content-type": TYPES[path.extname(f)] || "application/octet-stream" });
          return res.end(fs.readFileSync(f));
        }
      }
      res.writeHead(404, { "content-type": "text/html; charset=utf-8" });
      res.end(fs.readFileSync(path.join(PUBLIC, "404.html")));
    });
    srv.listen(0, "127.0.0.1", () => resolve(srv));
  });
}

/* gtag.js stand-in: forwards gtag('event', name, params) as GA4 would. */
function gtagStub(tid) {
  return `(function(){
    var dl = window.dataLayer = window.dataLayer || [];
    function send(args){
      if (!args || args[0] !== 'event') return;
      var params = args[2] || {}, q = ['v=2','tid=${tid}','en=' + encodeURIComponent(args[1])];
      Object.keys(params).forEach(function(k){ q.push('ep.' + encodeURIComponent(k) + '=' + encodeURIComponent(params[k])); });
      fetch('https://www.google-analytics.com/g/collect?' + q.join('&'), {method:'POST', mode:'no-cors', keepalive:true}).catch(function(){});
    }
    for (var i = 0; i < dl.length; i++) send(dl[i]);
    var push = dl.push;
    dl.push = function(a){ var r = push.call(dl, a); send(a); return r; };
  })();`;
}

const rows = [];
let failures = 0;
function assert(area, check, expected, got) {
  const ok = JSON.stringify(expected) === JSON.stringify(got);
  if (!ok) failures++;
  rows.push({ area, check, expected: JSON.stringify(expected), got: JSON.stringify(got), ok });
  return ok;
}

async function newPage(browser, { viewport } = {}) {
  const context = await browser.newContext({ viewport: viewport || { width: 1366, height: 900 } });
  const page = await context.newPage();
  const hits = []; // {kind, url, params}
  const logs = []; // "[omnifit-track] ..." console lines
  const other = new Set();
  await page.addInitScript(() => {
    // No navigation or popups in the test; the site's own listener still runs.
    window.addEventListener("click", (e) => {
      const a = e.target && e.target.closest ? e.target.closest("a[href]") : null;
      if (a) e.preventDefault();
    }, true);
  });
  page.on("console", (m) => { const t = m.text(); if (t.startsWith("[omnifit-track]")) logs.push(t); });
  await page.route("**/*", (route) => {
    const u = new URL(route.request().url());
    const h = u.hostname;
    if (h === "127.0.0.1" || h === "localhost" || h === PROD_HOST || h === PREVIEW_HOST) return route.continue();
    if (h === "www.googletagmanager.com" && u.pathname === "/gtag/js") {
      hits.push({ kind: "gtag.js", url: u.href, id: u.searchParams.get("id") });
      return route.fulfill({ status: 200, contentType: "text/javascript", body: gtagStub(u.searchParams.get("id")) });
    }
    if (/(^|\.)google-analytics\.com$/.test(h)) {
      const params = {};
      u.searchParams.forEach((v, k) => { if (k.startsWith("ep.")) params[k.slice(3)] = v; });
      hits.push({ kind: "ga", url: u.href, event: u.searchParams.get("en"), tid: u.searchParams.get("tid"), params });
      return route.fulfill({ status: 204, body: "" });
    }
    if (h === "www.clarity.ms") {
      hits.push({ kind: "clarity", url: u.href, id: u.pathname.split("/").pop() });
      return route.fulfill({ status: 200, contentType: "text/javascript", body: "" });
    }
    if (h === "js-na2.hs-scripts.com" || h === "js-na2.hsforms.net") {
      hits.push({ kind: "hubspot", url: u.href });
      return route.fulfill({ status: 200, contentType: "text/javascript", body: "" });
    }
    other.add(h);
    return route.abort();
  });
  const ga = () => hits.filter((x) => x.kind === "ga").map((x) => ({ event: x.event, params: x.params }));
  const count = (kind) => hits.filter((x) => x.kind === kind).length;
  const waitFor = async (pred, ms = 4000) => {
    const t0 = Date.now();
    while (Date.now() - t0 < ms) { if (pred()) return true; await page.waitForTimeout(50); }
    return pred();
  };
  const parsedLogs = () => logs.map((l) => {
    const m = l.match(/^\[omnifit-track\] (\S+) (.*)$/);
    return { event: m[1], params: JSON.parse(m[2]) };
  });
  return { context, page, hits, logs, other, ga, count, waitFor, parsedLogs };
}

async function scrollThrough(page, step = 500, pause = 120) {
  const total = await page.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y <= total; y += step) { await page.evaluate((v) => window.scrollTo(0, v), y); await page.waitForTimeout(pause); }
}

async function runFitCheck(page, answers) {
  // answers: array per question; number = option index, {scale: n} = scale value
  await page.click("#of-fit #start");
  for (let i = 0; i < answers.length; i++) {
    const a = answers[i];
    if (typeof a === "number") await page.locator("#of-fit #qbody .opts .opt").nth(a).click();
    else await page.locator(`#of-fit #qbody .scale .opt[data-v="${a.scale}"]`).click();
    await page.click("#of-fit #next");
  }
}

(async () => {
  const srv = await serve();
  const port = srv.address().port;
  const base = (host) => `http://${host}:${port}`;
  const L = base("localhost");
  const browser = await chromium.launch({ args: [`--host-resolver-rules=MAP ${PROD_HOST} 127.0.0.1, MAP ${PREVIEW_HOST} 127.0.0.1`] });

  // ---- 1. Production hostname, no flag: both load; Clarity not on /fit-check
  {
    const t = await newPage(browser);
    await t.page.goto(`${base(PROD_HOST)}/`);
    await t.waitFor(() => t.count("hubspot") > 0, 6000); // the deferred callback has run
    assert("prod host /", "gtag.js requested with the GA4 ID", [GA4], t.hits.filter((x) => x.kind === "gtag.js").map((x) => x.id));
    assert("prod host /", "Clarity tag requested with the project ID", [CLARITY], t.hits.filter((x) => x.kind === "clarity").map((x) => x.id));
    assert("prod host /", "window.gtag is a function", "function", await t.page.evaluate(() => typeof window.gtag));
    assert("prod host /", "no other external host requested", [], [...t.other].filter((h) => !/fonts\.(googleapis|gstatic)\.com|squarespace-cdn\.com/.test(h)));
    await t.context.close();
    const f = await newPage(browser);
    await f.page.goto(`${base(PROD_HOST)}/fit-check`);
    await f.waitFor(() => f.count("hubspot") > 0, 6000);
    assert("prod host /fit-check", "gtag.js requested", 1, f.count("gtag.js"));
    assert("prod host /fit-check", "Clarity NOT requested", 0, f.count("clarity"));
    await f.context.close();
  }

  // ---- 2. localhost + override: homepage clicks (nav, hero, footer, tel, mailto)
  {
    const t = await newPage(browser);
    await t.page.goto(`${L}/?${FLAG}`);
    await t.waitFor(() => t.count("hubspot") > 0, 6000);
    assert("localhost+flag /", "override loads gtag.js and Clarity", { gtag: 1, clarity: 1 }, { gtag: t.count("gtag.js"), clarity: t.count("clarity") });
    await t.page.click("#site-header .site-nav__cta");
    await t.waitFor(() => t.ga().length >= 1);
    assert("localhost+flag /", "nav Calendly click", [{ event: "book_consultation_click", params: { cta_location: "home", cta_label: "Book Your Consultation", cta_position: "nav" } }], t.ga().slice(0, 1));
    await t.page.click("#omni-hero a[href*='calendly.com']");
    await t.waitFor(() => t.ga().length >= 2);
    assert("localhost+flag /", "homepage hero Calendly click", { event: "book_consultation_click", params: { cta_location: "home", cta_label: "Book Your Consultation", cta_position: "hero" } }, t.ga()[1]);
    await t.page.click("#site-announce .site-announce__link");
    await t.waitFor(() => t.ga().length >= 3);
    assert("localhost+flag /", "announcement bar Calendly click is nav", "nav", t.ga()[2] && t.ga()[2].params.cta_position);
    await t.page.click("footer a[href*='calendly.com']");
    await t.waitFor(() => t.ga().length >= 4);
    assert("localhost+flag /", "footer Calendly click", { event: "book_consultation_click", params: { cta_location: "home", cta_label: "Book Your 45-Min Consultation", cta_position: "footer" } }, t.ga()[3]);
    await t.page.click("footer a[href^='tel:']");
    await t.waitFor(() => t.ga().length >= 5);
    assert("localhost+flag /", "tel: click", { event: "phone_click", params: { cta_location: "home" } }, t.ga()[4]);
    await t.page.click("footer a[href^='mailto:']");
    await t.waitFor(() => t.ga().length >= 6);
    assert("localhost+flag /", "mailto: click", { event: "email_click", params: { cta_location: "home" } }, t.ga()[5]);
    await t.page.click("#site-nav a[href='/training-rates-san-diego']");
    await t.page.waitForTimeout(300);
    assert("localhost+flag /", "an internal link sends nothing", 6, t.ga().length);
    assert("localhost+flag /", "every hit carries the GA4 ID", [GA4], [...new Set(t.hits.filter((x) => x.kind === "ga").map((x) => x.tid))]);
    assert("localhost+flag /", "no console fallback lines in production mode", 0, t.logs.length);
    await t.context.close();
  }

  // ---- 3. localhost + override: rates hero click, section views once each
  {
    const t = await newPage(browser);
    await t.page.goto(`${L}/training-rates-san-diego?${FLAG}`);
    await t.page.click(".rt-hero a[href*='calendly.com']");
    await t.waitFor(() => t.ga().length >= 1);
    assert("localhost+flag /training-rates-san-diego", "rates hero Calendly click", { event: "book_consultation_click", params: { cta_location: "training-rates-san-diego", cta_label: "Book Your Consultation", cta_position: "hero" } }, t.ga()[0]);
    const views = () => t.ga().filter((e) => e.event === "rates_section_view").map((e) => e.params.section);
    assert("localhost+flag /training-rates-san-diego", "no section view before scrolling", [], views());
    // Chooser: one rates_chooser_result per new result, nothing before both steps are chosen
    const chooser = () => t.ga().filter((e) => e.event === "rates_chooser_result").map((e) => e.params);
    const pick = (name, value) => t.page.click(`#rt-chooser label:has(input[name="${name}"][value="${value}"])`);
    await pick("rt-ch-format", "studio");
    await t.page.waitForTimeout(200);
    assert("localhost+flag /training-rates-san-diego", "chooser: no event after step 1 alone", [], chooser());
    await pick("rt-ch-freq", "1");
    await t.waitFor(() => chooser().length >= 1);
    await t.page.click("#rt-chooser .rt-ch-couples");
    await t.waitFor(() => chooser().length >= 2);
    await pick("rt-ch-format", "inhome");
    await pick("rt-ch-freq", "3");
    await t.waitFor(() => chooser().length >= 4);
    await pick("rt-ch-format", "virtual");
    await t.page.waitForTimeout(200);
    const beforeTier = chooser().length;
    await pick("rt-ch-tier", "async");
    await t.waitFor(() => chooser().length >= beforeTier + 1);
    await pick("rt-ch-tier", "async"); // same result again: nothing new
    await t.page.waitForTimeout(200);
    assert("localhost+flag /training-rates-san-diego", "chooser: rates_chooser_result per new result, params format/frequency/couples/offer", [
      { format: "studio", frequency: "1x", couples: "false", offer: "foundation" },
      { format: "studio", frequency: "1x", couples: "true", offer: "foundation" },
      { format: "inhome", frequency: "1x", couples: "true", offer: "foundation" },
      { format: "inhome", frequency: "3x", couples: "true", offer: "program" },
      { format: "virtual", frequency: "async", couples: "false", offer: "reset" },
    ], chooser());
    assert("localhost+flag /training-rates-san-diego", "chooser: switching to virtual before a tier sends nothing", 4, beforeTier);
    assert("localhost+flag /training-rates-san-diego", "chooser clicks send no section view", [], views());
    const xsecOpen = () => t.page.evaluate(() => [...document.querySelectorAll("details.rt-xsec")].map((d) => d.id + ":" + d.open));
    assert("localhost+flag /training-rates-san-diego", "seven expandable sections, closed by default", ["rt-foundation:false", "rt-program:false", "rt-sessions:false", "rt-tuneup:false", "rt-reset:false", "rt-change:false", "rt-dial:false"], await xsecOpen());
    await scrollThrough(t.page);
    await t.page.waitForTimeout(300);
    assert("localhost+flag /training-rates-san-diego", "rates scroll: four sections, in page order", ["rt-foundation", "rt-program", "rt-sessions", "rt-reset"], views());
    await t.page.evaluate(() => window.scrollTo(0, 0));
    await scrollThrough(t.page, 800, 60);
    await t.page.waitForTimeout(300);
    assert("localhost+flag /training-rates-san-diego", "second scroll adds nothing (once per section)", 4, views().length);
    assert("localhost+flag /training-rates-san-diego", "scrolling past opens nothing", 0, (await xsecOpen()).filter((x) => x.endsWith(":true")).length);
    await t.page.click(".rt-jump a[href='#rt-foundation']");
    await t.page.waitForTimeout(300);
    assert("localhost+flag /training-rates-san-diego", "jump-bar anchor opens the closed Foundation section", true, await t.page.evaluate(() => document.getElementById("rt-foundation").open));
    await t.page.click("#omni-rates a[href*='calendly.com']:has-text('Start With the Foundation')");
    await t.waitFor(() => t.ga().filter((e) => e.event === "book_consultation_click").length >= 2);
    assert("localhost+flag /training-rates-san-diego", "Foundation ladder CTA (below the section head) is body", { event: "book_consultation_click", params: { cta_location: "training-rates-san-diego", cta_label: "Start With the Foundation", cta_position: "body" } }, t.ga().filter((e) => e.event === "book_consultation_click")[1]);
    await t.context.close();
    const h = await newPage(browser);
    await h.page.goto(`${L}/training-rates-san-diego#rt-program`);
    await h.page.waitForTimeout(300);
    assert("localhost /training-rates-san-diego#rt-program", "a URL hash opens its closed section, and only that one", ["rt-program"], await h.page.evaluate(() => [...document.querySelectorAll("details.rt-xsec")].filter((d) => d.open).map((d) => d.id)));
    await h.page.click("#rt-chooser label:has(input[value='virtual'])");
    await h.page.click("#rt-chooser label:has(input[name='rt-ch-tier'][value='1'])");
    await h.page.click("#rt-ch-result a.rt-ch-more");
    await h.page.waitForTimeout(300);
    assert("localhost /training-rates-san-diego#rt-program", "the result's section link opens the Executive Reset section", true, await h.page.evaluate(() => document.getElementById("rt-reset").open));
    await h.context.close();
  }

  // ---- 4. localhost + override: Fit Check to PASS (no Clarity)
  {
    const t = await newPage(browser);
    await t.page.goto(`${L}/fit-check?${FLAG}`);
    await t.waitFor(() => t.count("hubspot") > 0, 6000);
    assert("localhost+flag /fit-check", "Clarity NOT requested on /fit-check", 0, t.count("clarity"));
    assert("localhost+flag /fit-check", "GA4 still loads on /fit-check", 1, t.count("gtag.js"));
    await t.page.click("#of-fit #start");
    assert("localhost+flag /fit-check", "nothing sent on Start", [], t.ga());
    await t.page.locator("#of-fit #qbody .opts .opt").nth(2).click();
    await t.waitFor(() => t.ga().length >= 1);
    assert("localhost+flag /fit-check", "fit_check_start on the first answer, no params", [{ event: "fit_check_start", params: {} }], t.ga());
    await t.page.locator("#of-fit #qbody .opts .opt").nth(3).click(); // change the answer
    await t.page.click("#of-fit #next");
    for (const a of [{ scale: 9 }, 0, 0, 0, 1, { scale: 9 }]) {
      if (typeof a === "number") await t.page.locator("#of-fit #qbody .opts .opt").nth(a).click();
      else await t.page.locator(`#of-fit #qbody .scale .opt[data-v="${a.scale}"]`).click();
      await t.page.click("#of-fit #next");
    }
    await t.waitFor(() => t.ga().length >= 2);
    assert("localhost+flag /fit-check", "pass: fit_check_complete with result and setting only", [{ event: "fit_check_start", params: {} }, { event: "fit_check_complete", params: { fit_result: "pass", fit_setting: "Coached" } }], t.ga());
    assert("localhost+flag /fit-check", "result section visible, verdict pass", true, await t.page.evaluate(() => !document.querySelector("#of-fit #result").hidden && !!document.querySelector("#of-fit .verdict.pass")));
    await t.page.click("#of-fit #result a[href*='calendly.com']");
    await t.waitFor(() => t.ga().length >= 3);
    assert("localhost+flag /fit-check", "result Book button click", { event: "book_consultation_click", params: { cta_location: "fit-check", cta_label: "Book Your Consultation", cta_position: "body" } }, t.ga()[2]);
    // Retake -> a new start and a new completion (hold this time)
    await t.page.click("#of-fit #redo");
    await runFitCheck(t.page, [0, { scale: 9 }, 0, 0, 0, 0, { scale: 9 }]);
    await t.waitFor(() => t.ga().length >= 5);
    assert("localhost+flag /fit-check", "retake: start again, then hold with no setting", [{ event: "fit_check_start", params: {} }, { event: "fit_check_complete", params: { fit_result: "hold" } }], t.ga().slice(3));
    await t.context.close();
  }

  // ---- 5. localhost + override: Fit Check to HOLD in a fresh session
  {
    const t = await newPage(browser);
    await t.page.goto(`${L}/fit-check?${FLAG}`);
    await runFitCheck(t.page, [2, { scale: 9 }, 3, 0, 0, 2, { scale: 9 }]); // budget "Money's tight" = fail on Able
    await t.waitFor(() => t.ga().length >= 2);
    assert("localhost+flag /fit-check (hold)", "hold: start once, complete with fit_result hold only", [{ event: "fit_check_start", params: {} }, { event: "fit_check_complete", params: { fit_result: "hold" } }], t.ga());
    assert("localhost+flag /fit-check (hold)", "no param on any hit names an answer", [], t.hits.filter((x) => x.kind === "ga").flatMap((x) => Object.keys(x.params)).filter((k) => !["fit_result", "fit_setting"].includes(k)));
    assert("localhost+flag /fit-check (hold)", "hold result shown", true, await t.page.evaluate(() => !!document.querySelector("#of-fit .verdict.hold")));
    await t.context.close();
  }

  // ---- 6. localhost + override: HubSpot form submitted on /contactform
  {
    const t = await newPage(browser);
    await t.page.goto(`${L}/contactform?${FLAG}`);
    await t.page.evaluate(() => window.postMessage({ type: "hsFormCallback", eventName: "onFormReady", id: "x" }, "*"));
    await t.page.evaluate(() => window.postMessage("hsFormCallback onFormSubmitted", "*"));
    await t.page.waitForTimeout(300);
    assert("localhost+flag /contactform", "onFormReady and a string message send nothing", [], t.ga());
    await t.page.evaluate(() => window.postMessage({ type: "hsFormCallback", eventName: "onFormSubmitted", id: "x" }, "*"));
    await t.waitFor(() => t.ga().length >= 1);
    assert("localhost+flag /contactform", "HubSpot onFormSubmitted -> generate_lead", [{ event: "generate_lead", params: { form_location: "contactform" } }], t.ga());
    await t.context.close();
  }

  // ---- 7. localhost + override, phone viewport: 4S Ranch sticky bar
  {
    const t = await newPage(browser, { viewport: { width: 390, height: 844 } });
    await t.page.goto(`${L}/personal-trainer-4s-ranch?${FLAG}`);
    await t.page.click(".sticky-bar-4sr a[href*='calendly.com']");
    await t.page.click(".sticky-bar-4sr a[href^='tel:']");
    await t.waitFor(() => t.ga().length >= 2);
    assert("localhost+flag /personal-trainer-4s-ranch (390px)", "sticky bar Calendly click", { event: "book_consultation_click", params: { cta_location: "personal-trainer-4s-ranch", cta_label: "Book 45-Min Consult", cta_position: "sticky" } }, t.ga()[0]);
    assert("localhost+flag /personal-trainer-4s-ranch (390px)", "sticky bar tel: click", { event: "phone_click", params: { cta_location: "personal-trainer-4s-ranch" } }, t.ga()[1]);
    assert("localhost+flag /personal-trainer-4s-ranch (390px)", "no page-level tracking script remains in <main>", 0, await t.page.evaluate(() => [...document.querySelectorAll("main script")].filter((s) => /gtag\(|dataLayer|lead_form_submit|cta_click/.test(s.textContent)).length));
    await t.context.close();
  }

  // ---- 8. Non-production host (localhost, no flag): nothing loads, console only
  {
    const t = await newPage(browser);
    await t.page.goto(`${L}/`);
    await t.waitFor(() => t.count("hubspot") > 0, 6000);
    assert("localhost no flag /", "no request to googletagmanager.com, google-analytics.com or clarity.ms", { gtag: 0, ga: 0, clarity: 0 }, { gtag: t.count("gtag.js"), ga: t.count("ga"), clarity: t.count("clarity") });
    assert("localhost no flag /", "HubSpot still loads", 1, t.count("hubspot"));
    assert("localhost no flag /", "window.gtag undefined", "undefined", await t.page.evaluate(() => typeof window.gtag));
    await t.page.click("#site-header .site-nav__cta");
    await t.page.click("footer a[href^='tel:']");
    await t.waitFor(() => t.logs.length >= 2);
    assert("localhost no flag /", "console line per event", ["[omnifit-track] book_consultation_click {\"cta_location\":\"home\",\"cta_label\":\"Book Your Consultation\",\"cta_position\":\"nav\"}", "[omnifit-track] phone_click {\"cta_location\":\"home\"}"], t.logs);
    assert("localhost no flag /", "still no request to either service after events", 0, t.count("ga") + t.count("clarity"));
    await t.context.close();
    const r = await newPage(browser);
    await r.page.goto(`${L}/training-rates-san-diego`);
    await scrollThrough(r.page, 800, 60);
    await r.page.waitForTimeout(300);
    await r.page.click("#rt-chooser label:has(input[value='studio'])");
    await r.page.click("#rt-chooser label:has(input[name='rt-ch-freq'][value='2'])");
    await r.waitFor(() => r.parsedLogs().some((e) => e.event === "rates_chooser_result"));
    assert("localhost no flag /training-rates-san-diego", "chooser result logged to the console with boolean couples, no requests", { logged: [{ format: "studio", frequency: "2x", couples: false, offer: "foundation" }], ga: 0 }, { logged: r.parsedLogs().filter((e) => e.event === "rates_chooser_result").map((e) => e.params), ga: r.count("ga") });
    assert("localhost no flag /training-rates-san-diego", "section views logged to the console, no requests", { logged: ["rt-foundation", "rt-program", "rt-sessions", "rt-reset"], ga: 0, clarity: 0 }, { logged: r.parsedLogs().filter((e) => e.event === "rates_section_view").map((e) => e.params.section), ga: r.count("ga"), clarity: r.count("clarity") });
    await r.context.close();
    const f = await newPage(browser);
    await f.page.goto(`${L}/fit-check`);
    await runFitCheck(f.page, [2, { scale: 9 }, 0, 0, 0, 0, { scale: 9 }]);
    await f.waitFor(() => f.logs.length >= 2);
    assert("localhost no flag /fit-check", "Fit Check events logged to the console, no requests", { logged: [{ event: "fit_check_start", params: {} }, { event: "fit_check_complete", params: { fit_result: "pass", fit_setting: "Full Accountability" } }], ga: 0, clarity: 0, gtag: 0 }, { logged: f.parsedLogs(), ga: f.count("ga"), clarity: f.count("clarity"), gtag: f.count("gtag.js") });
    await f.context.close();
  }

  // ---- 9. The override is honoured on localhost only
  {
    const t = await newPage(browser);
    await t.page.goto(`${base(PREVIEW_HOST)}/?${FLAG}`);
    await t.waitFor(() => t.count("hubspot") > 0, 6000);
    assert("preview host + flag /", "flag ignored off localhost: nothing loads", { gtag: 0, clarity: 0, gtagType: "undefined" }, { gtag: t.count("gtag.js"), clarity: t.count("clarity"), gtagType: await t.page.evaluate(() => typeof window.gtag) });
    await t.context.close();
    const u = await newPage(browser);
    await u.page.goto(`${base("127.0.0.1")}/?${FLAG}`);
    await u.waitFor(() => u.count("hubspot") > 0, 6000);
    assert("127.0.0.1 + flag /", "flag honoured on 127.0.0.1 too", { gtag: 1, clarity: 1 }, { gtag: u.count("gtag.js"), clarity: u.count("clarity") });
    await u.context.close();
  }

  await browser.close();
  srv.close();

  console.log("| # | Where | Check | Expected | Got | Result |");
  console.log("|---|---|---|---|---|---|");
  rows.forEach((r, i) => {
    const esc = (s) => s.replace(/\|/g, "\\|");
    console.log(`| ${i + 1} | ${r.area} | ${r.check} | \`${esc(r.expected)}\` | \`${esc(r.got)}\` | ${r.ok ? "PASS" : "**FAIL**"} |`);
  });
  console.log(`\nRESULT: ${failures === 0 ? "PASSED" : failures + " FAILED"} (${rows.length} assertions)`);
  process.exit(failures ? 1 : 0);
})().catch((e) => { console.error("tracktest aborted:", e); process.exit(1); });
