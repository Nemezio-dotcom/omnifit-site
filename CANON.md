═══ OMNIFIT SITE — CANONICAL BRIEF (Aug 2026, REPO STATE reconciled Sept 2026) ═══

REPO STATE (reconciled with disk, Sept 2026)
- main = paste source. Every file under pages/ is IN CERTIFICATION SCOPE unless
  listed as not-yet-certified below. archive/ is NEVER in scope.
- Header naming is standardised: pages/headers/<slug>-header.html, no
  exceptions. Naming slips are corrected AFTER the content certifies, with
  disclosure, never before - fixing the name first hides a real structural
  check behind a filename mismatch.

  CERTIFIED - 30 page/header pairs (29 between the Keyword Ownership run,
  Oct 2026, which archived strength-training-1, and the Dial follow-up run,
  Oct 17 2026, which restored it; see ARCHIVE)
    11 territory pages: personal-trainer-4s-ranch, -carlsbad,
      -carmel-valley, -del-mar, -encinitas, -fairbanks-ranch, -la-jolla,
      -rancho-bernardo, -rancho-santa-fe, -santaluz, -solana-beach
    corrective-exercise-post-rehab · FAQs · how-it-works-pricing ·
      in-home-personal-trainer-san-diego · private-personal-trainer-san-diego
    the 9 live Batch 3 pages: the-omnifit-method, how-we-measure-your-progress,
      omnifit-vs-competitors, weight-loss, strength-training-1,
      hiit-personal-trainer-san-diego, personal-training-services,
      body-composition-testing, partners
      (strength-training-1 was archived Oct 2026 with a 301 to /, and
      RESTORED in the Dial follow-up run, Oct 17 2026, as "Strength Training
      for Professionals 30+": byte-identical content plus the who-for block,
      Method line, roles line and entity line; the 301 is gone from
      build.py REDIRECTS; back in mkheaders META, the sitemap and the link
      lists on personal-training-services and the homepage.)
    training-rates-san-diego (refreshed from live and corrected, Aug 2026:
      two-ladder session packs, guest add-on, DEFERRED-01 applied).
      V16, Oct 17 2026 (rates restructure run): decision-first layout, no
      price, term, policy, FAQ answer or locked wording changed. Order:
      hero, the starting-option CHOOSER (#rt-choose: format, frequency,
      couples toggle; result in an aria-live region; every figure computed
      by the page script from data attributes carrying the card prices;
      "Two Ways to Train" is now an H3 inside it, #rt-paths), What You Pay
      (assessment, "Commitment at a Glance" as an H3, #rt-commit,
      inclusions), What Protects Your Investment (+ the three policy
      cards), Why This Costs More (+ Built For / Not the Right Fit), then
      SEVEN EXPANDABLE SECTIONS, <details> closed by default with the
      existing H2 inside <summary class="... section-toggle"> and the full
      text in the HTML: The Foundation, The Program, Sessions Without a
      Program, The Tune-Up, The Executive Reset, What Happens If Your
      Schedule or Goals Change, Every Tier Includes Your Choice of
      Accountability; then the FAQ (eleven: "Is OmniFit worth the price
      compared to a regular gym membership?" added, the homepage answer
      verbatim; header mirrors) and the final CTA. Every rt-* id still
      resolves; each section id sits on its <details>, and site.js opens a
      closed section when a link or the URL hash targets it. tools/faq.py
      skips section-toggle summaries (they are sections, not questions);
      certify.py self-tests that both ways. tools/choosertest.js checks
      every chooser combination against this card.
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
    nutrition-coaching-san-diego - certified in the Enforcement run (Sept 2026)
      once its header entered the glob. The header arrived as
      "nutrition-coaching-san-diego.header" - extension .header, not .html - so
      pages/**/*.html never saw it and the pair was neither checked nor
      reported missing. Renamed to the standard <slug>-header.html; the content
      had already been verified to mirror by hand, and certified unchanged on
      the first run that could see it. 7-question FAQPage, mirrors in count,
      order and text. Zero findings.
    the-30-minute-executive-reset - certified in the Reset Refresh run (Sept
      2026). Brought to the October card: Reset tiers $200/$500/$750/$1,100,
      the pricing invariant block byte-identical to the other twelve pairs,
      the device references swapped to Bodystat QuadScan 4000, and all four
      RED-PEN FLAGS closed. Removed from certify.py's OUT_OF_SCOPE list; it
      is the THIRTEENTH carrier of both pricing invariants.
      CAVEAT, recorded because it is the one condition under which this
      certification is wrong: the page was PATCHED, not refreshed from live.
      CANON's closing procedure begins "paste the live page into the repo",
      and that step did not happen - no run in this repo can reach the live
      page. The content is correct against the October card and against this
      brief. If production has diverged from the repo copy since the file was
      last pasted, the diff must be reviewed BEFORE this page is pasted back.

  IN SCOPE, NOT YET CERTIFIED - carry real findings, do not paste
    · couples-personal-training-san-diego - NEW, arrived on main Sept 2026.
      NOT certified and BLOCKED on three things, all reported in the Link Graph
      Repair run and none fixed there:
        1. RESOLVED in the Reset Refresh run. Its header was at
           "pages/headers /couples-personal-training-san-diego-header.html" -
           a stray directory with a TRAILING SPACE. The directory is gone and
           the file now sits in pages/headers/ under the standard name. The
           glob and mkheaders.py both still find every file.
        2. one stale-canon hit at line 274, which is a CHECKER false positive,
           not a content defect - see tools/README, Known checker defects.
        3. the naming cannot be fixed until its content certifies, per the
           naming rule above.
      The page itself is live and is now linked from four hub pages.
    · about, contactform, desk-worker-posture-pain, hsa-fsa-personal-training
      - each has a header. desk-worker's header now carries a 6-question
      FAQPage that mirrors the page (see PAGE HEADER SHAPE).
    · home-0 … home-6 - homepage section fragments, no headers of their own
      (pages/headers/home-header.html is the homepage header). REBUILT in the
      Homepage rebuild run (Oct 17 2026) from ~6,850 words of body copy to
      ~2,000, same URL, title, meta description, H1 and canonical. Order
      (HOME_ORDER unchanged): home-0 hero (POSITIONING LINE subhead, Calendly
      + Fit Check link, deposit line) · home-1 In Short + proof strip (and the
      shared .omh styles) · home-2 Who it's for + How it works · home-3 three
      case cards · home-4 Ways to train · home-6 couples · home-5 Meet
      Nemezio + the ONE homepage FAQ + final CTA · home-motion. Every unique
      fact the old sections carried is on /the-omnifit-method, /case-studies,
      /about or /how-we-measure-your-progress (REPORT.md lists the moves).
    · case-studies - JSON-LD is BODY-EMBEDDED, there is no header file and
      none is missing. The mirror check iterates headers, so it does not and
      must not flag this.
    · home-3 - NO LONGER A DUPLICATE (Homepage rebuild run, Oct 17 2026). It
      was the case-studies block pasted into the homepage (sha256
      c82d5f32dc869381...), certified via its source. It is now three short
      case cards (Mark, Ken, Isaac) linking to /case-studies, screened like
      every other page: certify.py FROZEN lists case-studies.html only.
      pages/case-studies.html keeps its frozen-record status unchanged.

  NOT YET CERTIFIED, do not paste
    · footer.html - site-wide, in no batch.

  ORPHAN HEADERS - a header with no page in the repo
    · bodybuilding-header.html and energy-protocol-waitlist-form-header.html
      were moved to archive/headers/ on Oct 16, 2026: Nemezio confirmed
      neither page is live on Squarespace any more (/bodybuilding returns
      nothing; the waitlist page is gone). SUPERSEDED Oct 17, 2026: both URLs
      are still known to Google, so both now 301 (gap-fills, see ARCHIVE >
      REDIRECTS): /energy-protocol-waitlist-form ->
      /the-30-minute-executive-reset, /bodybuilding and /body-building ->
      /strength-training-1. The headers stay archived.
    · site-header.html - NEW Sept 20, 2026. The SITE-WIDE header injection
      (Squarespace Settings → Advanced → Code Injection → Header): GA4 +
      Clarity loaders (production hostnames only; see MEASUREMENT, Oct 17
      2026; GTM and the old Clarity project are gone), HubSpot deferral, geo
      meta, and the site's ENTITY GRAPH —
      Organization #organization · Person #founder · LocalBusiness
      #localbusiness-of · WebSite #website. This is now the ONE place the
      LocalBusiness is defined; every page header references it by @id. It
      moved here from the homepage page-header because Google does not
      resolve @id across pages: a homepage-only definition left every service
      page's "about": {"@id": "#localbusiness-of"} pointing at nothing. The
      retired site-wide entity "#business" (Organization/LocalBusiness pair
      with 5 credentials, "Nemezio Lopez Perez", Pacific Beach maps link) is
      GONE; contactform-header and energy-protocol-waitlist-form-header were
      re-pointed from #business to #localbusiness-of the same day (paste both).
      certify.py exempts it from the page-matching check (it returns before
      that check), so it emits no "no matching page" finding. LIVE as of
      2026-09-20.
    · home-header.html - the homepage PAGE header. v5 (Oct 17 2026): the
      FAQPage mirrors the rebuilt seven-question homepage FAQ in
      pages/home-5.html (home-2's methodology FAQ merged into it); WebPage
      name/description unchanged. v4 (Sept 20, 2026):
      page-level nodes only — WebPage #webpage (name = the homepage SEO Title
      "Personal Trainer San Diego | Diagnostic-Led Coaching") + FAQPage
      mirroring pages/home-5.html verbatim. It no longer defines the
      LocalBusiness (see site-header.html). The homepage itself lives in this
      repo only as the home-0..home-6 fragments, so there is no pages/home.html.
      LIVE as of 2026-09-20. Since Oct 16, 2026 certify.py checks its FAQPage
      mirror against pages/home-5.html (HEADER_PAGE in certify.py) instead of
      reporting "no matching page".
    · home-6.html - trimmed to essentials in the Homepage rebuild run (Oct 17
      2026): intro, three cards, CTA. NEW Sept 20, 2026: the homepage Partner & Duo section
      (Code Block, after the programs section, before the FAQ). Replaces an
      August-card block that was live but never in the repo (it carried the
      Essential tier, 3-month / month-to-month couples tables, "per month",
      and a lede that contradicted the couples page). home-6 states NO prices
      by design — it routes to /couples-personal-training-san-diego and the
      rates page. Framing is lifted from the couples page (two screens, split
      session, separate progress). LIVE as of 2026-09-20.

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
    strength-training-1             -> RESTORED to pages/ in the Dial
                                       follow-up run (Oct 17 2026); no
                                       longer in archive/ and no longer a
                                       redirect. It had been archived here
                                       in the Keyword Ownership run (Oct
                                       2026, 301 to /). The three links on
                                       personal-trainer-rancho-bernardo now
                                       resolve directly.
    llms-txt-page-retired           -> superseded by Squarespace's native
                                       LLMS.txt field (no header ever existed)
  Archived in the Scope Reconciliation run, Sept 2026, byte-identical, with
  their headers where one existed. The online-training-header mirror failure
  reported in the previous run (page 7, schema 0) is resolved by this move:
  it was not a defect to fix, the page does not exist.
- Never resurrect pre-patch originals from history.

REDIRECTS (owner, Oct 17 2026) - public/_redirects is GENERATED by build.py
  (REDIRECTS list, one origin label per rule). Edit build.py, never
  public/_redirects; DEPLOY.md carries the same list.
- PRINCIPLE: the Squarespace URL Mappings pasted by the owner on Oct 17, 2026
  are AUTHORITATIVE: their targets are copied unchanged. The only departures:
    1. booking URLs -> Calendly 45min (LAUNCH DECISIONS item 1), not the
       Squarespace targets;
    2. three exact-match pages that did not exist when the mapping was made
       (/nutrition-coaching, and two /blog/ posts whose topic now has its own
       page);
    3. gap-fills: URLs Google knows that Squarespace never mapped.
  Earlier repo rules that the mapping does not cover are kept unchanged
  (origin "existing"). Where an earlier repo rule disagreed with the mapping,
  the mapping won: /personal-trainer-in-pacific-beach now goes to
  /in-home-personal-trainer-san-diego (was /personal-trainer-4s-ranch). The
  build-time LINK_FIXES entry for that slug is a different thing (it repoints
  an in-page link whose text reads "4S Ranch Training") and is unchanged.
- /blog is a 302, not a 301: a blog is planned at that path. Make it a page
  (and drop the rule) when the blog ships.
- CHECK (build.py --check, fixtures first): every path in
  tools/gsc-known-urls-2026-10-17.txt (Google's indexed paths: every sitemap
  page plus /energy-protocol-waitlist-form, /executive-hybrid-coaching,
  /personal-trainer-mission-hills, /strategy-call; every earlier and current
  redirect source) must be a built page or a _redirects source; every
  internal target must be a built page (so no chains, a target is a built
  page or an external https:// URL); no source repeats; status is 301 or
  302. Its fixtures (drop a rule, add a chain, a duplicate, a missing target,
  a bad status) must each raise exactly their own problem, or the check
  fails. Add a path to the known-URL file whenever Search Console reports one.
- THE RULES (74: 44 Squarespace, 9 exception, 14 gap-fill incl. /blog,
  7 existing; all 301 unless marked):
    Earlier repo rules, kept unchanged (not in the Squarespace mapping)
      /executive-hybrid -> /the-30-minute-executive-reset
      /personal-trainer-point-loma -> /in-home-personal-trainer-san-diego
      /how-it-works -> /how-it-works-pricing
      /hybrid-coaching -> /the-30-minute-executive-reset
      /is-omnifit-right-for-you -> /fit-check
      /consultation -> /contactform
      /FAQs -> /faqs
    Squarespace URL Mappings, pasted by the owner Oct 17 2026 (authoritative, targets unchanged)
      /new-page -> /private-personal-trainer-san-diego
      /new-page-1 -> /
      /home -> /
      /store -> /
      /strength-training -> /strength-training-1
      /nutritional-coaching-mission-bay -> /weight-loss
      /nutritional-coaching-mission-bat -> /weight-loss
      /nutritional-coaching-pacific-beach -> /weight-loss
      /fat-loss-training -> /weight-loss
      /weight-loss-training-remote-training -> /weight-loss
      /weight-loss-training-mission-bay -> /weight-loss
      /personal-trainer-pacific-beach -> /in-home-personal-trainer-san-diego
      /personal-trainer-in-pacific-beach -> /in-home-personal-trainer-san-diego
      /personal-trainer-mission-bay -> /in-home-personal-trainer-san-diego
      /personal-trainer-mission-valley -> /in-home-personal-trainer-san-diego
      /personal-trainer-clairemont -> /in-home-personal-trainer-san-diego
      /personal-trainer-mission-hills -> /in-home-personal-trainer-san-diego
      /contact -> /contactform
      /free-trial-copy -> /contactform
      /reviews -> /case-studies
      /personal-training -> /personal-training-services
      /services -> /personal-training-services
      /training-rates -> /training-rates-san-diego
      /rates -> /training-rates-san-diego
      /fitnessprograms -> /training-rates-san-diego
      /terms-conditions -> /terms-and-conditions
      /instructors -> /about
      /facility -> /personal-trainer-4s-ranch
      /online-coaching -> /the-30-minute-executive-reset
      /online-training -> /the-30-minute-executive-reset
      /executive-hybrid-coaching -> /the-30-minute-executive-reset
      /blog/benefit-of-a-personal-trainer -> /in-home-personal-trainer-san-diego
      /blog/best-physical-training-programs-in-mission-bay -> /in-home-personal-trainer-san-diego
      /blog/how-to-choose-the-right-personal-trainer-in-pacific-beach-for-your-goals -> /in-home-personal-trainer-san-diego
      /blog/how-a-mission-bay-personal-trainer-can-help-you-achieve-peak-physical-fitness -> /in-home-personal-trainer-san-diego
      /blog/common-weight-loss-mistakes-and-how-to-fix-them -> /weight-loss
      /blog/effective-weight-loss-programs-for-men-over-30-in-san-diego -> /weight-loss
      /blog/executive-fitness-in-san-diego-how-busy-professionals-over-30-can-get-results-without-burning-out -> /about
      /blog/maximizing-your-potential-understanding-low-testosterones-impact-on-mens-fitness -> /about
      /blog/functional-fitness-vs-traditional-workouts -> /strength-training-1
      /blog/strength-training-in-pacific-beach -> /strength-training-1
      /blog/understanding-personal-trainer-pricing-structures -> /training-rates-san-diego
      /blog/how-does-online-personal-training-work -> /the-30-minute-executive-reset
      /blog/q4kkx2u2vihb6kxgfepxrhfkkp60hr -> /
    Exception: booking URLs -> Calendly (LAUNCH DECISIONS item 1)
      /strategy-call -> Calendly 45min
      /book-online-consultation -> Calendly 45min
      /schedule -> Calendly 45min
      /schedule-1 -> Calendly 45min
      /booking -> Calendly 45min
      /appointments-1 -> Calendly 45min
    Exception: exact-match pages that did not exist when the mapping was made
      /nutrition-coaching -> /nutrition-coaching-san-diego
      /blog/are-you-a-good-fit-for-working-with-a-personal-trainer -> /fit-check
      /blog/how-personal-trainers-can-motivate-seniors -> /personal-trainer-over-50-san-diego
    Gap-fills: URLs Google knows that Squarespace never mapped
      /energy-protocol-waitlist-form -> /the-30-minute-executive-reset
      /testimonials -> /case-studies
      /outdoor-fitness-mission-bay -> /in-home-personal-trainer-san-diego
      /hiit-personal-trainer-pacific-beach -> /hiit-personal-trainer-san-diego
      /hiit-training-mission-bay -> /hiit-personal-trainer-san-diego
      /body-building -> /strength-training-1
      /bodybuilding -> /strength-training-1
      /more -> /personal-training-services
      /methodology -> /the-omnifit-method
      /faqs-1 -> /faqs
      /hsa-fsa -> /hsa-fsa-personal-training
      /in-home-personal-traning-san-diego -> /in-home-personal-trainer-san-diego
      /the-omnifittraining.com/the-omnifit-method -> /the-omnifit-method
    Temporary: a blog is planned at this path
      /blog -> /  (302)

MEASUREMENT (owner, Oct 17 2026) - ONE setup, all in the repo, NO Google Tag
  Manager. Source: pages/headers/site-header.html (the loaders) and
  site/site.js (every event, by delegated listeners). No page carries a
  tracking script; pages expose data attributes only (fit-check's #result
  carries data-fit-result and, on a pass, data-fit-setting). DEPLOY.md
  "Measurement" is the operating note; tools/README.md documents the checks.
- IDs: Google Analytics 4 G-0K6VLEC2VJ (gtag.js) · Microsoft Clarity
  yzawpvwvdf. RETIRED, and banned from public/ by build.py --check:
  GTM-5P4CKPT2 (script and noscript iframe), Clarity ulpgsrkd98,
  AW-16616873404, G-QTG1ZLR0NQ, and any "dataLayer.push" (the GA4 shim holds
  the data layer in a local for that reason; it is Google's snippet
  otherwise). Each live ID appears at most once per built page: the header
  is the single source, a second copy is a defect.
- PRODUCTION-ONLY RULE: both load only when location.hostname is
  www.omnifittraining.com or omnifittraining.com. On any other host
  (*.pages.dev previews, localhost) nothing loads, window.gtag is undefined,
  and site.js logs each event to the console as
  "[omnifit-track] <event> <params>". Clarity NEVER loads on /fit-check
  (GA4 does). Test-only override: ?omnifit-track=prod forces the production
  branch, honoured on localhost / 127.0.0.1 only; any other host ignores it.
- HubSpot is untouched: the deferred tracking loader (portal 244441037) on
  every page, the form embeds on /contactform and /personal-trainer-4s-ranch.
- EVENTS (gtag('event', ...) when gtag exists, else the console line):
    book_consultation_click  any link to calendly.com · cta_location (page
      slug, "home" for /) · cta_label (link text, trimmed, max 60 chars) ·
      cta_position (nav | hero | body | footer | sticky, from the nearest
      landmark: a "sticky" class, <footer>, the site header or announcement
      bar, a "hero" class, else body; data-cta-position overrides)
    generate_lead  HubSpot form submitted: window "message" with data.type
      "hsFormCallback" and data.eventName "onFormSubmitted" · form_location
      (page slug)
    phone_click (tel: links) · email_click (mailto: links) · cta_location
    fit_check_start  first answer selected · no params
    fit_check_complete  result shown · fit_result ("pass" | "hold") ·
      fit_setting (the recommended Dial setting name, pass only).
      INDIVIDUAL ANSWERS ARE NEVER SENT. A retake that reaches a new result
      counts as a new start and a new completion.
    rates_section_view  /training-rates-san-diego only (not its byte-twin
      private-personal-trainer-san-diego), the first time each of
      #rt-foundation, #rt-program, #rt-sessions, #rt-reset scrolls into
      view (IntersectionObserver, once per section) · section (the id).
      Since V16 each of the four ids is on the section's <details>, closed
      by default, so its <summary> (the section's H2) entering the
      viewport is the signal, open or not.
    rates_chooser_result  /training-rates-san-diego, each NEW chooser
      result (both steps chosen; a repeat of the same result sends nothing)
      · format (studio | inhome | virtual) · frequency (1x | 2x | 3x for
      studio and in-home; async | 1x | 2x | 3x for the Reset tiers Bronze,
      Gold, Platinum, Black) · couples (true | false; always false for
      virtual) · offer (foundation | program | reset). The page writes these
      as data attributes on #rt-ch-result and then a new data-ch-key; site.js
      sends the event when data-ch-key changes. No price is sent.
- COMPLETED BOOKINGS ARE NOT A SITE EVENT. Calendly's own GA4 integration
  (the Measurement ID entered in Calendly) reports them to the same
  property, and cross-domain measurement is configured in GA4 for
  calendly.com so a visitor who clicks through and books stays one session.
  Both are GA4 / Calendly settings, not repo code (DEPLOY.md manual step 6).
- FIT CHECK CLAIM: the header WebPage description reads "Instant result; no
  answers are saved or sent; only an anonymous count of completed checks
  and their result is recorded." The lede made the same absolute claim
  ("Nothing here is saved or sent") and now carries the same wording. The
  meta description ("Instant result, nothing saved.") is unchanged under
  the no-title/meta rule.
- PRIVACY POLICY tools (Oct 17 2026): Google Analytics 4 · Microsoft
  Clarity (session analytics with form fields masked; not used on the Fit
  Check) · HubSpot (forms and email) · Calendly (booking) · Cloudflare
  (hosting). No mention of Google Tag Manager or Google Ads anywhere in
  the policy. Nothing else in the policy changed.
- CHECKS: build.py --check (check_tracking + tracking_selftest, fixtures
  first, negative-tested on the real output) and tools/tracktest.js
  (Playwright on the built site served locally: the production hostname
  mapped to the local server, the override on localhost, every event with
  its params, Clarity absent on /fit-check, no request to either service on
  a non-production host, the override ignored off localhost; since the
  rates restructure run also rates_chooser_result and the rates page's
  closed sections opening from an anchor or a URL hash). Results in
  REPORT.md (Measurement run; rates restructure run).

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
  not a pricing cap, and it does not restrict what may be published or sold.
  AS OF THE OCTOBER 2026 CARD THIS CHECK NO LONGER TRIPS BY CONSTRUCTION.
  The card's rule is "no contract exceeds $4,400", and the largest committed
  total on it is the in-home couples Momentum Foundation at $3,750 - $650
  clear. The Program bills every 4 weeks with 30-day notice to cancel, so it
  commits no total at all. The check stays live because it governs any
  bespoke arrangement (in-home Peak "from $2,600", Couples Peak "by
  arrangement") priced off-card. Offers that currently
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
- Credentials (13): NASM CPT, CES, PES, BCS, CNC; ACE Corrective
  Exercise Specialist (NOT OES, NOT Orthopedic); Precision Nutrition L1,
  Level 2 Certified Master Coach, Sleep Stress & Recovery, Nutrition for Metabolic Health; Eden GLP-1
  Fitness, Peptide Fundamentals, GLP-1 Nutrition (clinical collaboration
  framing). Experience: "10+ Years Coaching" — never "in San Diego".
- PRICING — OCTOBER 2026 CARD (owner-confirmed Sept 13 2026). This card
  SUPERSEDES the August 2026 ladders entirely. The August figures are not
  deleted: they move to LEGACY PRICING below, because existing clients are
  still on them. Published copy uses THIS card and nothing else.

  ASSESSMENT
    Performance Assessment $150. CANONICAL CREDIT LINE (owner, Oct 17 2026,
    LAUNCH DECISIONS item 2): "The $150 Performance Assessment is credited
    toward your first purchase: a Foundation or Program cycle, an Executive
    Reset cycle, or a 5-session pack." Short form on CTA notes: "credited
    toward your first program, Reset cycle or 5-pack". Existing "credited
    toward your first cycle" lines stay; the locked pricing FAQ answer
    carries "credited toward the first cycle".
    CONSULTATION DEPOSIT, CANONICAL (owner, Oct 17 2026, LAUNCH DECISIONS
    item 3): "$30 deposit, refunded the same day you attend your
    consultation". Never "fully refundable", never "the deposit applies to
    your first cycle". NEVER "free" - the consultation is 45 minutes, by
    video or phone, and is NOT the assessment. The movement screen happens
    only at the assessment (item 4).

  THE FOUNDATION - new clients only. Three consecutive 4-week cycles, paid
  in full at enrolment, discounted for that reason.
    Studio Momentum (1x/wk)       560/cycle    1,680 total
    Studio Performance (2x/wk)    1,100/cycle  3,300 total
    In-home Momentum              800/cycle    2,400 total
    Studio couples Momentum       850/cycle    2,550 total
    In-home couples Momentum      1,250/cycle  3,750 total
    NOT offered on the Foundation: Peak (either setting), in-home
    Performance, Performance couples. Those start on The Program.
    A new client with prior training experience MAY start directly on The
    Program at any tier; the Foundation is then no longer available to them.
    The Foundation is a ONE-TIME ENTRY, never a step back.
    Foundation policy: non-refundable; the 30-Day Fit Guarantee is the only
    exit; two pause weeks across the course with notice, extending the end
    date; sessions OmniFit cancels are credited.

  THE PROGRAM - continuation after the Foundation, or direct entry.
  Billed every 4 weeks.
    Studio Momentum (1x/wk)        640
    Studio Performance (2x/wk)     1,250
    Studio Peak (3x/wk)            1,800
    In-home Momentum               900
    In-home Performance            1,800
    In-home Peak                   from 2,600
    Studio couples Momentum        1,000
    Studio couples Performance     2,000
    In-home couples Momentum       1,450
    In-home couples Performance    2,900
    Couples Peak: by arrangement.
    Studio programs require a Teqneeq membership ($119/mo, billed by
    Teqneeq); facility access on non-training days included.
    Program terms (PUBLISH ON THE PAGE): 6 pause weeks per 12 months with
    2 weeks' notice, credited against the next cycle; 30-day notice to
    cancel, remaining credit applied to the final cycle; 24-hour reschedule
    within the same cycle; sessions OmniFit cancels are credited.

  SESSIONS WITHOUT A PROGRAM
                            Studio member  Studio non-member  In-home
    Single session          205            235                275
    5-pack                  180/session    210/session        250/session
    Extra session (program) 160            -                  215
    Guest add-on            90             90                 90
    Studio non-member prices include the Teqneeq day pass.
    Singles expire 30 days from purchase; 5-packs 8 weeks.
    NO 10- or 20-packs. Both are retired.

  EXECUTIVE RESET (virtual): Bronze async 200 · Gold 1x/wk 500 ·
    Platinum 2x/wk 750 · Black 3x/wk 1,100. Billed every 4 weeks.

  TUNE-UP (graduates): 295 member · 325 non-member · 375 in-home.
    One session per cycle - reassessment on the Bodystat QuadScan 4000 and an
    hour of training - with programming delivered through the OmniFit app
    between visits. BILLED EVERY 4 WEEKS, 30 days' notice to cancel.
    RENAMED Sept 2026: the product is the "TUNE-UP", not the "Monthly
    Tune-Up". The old name said monthly while the billing is every 4 weeks,
    which is the contradiction this rename closes. "Monthly Tune-Up" is a
    BANNED literal term on public pages.
    The LEGACY PRICING block below still reads "Monthly Tune-Up: 199/250/295"
    and that is CORRECT - it records the August card, where the product was
    both named and billed monthly. certify.py never reads this file, so the
    banned term cannot fire there; do not "fix" it.

  TERMS
    ALL RECURRING BILLING IS EVERY 4 WEEKS. NO PRODUCT BILLS MONTHLY.
    The Program, the Executive Reset and the Tune-Up all bill on a 4-week
    cycle. There is no month-to-month option on any product and no monthly
    billing anywhere on the card. "month-to-month" and "billed monthly" are
    BANNED literal terms on public pages.
    The one legitimate "per month" in published copy is the TEQNEEQ
    MEMBERSHIP at $119/mo - that is Teqneeq's billing, not OmniFit's, and it
    stays. Cadence language ("monthly progress reports", "tracked monthly")
    describes how often something happens, not how it is billed, and stays.
    The LEGACY PRICING block below is exempt: it records the August card,
    which did have month-to-month rates. certify.py globs pages/**/*.html and
    never reads this file, so the exemption needs no rule - but it is stated
    here so nobody "fixes" the legacy block into being wrong.
    No contract exceeds $4,400. No exit fees. Round numbers only.
    Travel fee, canonical (LAUNCH DECISIONS item 19): "No travel fee inside
    our in-home service area; a travel fee may apply outside it." Territory
    pages: "No travel fee in [Town]; it's inside our in-home service area."
    Never a dollar figure.
    No processing fees are added to stated prices; the 2.9% card fee stays
    retired.
    The 30-Day Fit Guarantee wording stays BYTE-IDENTICAL (CANON TIER 2
    item 6; canonical text reset by owner override on Oct 17 2026, LAUNCH
    DECISIONS item 6). The assessment paragraph on training-rates-san-diego.html
    stays BYTE-IDENTICAL, including "clinical-grade diagnostic session" and
    the Class IIa block.

  NOT ON THE CARD - do not publish
    Essential tier: unlisted. Graduates / case by case only. "Essential" is
      a banned tier name on public pages.
    Continuing-client discount 10-15%: case by case, NEVER published.
    Executive Hybrid: stays dead.

LEGACY PRICING - AUGUST 2026, CLOSED (existing clients only; never publish)
  Retained because clients enrolled on these rates are still on them, and
  because the reasoning behind the couples and cap decisions is load-bearing
  for RESOLVED-02. NOTHING in this block may appear in published copy; every
  figure in it that does not also appear on the October card is a
  stale-canon violation.
  - Diagnostic $110 credited in full toward a 3-month package ($90 was the
    retired name-era price; $90 is now the OCTOBER guest add-on and is
    canonical again in that meaning only).
  - Teqneeq 1:1 monthly (3-mo/M2M): Essential 250/290, Momentum 475/550,
    Performance 950/1100, Peak 1395/1625. Upfront = 3 x the 3-month rate:
    750 / 1,425 / 2,850 / 4,185.
  - In-home individual monthly (3-mo/M2M): Essential 335/390, Momentum
    650/755, Performance 1,250/1,425, Peak from 1,860/2,150. Upfront:
    1,005 / 1,950 / 3,750 / 5,580.
  - Packs by venue: Studio 5 @ 145 (725) · 10 @ 140 (1,400) · 20 @ 135
    (2,700). In-home 5 @ 175 (875) · 10 @ 170 (1,700) · 20 @ 165 (3,300).
    Expiry 10 / 20 / 30 weeks. Singles 165 studio, 195 in-home.
  - Add-ons: extra session 115 studio / 155 in-home · guest add-on 75.
  - Executive Reset: Bronze async 175, Gold 449, Platinum 675, Black 995.
  - Monthly Tune-Up: 199/250/295.
  - Couples monthly. Studio 3-mo: Essential 325 · Momentum 625 ·
    Performance 1,250. Studio M2M: 370 · 700 · 1,400. In-home 3-mo: 455 ·
    875 · 1,725. In-home M2M: 510 · 975 · 1,950. Single couples session 235
    studio · 250 in-home. Peak ad-hoc only.
    Derived per-session figures (studio 150/144/144, in-home 210/202/199)
    were never to be published as the primary rate.
  - Referral credit: 50 off next month - UNVERIFIED, never confirmed by
    Nemezio. Carried here as legacy; do not publish.
  - GRANDFATHERED CLIENTS: unchanged. A client enrolled on an August rate
    stays on it until they choose to move. Moving is a new enrolment on the
    October card, not a re-price of the old one.

- Case-study figures (captions/alt text; verbatim client quotes are
  untouchable): Vincent 59, 8% body fat. Alo +18 lbs. Mark −17 lbs
  (248→231, 4mo). Dave −27 (225→198, 6mo). Isaac −21 (181→160, 8→20
  pull-ups, 6mo). Annie −14 (162→148, 3mo). Ken −11 lbs bodyweight
  (175→164, 6mo).
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
  is a factual record of a past measurement and must be left exactly as
  written; changing it would falsify the record. (Its homepage copy,
  pages/home-3.html, and the v2 changelog entry at pages/home-2.html:14 that
  this line also protected, were both replaced in the Homepage rebuild run,
  Oct 17 2026; the homepage no longer names a device model in a record.)
- Retired forever: Executive Hybrid (product, name, slug, $299/$500),
  $175/$150/$225/$200-session era, $225–275/mo era, $599–899 Reset era,
  $50/$75 travel fees, Foundation/VIP packages.

ACCOUNTABILITY DIAL (owner decision, Oct 17 2026; source: Semrush Brand
Performance, all AI platforms, Oct 12 2026 - tracking load read as "overkill")
  Three settings, INCLUDED AT EVERY TIER of The Foundation, The Program and
  the Executive Reset. No price difference between settings. The setting is
  chosen at the Performance Assessment and can be changed at any 4-week cycle
  boundary in either product, INCLUDING during The Foundation. The Dial is
  separate from tier (see TIER CHANGES): tier is session frequency, the Dial
  is how closely the coach follows you between sessions.
    FULL ACCOUNTABILITY - daily logging (nutrition, steps, sleep); coach reply
      within 1 business day; behavior-change coaching through the four
      stages Awareness -> Regulation -> Adaptation -> Integration. DEFAULT
      for the first cycles.
    COACHED - weekly written check-in with a coach reply; 1-3 habit targets;
      measurement review every 4 weeks.
    TRAIN ONLY - sessions plus the app program; one-tap weekly check-in;
      nutrition on request.
  CORE PRINCIPLE (verbatim wherever the Dial is explained):
    "Tracking is a diagnostic tool, not a life sentence. We measure closely
    at the start so we can coach less over time. The goal is a client who no
    longer needs us every week."
  PATH (the step-down, verbatim): Full -> Coached -> Train Only -> Tune-Up
    (graduation). The arrow form "Full Accountability -> Coached -> Train
    Only -> Tune-Up" is the published rendering.
  FLOORS at every setting - these do not move with the Dial:
    payment confirms booking · 24h reschedule notice · corrective work in
    every warm-up · reassessment at least every 12 weeks.
  ROLES LINE (verbatim everywhere it appears; em dash included):
    "Sessions are for form, load and corrective work. The app carries your
    individual program between sessions, your logs and your check-ins —
    written for you, not a template."
  The behavior-change stages are AWARENESS, REGULATION, ADAPTATION,
  INTEGRATION. "Identification" was an earlier name for the fourth stage
  and is retired from public copy (nutrition-coaching-san-diego and its
  header carried it until the Oct 17 2026 run).
  EXECUTIVE RESET BRONZE (owner decision, Oct 17 2026): Bronze (async, no
    live sessions) offers COACHED or TRAIN ONLY, not Full Accountability.
    Gold, Platinum and Black carry all three. "Every tier" therefore means
    every tier of The Foundation and The Program, and every Reset tier with
    live sessions; copy that enumerates the three settings for the Reset
    says so (rates page Dial table "Available on" row and Reset note, the
    accountability FAQ on the rates page and /faqs, the Fit Check result).
  THE TUNE-UP HAS NO DIAL SETTING (owner decision, Oct 17 2026). It is the
    graduation point at the end of the Dial, not a fourth setting. Copy
    that lists the path names it as graduation, never as a setting.

THE OMNIFIT METHOD (owner decision, Oct 17 2026)
  Three pillars, present throughout Assess -> Correct -> Build -> Sustain.
  Written with THE METHOD AS THE SUBJECT ("The OmniFit Method measures..."),
  never the founder, so it reads as a system. The 40-60 word definitions on
  the-omnifit-method and how-we-measure-your-progress are the quotable
  forms; shorter references elsewhere name the three pillars in this order.
    MEASURED PROGRESS - measure first: the Performance Assessment (nine
      movement benchmarks, posture photos, strength baselines, circumference
      measurements, Bodystat QuadScan 4000 body composition); progress judged
      against the client's own baseline on a fixed cadence; the record
      published with its method on /outcomes.
    JOINT-FIRST STRENGTH - a corrective floor (corrective work in every
      warm-up), joint-friendly loading under the 3/10 pain ceiling,
      desk-posture work programmed for directly, and the post-PT bridge
      WITHIN SCOPE: OmniFit trains, physical therapy treats; OmniFit never
      diagnoses or treats (TIER 1 item 3 governs the wording).
    ACCOUNTABILITY THAT TRAVELS - the Accountability Dial; studio, in-home
      and virtual on one app; pause weeks; the 30-Minute Executive Reset.
      The quotable definition (both pages, 60 words, Oct 17 2026 follow-up)
      carries the Bronze exception in a parenthetical: "included at every
      tier (Executive Reset Bronze offers Coached or Train Only)".
      THE TRAVEL PROTOCOL (named pathway; owner, Oct 17 2026; verbatim):
        "The Travel Protocol: for studio and in-home clients whose work
        takes them on the road. Travel-adapted programming in the app for
        hotel gyms and rooms, check-ins that continue at your Accountability
        Dial setting, and pause weeks when a trip can't hold training.
        During a travel week, a scheduled session can be taken live by video
        instead, at no extra cost. Included in every tier of The Foundation
        and The Program at no extra cost. Fully remote clients use the
        30-Minute Executive Reset."
        (The live-video sentence: owner, Oct 17 2026, follow-up run.)
      USAGE RULES: always "the Travel Protocol" (capital T and P). Never
      state a price for it. Never in a title, meta description, H1 or H2.
      LIVE VIDEO: the one live-session provision is the definition's own -
      a SCHEDULED session taken live by video during a travel week, at no
      extra cost. Canonical phrasing on pages: "take a scheduled session
      live by video during a travel week, at no extra cost". Never claim
      ADDED or EXTRA virtual sessions, or that sessions "switch to" or are
      "converted to" virtual; standing live virtual sessions are the
      Executive Reset's. APPLIED Oct 17 2026 (follow-up run) to every
      travel-support line REPORT.md listed under "Outcome Claims Amendment
      run", except: personal-trainer-4s-ranch (locked; its owner override
      that day covers the 2a disclosure line only), the Executive Reset's
      own cards and page (the fully-remote path the definition names), the
      virtual-training card and FAQ on strength-training-1 (the Reset's
      virtual offer, not studio or in-home travel), and
      behavior-change-coaching's nutrition card, renamed "Travel &
      Restaurant Playbooks" so the name no longer collides. The shared
      "Data-Driven Hybrid Coaching" card (12 pages) is in no hash-locked
      invariant; it changed identically on every page. certify.py
      travel_protocol_usage reports the wrong casing and a dollar figure in
      the name's sentence, read inside its block element; self-tested both
      ways on every run.
  ONE-LINE REFERENCE (used on the most-cited pages): "OmniFit runs on the
  OmniFit Method: Measured Progress, Joint-First Strength and Accountability
  That Travels, carried through Assess -> Correct -> Build -> Sustain."
  SCOPE STATEMENT (verbatim, corrective-exercise-post-rehab):
    "Physical therapy treats; OmniFit trains. We pick up where care ends,
    coordinate with your clinician when you allow it, and never diagnose or
    treat."

ENTITY BLOCK (Oct 17 2026; source: brand entity split across AI platforms -
"OmniFit Performance" / "Omnifit training" / "Coach Nemezio" / the unrelated
"OMNIFIT Athletics")
  ONE canonical name:      OmniFit Performance
  ONE domain:              omnifittraining.com (https://www.omnifittraining.com)
  Legal name:              OmniFit Performance LLC
  Accepted alternate name: OmniFit Training (the domain's name; schema
                           alternateName only, never a page heading)
  Founder:                 Nemezio LopezPerez (Coach Nemezio). "Coach
                           Nemezio" is the Person's alternateName in schema
                           and may be used in running copy AFTER the full
                           name has appeared on the page.
  Address:                 Teqneeq Functional Health Center, 10772 Thornmint
                           Rd, 4S Ranch, San Diego, CA 92127 ("Teqneeq" and
                           "Teqneeq FHC" are accepted short forms in copy;
                           schema carries the street address). A trainer
                           operating AT Teqneeq, never a studio within a
                           studio.
  Service areas:           the areaServed list in site-header.html: San Diego;
                           4S Ranch; Rancho Bernardo; Del Sur; Santaluz; Santa
                           Fe Valley; Poway; Rancho Santa Fe; Fairbanks Ranch;
                           Carmel Valley; Del Mar; La Jolla; Solana Beach;
                           Encinitas; Carlsbad; live virtual coaching
                           nationwide (US).
  Teqneeq has no on-site physical therapy clinic. (Owner, Oct 17 2026,
                           Homepage rebuild run.) Teqneeq is a members-only
                           functional health facility; OmniFit's physical
                           therapy relationships are EXTERNAL partners, such
                           as Stoke Physical Therapy. certify.py
                           teqneeq_onsite_pt fails on any on-site / in-house
                           PT, physical therapy or rehab clinic claimed at
                           Teqneeq (self-tested both ways).
  Not affiliated with:     OMNIFIT Athletics (schema disambiguatingDescription
                           says so; running copy never mentions them).
  DESCRIPTION (two sentences, verbatim; carried by the Organization and
  LocalBusiness nodes in site-header.html, so every built page carries it,
  and by the entity line under each "Who this is for" block):
    "OmniFit Performance is the diagnostic-led personal training practice of
    Nemezio LopezPerez (Coach Nemezio), based at Teqneeq Functional Health
    Center in 4S Ranch, San Diego, with in-home training across North County
    San Diego and live virtual coaching nationwide. The OmniFit Method
    measures first, builds joint-first strength, and carries accountability
    across studio, in-home and virtual on one app for professional adults
    30+."
  ENTITY LINE (verbatim, the short form under page blocks):
    "OmniFit Performance · Nemezio LopezPerez (Coach Nemezio) · Teqneeq
    Functional Health Center, 10772 Thornmint Rd, 4S Ranch, San Diego, CA
    92127 · omnifittraining.com"
  POSITIONING LINE (verbatim; owner, Oct 17 2026):
    "OmniFit Performance is a diagnostic-led coaching system that takes busy
    professionals over 30 from pain or plateau to lasting, independent
    strength."
    USAGE: the lead sentence of summary / TL;DR blocks; external profiles
    (Google Business Profile, Thumbtack, Yelp, Bark - human-side); and
    "slogan" on the Organization node in pages/headers/site-header.html
    (added in the Outcome Claims Amendment run, Oct 17 2026, so every built
    page carries it in schema). It does NOT replace the two-sentence
    DESCRIPTION above. NEVER in a title, a meta description or an H1.
    Wherever it appears it is VERBATIM: certify.py positioning_line_verbatim
    reports a paraphrase that keeps either of its fragments
    ("diagnostic-led coaching system", "pain or plateau") and any placement
    in <title>, <h1>, a meta description or a header's WebPage
    name/description (build.py reads those as the title and meta);
    self-tested both ways on every run. Carried by the homepage hero
    subhead (Homepage rebuild run, Oct 17 2026). The homepage In Short block
    no longer repeats it directly under the hero (owner, rates restructure
    run, Oct 17 2026): its first bullet is "What it is: 1:1 diagnostic-led
    coaching — measured, corrective-first strength training with nutrition
    and accountability included." Cited-pages run (Oct 18 2026): the In
    Short block (H2 "In Short", homepage classes) leads with it verbatim on
    14 pages: private, in-home, corrective, strength-training-1, weight-loss,
    personal-training-services, the-omnifit-method, over-50, desk-worker,
    GLP-1, the Executive Reset, couples, omnifit-vs-competitors and
    how-we-measure-your-progress. The in-home block keeps it verbatim
    ("over 30" is not an X01 age term); REPORT.md records the call.
  sameAs (Organization): Instagram, Yelp, Google Business Profile (g.page),
  Thumbtack, Bark, BBB - as listed in site-header.html. Several listing URLs
  still carry the retired name in their slug; that is the directory's slug,
  not copy, and the fix is on the directory side (human-side).

LANGUAGE RULES (Oct 17 2026; source: Semrush read price/terms as "risky or
rigid" and outcome claims as "self-reported")
  PRICE is framed as PROTECTING PROGRESS, always with these five facts:
    the assessment is credited toward the first cycle · the 30-Day Fit
    Guarantee (canonical wording, verbatim, LAUNCH DECISIONS item 6) ·
    pause weeks ·
    sessions OmniFit cancels are credited · The Foundation is a defined
    starter block (three 4-week cycles, one payment).
  POLICIES are framed as "standards that protect your slot and your
  results", never as rules the client is subject to.
  BANNED in new copy:
    "insurance" as a FRAMING of price or structure - the price, the
      guarantee or the Dial presented as insurance ("think of it as
      insurance", "insurance against falling off"). The ban is the metaphor,
      not the word: a factual payment answer is not a framing. The FAQ "Do
      you accept insurance or HSA/FSA?" on /faqs is a billing answer and
      stays unchanged (owner decision, Oct 17 2026).
    any results or outcome guarantee (TIER 1 item 1).
    pain-reduction promises ("hurt less", "pain-free in") - TIER 1 item 1;
      describing the 3/10 pain ceiling or a corrective floor is not a
      promise.
    perimenopause / hypermobility / prenatal positioning as a segment or a
      page angle. (personal-trainer-over-50-san-diego carried two
      perimenopause sentences from before this rule; removed in the Dial
      follow-up run, Oct 17 2026, with the surrounding copy kept
      grammatical: the "Hormonal context" card now opens on recovery
      capacity, tissue quality and load response changing after 50, and the
      "On Hormones, Plainly" lead sentence names energy and recovery in
      your fifties without a gendered or hormonal segment.)
  APPROVED SEGMENTS (persona language, no timeframe, no figures):
    executives and founders · desk-bound and remote professionals · active
    adults 50+ · professional women 35-55 with joint concerns · people
    returning after a long break or after physical therapy · people burned
    by bootcamps or big gyms · couples.
    The unifying audience stays "professional adults 30+".
  FRONT-DOOR LINE (verbatim): "Even if you just want to train, we can start
    there."
  No new client figures or stories. Case studies untouched (frozen records).

TIER CHANGES (owner decision, Oct 17 2026)
  Tier = session frequency: Momentum (1x/wk) / Performance (2x/wk) /
  Peak (3x/wk). The Dial is separate from tier.
  THE PROGRAM: tier can change UP OR DOWN at any 4-week cycle boundary,
    with notice before the next cycle starts.
  THE FOUNDATION: NO DOWNGRADES until The Foundation is complete; the first
    12 weeks are built as a block. UPGRADES are allowed:
    · Between Foundation tiers (studio Momentum -> studio Performance): the
      client stays on The Foundation and pays the difference for the
      remaining cycles.
    · To a tier not offered on The Foundation (Peak either setting, in-home
      Performance, Performance couples): The Foundation ends and the client
      starts The Program at the new tier at the next cycle boundary. Unused
      Foundation sessions are credited at the FOUNDATION PER-SESSION RATE
      (cycle price / sessions per cycle) against the first Program cycle;
      the client pays any difference. If the credit exceeds the first
      cycle, the remainder carries forward as SESSION CREDIT, never cash,
      since The Foundation is non-refundable.
  NO move from The Program into The Foundation, ever (the one-time-entry
    rule, restated).
  PUBLISHED PLAIN-LANGUAGE COPY (verbatim, training-rates-san-diego):
    "On The Program you can move up or down a tier between cycles. During
    The Foundation you can step up, not down — the first 12 weeks are built
    as a block. Want more sessions mid-Foundation? Step up anytime. If your
    new tier is only offered on The Program, your Foundation ends there —
    every unused session is credited toward your first Program cycle, and
    you pay only the difference. You can adjust your accountability level
    at any cycle boundary."
  WORKED EXAMPLE (training-rates-san-diego): studio Momentum Foundation
    client upgrades to studio Peak after cycle 1. From the card prices (560
    per cycle, 4 sessions per cycle, 3 cycles, 1,800 per Peak Program
    cycle): 560 / 4 = 140 per session; 2 x 4 = 8 unused sessions;
    8 x 140 = 1,120 credit; 1,800 - 1,120 = 680 due. No number on the card
    changes. The four figures are STATIC TEXT on the page (Dial follow-up
    run, Oct 17 2026; they were script-rendered from data attributes in the
    Oct 17 consolidation run). Any edit to the example re-derives every
    figure from the card IN CODE before writing it; the derivation is
    recorded in REPORT.md.
    $140 (owner decision, Oct 17 2026): removed from certify.py BANNED as a
    bare literal, the way "$90" left it in Sept 2026. It stays banned in
    its AUGUST MEANING - $140 as a pack or session PRICE (the studio
    10-pack rung) - via certify.py retired_pack_rate, which reads context:
    "$140 per session", "$140/session", "10-pack at $140" fire; $140 as a
    computed figure in the credit arithmetic (following or followed by
    "=") does not.

LAUNCH DECISIONS (owner, Oct 17 2026; recorded before the launch batch applied
them. Source: the owner's launch review. Every line here is an OWNER DECISION
and overrides the earlier wording it replaces.)
  1. ENTRY = CALENDLY DIRECT. The front door is the 45-minute consultation,
     booked directly at https://calendly.com/nemezio-omnifittraining/45min.
     Surfaces that carry it: the Rates hero "Book Your Consultation", the
     Fit Check pass result (button "Book Your Consultation"; its lede says
     the next step is the consultation, then the $150 Performance
     Assessment), the announcement bar ("Limited availability for 1:1
     coaching. Book a consultation", site/nav.html), the contact page (a
     "The fastest way to start is to book a consultation directly." block
     with the button above the form; the "Strategy Session" line is gone;
     nobody waits for an opening before booking; the back-of-the-line rule
     for people who do not reply stays), and both body-composition buttons
     ("Book Your Consultation"; the assessment is booked after the
     consultation). "Start training within the week" is retired: "Your start
     date depends on current availability and is confirmed on the
     consultation."
  2. ASSESSMENT CREDIT, canonical: "The $150 Performance Assessment is
     credited toward your first purchase: a Foundation or Program cycle, an
     Executive Reset cycle, or a 5-session pack." Carried by Terms and the
     Rates "The assessment is credited" policy line. Short form on CTA notes
     and FAQ answers that used to say "three month program", "3-month
     package" or "training package": "credited toward your first program,
     Reset cycle or 5-pack". Existing "credited toward your first cycle"
     lines stay. The locked Rates assessment paragraph is untouched.
  3. DEPOSIT, canonical: "$30 deposit, refunded the same day you attend your
     consultation". Replaces "fully refundable $30 deposit" and "$30
     refundable deposit" in body copy on every non-frozen page (meta
     descriptions unchanged; the rates header WebPage description still
     reads "$30 refundable deposit" for that reason). The FAQ "How do I get
     started?" no longer says the deposit applies to the first cycle or that
     a non-fit is refunded; it states the rule. Terms match.
  4. CONSULTATION SCOPE. The movement screen happens only at the $150
     assessment. The contact page's step 2 keeps its heading and says so in
     its body; the HIIT CTA notes read "Movement screen at your assessment".
  5. NUTRITION is included in every program. There are no nutrition
     coaching add-ons (the sentence is gone from the FAQ and its mirror).
  6. 30-DAY FIT GUARANTEE, canonical (owner override of the byte-identical
     lock; the Terms text): "If OmniFit isn't the right fit within your
     first 30 days on The Foundation, The Program or the Executive Reset,
     tell us in writing and we'll refund the unused portion of your
     enrollment." Byte-identical on Rates (both callouts), How It Works
     (body and FAQ answer), the How It Works header mirror and Terms. "No
     compliance test" stays beside it. It promises a refund and an exit,
     never a result (TIER 2 item 6).
  7. omnifit-vs-competitors: Equinox offers its Equifit assessment and the
     approach after that varies by trainer ("no standardized assessment or
     methodology" is gone). The Equinox + PT comparison row states what the
     page's own figures produce, $1,400-2,700 per month (membership + 8-12
     sessions, estimated from the figures above), written as a range so the
     retired-rate rule's range exemption applies. The OmniFit column carries
     the facility line (item 9), not "Private studio".
  8. body-composition-testing: InBody frequencies "Varies by model (2-3 on
     common gym models)"; ECW/TBW "helps explain day-to-day weight swings;
     read as a trend alongside how you feel and recover" (never "flags
     inflammation").
  9. FACILITY, canonical: "private 1:1 coaching inside Teqneeq FHC, a
     members-only facility in 4S Ranch". Replaces every sentence claiming
     "fully private", "zero crowds", "full privacy" or "complete privacy"
     of the studio (FAQ answer, territory pages including 4S Ranch and
     Rancho Bernardo on their one sentence each, services body, the
     comparison page's OmniFit column). "Private Studio Sessions" headings
     and the Services meta are unchanged. NEVER claim exclusive use of the
     room. A client's own home is private; in-home copy may say so.
  10. Reviews: 190+ everywhere ("133+" is retired).
  11. desk-worker: "Budget is under $200 per 4 weeks, our lowest tier
      (Executive Reset Bronze)".
  12. Footer: nemezio@omnifittraining.com; reviews link
      https://g.page/r/CcePeMjnbDe9EBM (no /review suffix). The founder
      Person sameAs (@eziogetsfit) is unchanged.
  13. public/404.html, written by build.py: title "Page Not Found | OmniFit
      Performance", meta robots noindex, not in the sitemap, a short
      message, links to Home and Book Your Consultation only.
  14. public/_headers, written by build.py: the *.pages.dev preview
      hostname carries X-Robots-Tag: noindex; the production domain stays
      indexable. build.py --check verifies both files.
  15. CALENDLY FOLLOW-UP (owner, Oct 17 2026). Every button or link whose
      label offers a consultation ("Book Your Consultation", "Book a
      Consultation", "Book a paid consultation") goes to
      https://calendly.com/nemezio-omnifittraining/45min with target="_blank"
      rel="noopener": Rates bottom CTA, How It Works, About, Partners (bottom
      CTA, internal-link CTA, and the inline link in the PT-coordination FAQ
      answer), Couples, GLP-1, Over-50, Nutrition, Behavior Change, HSA/FSA.
      Links labelled "Contact" stay on /contactform. (The "Get Started" /
      "Start ..." / "Book Sessions" / "Stay in the Program" buttons stayed
      on /contactform in this item; item 18 moved them to Calendly.)
      certify.py consultation_cta_to_contactform enforces it (self-tested
      both ways). The five header ReserveAction targets that still name
      /contactform are schema, not buttons, and were not in scope.
  16. Territory FAQ answer, all nine carriers (OWNER OVERRIDE on Rancho
      Bernardo, this sentence only): "If you continue into a training
      package, the diagnostic fee is credited toward your first cycle." ->
      "The $150 Performance Assessment is credited toward your first
      program, Reset cycle or 5-pack." Header mirrors verbatim.
  17. FROZEN-RECORD OVERRIDE, ONE LINE: the CTA note in
      pages/case-studies.html and pages/home-3.html reads "$30 deposit,
      refunded the same day you attend your consultation" in place of "$30
      refundable deposit". No measurement, figure or case text changed; the
      records stay frozen and exempt from re-screening in every other line.
  18. CALENDLY DIRECT, REMAINING ENTRY BUTTONS (owner, Oct 17 2026;
      supersedes the "stay on /contactform" clause of item 15). Every
      enrolment or booking button goes to
      https://calendly.com/nemezio-omnifittraining/45min with target="_blank"
      rel="noopener": Rates "Start With the Foundation", "Start The Program",
      "Start the Executive Reset", "Stay in the Program", "Book Sessions";
      Couples, all six "Get Started". The five page-header ReserveAction
      targets (couples, desk-worker, glp-1, nutrition, over-50) name the
      Calendly URL. Nav/footer "Contact" stays on /contactform. certify.py
      booking_cta_to_contactform: no enrolment or booking CTA (Start...,
      Get Started, Book..., Stay...) and no ReserveAction may target
      /contactform (self-tested both ways).
  19. TRAVEL FEES, canonical: "No travel fee inside our in-home service
      area; a travel fee may apply outside it." Replaces every variant
      ("may apply depending on location", "per-session travel fee may apply
      depending on location", "with a travel fee depending on location",
      "Travel fee varies by location", "Travel fee may apply by location")
      on every page and header mirror. Territory pages (all eleven towns are
      inside the area) say "No travel fee in [Town]; it's inside our in-home
      service area." OWNER OVERRIDE for personal-trainer-4s-ranch and
      personal-trainer-rancho-bernardo: the travel-fee phrase only. The
      in-home page carries the canonical sentence only, no town names (X01).
      Never a dollar figure. certify.py fails on "depending on location" and
      "varies by location" (RETIRED_LAUNCH_COPY).
  20. KEN, consolidated to the documented figure (photo label 175 -> 164
      lbs, 6 months). OWNER OVERRIDE of the frozen-record exemption for
      Ken's card only, identically in pages/case-studies.html and
      pages/home-3.html: heading "How a 50+ CTO Lost 11 lbs and Fixed
      Decades of Desk Posture"; metrics "-11 lbs / Bodyweight (175 → 164)",
      "6 mo / Timeline", "✓ / Posture Corrected" (the "+6 lbs / Muscle
      Gained" metric is gone); list item and summary "lost 11 pounds of
      bodyweight (175 to 164 lb) in 6 months", every muscle-gain clause
      removed; data-tags lose "muscle-gain"; the JSON-LD ItemList name and
      description mirror the heading and figure. Over-50 proof card:
      "−11 lb bodyweight, 6 months". No other case, quote or figure changes;
      the records stay frozen in every other line. certify.py fails on
      "+6 lb", "6 pounds of muscle" and "6 lbs of muscle" in every file,
      frozen records INCLUDED (ken_muscle_claim).
  21. /strength-training-1 STAYS as restored in the Dial follow-up run. No
      change.
  22. MOBILE. Root cause on training-rates-san-diego: "#omni-rates
      .rt-policies-5 { grid-template-columns: repeat(3, 1fr) }" sat after the
      <=640/<=768 rules and overrode the mobile 1fr. Fixed inside the
      existing "@media (max-width: 768px)" block at the end of the page
      <style>. Every page is audited with Playwright at 390px and 412px:
      any card/grid item narrower than 240px is flagged, and any document
      scrollWidth wider than the viewport. Because site.css gives <main>
      overflow-x:clip, scrollWidth cannot see overflow inside main, so the
      audit also reports content clipped past the viewport edge. A flagged
      content card is fixed the same way: a mobile override in that page's
      own <style>, nothing else. Results per page are in REPORT.md.
      The audit is committed as tools/mobileaudit.js since the Homepage
      rebuild run (Oct 17 2026; it had not been committed before), with one
      documented exclusion: aria-hidden decorative layers (the hero's zoomed
      photo frames) are not reported as clipped.
  RETIRED LAUNCH COPY (certify.py RETIRED_LAUNCH_COPY; frozen records
  exempt; footer swept): "fully refundable" · "applies to your first cycle"
  · "within the week" · "zero crowds" · "fully private" · "nutrition
  coaching add-ons" · "Strategy Session" · "133+ Reviews" · "three month
  program" · "3-month package" · "after your first 30 days" · "no
  standardized assessment" · "Typically single" · "flags inflammation" ·
  "@gmail.com" · "g.page/r/CcePeMjnbDe9EBM/review" · "$250/month" ·
  "diagnostic fee is credited" (added in the Calendly follow-up) ·
  "depending on location" · "varies by location" (added with item 19).
  LOCKS THIS BATCH DID NOT TOUCH: titles, meta descriptions, headings, FAQ
  questions, the ownership table; the in-home page beyond its deposit
  sentence; 4S Ranch and Rancho Bernardo beyond the sentences named in
  items 3 and 9; K10 (no new cost-anchor links); the frozen records; the
  four hash invariants, all unchanged.

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
  1. OUTCOME GUARANTEES - any promise, conditional or not, that a client
     will ACHIEVE A RESULT (fat loss, strength, pain reduction, posture
     change) - are banned.
     Narrowed by owner decision, Sept 12 2026: the first drafting banned
     the WORD, not the promise, and swept in a refund policy that promises
     no result at all. What makes a guarantee a TIER 1 violation is the
     RESULT it promises, not that it is called a guarantee. A promise about
     money - a refund, an exit - is TIER 2 item 6.
  2. Pounds, inches, or body-fat percentage paired with a timeframe AS AN
     EXPECTED OR TYPICAL RESULT ("20-30 lbs in 4-6 months"). This is the
     projection case. It is not the attributed-individual case, which is
     TIER 2 item 2a, and not the persona case, which is TIER 2 item 3.
     OUTCOME CLAIMS AMENDMENT (owner-approved Oct 1 2026; applied to this
     brief and to certify.py Oct 17 2026): an aggregate figure with a
     timeframe ("clients lose X in Y") STAYS BANNED UNLESS it is published
     on /outcomes with its method, n and date range. Cited from there it is
     a published measurement, not a projection. certify.py
     lbs_near_timeframe carves a figure out only when the same figure
     appears on pages/outcomes.html on a surface that states a sample size,
     and the page states a date range; self-tested both ways on every run.
  3. Any statement that OmniFit diagnoses, treats, assesses, or manages a
     MEDICAL CONDITION, or that a device is used to do so. "Assesses" is
     new to this tier and is scoped to a medical condition: assessing
     MOVEMENT is what OmniFit does and stays legal. Negations and referral
     language stay legal and are the recommended form.
  4. "Free consultation" framing, under any name for the first session.
     The consultation is paid: 45 minutes, $30 deposit, refunded the same
     day you attend your consultation (the canonical wording, LAUNCH
     DECISIONS item 3; this line said "$30 refundable deposit" until the
     Outcome Claims Amendment run, Oct 17 2026).
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
  2a. ATTRIBUTED INDIVIDUAL OUTCOMES (OUTCOME CLAIMS AMENDMENT, owner-
     approved Oct 1 2026; applied Oct 17 2026; replaces the Sept 2026 item 2
     recorded below it). An individual client's measured result is
     permitted ONLY when ALL FIVE conditions hold:
       (1) written client consent;
       (2) measured by OmniFit, with dates;
       (3) elapsed time stated as fact, never "in just";
       (4) this disclosure VERBATIM on the same surface as the figure:
           "Individual result, measured by OmniFit. How clients typically
           progress: omnifittraining.com/outcomes."
           /OUTCOMES EXEMPTION (owner, Oct 17 2026): on /outcomes ONLY the
           disclosure is the first sentence alone, "Individual result,
           measured by OmniFit." - the full line would point the reader at
           the page they are on. Everywhere else it stays the full verbatim
           line. Page-scoped in certify.py (outcomes.html and its header)
           and exact both ways: the full line on /outcomes, and the short
           line on any other page, are both condition (4) findings.
       (5) third person, past tense; no projection and no "you".
     Surface = the enclosing <section>, falling back to the page (the same
     reading as TIER 2 item 1). Attribution is still required - a named
     individual beside a role noun, or an explicit anonymisation with a
     stated profile - and aggregate or typical-results framing is still
     never this item.
     OWNER-ATTESTED CONSENT LIST (condition 1; owner, Oct 17 2026): Isaac
     M., Egor B., Chad C., Alo S., Mark M., Vincent, Ken, Dave R. certify.py
     cannot verify a consent form, so it reads this list (CONSENT_LIST): a
     figure attributed to anyone else, or to an anonymised profile, is a
     consent finding until the owner adds the name here. Dave R. added by the
     owner Oct 17 2026 (follow-up run): Dave's case study and the 4S Ranch
     transformation card.
     BODY COMPOSITION: Bodystat readings exist only for clients who started
     at Teqneeq; older clients have no comparable readings. A body-fat or
     lean-mass figure for a client who predates Teqneeq cannot be measured
     by OmniFit (condition 2) and comes down under item 2g.
     ENFORCED: conditions (3), (4), (5) and the consent list, on every
     non-frozen page (certify.py attributed_outcome_conditions, self-tested
     both ways on every run). Conditions (1) beyond the list and (2) are
     human warranties. Figures inside tag attributes (alt text, aria-label)
     are outside every rule here, because the flattener drops attributes.
     What the Sept 2026 item 2 RELAXED against the old screen still stands:
     the disclosure does not have to sit in a dedicated block; it has to be
     on the same surface, verbatim.
     FROZEN RECORDS: pages/case-studies.html (and, until the Homepage
     rebuild run of Oct 17 2026, its byte-identical duplicate
     pages/home-3.html) are historical records, exempt from
     re-screening entirely. They record measurements that happened. Do not
     run a case-study figure check.
     SEPT 2026 WORDING, SUPERSEDED (kept so the reasoning survives):
     "Attributed individual outcomes in case studies are permitted with the
     individual-results disclaimer on the same page. Attribution is still
     required - a named individual beside a role noun, or an explicit
     anonymisation with a stated profile - and aggregate framing is still
     never exempt. What is relaxed against the old screen: the disclaimer
     no longer has to sit in a dedicated block opening with the phrase."
  2g. DATA-BACKED FIGURES (OUTCOME CLAIMS AMENDMENT; lettered by the
     owner's amendment, which this brief follows - 2b to 2f are not in it).
     Every client-results number on the site must either appear on
     /outcomes or meet 2a. A figure that can't be recomputed from records
     comes down. No adherence percentage until attendance is logged.
     ENFORCED (certify.py data_backed_figures, self-tested both ways): an
     unattributed figure framed as a recorded OmniFit client result (a
     past-tense result verb or a statistic word beside a client word) must
     appear on pages/outcomes.html; a percentage beside adherence /
     attendance / sessions completed is a finding on sight. Goals ("want to
     lose 20-30 lbs", TIER 2 item 3), published-trial figures (the GLP-1
     page's STEP-1 numbers) and surfaces labelled illustrative (TIER 2 item
     5) are not client results. Third-party statistics ("80% of members
     quit by month 3", the comparison table on how-it-works-pricing) are
     not OmniFit client results and are outside this rule as encoded;
     WRONG IF the owner reads 2g as covering every figure on the site.
     REPORTING: both amendment rules print in full on every run under
     "(a') OUTCOME CLAIMS AMENDMENT" and COUNT toward the result:
     certify.py AMENDMENT_COUNTS = True since the follow-up run, Oct 17
     2026 (owner), which brought the 17 findings to zero. The RESULT line
     always carries their count.
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
  6. A FIT OR SATISFACTION REFUND POLICY - the 30-Day Fit Guarantee,
     DEFERRED-01, CLOSED Aug 2026 with approved wording - is permitted
     PROVIDED IT PROMISES ONLY A REFUND OR AN EXIT, NEVER A RESULT.
     The distinction TIER 1 item 1 now turns on: "we guarantee you will
     lose 20 lbs" promises an outcome and is banned at TIER 1; "if it isn't
     the right fit, stop and I'll refund the unused balance" promises only
     money back and is legal here. The approved wording pairs no outcome
     word with the guarantee, which is what makes it clear the tier.
     WORDING CHANGES REQUIRE OWNER APPROVAL. The text is not a template to
     paraphrase: a rewrite that reintroduces a result promise moves the
     item back to TIER 1 without anyone editing this brief.
     OWNER OVERRIDE, Oct 17 2026: the canonical wording is now the Terms
     text recorded under LAUNCH DECISIONS item 6. It still promises only a
     refund and an exit; the tiering is unchanged.

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
  · guarantee_any (T1-1) - "guarantee" with a RESULT NOUN as its object or
    anywhere in the same sentence. Narrowed Sept 12 2026 by owner decision:
    the first drafting flagged the word, which made a refund policy that
    promises no result read as an outcome guarantee. A guarantee stated as
    ABSENT ("reimbursement is not guaranteed") is exempt on the preceding
    words only. <style> and executable <script> bodies are not copy and are
    excluded; ld+json IS copy. Negative test is the approved 30-Day Fit
    Guarantee wording (TIER 2 item 6), which must pass, against
    "guarantee you'll lose 20 lbs", which must fire.
  · lbs_near_timeframe (T1-2) - pounds, inches or body-fat % within ~15
    words of a quantified timeframe. Inches and body-fat % are new to this
    rule. Exempt: TIER 2 item 2a (attributed individual, page disclaimer),
    TIER 2 item 3 (no timeframe at all never matches), frozen records, and
    (Outcome Claims Amendment, Oct 17 2026) an aggregate figure published on
    /outcomes with a sample size on its surface and a date range on the
    page - the TIER 1 item 2 carve-out, self-tested both ways.
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
  · attributed_outcome_conditions (T2-2a) - OUTCOME CLAIMS AMENDMENT, Oct
    17 2026. For every figure (pounds, inches, body-fat %, a percentage)
    attributed to an individual within 80 words - a consent-list name, or a
    capitalised name beside a role noun, "Name is a <role>", or "Name, <age>"
    - reports: the name not on CONSENT_LIST; "in just" / "in only" / "in as
    little as" beside the figure (condition 3); the verbatim disclosure
    absent from the figure's surface (condition 4); "you", first person, a
    projection word or a present-tense outcome verb in the figure's own
    block sentence (condition 5). The nearest preceding name within 12
    words wins (table rows, "Name: figure" captions), else the nearest
    name (stat cards). Reported with file:line and client.
  · data_backed_figures (T2-2g) - same amendment. An unattributed figure
    framed as a recorded OmniFit client result that does not appear on
    pages/outcomes.html, and any adherence / attendance percentage. Goals,
    trial figures, illustrative surfaces and alt text are outside it.
  BOTH amendment rules print under "(a') OUTCOME CLAIMS AMENDMENT" and
  COUNT toward the result (AMENDMENT_COUNTS = True, Oct 17 2026 follow-up;
  see TIER 2 item 2g). Condition (4) carries the page-scoped /outcomes
  exemption (TIER 2 item 2a). Self-tested both ways on every run
  (_selftest_amendment).
  CHECKER FIX, OWNER DECISION, Homepage rebuild run (Oct 17 2026) - the T1-2
  twin of the fix below: lbs_near_timeframe's named-individual exemption
  (_case_study_exempt) read the verbatim 2a disclosure's "How clients
  typically progress" as aggregate wording, so a card carrying the
  disclosure lost its exemption. ONLY the exact sentence "How clients
  typically progress: omnifittraining.com/outcomes." (link-wrapped or not)
  is blanked, on the whole text before the 45-word window is cut so a window
  edge cannot split it; any other "typically" / "most clients" / "on
  average" near a figure still fails. Self-tests (_selftest_case_study_exempt):
  a named card with the verbatim disclosure passes, at every window offset;
  a named card beside "clients typically lose 10 lbs in 3 months" fails on
  the named figure; the disclosure with one word changed is not exempt.
  CHECKER FIX, Oct 17 2026 follow-up: aggregate_metric_conditions (T2-1)
  read the disclosure's own "How clients typically progress" as aggregate
  framing and struck Vincent's "-8% body fat" card on the over-50 page the
  moment the disclosure went on. The verbatim pointer (link-wrapped or not)
  is blanked for the framing test only; any other "typically" beside a
  figure still fires. Self-tested both ways.

  WITHDRAWN WITH THE OLD SCREEN
  · The DEDICATED-BLOCK disclaimer test for case studies. It required the
    disclaimer to open its own p/div/aside/section/blockquote. TIER 2 item
    2a asks only that the disclosure be on the same surface (the Sept 2026
    item 2 said page), so the test is withdrawn for that item. It is NOT
    withdrawn from TIER 2 item 1, which states its own three conditions.
    Consequence recorded so it is not rediscovered as a surprise:
    how-we-measure-your-progress and desk-worker-posture-pain both failed
    the dedicated-block test and now pass the same-page test. Neither gains
    an exemption from it on its own, because TIER 2 item 2a also requires
    ATTRIBUTION, and both fail that independently.
  · clinical_stat as a blanket ban on quantified figures near a clinical
    word. Split: the population-scope clinical case is T1-6 and is
    unchanged in force; everything else is T2-1 and is conditional.
  · result_near_timeframe as an unconditional rule. It now exempts a
    surface carrying the full TIER 2 item 1 conditions, because a measured
    aggregate reported with its period IS a measurement with its method,
    which is the thing this screen stopped treating as a claim.

  EXCEPTION - ATTRIBUTED INDIVIDUAL OUTCOMES (TIER 2 item 2a)
  Individual client results carrying a timeframe are exempt from
  lbs_near_timeframe and result_near_timeframe when (the T1-2 exemption;
  the five 2a conditions are checked separately by
  attributed_outcome_conditions, above):
    1. the result is attributed to a specific individual (named beside a
       role noun, or explicitly anonymised WITH a stated profile), AND
    2. the page carries the individual-results disclaimer ANYWHERE on the
       page. Relaxed Sept 2026 from a dedicated block, per TIER 2 item 2a.
    3. substantiation exists on file. Not machine-checkable; a human
       warranty, unchanged.
  Page-scoped, not site-wide. Aggregate or typical-results framing is NEVER
  exempt, on any page. Fails CLOSED: anything the attribution test cannot
  confirm stays a strike.
  CHECKER FIXES, Oct 17 2026 (item 20 surfaced both): the page disclaimer may
  carry its condition word in the sentence AFTER "individual results"
  ("Individual results. Outcomes ... vary between clients."), and
  "everyone else" / "anyone else" no longer read as aggregate framing
  ("putting everyone else first" in a neighbouring card). Both self-tested
  both ways on every run (certify.py _selftest_case_study_exempt).
  FROZEN: case-studies.html is exempt from re-screening (home-3.html left
  the list in the Homepage rebuild run, Oct 17 2026: it is no longer a copy).

  Reasoning, recorded so it survives: an individual, attributed, documented
  client outcome is a fact about a named person; a claim about what a
  prospective client can expect is a projection. Only the projection is
  what these rules exist to prevent. The same distinction is what moved
  aggregate measured metrics from banned to conditional - a median with its
  sample size and period is a record of what happened, and the conditions
  are there to keep it readable as one.

(b) STALE CANON
  RETIRED LAUNCH COPY (LAUNCH DECISIONS, Oct 17 2026): the twenty literal
  phrases listed there, swept case-insensitively on the flattened copy of
  every file in the glob, footer.html included, frozen records exempt
  (certify.py RETIRED_LAUNCH_COPY, self-tested both ways on every run).
  CONSULTATION CTA TO /contactform (LAUNCH DECISIONS item 15): a link
  labelled as a consultation that points at the contact form (certify.py
  consultation_cta_to_contactform, self-tested both ways on every run).
  BOOKING CTA OR RESERVEACTION TO /contactform (LAUNCH DECISIONS item 18):
  a link labelled "Start ...", "Get Started", "Book ..." or "Stay ..."
  that points at the contact form, or a schema ReserveAction whose target
  names it (certify.py booking_cta_to_contactform and
  reserve_action_to_contactform, self-tested both ways on every run).
  KEN'S RETIRED MUSCLE FIGURE (LAUNCH DECISIONS item 20): "+6 lb(s)", "6
  pounds of muscle", "6 lbs of muscle", in EVERY file, frozen records
  included (certify.py ken_muscle_claim, self-tested both ways).
  POSITIONING LINE NOT VERBATIM, OR IN A TITLE / META / H1 (ENTITY BLOCK,
  Oct 17 2026): certify.py positioning_line_verbatim, every file in the
  glob, frozen records exempt, self-tested both ways on every run.
  TEQNEEQ ON-SITE PT CLINIC CLAIMED (ENTITY BLOCK, Oct 17 2026, Homepage
  rebuild run): a sentence naming Teqneeq, or the sentence after it, that
  places a PT / physical therapy / rehab clinic on site or in-house
  (certify.py teqneeq_onsite_pt, every file in the glob, frozen records
  INCLUDED, negations pass, self-tested both ways on every run).
  THE TRAVEL PROTOCOL MISCASED OR PRICED (THE OMNIFIT METHOD, Oct 17 2026):
  "travel protocol" in any casing but "Travel Protocol", or a dollar figure
  in the same sentence as the name (certify.py travel_protocol_usage,
  self-tested both ways on every run).
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
  LocalBusiness redefined in a page header instead of referenced by @id ·
  a page declared as having no FAQ that carries FAQ markup.

PAGE HEADER SHAPE (Oct 16, 2026)
  Every page header is ONE @graph document with a page node (WebPage, or the
  subtype AboutPage / ContactPage) whose "about" references
  #localbusiness-of, plus BreadcrumbList and any Service / FAQPage nodes.
  contactform and desk-worker-posture-pain were converted from bare nodes on
  Oct 16, 2026; their Service and FAQPage content is unchanged, and their
  WebPage name/description are the SEO title and meta (build.py reads them).

PAGES WITH NO FAQ (Oct 16, 2026)
  about · contactform · fit-check · personal-training-services ·
  privacy-policy · terms-and-conditions. These have no FAQ by design.
  (fit-check was rebuilt Oct 17 2026 around two gates, READY and ABLE, plus
  an Accountability Dial question; its "Not a fit right now" result and
  its intro are page copy, not FAQ markup, and the page stays on this list.)
  certify.py (NO_FAQ) verifies it: the page body must carry no FAQ-shaped
  markup and the header no FAQPage, or it is a structure finding. A new page
  without an FAQ must be added here AND to NO_FAQ, or certification reports
  it under CHECKS THAT COULD NOT RUN.

KEYWORD OWNERSHIP (Keyword Ownership run, Oct 2026)
Source: the Keyword Ownership Map, Semrush Position Tracking, Oct 5-11 2026.
Google kept swapping the in-home page in for keywords other pages own, and the
ranking dropped every time it won the swap. The proven fix: once Del Mar was
stripped from the in-home page, the Del Mar query moved to the Del Mar page and
went 26 -> 16. So every tracked keyword has ONE owner page.

"Owns" means the phrase or a close variant appears in the owner's title, H1,
H2s and meta description, and in NO other page's title, H1, H2s or meta. Other
pages may cover the topic in body copy and should link to the owner with the
phrase as anchor text.

Enforced by tools/ownership.py, run from `python3 build.py --check` (and
`python3 tools/ownership.py`). It reads the RENDERED page in public/ - title
and meta are only resolved at build time - and fails when an owned phrase sits
on a title/H1/H2/meta of any page other than its owner or an "also" page.
It is deliberately NOT in certify.py: certification reports exactly three
categories and keyword ownership is none of them. Fixtures that must fail and
must pass live in tools/fixtures/ownership/; build.py --check runs them first,
so a green ownership result always comes from a check seen failing.

Matching rules (encoded in tools/ownership.py; change both together):
  - Case-insensitive regex on tag-stripped text. HTML comments, <style> and
    <script> are not copy. Headings are read from <main> only.
  - LONGEST MATCH WINS. A match lying wholly inside another keyword's match
    belongs to that keyword: "In-Home Personal Trainer in San Diego" counts
    for K06 only, never for K01. This is what "keeps the in-home qualifier"
    means mechanically.
  - K01 matches the noun "personal trainer(s)", not "personal training".
    JUDGMENT CALL: "personal training in San Diego" is the site-wide service
    description (homepage H2, FAQs and HIIT titles, comparison page title) and
    is not a tracked keyword. WRONG IF Semrush shows "personal training san
    diego" being cannibalized; then K01 widens and those surfaces move.
    K05 (private) and K06 (in-home) DO match "training": their qualifier is
    the distinctive token, and the only non-owner hit (the FAQs meta,
    "private personal training programs") was cheap to fix.
  - Owner COVERAGE is reported as a note, not a failure. Since the Homepage
    rebuild run (Oct 17 2026) the homepage carries K02, K03 and K04 on H2s
    ("Is a Personal Trainer in North County San Diego Right for You?",
    "Your Personal Trainer in 4S Ranch, at Home, or Online", "How Our
    Executive Fitness Coaching Works"), and the three coverage notes are gone.
  - An owner of "-" is UNASSIGNED: its phrase still claims its span (so a
    cost question is not read as K01) but exclusivity is not enforced, and
    the check prints that it is not enforced rather than passing silently.

Page-specific rules that are NOT ownership but are locked in the same table:
  - In-home (X01): no "private", North County, cost/pricing/"how much",
    age group, or town name in its title, meta, any heading, FAQ question or
    its own JSON-LD. In body copy towns appear ONLY as links to their own
    territory page, in the one service-area list; Poway stays as text (no
    page exists and ChatGPT cites this page for it). Del Mar, 4S Ranch and
    North County do not appear in the body at all.
  - Homepage (X02): "private" stays out of the title, H1 and H2s.
  - /personal-trainer-4s-ranch and /personal-trainer-rancho-bernardo stay
    exactly as they are (ChatGPT cites both). 4S Ranch is listed as an "also"
    page on K03 for that reason: the homepage owns the keyword for Google.

  OWNERSHIP TABLE - read by tools/ownership.py. Entry lines start "  K" or
  "  X"; field lines are indented six spaces. owner/page = URL path. match =
  regex, "|" between close variants. also = extra permitted pages, or "-".

  K01 personal trainer san diego / personal trainer in san diego
      owner  /
      match  personal trainers? (?:in )?san diego|san diego personal trainers?
  K02 personal trainer north county san diego
      owner  /
      match  personal trainers? (?:in )?north county(?: san diego)?|north county(?: san diego)? personal trainers?
  K03 personal trainer 4s ranch
      owner  /
      also   /personal-trainer-4s-ranch
      match  personal trainers? (?:in )?4s ranch|4s ranch personal trainers?
  K04 executive fitness coach san diego
      owner  /
      match  executive fitness coach(?:es|ing)?
  K05 private personal trainer san diego
      owner  /private-personal-trainer-san-diego
      match  private (?:1:1 |one-on-one )?personal train(?:er|ers|ing)(?: (?:in )?san diego)?
  K06 in home personal trainer san diego
      owner  /in-home-personal-trainer-san-diego
      match  in[- ]home (?:personal )?train(?:er|ers|ing) (?:in )?san diego|san diego in[- ]home (?:personal )?train(?:er|ers|ing)
  K07 personal trainer for older adults san diego / strength training over 50
      owner  /personal-trainer-over-50-san-diego
      match  personal trainers? for (?:older adults|(?:\w+ ){0,3}over 50)|older adults?|strength training (?:for (?:\w+ ){0,3})?(?:over|after) 50|\b(?:over|after)[- ]50\b
  K08 corrective exercise specialist (near me / san diego)
      owner  /corrective-exercise-post-rehab
      match  corrective exercise specialists?
  K09 personal trainer for back pain san diego
      owner  /corrective-exercise-post-rehab
      match  back[- ]pain
  K10 personal trainer san diego cost (dedicated cost page: a later run)
      owner  -
      match  personal trainers? (?:in )?san diego cost|cost of (?:a |an )?(?:in[- ]home )?personal trainer(?: in san diego)?|how much (?:does|is|do) (?:a |an )?(?:in[- ]home )?personal trainers?(?: cost)?(?: in san diego)?
  K20 personal trainer carlsbad / in home personal trainer carlsbad
      owner  /personal-trainer-carlsbad
      match  (?:in[- ]home )?personal trainers? (?:in )?carlsbad|carlsbad (?:in[- ]home )?personal trainers?
  K21 personal trainer carmel valley / in home personal trainer carmel valley
      owner  /personal-trainer-carmel-valley
      match  (?:in[- ]home )?personal trainers? (?:in )?carmel valley|carmel valley (?:in[- ]home )?personal trainers?
  K22 personal trainer del mar / in home personal trainer del mar
      owner  /personal-trainer-del-mar
      match  (?:in[- ]home )?personal trainers? (?:in )?del mar|del mar (?:in[- ]home )?personal trainers?
  K23 personal trainer encinitas / in home personal trainer encinitas
      owner  /personal-trainer-encinitas
      match  (?:in[- ]home )?personal trainers? (?:in )?encinitas|encinitas (?:in[- ]home )?personal trainers?
  K24 personal trainer fairbanks ranch / in home personal trainer fairbanks ranch
      owner  /personal-trainer-fairbanks-ranch
      match  (?:in[- ]home )?personal trainers? (?:in )?fairbanks ranch|fairbanks ranch (?:in[- ]home )?personal trainers?
  K25 personal trainer la jolla / in home personal trainer la jolla
      owner  /personal-trainer-la-jolla
      match  (?:in[- ]home )?personal trainers? (?:in )?la jolla|la jolla (?:in[- ]home )?personal trainers?
  K26 personal trainer rancho bernardo / in home personal trainer rancho bernardo
      owner  /personal-trainer-rancho-bernardo
      match  (?:in[- ]home )?personal trainers? (?:in )?rancho bernardo|rancho bernardo (?:in[- ]home )?personal trainers?
  K27 personal trainer rancho santa fe / in home personal trainer rancho santa fe
      owner  /personal-trainer-rancho-santa-fe
      match  (?:in[- ]home )?personal trainers? (?:in )?rancho santa fe|rancho santa fe (?:in[- ]home )?personal trainers?
  K28 personal trainer santaluz / in home personal trainer santaluz
      owner  /personal-trainer-santaluz
      match  (?:in[- ]home )?personal trainers? (?:in )?santaluz|santaluz (?:in[- ]home )?personal trainers?
  K29 personal trainer solana beach / in home personal trainer solana beach
      owner  /personal-trainer-solana-beach
      match  (?:in[- ]home )?personal trainers? (?:in )?solana beach|solana beach (?:in[- ]home )?personal trainers?
  X01 in-home page carries no other keyword's qualifier
      page   /in-home-personal-trainer-san-diego
      in     title meta h1 h2 h3 h4 h5 h6 faq jsonld
      match  \bprivate\b|north county|older adults?|\b(?:over|after)[- ]50\b|\bseniors?\b|\bcost\b|how much|\bpric(?:e|es|ing)\b|4s ranch|carlsbad|carmel valley|del mar|encinitas|fairbanks ranch|la jolla|rancho bernardo|rancho santa fe|santaluz|solana beach|poway|del sur|olivenhain|la costa
  X02 homepage keeps "private" out of its title, H1 and H2s
      page   /
      in     title h1 h2
      match  \bprivate\b
  END OWNERSHIP TABLE

  K10 is the cost keyword: no new cost-anchor links anywhere until its page
  exists, and /training-rates-san-diego stays transactional.

INVARIANTS (hash-verify every run; update hashes here when a run
legitimately changes an invariant, and say so in REPORT.md)
- Canonical pricing FAQ answer: byte-identical on every page carrying it
  (page hash a6c7e65dddff4795, header hash 7af0d0049b0b7aba). Currently 13
  pages and 13 headers - the-30-minute-executive-reset joined in the Reset
  Refresh run, byte-identical to the other twelve, so neither hash moved. BOTH HASHES CHANGED in the October Card run: the
  block states the rates, so repricing rewrote the same bytes on all 24
  files. Previous values ae388d31c0b6149e / 7e5de5984b133663. The
  the-30-minute-executive-reset pair also carries this block and was NOT
  rewritten - it is out of certification scope and on the do-not-paste list,
  so it still carries the August wording and does not enter either hash.
- Credentials block body: byte-identical on 11 pages (02bd9cb90a71ce69,
  663 bytes)
  — the 10 territory pages plus corrective-exercise-post-rehab. 4S Ranch keeps
  its own Meet Nemezio section instead. Hash changed legitimately in the
  Thirteen Certifications run (Oct 2026): the block now reads thirteen
  certifications and four Precision Nutrition certifications (Level 2
  Certified Master Coach added), rewriting the same bytes on all eleven
  pages. Previous value 6492e3ca1545dc26 (630 bytes).
- Archetype card bodies (Section A): byte-identical × 11 pages
  (hash 6b1b0f4efbd4a72c; concatenation of the three card <p> bodies in
  page order, set by the Section A/B run).
- 9-point screen section body (Section B): byte-identical × 11 pages
  (hash 4c720960dec5a809; intro + nine <li> items + closing line, set by
  the Section A/B run). Hash changed legitimately in the Device Swap run
  (Sept 2026): the Body Composition <li> names the device, so retiring the
  1500 MDD rewrote the same bytes on all eleven pages. Previous value
  bd73ea51bc9ec5eb. All eleven pages still agree; certify.py reported no
  invariant mismatch. (That run recorded "ten"; rancho-bernardo was already
  on main and carrying the invariant, so the count was one low even then.)
  CHANGED AGAIN in the October Card run: ba590a09107ffda0 -> 4c720960dec5a809.
  The invariant spans intro + nine <li> items + closing line, and the INTRO
  carried the retired "$110 Performance Diagnostic, credited in full toward a
  3-month package". All NINE <li> ITEMS AND THE CLOSING LINE ARE BYTE-IDENTICAL
  across the change, verified item by item; only the intro sentence moved, and
  identically on all eleven pages. The alternative was leaving a retired price
  live on eleven territory pages to protect a hash, which is the wrong way
  round: the hash records the block, it does not license its contents.
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
- STATUS: CLOSED, Aug 2026, with the approved wording above. It was briefly
  re-opened by the first drafting of TIER 1 item 1, which banned the word
  "guarantee" rather than the promise of a result; that drafting was
  narrowed by owner decision on Sept 12 2026 and the item is CLOSED again.
  The approved wording is now covered by TIER 2 item 6: it promises a
  refund and an exit, never a result. Wording changes require owner
  approval.
- SUPERSEDED Oct 17 2026 by owner override (LAUNCH DECISIONS item 6): the
  canonical wording is now the Terms sentence, applied byte-identically on
  Rates (both callouts), How It Works (body and FAQ answer) and the How It
  Works header mirror. The Aug 2026 text above is the historical record.

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
- Every published figure comes from the OCTOBER 2026 CARD. Anything from the
  LEGACY block in published copy is a stale-canon violation, not a variant.
- Round numbers only. No contract exceeds $4,400.
- Committed totals on the card, highest first - the only figures the CONTRACT
  VALUE CHECK can reach, because The Program commits no total:
    In-home couples Momentum Foundation   1,250 x 3 = 3,750   clear by 650
    Studio Performance Foundation         1,100 x 3 = 3,300   clear by 1,100
    Studio couples Momentum Foundation      850 x 3 = 2,550   clear by 1,850
    In-home Momentum Foundation             800 x 3 = 2,400   clear by 2,000
    Studio Momentum Foundation              560 x 3 = 1,680   clear by 2,720
  Those five are the whole list: the Foundation is the only committed total
  on the card. The Program, the Reset and the Tune-Up all bill per cycle or
  per month with notice, so none of them commits a total to check.
- Break point for a THREE-CYCLE Foundation: any per-cycle rate above $1,466
  produces a total over $4,400 (4,400 / 3 = 1,466.67). In-home couples
  Momentum at 1,250 is the closest under it. No Foundation tier may be
  introduced above that rate without the CONTRACT VALUE CHECK.
- Off-card arrangements (in-home Peak "from $2,600", Couples Peak "by
  arrangement") are the only route to a contract that can exceed $4,400, and
  they take owner approval before a client is filed.

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
  omnifit-vs-competitors · weight-loss · strength-training-1 (archived Oct 2026, restored Oct 17 2026) ·
  hiit-personal-trainer-san-diego · personal-training-services ·
  body-composition-testing · partners.
- BATCH 4: terms-and-conditions DONE (Sept 20, 2026 — pages/terms-and-conditions.html
  + header, rewritten to the October card and OmniFit Performance LLC, live;
  the live page is a Squarespace text page, the repo file records its content)
  · contactform (brand sweep only — header still carries "Executive
  Transformation Program" and 7-metric wording; only its provider @id was
  re-pointed on Sept 20, 2026).
- Human-side, done Sept 20, 2026: /hsa-fsa-personal-training Squarespace SEO
  Description set ("Personal training is HSA and FSA eligible with a letter of
  medical necessity. OmniFit Performance partners with Truemed so eligible San
  Diego clients can pay for training with pre-tax funds."). Terms page SEO
  Title "Terms of Service", SEO Description per its header comment.
- NOTE on aggregateRating (Sept 20, 2026): the 190 rating lives on
  #localbusiness-of site-wide and therefore on every page. Google does not
  show star snippets for a business rating its own site (self-serving
  LocalBusiness/Organization reviews, since 2019); Semrush's "add aggregate
  rating via Product/ItemList markup" ideas are a policy violation and are
  to be ignored. The rating is for entity understanding and AI readers only.
- Human-side, not repo: per-page SEO meta descriptions (190+), 301
  /executive-hybrid-coaching → /the-30-minute-executive-reset then
  delete page, Search Console recrawl of ALL changed URLs as one batch
  at the very end, fitnesstrainer.com URL into homepage sameAs when
  retrievable, homepage Over-50 / Partner & Duo / female-clients FAQ
  sections (Claude drafts, human pastes), post-recrawl third-party
  signal work (review-prompt kit, directories, thought leadership).
- OUTCOME CLAIMS AMENDMENT FOLLOW-UP - DONE Oct 17 2026 (follow-up run,
  owner decisions: Dave R. on the consent list, the /outcomes short
  disclosure, the Travel Protocol live-video sentence, AMENDMENT_COUNTS =
  True; see REPORT.md "Canon Oct 17 follow-up run"), except the POSITIONING
  LINE item, which stays open. Kept as recorded:
  · Bring the attributed individual outcomes to TIER 2 item 2a. The 17
    instances certify.py reports under "(a') OUTCOME CLAIMS AMENDMENT" are
    listed file:line in REPORT.md: the verbatim disclosure on the surface
    of every figure (desk-worker-posture-pain, personal-trainer-4s-ranch,
    personal-trainer-over-50-san-diego, outcomes), and Dave's 27 lb figure
    on the 4S Ranch gallery, which needs the owner to add Dave to the
    CONSENT LIST or the figure comes down (item 2g). OWNER DECISION NEEDED:
    on /outcomes itself the disclosure points the reader at /outcomes; the
    rule is encoded as written and reports the page, and the owner may
    exempt /outcomes from condition (4) or accept the self-reference.
  · Then flip certify.py AMENDMENT_COUNTS to True so the two rules count.
  · Use "the Travel Protocol" on the pages that describe travel support
    (the file:line list in REPORT.md), reconciling "switch to virtual" /
    "virtual sessions during travel weeks" wording with the definition.
  · Lead every summary / TL;DR block with the POSITIONING LINE, verbatim
    (homepage: carried by the hero subhead, which sits directly above In
    Short, so In Short no longer repeats it - owner, Oct 17 2026; other
    pages open);
    human-side, paste it to Google Business Profile, Thumbtack, Yelp and
    Bark.
