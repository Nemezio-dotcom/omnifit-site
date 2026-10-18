#!/usr/bin/env node
/* Rates-page chooser test (training-rates-san-diego V16), Playwright on the
   built site.

       python3 build.py
       NODE_PATH="$(npm root -g)" node tools/choosertest.js [--shots DIR]

   1. CARD: every combination (studio / in-home x 1x / 2x / 3x x individual /
      couples, and the four virtual Reset tiers) is selected in the page and
      the rendered result is compared with figures parsed from CANON.md's
      OCTOBER 2026 CARD - not from the page's data attributes, so a wrong data
      attribute fails here. Prints the table REPORT.md carries.
   2. KEYBOARD AND ARIA: the steps are radio groups with legends, the result
      is an aria-live region, and the chooser is operable with Tab, arrows
      and Space alone.
   3. LAYOUT at 390 and 412px (isMobile): in every state, no chooser element
      passes the viewport edge and no text box is cut off inside its own box.
   4. --shots DIR: the chooser at 390px in three states (studio 1x, in-home
      2x, virtual).
   Exit 1 on any failure. */
"use strict";
const http = require("http");
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const PUBLIC = path.join(ROOT, "public");
const args = process.argv.slice(2);
const SHOTS = args.includes("--shots") ? args[args.indexOf("--shots") + 1] : null;
const TYPES = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml",
  ".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp" };

/* ---- CANON.md, OCTOBER 2026 CARD ---- */
function card() {
  const t = fs.readFileSync(path.join(ROOT, "CANON.md"), "utf8");
  const sec = (from, to) => { const a = t.indexOf(from), b = t.indexOf(to, a); if (a < 0 || b < 0) throw new Error(`CANON section not found: ${from}`); return t.slice(a, b); };
  const n = (s) => Number(s.replace(/,/g, ""));
  const key = (place, couples, tier) => `${couples ? "couples-" : ""}${place === "Studio" ? "studio" : "inhome"}-${{ Momentum: 1, Performance: 2, Peak: 3 }[tier]}`;
  const foundation = {}, program = {}, from = {};
  const f = sec("THE FOUNDATION - new clients only", "NOT offered on the Foundation");
  for (const m of f.matchAll(/^\s+(Studio|In-home)( couples)? (Momentum|Performance|Peak)(?: \(\dx\/wk\))?\s+([\d,]+)\/cycle\s+([\d,]+) total\s*$/gm)) {
    foundation[key(m[1], m[2], m[3])] = { cycle: n(m[4]), total: n(m[5]) };
  }
  const p = sec("THE PROGRAM - continuation", "Couples Peak: by arrangement.");
  for (const m of p.matchAll(/^\s+(Studio|In-home)( couples)? (Momentum|Performance|Peak)(?: \(\dx\/wk\))?\s+(from )?([\d,]+)\s*$/gm)) {
    program[key(m[1], m[2], m[3])] = n(m[5]);
    if (m[4]) from[key(m[1], m[2], m[3])] = true;
  }
  const words = { two: 2, three: 3, four: 4 };
  const fc = f.match(/(\w+) consecutive (\d+)-week cycles/i);
  const r = t.match(/Bronze async ([\d,]+) · Gold 1x\/wk ([\d,]+) ·\s+Platinum 2x\/wk ([\d,]+) · Black 3x\/wk ([\d,]+)/);
  const a = t.match(/Performance Assessment \$(\d+)/);
  const m = t.match(/Teqneeq membership \(\$(\d+)\/mo/);
  // CANONICAL FACTS (Oct 17 2026): the remote clients' assessment price.
  const va = t.match(/VIRTUAL PERFORMANCE ASSESSMENT[\s\S]*?\$(\d+), credited/);
  if (!fc || !r || !a || !m || !va || !t.includes("Couples Peak: by arrangement.")) throw new Error("CANON card lines not parsed");
  if (Object.keys(foundation).length !== 5 || Object.keys(program).length !== 10) throw new Error(`CANON card parsed ${Object.keys(foundation).length} Foundation / ${Object.keys(program).length} Program rows, expected 5 / 10`);
  return { foundation, program, from, cycles: words[fc[1].toLowerCase()], weeks: Number(fc[2]),
    reset: { async: n(r[1]), 1: n(r[2]), 2: n(r[3]), 3: n(r[4]) }, assessment: Number(a[1]), membership: Number(m[1]), virtualAssessment: Number(va[1]) };
}

const money = (x) => "$" + x.toLocaleString("en-US");

/* What the result must say for one combination, derived from the card. */
function expected(C, format, freq, couples) {
  const must = [], mustNot = [];
  let offer, summary;
  must.push(`${C.weeks}-week cycles = ${Math.round(52 / C.weeks)} per year, never billed by the calendar month.`);
  const member = `Plus Teqneeq membership, ${money(C.membership)}/month, billed by Teqneeq.`;
  if (format === "virtual") {
    offer = "reset";
    must.push(`${money(C.reset[freq])}per 4-week cycle`);
    summary = `Reset ${money(C.reset[freq])} per 4-week cycle`;
    mustNot.push("Teqneeq membership");
    must.push(`How remote clients are assessed: the ${money(C.virtualAssessment)} Virtual Performance Assessment`, "no Bodystat scan");
  } else {
    const k = `${couples ? "couples-" : ""}${format}-${freq}`;
    const F = C.foundation[k], P = C.program[k], from = C.from[k] ? "from " : "";
    must.push(`${C.weeks * Number(freq)} sessions per cycle`);
    if (F) {
      offer = "foundation";
      const total = F.cycle * C.cycles, due = total - C.assessment;
      must.push(`${money(total)}Foundation total: ${C.cycles} cycles, one payment`, `${money(F.cycle)}per 4-week cycle`,
        `Due at signup after your ${money(C.assessment)} assessment credit: ${money(due)}`, `Then The Program at ${money(P)} per 4 weeks.`);
      summary = `Foundation ${money(total)} (${money(F.cycle)} x ${C.cycles}); due ${money(due)}; then Program ${money(P)}`;
    } else if (P) {
      offer = "program";
      must.push(`Starts directly on The Program ${from || "at "}${money(P)} per 4 weeks.`);
      if (from) must.push(`Your ${money(C.assessment)} assessment credit comes off the first cycle.`);
      else must.push(`Your ${money(C.assessment)} assessment credit comes off the first cycle: ${money(P - C.assessment)} due.`);
      summary = `Program ${from}${money(P)}` + (from ? "; credit off cycle 1" : `; cycle 1 after credit ${money(P - C.assessment)}`);
    } else {
      offer = "program";
      must.push("Couples Peak on The Program is by arrangement.", `Your ${money(C.assessment)} assessment credit comes off the first cycle.`);
      summary = "Program, Couples Peak by arrangement";
    }
    if (format === "studio") must.push(member); else mustNot.push("Teqneeq membership");
    mustNot.push("Virtual Performance Assessment");
    if (couples) must.push("Priced per couple, not per person.");
  }
  return { must, mustNot, offer, summary };
}

function serve() {
  return new Promise((resolve) => {
    const srv = http.createServer((req, res) => {
      let p = decodeURIComponent(new URL(req.url, "http://x").pathname);
      if (p.length > 1) p = p.replace(/\/+$/, "");
      // Cloudflare Pages layout: / -> index.html, /<slug> -> <slug>.html.
      const cands = p === "/" ? [path.join(PUBLIC, "index.html")] : [path.join(PUBLIC, p), path.join(PUBLIC, p + ".html")];
      for (const f of cands) {
        if (f.startsWith(PUBLIC) && fs.existsSync(f) && fs.statSync(f).isFile()) {
          res.writeHead(200, { "content-type": TYPES[path.extname(f)] || "application/octet-stream" });
          return res.end(fs.readFileSync(f));
        }
      }
      res.writeHead(404); res.end();
    });
    srv.listen(0, "127.0.0.1", () => resolve(srv));
  });
}

const rows = [];
let failures = 0;
function check(area, what, ok, detail) {
  if (!ok) failures++;
  rows.push({ area, what, ok, detail: detail || "" });
}

async function choose(page, format, freq, couples) {
  await page.click(`#rt-chooser label:has(input[name="rt-ch-format"][value="${format}"])`);
  const group = format === "virtual" ? "rt-ch-tier" : "rt-ch-freq";
  await page.click(`#rt-chooser label:has(input[name="${group}"][value="${freq}"])`);
  if (format !== "virtual") {
    const on = await page.isChecked("#rt-ch-couples");
    if (on !== couples) await page.click("#rt-chooser .rt-ch-couples");
  }
}

async function layout(page) {
  return page.evaluate(() => {
    const vw = document.documentElement.clientWidth, bad = [];
    for (const e of document.querySelectorAll("#rt-choose *")) {
      const s = getComputedStyle(e), b = e.getBoundingClientRect();
      if (s.display === "none" || s.visibility === "hidden" || !b.width || e.closest("[hidden]")) continue;
      if (e.tagName === "INPUT") continue; // radios are full-tile transparent overlays
      const name = e.tagName.toLowerCase() + (e.className && typeof e.className === "string" ? "." + e.className.trim().split(/\s+/).join(".") : "");
      if (b.right > vw + 0.5 || b.left < -0.5) bad.push(`${name} [${Math.round(b.left)}, ${Math.round(b.right)}] past viewport ${vw}`);
      if (e.scrollWidth > e.clientWidth + 1 && s.overflowX !== "visible" && e.clientWidth) bad.push(`${name} cut off (${e.scrollWidth} > ${e.clientWidth})`);
      if (e.children.length === 0 && e.textContent.trim() && e.scrollWidth > b.width + 1) bad.push(`${name} text wider than its box`);
    }
    return { bad, sw: document.documentElement.scrollWidth, vw };
  });
}

(async () => {
  const C = card();
  const srv = await serve();
  const URL0 = `http://127.0.0.1:${srv.address().port}/training-rates-san-diego`;
  const browser = await chromium.launch({ executablePath: process.env.PW_CHROMIUM || undefined });
  const combos = [];
  for (const format of ["studio", "inhome"]) for (const couples of [false, true]) for (const freq of ["1", "2", "3"]) combos.push([format, freq, couples]);
  for (const freq of ["async", "1", "2", "3"]) combos.push(["virtual", freq, false]);

  /* 1. card */
  const table = [];
  {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await ctx.newPage();
    await page.goto(URL0);
    check("static", "chooser UI shown when JS runs", await page.isVisible("#rt-chooser .rt-ch-ui"));
    for (const [format, freq, couples] of combos) {
      await choose(page, format, freq, couples);
      const got = await page.evaluate(() => {
        const r = document.getElementById("rt-ch-result");
        return { text: r.innerText.replace(/\s*\n\s*/g, "\n"), flat: r.textContent.replace(/\s+/g, " "),
          attrs: { format: r.getAttribute("data-ch-format"), frequency: r.getAttribute("data-ch-frequency"), couples: r.getAttribute("data-ch-couples"), offer: r.getAttribute("data-ch-offer") } };
      });
      const exp = expected(C, format, freq, couples);
      const missing = exp.must.filter((s) => !got.flat.includes(s));
      const extra = exp.mustNot.filter((s) => got.flat.includes(s));
      const freqParam = freq === "async" ? "async" : freq + "x";
      const attrsOk = got.attrs.format === format && got.attrs.frequency === freqParam && got.attrs.couples === String(couples) && got.attrs.offer === exp.offer;
      const ok = !missing.length && !extra.length && attrsOk;
      const label = `${format} ${format === "virtual" ? { async: "Bronze", 1: "Gold", 2: "Platinum", 3: "Black" }[freq] : freqParam}${couples ? " couples" : ""}`;
      check("card", label, ok, [missing.length ? "missing: " + missing.join(" | ") : "", extra.length ? "unexpected: " + extra.join(" | ") : "", attrsOk ? "" : "attrs " + JSON.stringify(got.attrs)].filter(Boolean).join("; "));
      table.push({ label, offer: got.attrs.offer, shown: got.text.split("\n").filter((l) => /\$|arrangement/.test(l)).join(" · "), canon: exp.summary, ok });
    }
    await ctx.close();
  }

  /* 2. keyboard and ARIA */
  {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
    const page = await ctx.newPage();
    await page.goto(URL0);
    const aria = await page.evaluate(() => {
      const r = document.getElementById("rt-ch-result");
      const sets = [...document.querySelectorAll("#rt-chooser fieldset")];
      const radios = [...document.querySelectorAll('#rt-chooser input[type="radio"]')];
      return { live: r.getAttribute("aria-live"), legends: sets.map((f) => !!f.querySelector("legend") && f.querySelector("legend").textContent.trim().length > 0),
        labelled: radios.every((i) => i.closest("label") && i.closest("label").textContent.trim().length > 0),
        sw: document.getElementById("rt-ch-couples").getAttribute("role"), swLabel: document.getElementById("rt-ch-couples").closest("label").textContent.trim() };
    });
    check("aria", "result region is aria-live polite", aria.live === "polite", aria.live);
    check("aria", "both steps are fieldsets with a legend", aria.legends.length === 2 && aria.legends.every(Boolean), JSON.stringify(aria.legends));
    check("aria", "every radio is labelled by its tile", aria.labelled);
    check("aria", "couples toggle is a labelled switch", aria.sw === "switch" && aria.swLabel === "Training as a couple?", aria.swLabel);
    await page.focus('#rt-chooser input[name="rt-ch-format"][value="studio"]');
    await page.keyboard.press("Space");
    await page.keyboard.press("ArrowDown");          // -> In-home (arrow keys move and select)
    await page.keyboard.press("Tab");                // -> step 2, first radio
    await page.keyboard.press("Space");              // 1x/week
    let t = await page.textContent("#rt-ch-result");
    check("keyboard", "Space, ArrowDown, Tab, Space -> in-home 1x Foundation", /The Foundation/.test(t) && /In-Home Momentum/.test(t) && t.includes(money(C.foundation["inhome-1"].total)), t.slice(0, 90));
    await page.keyboard.press("ArrowDown");          // 2x/week
    t = await page.textContent("#rt-ch-result");
    check("keyboard", "ArrowDown -> in-home 2x Program", /The Program/.test(t) && t.includes(money(C.program["inhome-2"])), t.slice(0, 90));
    await page.keyboard.press("Tab");                // -> couples switch
    await page.keyboard.press("Space");
    t = await page.textContent("#rt-ch-result");
    check("keyboard", "Tab, Space toggles couples -> couples in-home 2x", t.includes(money(C.program["couples-inhome-2"])) && /Couples In-Home Performance/.test(t), t.slice(0, 90));
    const focusOk = await page.evaluate(() => document.activeElement && document.activeElement.id === "rt-ch-couples");
    check("keyboard", "focus lands on the couples switch", focusOk);
    await ctx.close();
  }

  /* 2b. no JavaScript: the noscript link list, no empty chooser */
  {
    const ctx = await browser.newContext({ javaScriptEnabled: false });
    const page = await ctx.newPage();
    await page.goto(URL0);
    const r = await page.evaluate(() => ({ uiHidden: document.querySelector("#rt-chooser .rt-ch-ui").hidden,
      links: [...document.querySelectorAll("#rt-chooser .rt-ch-noscript a")].map((a) => a.getAttribute("href")),
      closed: [...document.querySelectorAll("details.rt-xsec")].map((d) => d.open) }));
    check("no-js", "chooser UI stays hidden", r.uiHidden);
    check("no-js", "noscript link list to the sections below", r.links.length >= 5 && r.links.every((h) => /^#rt-/.test(h)), r.links.join(" "));
    check("no-js", "seven expandable sections, closed by default", r.closed.length === 7 && r.closed.every((o) => !o), JSON.stringify(r.closed));
    await ctx.close();
  }

  /* 3. layout at 390 / 412, every state; 4. screenshots */
  for (const width of [390, 412]) {
    const ctx = await browser.newContext({ viewport: { width, height: 900 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
    const page = await ctx.newPage();
    await page.goto(URL0);
    let worst = [];
    const empty = await layout(page);
    worst = worst.concat(empty.bad.map((b) => "empty: " + b));
    for (const [format, freq, couples] of combos) {
      await choose(page, format, freq, couples);
      const r = await layout(page);
      worst = worst.concat(r.bad.map((b) => `${format}/${freq}/${couples}: ${b}`));
      if (r.sw > r.vw) worst.push(`${format}/${freq}/${couples}: document scrollWidth ${r.sw} > ${r.vw}`);
    }
    check("layout", `${width}px: no clipping or overflow in any of ${combos.length + 1} states`, worst.length === 0, worst.slice(0, 6).join(" ; "));
    if (SHOTS && width === 390) {
      fs.mkdirSync(SHOTS, { recursive: true });
      for (const [name, format, freq] of [["studio-1x", "studio", "1"], ["inhome-2x", "inhome", "2"], ["virtual", "virtual", "1"]]) {
        await page.reload();
        await choose(page, format, freq, false);
        await page.evaluate(() => {
          document.querySelectorAll("#omni-rates .rt-reveal").forEach((e) => e.classList.add("is-in"));
          // the fixed site header would sit over an element screenshot; hide it for the capture only
          document.querySelectorAll("#site-header, #site-announce").forEach((e) => { e.style.visibility = "hidden"; });
          if (document.activeElement) document.activeElement.blur();
        });
        await page.waitForTimeout(250);
        await page.locator("#rt-choose").screenshot({ path: path.join(SHOTS, `2026-10-17-rates-chooser-${name}-390.png`) });
      }
    }
    await ctx.close();
  }

  await browser.close();
  srv.close();

  console.log("| # | Combination | Offer | Chooser shows | CANON card | Match |");
  console.log("|---|---|---|---|---|---|");
  table.forEach((r, i) => console.log(`| ${i + 1} | ${r.label} | ${r.offer} | ${r.shown.replace(/\|/g, "\\|")} | ${r.canon} | ${r.ok ? "yes" : "**NO**"} |`));
  console.log("");
  for (const r of rows) if (r.area !== "card") console.log(`${r.ok ? "PASS" : "FAIL"}  [${r.area}] ${r.what}${r.detail ? "  - " + r.detail : ""}`);
  for (const r of rows) if (r.area === "card" && !r.ok) console.log(`FAIL  [card] ${r.what}  - ${r.detail}`);
  console.log(`\nRESULT: ${failures ? failures + " FAILED" : "PASSED"} (${rows.length} checks, ${combos.length} combinations)`);
  process.exit(failures ? 1 : 0);
})().catch((e) => { console.error("choosertest aborted:", e); process.exit(1); });
