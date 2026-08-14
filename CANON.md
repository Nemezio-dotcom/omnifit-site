═══ OMNIFIT SITE — CANONICAL BRIEF (Aug 2026) ═══

REPO STATE
- main = paste source. Certified: 10 territory pages,
  corrective-exercise-post-rehab, FAQs, how-it-works-pricing,
  in-home-personal-trainer-san-diego, private-personal-trainer-san-diego,
  and the 9 Batch 3 pages — the-omnifit-method,
  how-we-measure-your-progress, omnifit-vs-competitors, weight-loss,
  strength-training-1, hiit-personal-trainer-san-diego,
  personal-training-services, body-composition-testing, partners —
  each with a header under pages/headers/<slug>-header.html.
  25 page/header pairs in total.
  NOT YET CERTIFIED, do not paste:
  · training-rates-san-diego.html and the-30-minute-executive-reset.html —
    the REPO COPIES ARE STALE RELATIVE TO PRODUCTION. The live versions on
    the domain are ahead of these files. They need REFRESHING FROM LIVE, not
    patching: any run that patches the repo copy would be editing a version
    the site has already moved past. Deferred from Batch 3 on that basis.
  · footer.html — site-wide, in no batch.
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
- The rules in this brief are ENCODED IN tools/ (certify.py, faq.py,
  mkheaders.py, README.md). Run `python3 tools/certify.py` from the repo
  root; do not rebuild the rules from scratch. If a rule is wrong, fix it
  in tools/ and update this brief in the same commit so the two stay in
  step. tools/README.md records the three checks that have reported
  success while not actually looking — negative-test every rule change in
  both directions before trusting it.
- CONTRACT VALUE CHECK (counsel condition, Andrew Flores, Aug 2026):
  before filing a client on any contract whose total exceeds $4,400,
  contact counsel first. This is a workflow step, not a pricing cap, and it
  does not restrict what may be published or sold. Offers that currently
  trip it on a 3-month prepaid: in-home Peak individual (5,580) and in-home
  couples Performance (5,175). Teqneeq Peak individual sits closest to the
  line at 4,185, $215 clear.

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
- Consultation: 45 minutes, ALWAYS by video or phone, never in person.
  Preceded by a client intake form. $30 refundable deposit. The
  consultation is NOT the movement screen: the $110 Performance
  Diagnostic is a separate in-person session, credited in full toward a
  3-month package. Copy must not describe the consultation as producing
  baseline metrics, body composition, or a movement assessment.
  Teqneeq 1:1 monthly (3-mo/M2M): Essential 250/290, Momentum 475/550,
  Performance 950/1100, Peak 1395/1625. Upfront on a 3-month program =
  3 × the 3-month monthly rate, no discount: 750 / 1,425 / 2,850 / 4,185.
  In-home individual monthly (3-mo/M2M), complete ladder: Essential 335/390,
  Momentum 650/755, Performance 1,250/1,425, Peak from 1,860/2,150. Upfront
  on a 3-month program = 3 x the 3-month rate: 1,005 / 1,950 / 3,750 / 5,580.
  Packs: 5 @ 175/session ($875),
  10 @ 150 ($1,500), 20 @ 135 ($2,700), one ladder regardless of location.
  Singles 165 studio, 195 in-home.
  Executive Reset: Bronze async 175, Gold 449, Platinum 675, Black 995.
  Monthly Tune-Up (graduates): 199/250/295. Facility rule: Momentum+
  requires Teqneeq membership $119/mo paid to Teqneeq; Essential and
  packs use sponsored guest passes. Travel fee: "may apply" language OK,
  never a dollar figure.
  CONFIRMED Aug 2026, source = signed Prepaid Program Agreement:
  · No processing fees are added to stated prices. The 2.9% card fee is
    retired everywhere; never reintroduce it.
  · The total is paid in a SINGLE UPFRONT PAYMENT at signing on 3-month
    programs. Copy must not say "billed monthly, no large upfront payments".
  · The widened $150/$175 exception (pack rungs + Reset Bronze) is approved.
- Couples pricing (monthly; both partners train in one session). Supersedes
  the earlier "from 325/mo, monthly only" line:
    Studio  3-mo: Essential 325 · Momentum 625 · Performance 1,250
    Studio  M2M : Essential 370 · Momentum 700 · Performance 1,400
    In-home 3-mo: Essential 455 · Momentum 875 · Performance 1,725
    In-home M2M : Essential 510 · Momentum 975 · Performance 1,950
    Single couples session: 235 studio · 250 in-home
  Peak is ad-hoc only at both venues and is NOT offered as a prepaid couples
  commitment.
  Derived per-session figures exist (studio 150/144/144, in-home 210/202/199
  by tier) but are NOT to be published as the primary rate. Note that the
  studio Essential derivation is $150, which the certification rule treats as
  a violation outside the approved contexts, so publishing it would fail
  certification as well as contradict this line.
  In-home couples Performance (1,725/mo) MAY be sold and published as a
  3-month prepaid commitment (5,175 upfront). The earlier month-to-month-only
  restriction is lifted. See RESOLVED-02 for the counsel workflow rule.
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
- No quantified clinical-shaped outcome statistics. A percentage or figure
  attached to a clinical result — pain, injury, recovery, healing,
  rehabilitation, range of motion presented as a health outcome — is banned
  whether or not it carries a timeframe, and whether or not it is averaged
  or disclaimed ("87% Pain Reduction", "reduced chronic pain in 90% of
  clients"). A non-clinician publishing a clinical result rate is the
  exposure, not the timeframe. Behavioural and business stats are NOT
  clinical and stay: session adherence, nutrition compliance, client
  rating, review count, retention. Performance stats (strength, body
  composition) stay only WITHOUT a timeframe.
- No outcome claims that pair a result with a promised window, in any
  units. The lbs-with-timeframe rule is the specific case; the general
  rule is that the result must be framed against the client's own
  baseline, never against a calendar ("measurable body composition
  changes within 6-8 weeks", "Over 4-6 months: measurable increases").

EM-DASH RULES (voice preference, NOT a compliance issue)
- Do not scan for em-dashes. Do not flag them. Do not include them in
  certification results. They are a house-style preference, not a finding.
- Keep the sweep active only when already editing a page: new copy written
  by a run should not contain em-dashes in prose. Existing ones stay.
- The four in how-it-works-pricing.html stay as they are, by decision.

CERTIFICATION — REPORTS EXACTLY THREE CATEGORIES, NOTHING ELSE
A run reports (a) compliance strikes, (b) stale canon, (c) broken structure.
Anything outside these is NOT a certification finding: report it as a
judgment call if it needs a human decision, otherwise handle it silently.

(a) COMPLIANCE STRIKES — shape-based, not just literal strings
  · outcome guarantees: any form of "guarantee" within ~30 words of an
    outcome promise (stronger, leaner, energized, more in control, lose,
    fat loss, transformation, results, pounds, lbs, body fat, inches)
  · lbs/pounds within ~15 words of a timeframe (day/week/month/year).
    Persona language with NO timeframe stays legal
  · free-consultation framing: "free" within ~6 words of any of
    consultation · assessment · screen · screening · session ·
    diagnostic · call · intake
  · prenatal / postpartum content, unless it is an explicit out-of-scope
    disclaimer
  · uncertified specialty claims: asserting OmniFit diagnoses, treats,
    prescribes, cures, rehabilitates, or provides physical therapy or
    chiropractic. Negations and referral language are legal
  DEFERRED-01 is exempt while listed under KNOWN DEFERRED ITEMS.

(b) STALE CANON
  "OmniFit Personal Fitness Training" · "Pacific Beach" · "ACE OES" ·
  "Orthopedic Exercise" · "Executive Hybrid" · "Lopez Perez" · "180+" ·
  "$90 " · "$225" · "$275" · "$299" · "$500/mo" · "$599" ·
  "$50"/"$75" as travel fees.
  $150/$175 legal ONLY inside (a) the canonical pricing FAQ answer,
  (b) the card bullet "Fully virtual Executive Reset from $175/mo",
  (c) the canonical pack rungs (5 @ $175, 10 @ $150, 20 @ $135, totals
  $875/$1,500/$2,700), and (d) the Reset Bronze async tier at $175/mo.
  $150 or $175 as a STUDIO PER-SESSION RATE is retired and a violation.

(c) BROKEN STRUCTURE
  invalid JSON · header FAQPage not mirroring the page FAQ in count, order
  and text · invariant hash mismatch · HTML tag-balance failure ·
  LocalBusiness redefined in a page header instead of referenced by @id.

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

KNOWN DEFERRED ITEMS
Two kinds live here and they behave differently:
  · ACCEPTED EXCEPTION — an existing violation deliberately tolerated.
    Certification must NOT flag it while listed.
  · ACTIVE CONSTRAINT — a restriction that must be HONOURED when publishing.
    Not a tolerated violation; breaking it is a real error.

DEFERRED-01 · ACCEPTED EXCEPTION · Executive Reset guarantee wording (rates page)
- File: pages/training-rates-san-diego.html, plus its header file.
  NOTE: that header file does not exist yet. The page's schema is still
  body-embedded (line 822), so the third instance currently lives in the
  body block and moves with the schema when it is extracted.
- Three instances, verified Aug 2026:
  · line 664 — body callout inside the Executive Reset section
  · line 767 — "Does OmniFit offer a money-back guarantee?" FAQ answer
  · line 880 — the same answer inside the FAQPage schema
- Current text promises an outcome ("feel clearly stronger, more energized,
  and more in control") and conditions the refund on undefined "full
  compliance" of a "remaining program balance".
- Two problems: (1) CANON bans outcome guarantees; this is named a guarantee
  and promises a result. (2) "Full compliance" and "remaining balance" are
  undefined terms in a refund promise under an upfront billing model.
- Approved replacement, to apply in a future cleanup pass:
  Callout heading: "30-Day Fit Guarantee"
  Callout body: "If after your first 30 days you decide the Executive Reset
  isn't the right fit, you can stop and I'll refund the unused balance of
  your program. You keep the first month and everything you've learned.
  No compliance test, no negotiation."
  FAQ answer: "Yes, on the Executive Reset. It includes a 30-Day Fit
  Guarantee: if after your first 30 days you decide it isn't the right fit,
  you can cancel and receive a refund of the unused balance of your program.
  You keep the first month and everything you've learned. There is no
  compliance test to pass and nothing to negotiate."
- Status: approved, not yet applied. Deliberately deferred by Nemezio.
  Known, accepted exception until scheduled.

RESOLVED ITEMS (kept so the reasoning survives; no longer constraints)

RESOLVED-02 · Statutory cap exposure on prepaid tiers · CLOSED Aug 2026
- Was DEFERRED-02, an ACTIVE CONSTRAINT. Resolved by counsel (Andrew
  Flores), who confirmed the current pricing is acceptable.
- Outcome: the interim month-to-month-only rule is LIFTED. In-home
  Performance and Peak, individual and couples, may be sold and published
  as 3-month prepaid commitments.
- The condition attached to that clearance is not a pricing limit. It is the
  CONTRACT VALUE CHECK recorded under WORKFLOW RULES: contact counsel before
  filing a client on a contract exceeding $4,400.
- Original reasoning, retained: Cal. Civ. Code 1812.86 caps a single health
  studio services contract at $4,400, and OmniFit's own Couples Prepaid
  Program Agreement cites that cap. The open question was whether 1812.86
  reaches in-home personal training or only facility-based services. Both
  exposed rows were in-home; every facility-based offer cleared. Counsel's
  clearance settles it without the site needing to answer that question.

PRICING-CHANGE CHECKLIST (kept live from the above; consult before repricing)
- 3-month prepaid total = 3 x the 3-month monthly rate. Anything over $4,400
  triggers the CONTRACT VALUE CHECK before a client is filed.
- Current totals, highest first:
    In-home Peak individual      1,860 x 3 = 5,580   over
    In-home couples Performance  1,725 x 3 = 5,175   over
    Teqneeq Peak individual      1,395 x 3 = 4,185   under by 215
    In-home Performance indiv.   1,250 x 3 = 3,750   under by 650
    Studio couples Performance   1,250 x 3 = 3,750   under by 650
    Teqneeq Performance          950 x 3   = 2,850   under by 1,550
    In-home couples Momentum     875 x 3   = 2,625   under by 1,775
    In-home Momentum individual  650 x 3   = 1,950   under by 2,450
- Break point is the same for every offer: any 3-month monthly rate above
  $1,466 produces a total over $4,400 (4,400 / 3 = 1,466.67). Teqneeq Peak at
  1,395 is the closest under it. In-home Peak's 1,860 is a FLOOR, so its
  total can only rise.

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
