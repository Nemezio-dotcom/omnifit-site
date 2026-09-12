═══ OMNIFIT SITE — CANONICAL BRIEF (Aug 2026, REPO STATE reconciled Sept 2026) ═══

REPO STATE (reconciled with disk, Sept 2026)
- main = paste source. Every file under pages/ is IN CERTIFICATION SCOPE unless
  listed as not-yet-certified below. archive/ is NEVER in scope.
- Header naming is standardised: pages/headers/<slug>-header.html, no
  exceptions. Naming slips are corrected AFTER the content certifies, with
  disclosure, never before - fixing the name first hides a real structural
  check behind a filename mismatch.

  CERTIFIED - 28 page/header pairs
    11 territory pages: personal-trainer-4s-ranch, -carlsbad,
      -carmel-valley, -del-mar, -encinitas, -fairbanks-ranch, -la-jolla,
      -rancho-bernardo, -rancho-santa-fe, -santaluz, -solana-beach
    corrective-exercise-post-rehab · FAQs · how-it-works-pricing ·
      in-home-personal-trainer-san-diego · private-personal-trainer-san-diego
    the 9 Batch 3 pages: the-omnifit-method, how-we-measure-your-progress,
      omnifit-vs-competitors, weight-loss, strength-training-1,
      hiit-personal-trainer-san-diego, personal-training-services,
      body-composition-testing, partners
    training-rates-san-diego (refreshed from live and corrected, Aug 2026:
      two-ladder session packs, guest add-on, DEFERRED-01 applied)
    personal-trainer-over-50-san-diego - NEW, live as of Sept 2026, certified
      in the Scope Reconciliation run. Its header arrived misnamed
      (no -header suffix); renamed after its content certified clean.
    glp-1-personal-training-san-diego - NEW, arrived on main in the paste-source
      run (Sept 2026). Header is correctly named, is inside certify.py's glob,
      carries WebPage/BreadcrumbList/Service/FAQPage, and its 7-question FAQPage
      mirrors the page in count, order and text. Zero findings. Certified in the
      Compliance Re-tier run.
    personal-trainer-rancho-bernardo - NEW, arrived on main in the paste-source
      run (Sept 2026), renamed from personal-trainer-in-rancho-bernardo. Carries
      all four page invariants and its 7-question FAQPage mirrors. Zero findings.
      It is the ELEVENTH territory page, which is why every invariant count in
      this brief was one low until the Compliance Re-tier run.

  IN SCOPE, NOT YET CERTIFIED - carry real findings, do not paste
    · couples-personal-training-san-diego - NEW, arrived on main Sept 2026.
      NOT certified and BLOCKED on three things, all reported in the Link Graph
      Repair run and none fixed there:
        1. its header is at "pages/headers /COUPLES-PERSONAL-TRAINING-SAN-DIEGO.HTML"
           - a stray directory with a TRAILING SPACE, an uppercase filename, an
           uppercase .HTML extension and no -header suffix. certify.py globs
           pages/**/*.html, so the header is invisible to certification
           entirely: it is neither checked nor reported missing.
        2. one stale-canon hit at line 274, which is a CHECKER false positive,
           not a content defect - see tools/README, Known checker defects.
        3. the naming cannot be fixed until its content certifies, per the
           naming rule above.
      The page itself is live and is now linked from four hub pages.
    · nutrition-coaching-san-diego - NEW, arrived on main in the paste-source
      run (Sept 2026). The PAGE is clean and its FAQ mirrors its header exactly
      (7 vs 7, count, order and text, verified by hand with tools/faq.py). It is
      NOT certified for one reason only: its header is at
      "pages/headers/nutrition-coaching-san-diego.header" - the extension is
      .header, not .html, so certify.py's pages/**/*.html glob never sees it.
      The pair is neither checked nor reported missing, exactly the couples
      header's failure shape in a second form. Per the naming rule above the
      rename waits until the content certifies - which it cannot, while the
      file is invisible. Breaking that deadlock needs an owner decision, and
      is reported, not taken, by this run.
    · about, contactform, desk-worker-posture-pain, hsa-fsa-personal-training
      - each has a header. desk-worker's header carries no FAQPage while its
      page has 6 FAQs: a real, reported mirror failure, not fixed.
    · home-1, home-2, home-4, home-5 - homepage section fragments, no headers.
      Carry retired brand name, Pacific Beach, ACE OES, Executive Hybrid, $90
      and 180+. BATCH 4 or later.
    · case-studies - JSON-LD is BODY-EMBEDDED, there is no header file and
      none is missing. The mirror check iterates headers, so it does not and
      must not flag this.
    · home-3 - KNOWN DUPLICATE, byte-identical to case-studies.html
      (sha256 c82d5f32dc869381...). It IS the case-studies block pasted into
      the homepage. Certified via its source, not independently, and excluded
      from the finding count. Also body-embedded JSON-LD, no header.

  NOT YET CERTIFIED, do not paste
    · the-30-minute-executive-reset.html - the REPO COPY IS STALE RELATIVE TO
      PRODUCTION. The live version on the domain is ahead of this file. It
      needs REFRESHING FROM LIVE, not patching: any run that patches the repo
      copy would be editing a version the site has already moved past.
      Deferred from Batch 3 on that basis. A header file already exists
      (pages/headers/the-30-minute-executive-reset-header.html) but has not
      been verified against a refreshed page.
    · footer.html - site-wide, in no batch.

  ORPHAN HEADERS - a header with no page in the repo
    · bodybuilding-header.html (5 FAQ entries)
    · energy-protocol-waitlist-form-header.html (no FAQPage)
      Both pages are Squarespace block-built: there is no Code Block to
      retrieve, so the page will never exist here. The headers are real and
      deployed. Certification reports each as "no matching page" - expected,
      and left visible rather than suppressed.
    · home-header.html - the homepage header, and the site's LocalBusiness
      definition (the one place it is legitimately defined, referenced
      everywhere else by @id). The homepage itself lives in this repo only as
      the home-1..home-5 fragments, so there is no pages/home.html and the
      same "no matching page" finding applies. It also carries retired brand
      name, Pacific Beach and Orthopedic Exercise.

  DUPLICATE RULE, general: where two IN-SCOPE files are byte-identical,
  certify one and reference the other. certify.py hashes every in-scope file,
  keeps the alphabetically first of each identical group, and PRINTS the
  pairing in the SCOPE block. Certifying both double-counts every finding.

ARCHIVE - archive/ and archive/headers/, NEVER certified, NEVER corrected
- These pages are RETIRED from the live site. Each URL 301s elsewhere via
  Squarespace URL Mappings. They are historical records and they contain
  retired pricing, the Garnet Ave address, the retired brand name and
  unmirrored headers. That is EXPECTED and must be preserved. Do not correct
  them, and never bring them back into certification scope. certify.py
  asserts that no archive/ path can enter its glob.
    online-training                 -> 301 /the-30-minute-executive-reset
    executive-hybrid-coaching       -> 301 /the-30-minute-executive-reset
    personal-trainer-mission-hills  -> 301 /in-home-personal-trainer-san-diego
    llms-txt-page-retired           -> superseded by Squarespace's native
                                       LLMS.txt field (no header ever existed)
  Archived in the Scope Reconciliation run, Sept 2026, byte-identical, with
  their headers where one existed. The online-training-header mirror failure
  reported in the previous run (page 7, schema 0) is resolved by this move:
  it was not a defect to fix, the page does not exist.
- Never resurrect pre-patch originals from history.

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
- CONTRACT VALUE CHECK (counsel condition, Aug 2026; the counsel who set it
  is no longer engaged, so OWNER APPROVAL is the live gate):
  before filing a client on any contract whose total exceeds $4,400, obtain
  owner approval first, and re-engage counsel if the owner wants the
  statutory question answered rather than managed. This is a workflow step,
  not a pricing cap, and it does not restrict what may be published or sold. Offers that currently
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
  Packs, two ladders by venue, max 2 sessions/week:
    Studio  — 5 @ 145/session (725) · 10 @ 140 (1,400) · 20 @ 135 (2,700)
    In-home — 5 @ 175/session (875) · 10 @ 170 (1,700) · 20 @ 165 (3,300)
    Expiry: 5-pack 10 weeks · 10-pack 20 weeks · 20-pack 30 weeks
  Singles 165 studio, 195 in-home.
  Add-ons, confirmed Aug 2026: extra session 115 studio / 155 in-home ·
  guest add-on 75/session (was $50, corrected in the Rates Page Correction
  run — three named-package instances plus one FAQ mention).
  Referral credit: 50 off next month — UNVERIFIED, not yet confirmed by
  Nemezio. Left as published; do not treat as canonical until confirmed.
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
- DEVICE (confirmed by owner, Sept 2026; supersedes the Bodystat 1500 MDD
  everywhere the site describes what a client will receive):
  the body composition device is the "Bodystat QuadScan 4000". Brand casing
  is "Bodystat", never "BodyStat" — Bodystat's own materials use the former.
  VERIFIED FACTUAL CLAIM, same standing the 1500 MDD designation held: the
  QuadScan 4000 holds CE certification as a Class IIa medical device under
  MDD 93/42/EEC and has FDA clearance. Existing "Class IIa medical device"
  copy therefore stays as written; only the model name changes beside it.
  Capability, recorded but NOT yet written into copy (see NEXT RUNS): four
  frequencies (5/50/100/200 kHz) against the 1500 MDD's single 50 kHz;
  separates intracellular from extracellular water; Phase Angle;
  Prediction Marker (ECW/TBW); Body Cell Mass, FFMI, BFMI, segmental
  analysis. Practically: a weight change can be attributed to muscle, fat
  or fluid rather than inferred.
  THE 1500 MDD IS NOT RETIRED FROM THE RECORD. Scans that happened on it
  happened on it. Every 1500 MDD reference inside pages/case-studies.html
  and its byte-identical duplicate pages/home-3.html is a factual record of
  a past measurement and must be left exactly as written; changing it would
  falsify the record. The same reasoning protects the v2 changelog entry at
  pages/home-2.html:14, which records what a past edit added.
- Retired forever: Executive Hybrid (product, name, slug, $299/$500),
  $175/$150/$225/$200-session era, $225–275/mo era, $599–899 Reset era,
  $50/$75 travel fees, Foundation/VIP packages.

COMPLIANCE SCREEN — TWO TIERS (owner approval; Sept 2026)
Rewritten by the owner (Nemezio), who is now the sole compliance
decision-maker. The previous screen was written to outside counsel's
standard and stripped true measured metrics along with the projections it
was aimed at; the owner has judged that a mistake. Measured facts with
their method shown are no longer treated as claims. What replaced them is
not a weaker screen but a differently aimed one: TIER 1 is absolute, and
TIER 2 is conditional rather than banned.

The distinction that runs through both tiers: a PROJECTION of what a
prospective client can expect is the exposure. A MEASUREMENT that has
already happened, published with its method, is not.

TIER 1 — HARD BANS. No exception. No approver, owner included, can clear
one of these; they are removed on sight, and a run that finds one reports
it and STOPS rather than weighing context.
  1. Outcome guarantees of any kind, including conditional and
     compliance-tied guarantees, until a separately approved wording
     exists. DEFERRED-01 (the Executive Reset guarantee wording) STAYS
     DEFERRED and is not that approved wording. See the note under
     DEFERRED-01 in RESOLVED ITEMS: its replacement text is currently LIVE
     on training-rates-san-diego, which this tier makes a violation.
  2. Pounds, inches, or body-fat percentage paired with a timeframe AS AN
     EXPECTED OR TYPICAL RESULT ("20-30 lbs in 4-6 months"). This is the
     projection case. It is not the attributed-individual case, which is
     TIER 2 item 2, and not the persona case, which is TIER 2 item 3.
  3. Any statement that OmniFit diagnoses, treats, assesses, or manages a
     MEDICAL CONDITION, or that a device is used to do so. "Assesses" is
     new to this tier and is scoped to a medical condition: assessing
     MOVEMENT is what OmniFit does and stays legal. Negations and referral
     language stay legal and are the recommended form.
  4. "Free consultation" framing, under any name for the first session.
     The consultation is paid: 45 minutes, $30 refundable deposit.
  5. A client's PHASE ANGLE value, its change over time, or any improvement
     rate for it, presented as evidence of health. Phase angle may be NAMED
     as a tracked marker and DESCRIBED as what the device measures; it may
     not be REPORTED AS A RESULT. The line is description versus outcome,
     not mention versus silence.
  6. Population-level clinical claims attributed to OmniFit training
     ("reduces blood pressure", "reverses insulin resistance"). A clinical
     result rate published by a non-clinician is the exposure, and no
     method note, sample size or disclaimer clears it. This is the one part
     of the old clinical-statistic rule that survives intact, and it is the
     reason TIER 2 item 1 does not simply permit every percentage.

TIER 2 — PERMITTED WITH CONDITIONS. Not exceptions to a ban: these are
legal, and become findings only when a stated condition is MISSING. A run
reports the missing condition, never the content.
  1. AGGREGATE MEASURED METRICS — adherence %, median strength change,
     client rating, review count — are permitted when all three of these
     are present ON THE SAME SURFACE as the figure:
       (a) a stated METHOD: what was measured, sample size, period;
       (b) the COMPANY-REPORTED / NOT-INDEPENDENTLY-AUDITED note;
       (c) the INDIVIDUAL-RESULTS disclaimer.
     REFERENCE FORM: the Results section of
     how-we-measure-your-progress.html — each figure carries its own
     method line, and one note block carries both (b) and (c). Copy that
     shape rather than inventing another.
     TIER 1 item 6 still governs: a clinical result rate is never an
     aggregate measured metric, however well conditioned.
  2. ATTRIBUTED INDIVIDUAL OUTCOMES in case studies are permitted with the
     individual-results disclaimer ON THE SAME PAGE. Attribution is still
     required - a named individual beside a role noun, or an explicit
     anonymisation with a stated profile - and aggregate framing is still
     never exempt. What is RELAXED against the old screen: the disclaimer
     no longer has to sit in a dedicated block opening with the phrase.
     That dedicated-block test was written to counsel's standard and is
     withdrawn for this item.
     FROZEN RECORDS: pages/case-studies.html and its byte-identical
     duplicate pages/home-3.html are historical records, exempt from
     re-screening entirely. They record measurements that happened.
  3. PERSONA LANGUAGE without a timeframe ("sustainable fat loss of
     20-30 lbs") is permitted, unchanged from the old screen.
  4. DEVICE CAPABILITY LANGUAGE is permitted: what the Bodystat QuadScan
     4000 measures - multi-frequency BIA, ICW/ECW separation, phase angle,
     segmental analysis. Describing a capability is not claiming a clinical
     result, and TIER 1 item 5 draws that line for phase angle
     specifically.
     The "Class IIa medical device" statement is a VERIFIED FACT and stays
     BYTE-IDENTICAL wherever it appears, ALWAYS accompanied by the
     not-a-medical-provider note. Both halves are conditions, and both are
     checkable: a second, shorter wording of the fact is a finding even
     though the fact is true, and the fact standing without its note is a
     finding even though the wording is right.
  5. ILLUSTRATIVE SAMPLE DATA is permitted when labelled "illustrative,
     not client data" on the same surface. Unlabelled sample figures read
     as measurements and are a finding.

CARRIED OVER, NOT RE-TIERED
- No Groupon/deal content.
- No prenatal/postpartum content (uncertified). The owner's TIER 1 list did
  not name this and the rewrite did not ask for it to go; it is kept under
  TIER 1 item 3 as an uncertified-scope claim rather than dropped silently,
  because dropping a live protection is not something a rewrite should do
  by omission. This is a judgment call and it is WRONG IF the owner intends
  prenatal/postpartum content to be publishable now - in which case item 3
  should say so and the rule retires.

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

(a) COMPLIANCE STRIKES — shape-based, not just literal strings.
Every rule below names the tier it encodes. TIER 1 rules report a
violation. TIER 2 rules report a MISSING CONDITION, and are written to
check for the condition rather than to ban the content - a rule that flags
conditioned Tier 2 copy is a defect in the rule, not a finding.

  TIER 1 RULES
  · guarantee_any (T1-1) - any form of "guarantee" in page copy. Widened
    from the old "guarantee within ~30 words of an outcome word": Tier 1
    bans guarantees of any kind, so proximity to an outcome word is no
    longer what makes one. A guarantee stated as ABSENT ("no guarantee",
    "reimbursement is not guaranteed") is the opposite of the banned shape
    and is exempt on the preceding words only. <style> and <script> bodies
    are not copy and are excluded.
  · lbs_near_timeframe (T1-2) - pounds, inches or body-fat % within ~15
    words of a quantified timeframe. Inches and body-fat % are new to this
    rule. Exempt: TIER 2 item 2 (attributed individual, page disclaimer),
    TIER 2 item 3 (no timeframe at all never matches), frozen records.
  · uncertified_claims (T1-3) - asserting OmniFit diagnoses, treats,
    prescribes, cures or rehabilitates; provides physical therapy or
    chiropractic; ASSESSES OR MANAGES A MEDICAL CONDITION; or that a DEVICE
    is used for any of those. The medical-condition object is REQUIRED on
    the assess/manage shape, which is what keeps "we assess your movement"
    legal. Negations and referral language are legal.
  · prenatal_postpartum (T1-3, carried over) - unless an explicit
    out-of-scope disclaimer or attributed to a partner via knowsAbout.
  · free_consultation (T1-4) - "free" within ~6 words of any bookable first
    session: consultation · assessment · screen · screening · session ·
    diagnostic · call · intake. Unchanged.
  · phase_angle_result (T1-5) - NEW. A phase angle value, delta or
    improvement rate presented as evidence of health. Naming and describing
    the marker is legal, which is why the rule keys off a NUMBER or a
    change/improvement word beside "phase angle", not on the phrase.
  · population_clinical_claim (T1-6) - NEW. A clinical outcome verb applied
    to a clinical condition at population scope, attributed to OmniFit
    training. Never clearable by a method note, sample size or disclaimer -
    this is the part of the old clinical-statistic rule that survives.

  TIER 2 CONDITION RULES
  · aggregate_metric_conditions (T2-1) - REPLACES the old blanket
    clinical_stat ban for non-clinical measured metrics. A percentage or
    measured figure presented as an aggregate is a finding ONLY when the
    surface is missing a method line, the not-independently-audited note,
    or the individual-results disclaimer. The finding NAMES THE MISSING
    CONDITION. Surface = the enclosing <section>, falling back to the page.
  · class_iia_conditions (T2-4) - NEW. Every "Class IIa medical device"
    instance must be byte-identical to the canonical wording AND carry the
    not-a-medical-provider note on the same surface. Two separate findings.
  · illustrative_label (T2-5) - NEW. Sample or example figures presented
    without an "illustrative, not client data" label on the same surface.

  WITHDRAWN WITH THE OLD SCREEN
  · The DEDICATED-BLOCK disclaimer test for case studies. It required the
    disclaimer to open its own p/div/aside/section/blockquote. TIER 2 item
    2 asks only that the disclaimer be on the same page, so the test is
    withdrawn for that item. It is NOT withdrawn from TIER 2 item 1, which
    states its own three conditions.
    Consequence recorded so it is not rediscovered as a surprise:
    how-we-measure-your-progress and desk-worker-posture-pain both failed
    the dedicated-block test and now pass the same-page test. Neither gains
    an exemption from it on its own, because TIER 2 item 2 also requires
    ATTRIBUTION, and both fail that independently.
  · clinical_stat as a blanket ban on quantified figures near a clinical
    word. Split: the population-scope clinical case is T1-6 and is
    unchanged in force; everything else is T2-1 and is conditional.
  · result_near_timeframe as an unconditional rule. It now exempts a
    surface carrying the full TIER 2 item 1 conditions, because a measured
    aggregate reported with its period IS a measurement with its method,
    which is the thing this screen stopped treating as a claim.

  EXCEPTION - ATTRIBUTED INDIVIDUAL OUTCOMES (TIER 2 item 2)
  Individual client results carrying a timeframe are exempt from
  lbs_near_timeframe and result_near_timeframe when:
    1. the result is attributed to a specific individual (named beside a
       role noun, or explicitly anonymised WITH a stated profile), AND
    2. the page carries the individual-results disclaimer ANYWHERE on the
       page. Relaxed Sept 2026 from a dedicated block, per TIER 2 item 2.
    3. substantiation exists on file. Not machine-checkable; a human
       warranty, unchanged.
  Page-scoped, not site-wide. Aggregate or typical-results framing is NEVER
  exempt, on any page. Fails CLOSED: anything the attribution test cannot
  confirm stays a strike.
  FROZEN: case-studies.html and home-3.html are exempt from re-screening.

  Reasoning, recorded so it survives: an individual, attributed, documented
  client outcome is a fact about a named person; a claim about what a
  prospective client can expect is a projection. Only the projection is
  what these rules exist to prevent. The same distinction is what moved
  aggregate measured metrics from banned to conditional - a median with its
  sample size and period is a record of what happened, and the conditions
  are there to keep it readable as one.

(b) STALE CANON
  "OmniFit Personal Fitness Training" · "Pacific Beach" · "ACE OES" ·
  "Orthopedic Exercise" · "Executive Hybrid" · "Lopez Perez" · "180+" ·
  "$90 " · "$225" · "$275" · "$299" · "$500/mo" · "$599" ·
  "$50"/"$75" as travel fees.
  $150/$175 legal ONLY inside (a) the canonical pricing FAQ answer,
  (b) the card bullet "Fully virtual Executive Reset from $175/mo",
  (c) the canonical pack rungs (studio 5 @ $145/10 @ $140/20 @ $135,
  totals $725/$1,400/$2,700; in-home 5 @ $175/10 @ $170/20 @ $165, totals
  $875/$1,700/$3,300), (d) the Reset Bronze async tier at $175/mo, and (e)
  "virtual from $175" describing that same Bronze tier in a meta
  description. $150 as a pack rung is retired — it belonged to neither
  ladder, a mangled merge of the studio and in-home figures.
  $150 or $175 as a STUDIO PER-SESSION RATE is retired and a violation.

(c) BROKEN STRUCTURE
  invalid JSON · header FAQPage not mirroring the page FAQ in count, order
  and text · invariant hash mismatch · HTML tag-balance failure ·
  LocalBusiness redefined in a page header instead of referenced by @id.

INVARIANTS (hash-verify every run; update hashes here when a run
legitimately changes an invariant, and say so in REPORT.md)
- Canonical pricing FAQ answer: byte-identical on every page carrying it
  (page hash ae388d31c0b6149e, header hash 7e5de5984b133663). Currently 12
  pages and 12 headers.
- Credentials block body: byte-identical on 11 pages (6492e3ca1545dc26,
  630 bytes)
  — the 10 territory pages plus corrective-exercise-post-rehab. 4S Ranch keeps
  its own Meet Nemezio section instead.
- Archetype card bodies (Section A): byte-identical × 11 pages
  (hash 6b1b0f4efbd4a72c; concatenation of the three card <p> bodies in
  page order, set by the Section A/B run).
- 9-point screen section body (Section B): byte-identical × 11 pages
  (hash ba590a09107ffda0; intro + nine <li> items + closing line, set by
  the Section A/B run). Hash changed legitimately in the Device Swap run
  (Sept 2026): the Body Composition <li> names the device, so retiring the
  1500 MDD rewrote the same bytes on all eleven pages. Previous value
  bd73ea51bc9ec5eb. All eleven pages still agree; certify.py reported no
  invariant mismatch. (That run recorded "ten"; rancho-bernardo was already
  on main and carrying the invariant, so the count was one low even then.)
- Headers: FAQPage derived mechanically from that page's on-page FAQ,
  verbatim, in order, tags stripped. LocalBusiness never defined in page
  headers — reference "https://www.omnifittraining.com/#localbusiness-of".
  A header may carry its nodes across SEVERAL ld+json blocks rather than one
  @graph (desk-worker-posture-pain puts Service in block 1 and its FAQPage in
  block 2). certify.py reads every block and merges the nodes; a checker that
  read only the first reported that header as broken for two runs.

KNOWN DEFERRED ITEMS
Two kinds live here and they behave differently:
  · ACCEPTED EXCEPTION — an existing violation deliberately tolerated.
    Certification must NOT flag it while listed.
  · ACTIVE CONSTRAINT — a restriction that must be HONOURED when publishing.
    Not a tolerated violation; breaking it is a real error.

RESOLVED ITEMS (kept so the reasoning survives; no longer constraints)

DEFERRED-01 · Executive Reset guarantee wording (rates page) · CLOSED Aug 2026
- Was an ACCEPTED EXCEPTION. Applied in the Rates Page Correction run.
- File: pages/training-rates-san-diego.html and pages/headers/
  training-rates-san-diego-header.html. Three instances, located by content
  since the page had been refreshed from live and prior line numbers were
  stale: the body callout inside the Executive Reset section, the "Does
  OmniFit offer a money-back guarantee?" FAQ answer, and the same answer
  mirrored in the header's FAQPage schema (the page's schema was already
  extracted to the header by the time of this run, ahead of the older note
  that it was still body-embedded).
- Original text promised an outcome ("feel clearly stronger, more energized,
  and more in control") and conditioned the refund on undefined "full
  compliance" of a "remaining program balance" — banned as a named outcome
  guarantee, and vague as a refund term under an upfront billing model.
- Applied verbatim, exactly as previously approved:
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
- The (a) COMPLIANCE STRIKES exemption for this item is removed. The
  resolved text does not pair "guarantee" with an outcome word and needs no
  exemption; tools/certify.py no longer carries a DEFERRED_01 carve-out.
- RE-OPENED Sept 2026 by the two-tier screen. TIER 1 item 1 bans outcome
  guarantees OF ANY KIND, conditional and compliance-tied included, until a
  separately approved wording exists, and names DEFERRED-01 as still
  deferred. The wording above was cleared under the previous screen by
  counsel who is no longer engaged; it is not owner-approved.
  This entry stays in RESOLVED ITEMS because the RECORD of what was applied
  in Aug 2026 is accurate and must not be rewritten. What changed is its
  STANDING, not its history. The text is currently LIVE at
  training-rates-san-diego.html:866 (callout), :967 (FAQ answer) and
  training-rates-san-diego-header.html (the same answer in FAQPage), and
  under the new tier all three are violations awaiting owner-approved
  replacement wording. Reported by the Compliance Re-tier run, not fixed
  there - that run was scoped to rules, not pages.

RESOLVED-02 · Statutory cap exposure on prepaid tiers · CLOSED Aug 2026
- Was DEFERRED-02, an ACTIVE CONSTRAINT. Resolved Aug 2026 by the counsel
  then engaged (no longer engaged), who confirmed the current pricing is
  acceptable. Kept as the historical record of what actually cleared it;
  the live gate for any new exposure is OWNER APPROVAL.
- Outcome: the interim month-to-month-only rule is LIFTED. In-home
  Performance and Peak, individual and couples, may be sold and published
  as 3-month prepaid commitments.
- The condition attached to that clearance is not a pricing limit. It is the
  CONTRACT VALUE CHECK recorded under WORKFLOW RULES: owner approval before
  filing a client on a contract exceeding $4,400.
- Original reasoning, retained: Cal. Civ. Code 1812.86 caps a single health
  studio services contract at $4,400, and OmniFit's own Couples Prepaid
  Program Agreement cites that cap. The open question was whether 1812.86
  reaches in-home personal training or only facility-based services. Both
  exposed rows were in-home; every facility-based offer cleared. Counsel's
  clearance settles it without the site needing to answer that question.

PRICING-CHANGE CHECKLIST (kept live from the above; consult before repricing)
- 3-month prepaid total = 3 x the 3-month monthly rate. Anything over $4,400
  triggers the CONTRACT VALUE CHECK (owner approval) before a client is filed.
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
