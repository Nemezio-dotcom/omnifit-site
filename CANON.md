═══ OMNIFIT SITE — CANONICAL BRIEF (Aug 2026) ═══

REPO STATE
- main = paste source. Certified: 10 territory pages,
  corrective-exercise-post-rehab, FAQs, how-it-works-pricing,
  in-home-personal-trainer-san-diego, private-personal-trainer-san-diego,
  each with a header under pages/headers/<slug>-header.html.
  NOT YET CERTIFIED, do not paste: training-rates-san-diego.html (still the
  July V8 stale generation), the-30-minute-executive-reset.html, footer.html.
  Never resurrect pre-patch originals from history.
- Header naming is standardised: pages/headers/<slug>-header.html, no
  exceptions.

WORKFLOW RULES
- Repo-only. Never publish anywhere; the human pastes approved output
  into Squarespace.
- On certification failure or ambiguity: report file:line and STOP.
  Never fix silently. Naming slips (e.g. missing .html) may be corrected
  after content certifies, with disclosure.
- Judgment calls beyond written instructions: allowed, but each must be
  reported with the condition under which it would be wrong.
- Every run ends with: certification grep, invariant hashes, REPORT.md
  update, per-file commits, summary table.

CANONICAL TRUTH (sole source: Aug 2026 pricing doc + these lines)
- Brand: "OmniFit Performance" everywhere. Never "OmniFit Personal
  Fitness Training".
- Trainer: Nemezio LopezPerez (one word surname). NASM Elite Trainer
  (confirmed active). A trainer operating AT Teqneeq, never a studio
  within a studio.
- NAP: Teqneeq Functional Health Center, 10772 Thornmint Rd, San Diego,
  CA 92127. Email nemezio@omnifittraining.com. Phone (619) 259-0630.
  Pacific Beach is history — zero references.
- Reviews: 190+ (5.0). Never 180+.
- Credentials (12): NASM CPT, CES, PES, BCS, CNC; ACE Corrective
  Exercise Specialist (NOT OES, NOT Orthopedic); Precision Nutrition L1,
  Sleep Stress & Recovery, Nutrition for Metabolic Health; Eden GLP-1
  Fitness, Peptide Fundamentals, GLP-1 Nutrition (clinical collaboration
  framing). Experience: "10+ Years Coaching" — never "in San Diego".
- Pricing: Diagnostic $110 credited in full toward a 3-month package
  ($90 is the retired name-era price). $90 assessment = confirmed same
  product as the $110 Performance Diagnostic; rename settled. Deposit
  $30 refundable.
  Teqneeq 1:1 monthly (3-mo/M2M): Essential 250/290, Momentum 475/550,
  Performance 950/1100, Peak 1395/1625. Upfront on a 3-month program =
  3 × the 3-month monthly rate, no discount: 750 / 1,425 / 2,850 / 4,185.
  In-home from 335/mo (1,005 upfront). Couples from 325/mo (975 upfront),
  monthly only — no per-person figures. Packs: 5 @ 175/session ($875),
  10 @ 150 ($1,500), 20 @ 135 ($2,700), one ladder regardless of location.
  Singles 165 studio, 195 in-home.
  Executive Reset: Bronze async 175, Gold 449, Platinum 675, Black 995.
  Monthly Tune-Up (graduates): 199/250/295. Facility rule: Momentum+
  requires Teqneeq membership $119/mo paid to Teqneeq; Essential and
  packs use sponsored guest passes. Travel fee: "may apply" language OK,
  never a dollar figure.
- Case-study figures (captions/alt text; verbatim client quotes are
  untouchable): Vincent 59, 8% body fat. Alo +18 lbs. Mark −17 lbs
  (248→231, 4mo). Dave −27 (225→198, 6mo). Isaac −21 (181→160, 8→20
  pull-ups, 6mo). Annie −14 (162→148, 3mo). Ken −11 fat/+6 muscle.
- Retired forever: Executive Hybrid (product, name, slug, $299/$500),
  $175/$150/$225/$200-session era, $225–275/mo era, $599–899 Reset era,
  $50/$75 travel fees, Foundation/VIP packages.

COMPLIANCE SCREEN (attorney: strike on sight, any wave)
- No outcome guarantees. No lbs-with-timeframe claims ("20–30 lbs in
  4–6 months"). Persona language WITHOUT timeframe ("needs to lose
  20–30 lbs sustainably") is legal and stays.
- No free-consultation framing. Consultation = 45 minutes, $30
  refundable deposit.
- No prenatal/postpartum content (uncertified). No Groupon/deal content.

EM-DASH RULES (voice)
- No em-dashes in rendered prose copy.
- Legal exceptions: HTML comments; alt attributes; en-dashes in numeric
  ranges; "— Name, Title" testimonial attributions; and "Name — one-line
  descriptor" separators inside structured list items (e.g. the 9-point
  movement screen), including when the label is tag-wrapped such as
  <li><strong>Label</strong> — descriptor</li>; and CSS comments inside
  <style>. Certification tooling must carve out these exceptions by rule,
  not by hardcoded line numbers, and must be negative-tested so a prose
  em-dash placed inside a list item is still caught.

CERTIFICATION GREP (zero hits expected)
"OmniFit Personal Fitness Training" · "Pacific Beach" · "ACE OES" ·
"Orthopedic Exercise" · "Executive Hybrid" · "Lopez Perez" · "180+" ·
"free consultation" (any case) · "$90 " · "$225" · "$275" · "$299" ·
"$500/mo" · "$599" · "$50"/"$75" as travel fees
Exceptions: $150/$175 legal ONLY inside (a) the canonical pricing FAQ
answer, (b) the card bullet "Fully virtual Executive Reset from
$175/mo", (c) the canonical session-pack rungs confirmed Aug 2026
($175/session for a 5-pack, $150 for a 10-pack, $135 for a 20-pack, with
totals $875/$1,500/$2,700), and (d) the Executive Reset Bronze async
tier at $175/mo. $150 or $175 used as a STUDIO PER-SESSION RATE is the
retired era and remains a violation.

INVARIANTS (hash-verify every run; update hashes here when a run
legitimately changes an invariant, and say so in REPORT.md)
- Canonical pricing FAQ answer: byte-identical on every page carrying it
  (page hash ae388d31c0b6149e, header hash 7e5de5984b133663). Currently 11
  pages and 11 headers.
- Credentials block body: byte-identical on 10 pages (6492e3ca, 630 bytes)
  — the 9 territory pages plus corrective-exercise-post-rehab. 4S Ranch keeps
  its own Meet Nemezio section instead.
- Archetype card bodies (Section A): byte-identical × 10 pages
  (hash 6b1b0f4efbd4a72c; concatenation of the three card <p> bodies in
  page order, set by the Section A/B run).
- 9-point screen section body (Section B): byte-identical × 10 pages
  (hash bd73ea51bc9ec5eb; intro + nine <li> items + closing line, set by
  the Section A/B run).
- Headers: FAQPage derived mechanically from that page's on-page FAQ,
  verbatim, in order, tags stripped. LocalBusiness never defined in page
  headers — reference "https://www.omnifittraining.com/#localbusiness-of".

NEXT RUNS
- BATCH 2 DONE (Aug 2026): FAQs · how-it-works-pricing (converted to
  monthly tiers) · in-home-personal-trainer-san-diego (P3 depth spec) ·
  private-personal-trainer-san-diego.
  BATCH 2 REMAINING: training-rates-san-diego —
  ADD market-context section around existing tables (what drives SD
  trainer cost; tier framing, OmniFit = specialist tier; no competitor
  promotion), do NOT rebuild tables · how-it-works-pricing ·
  the-30-minute-executive-reset (carries $599–899 → canonical tiers) ·
  in-home-personal-trainer-san-diego (P3: 9-point screen + RHR/BP, "why
  we assess", desk-posture protocol, hedged genuinely-coached conditions
  only, comparison table with pricing-structure row) ·
  the-30-minute-executive-reset.
  Batch 2 and 3 offer pages ALSO get a "Who This Is For / Use Cases"
  section targeting adjacent queries (long-term transformation, no-crash
  fat loss, desk-worker posture and mobility, data-driven hybrid) —
  situation and approach language only, compliance screen applies.
- BATCH 3: corrective-exercise-post-rehab DONE (Aug 2026) ·
  the-omnifit-method (12 metrics, not 7) · how-we-measure-your-progress ·
  omnifit-vs-competitors · weight-loss · strength-training-1 ·
  hiit-personal-trainer-san-diego · personal-training-services ·
  body-composition-testing · partners.
- BATCH 4: terms-and-conditions, contactform (brand sweep only).
- Human-side, not repo: per-page SEO meta descriptions (190+), 301
  /executive-hybrid-coaching → /the-30-minute-executive-reset then
  delete page, Search Console recrawl of ALL changed URLs as one batch
  at the very end, fitnesstrainer.com URL into homepage sameAs when
  retrievable, homepage Over-50 / Partner & Duo / female-clients FAQ
  sections (Claude drafts, human pastes), post-recrawl third-party
  signal work (review-prompt kit, directories, thought leadership).
