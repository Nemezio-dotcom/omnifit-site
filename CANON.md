═══ OMNIFIT SITE — CANON (owner decisions; slimmed Nov 27 2026) ═══

This file holds three things: FACTS a published page must agree with, RULES THE OWNER SET about what may be published, and the few WORKFLOW lines a run needs. Run history, changelogs, judgment-call notes and descriptions of how the checkers work are not here: they are in archive/CANON-full-2026-11-27.md, the full brief as it stood before the slim-down (never certified, never corrected, not read on a run). Blocks marked VERBATIM are byte-for-byte from that file; where one cites LAUNCH DECISIONS, ENTITY BLOCK, INVARIANTS, NEXT RUNS, DEFERRED-01, REPORT.md or a named run, the citation points into the archive, and the fact it cites is carried here.

BUSINESS AND ENTITY (every page and every schema node agrees with these)
  Brand: "OmniFit Performance" everywhere; legal name OmniFit Performance LLC. Never "OmniFit Personal Fitness Training". Accepted alternate name: OmniFit Training (schema alternateName only, never a page heading). ONE domain: omnifittraining.com (https://www.omnifittraining.com). Not affiliated with OMNIFIT Athletics (schema disambiguatingDescription says so; running copy never mentions them).
  Founder: Nemezio LopezPerez (one-word surname, never "Lopez Perez"), NASM Elite Trainer. "Coach Nemezio" is the Person's alternateName in schema and may be used in running copy AFTER the full name has appeared on the page.
  Coaching tenure: "Coaching since 2016". Never a number of professional years ("10+ years", "over a decade"). Stat badges read "2016 / Started Coaching" or "Coaching Since 2016".
  Address: Teqneeq Functional Health Center, 10772 Thornmint Rd, 4S Ranch, San Diego, CA 92127 ("Teqneeq" and "Teqneeq FHC" are accepted short forms; schema carries the street address). Phone (619) 259-0630. Email nemezio@omnifittraining.com. A trainer operating AT Teqneeq, never a studio within a studio.
  Teqneeq is a members-only functional health facility with NO on-site physical therapy clinic; OmniFit's physical therapy relationships are EXTERNAL partners, such as Stoke Physical Therapy.
  FACILITY, canonical: "private 1:1 coaching inside Teqneeq FHC, a members-only facility in 4S Ranch". Never "fully private", "zero crowds", "full privacy" or exclusive use of the room. Studio access reads "Private, by appointment: no walk-ins, no crowds". A client's own home is private; in-home copy may say so.
  Service area: in studio at Teqneeq in 4S Ranch; in-home across North County San Diego (never "throughout San Diego County"); live virtual coaching nationwide. Schema areaServed: San Diego; 4S Ranch; Rancho Bernardo; Del Sur; Santaluz; Santa Fe Valley; Poway; Rancho Santa Fe; Fairbanks Ranch; Carmel Valley; Del Mar; La Jolla; Solana Beach; Encinitas; Carlsbad; live virtual coaching nationwide (US).
  RETIRED SERVICE AREAS, never mentioned in published copy: Pacific Beach, Mission Bay, Ocean Beach, and "PB" / "OB" as area names. ONE EXCEPTION: the Pacific Beach not-served line in the assistant's knowledge file (ASK OMNIFIT).
  Schema: the business is defined ONCE, in pages/headers/site-header.html (Organization #organization, Person #founder, LocalBusiness #localbusiness-of, WebSite #website); page headers reference it by @id. sameAs: Instagram, Yelp, Google Business Profile, Thumbtack, Bark, BBB. The rating sits on #localbusiness-of only; never add ratings through Product or ItemList markup.
  Footer: nemezio@omnifittraining.com; reviews link https://g.page/r/CcePeMjnbDe9EBM (no /review suffix).
  DESCRIPTION (two sentences, verbatim; the Organization and LocalBusiness nodes): "OmniFit Performance is the diagnostic-led personal training practice of Nemezio LopezPerez (Coach Nemezio), based at Teqneeq Functional Health Center in 4S Ranch, San Diego, with in-home training across North County San Diego and live virtual coaching nationwide. The OmniFit Method measures first, builds joint-first strength, and carries accountability across studio, in-home and virtual on one app for professional adults 30+."
  FOUNDER BIO (verbatim; owner, Oct 25 2026; the description of Person #founder): "Nemezio LopezPerez founded OmniFit Performance to coach busy professionals over 30 who keep losing progress to pain, plateaus and packed calendars. An NASM Elite Trainer with NASM certifications in corrective exercise, performance enhancement and nutrition, and a Precision Nutrition Level 2 Certified Master Coach, he trains clients at Teqneeq in 4S Ranch, in their homes, and virtually."
  ENTITY LINE (verbatim, the short form under page blocks): "OmniFit Performance · Nemezio LopezPerez (Coach Nemezio) · Teqneeq Functional Health Center, 10772 Thornmint Rd, 4S Ranch, San Diego, CA 92127 · omnifittraining.com"
  POSITIONING LINE (verbatim; owner, Oct 17 2026): "OmniFit Performance is a diagnostic-led coaching system that takes busy professionals over 30 from pain or plateau to lasting, independent strength." USAGE: the lead sentence of summary / In Short blocks (the homepage carries it as the hero subhead instead), external profiles, and the Organization slogan. NEVER in a title, a meta description or an H1, and never paraphrased.
  CREDENTIALS (14): NASM CPT, CES, PES, BCS, CNC; ACE Corrective Exercise Specialist (NOT OES, NOT Orthopedic); Precision Nutrition L1, Level 2 Certified Master Coach, Sleep Stress & Recovery, Nutrition for Metabolic Health; Eden GLP-1 Fitness, Peptide Fundamentals, GLP-1 Nutrition (clinical collaboration framing); Fascia Stretch Practitioner – Level 1 (Stretch to Win Institute; never "therapist").
  CREDENTIALS SENTENCE (verbatim in the Meet Nemezio block of the ten territory pages that carry it and of corrective-exercise-post-rehab; certify.py compares the text): "He holds fourteen certifications across movement, nutrition, and metabolic health: NASM CPT, CES, PES, BCS, and CNC, an ACE Corrective Exercise Specialist credential, four Precision Nutrition certifications (Level 1, Level 2 Certified Master Coach, Sleep Stress and Recovery, and Nutrition for Metabolic Health), three Eden clinical-collaboration certifications supporting clients on GLP-1 and peptide protocols, and Fascia Stretch Practitioner – Level 1 (Stretch to Win Institute)."
  DEVICE: the "Bodystat QuadScan 4000" ("Bodystat", never "BodyStat"). VERIFIED: it holds CE certification as a Class IIa medical device under MDD 93/42/EEC and has FDA clearance. The 1500 MDD references in pages/case-studies.html and in the Mariano G. report record past scans and are never changed.
  CASE-STUDY FIGURES (captions and alt text; verbatim client quotes are untouchable): Vincent "8 percentage points of body fat", no age in his label. Alo +18 lbs. Mark −17 lbs (248→231, 4mo). Dave −27 (225→198, 6mo). Isaac −21 (181→160, 8→20 pull-ups, 6mo). Annie −14 (162→148, 3mo). Ken −11 lbs bodyweight (175→164, 6mo), heading "How a 50+ CTO Lost 11 lbs and Rebuilt Posture After Decades at a Desk"; never "+6 lb" or any muscle-gain figure for Ken. No measurement method is stated for Alo's or Vincent's figures.

CANONICAL FACTS (owner decisions, Oct 17 2026 and later, as dated). EVERY PAGE MUST AGREE WITH THIS
BLOCK. From here to the end of STRETCH TO WIN MARKETING RULES the text is VERBATIM from the full
brief, except the founders landing page's layout notes, which are cut to the rules for its copy.
  CONSULTATION: 45 minutes by video or phone; $30 deposit, refunded the same
    day you attend. It is a CONVERSATION, NOT AN ASSESSMENT: no movement
    testing, no measurements. Published sequence everywhere a page describes
    how a client starts: consultation (conversation) -> if a fit, the
    Performance Assessment (measurements) -> programming. Never "we'll assess
    your movement / body composition" or "build your program" on the
    consultation.
  PERFORMANCE ASSESSMENT (in person, studio or home): $150, credited toward
    your first purchase (a Foundation or Program cycle, an Executive Reset
    cycle, or a 5-session pack). Contents: the 9-point movement screen,
    Bodystat QuadScan 4000 body composition, blood pressure, SpO2, grip
    strength, posture photos, circumference measurements. It sets the
    baselines for the 12-METRIC PROGRESS FRAMEWORK (12 metrics, measured and
    self-reported, in 7 categories). Never "seven tracked benchmarks" or any
    other count.
  VIRTUAL PERFORMANCE ASSESSMENT (Executive Reset / remote clients):
    self-measured with live video guidance; posture photos in the app; NO
    Bodystat scan; $75, credited toward the first purchase the same way.
    Booked after the consultation. Bodystat reassessment is an IN-PERSON
    inclusion only.
  SINGLE SESSIONS: the assessment is recommended, not required. Packs and
    programs require it.
  SESSION LENGTH: 60 minutes in studio and in-home; 30 minutes on the
    Executive Reset. Never "45-60 minutes", "30-45 minute" or "30 or
    45-minute".
    CARVE-OUT (owner, Nov 20 2026): Fascia Stretch Therapy. The FST First
    Visit is 90 minutes; FST sessions are 60 minutes. 90 minutes is legal
    only for the FST First Visit.
  IN-HOME NO-FEE AREA: Carmel Valley, Santaluz, Fairbanks Ranch, Rancho
    Bernardo, 4S Ranch, Poway and Harmony Grove (Harmony Grove added by the
    owner, Nov 22 2026, Founders run). WHERE HARMONY GROVE IS CARRIED SO FAR:
    the FST surfaces only, by the owner's scope for that run (the FST page and
    its header, the Rates FST section, the knowledge file's FST section, the
    founders landing page; site/llms.txt names no towns in its FST line). The
    TRAINING surfaces still read the six-town list (home-4, FAQs, private,
    couples, fit-check, the 4S Ranch territory FAQ, knowledge.md's in-home
    section, certify.py ASSISTANT_REQUIRED): a follow-up pass once the owner
    confirms Harmony Grove for in-home training, not a stale-canon finding
    until then. Elsewhere in the in-home service area
    (including La Jolla, Del Mar, Rancho Santa Fe, Solana Beach, Encinitas,
    Carlsbad) a travel fee applies, confirmed before you book. Never a dollar
    figure. Territory pages in the no-fee area: "No travel fee in [Town];
    it's inside our in-home service area." Territory pages outside it: "A
    travel fee applies in [Town], confirmed before you book." The service
    area is described as North County San Diego, never "throughout San Diego
    County".
  REVIEWS: "4.98 average across 190+ reviews (Google, Yelp, Thumbtack and
    Bark)". Never "5.0", "five-star reviews" for the total, or "verified".
    Schema aggregateRating: ratingValue 4.98, reviewCount 190.
  AUDIENCE: "built for professionals 30+". Never "exclusively".
  RETENTION: "About half of clients train with OmniFit for 6 months or
    longer (see Outcomes)." No other tenure or commitment figure.
  ACCOUNTABILITY: between-session communication and check-ins are "matched
    to your Accountability Dial setting"; no page promises unlimited
    communication or required weekly check-ins to every client.
  EARLY EXIT: "Apart from your statutory cancellation rights, the 30-Day Fit
    Guarantee is the only early exit."
  HSA / FSA: OmniFit doesn't bill insurance. HSA or FSA funds can be used
    only with a Letter of Medical Necessity from a licensed provider,
    available through Truemed. OmniFit provides itemized receipts.
  FASCIA STRETCH THERAPY (FST) (owner decisions, Nov 20 2026; FST Launch
    run. Where an older line in this brief disagrees, these lines win.)
    CREDENTIAL: Nemezio LopezPerez completed Stretch to Win Institute Fascia
      Stretch Therapy Level 1: 38 hours, certificate issued November 20,
      2026. His title, exactly as on the certificate: "Fascia Stretch
      Practitioner – Level 1" (en dash). NEVER "Fascial Stretch Therapist",
      "FST therapist" or "stretch therapist". In credential lists it is
      written "Fascia Stretch Practitioner – Level 1 (Stretch to Win
      Institute)". It is the FOURTEENTH certification (see Credentials).
    SPELLING: "Fascia Stretch Therapy" (as on the certificate and the Google
      Business Profile). "Fascial" may appear EXACTLY ONCE on the whole
      site: one sentence in the FST page's first FAQ answer (also written
      "fascial stretch therapy"), mirrored in that FAQ's schema.
    DEFINITION (owner, Nov 21 2026, FST Reach run; VERBATIM):
      "Fascia Stretch Therapy™ (FST™) is a modality of table-based assisted
      stretching that is pain-free, fully customizable and improves
      functionality." (The owner's sentence of the morning brief, with the
      mark on both names since the same day's every-mention decision.)
      It is OmniFit's own wording. It is NEVER attributed to any person or
      to the Stretch to Win Institute, on the site or in this brief.
      It is the LEAD SENTENCE in exactly five places, replacing "Fascia
      Stretch Therapy (FST) is assisted stretching for mobility and
      recovery" there: the bold sentence of the FST page's definition block;
      the Service node description in the FST header; the first bullet of
      the FST section in assistant/knowledge.md; the FST line in
      site/llms.txt; the homepage FST block. The older sentence STAYS where
      the owner left it: the DISCLAIMER block, the FAQ and its schema,
      Terms, the Services card, the page meta description.
      "PAIN-FREE" describes how the stretching FEELS. It is never an outcome
      and is never reworded as pain relief. It is legal ONLY inside this
      verbatim sentence: certify.py blanks the exact sentence before the
      FST word scan, so "pain-free" anywhere else on an FST surface still
      fails twice (pain, free), as do "pain relief" and "free".
      "IMPROVES FUNCTIONALITY" stays inside the definition. It is a
      statement about the modality, never "you will" framing and never a
      promised result for a client.
    TOP NAV (owner, Nov 21 2026; REVERSES "not in the top nav", owner, Nov
      20 2026): site/nav.html carries ONE item for the service, in the
      first row directly after Rates:
      <li><a href="/fascia-stretch-therapy-san-diego">Assisted Stretching</a></li>
      The label is exactly "Assisted Stretching". The nav never carries
      "FST", "Fascia Stretch Therapy", the trademark mark or the badge.
      (site.css: between 1100 and 1199px the two social icons in the header
      are hidden, because the extra item made the header 68px wider than
      the page there; they remain in the footer.)
    HOMEPAGE BLOCK (owner copy, Nov 21 2026; pages/home-4.html, section
      #omh-fst, directly after Ways to Train and before the couples section,
      HOME_ORDER unchanged, inside FST-BLOCK markers). Label "Assisted
      Stretching"; heading "Fascia Stretch Therapy™, in Your Home"; body =
      the DEFINITION, then "Nemezio LopezPerez, Fascia Stretch Practitioner
      – Level 1, brings the table to your home. It is a separate service
      from training and open to anyone."; points "In-home only", "First
      Visit: $150, 90 minutes", "No training program required"; ONE link,
      "Explore Fascia Stretch Therapy™ →", to the FST page. No Calendly link
      for FST on the homepage; no Teqneeq, studio or reviews line in the
      block. The heading is an H3 (see KEYWORD OWNERSHIP CHANGELOG). The
      homepage title, meta, H1, hero, positioning line and In Short list are
      unchanged. The homepage coach line reads "NASM Elite Trainer ·
      Precision Nutrition Level 2 Certified Master Coach · Fascia Stretch
      Practitioner – Level 1 · 14 certifications". The title is never
      "Stretch Practitioner" alone and never "therapist".
    SERVICE NAME: Fascia Stretch Therapy™ (FST™). It is a service offered by
      OmniFit Performance, never part of a business, brand or product-line
      name (see STRETCH TO WIN MARKETING RULES).
    THE MARK ON EVERY MENTION (owner, Nov 21 2026; SUPERSEDES "the first
      mention on a page carries the trademark mark", owner, Nov 20 2026):
      the name is the Stretch to Win Institute's property, so EVERY
      published mention carries the mark: "Fascia Stretch Therapy™" and
      "FST™". That covers page copy, headings, FAQ questions and answers,
      link text, alt text, the title and meta description, schema (the
      Service name and alternateName, Offer names, breadcrumb, FAQPage),
      site/llms.txt, the assistant's knowledge file, its prompt and its
      replies, and the Calendly booking page. The canonical sentences in
      this block are quoted with the mark for that reason.
      NOT mentions, and so unmarked: the alternate spelling in its one FAQ
      sentence (also written "fascial stretch therapy"); the credential
      "Fascia Stretch Practitioner – Level 1"; the nav label "Assisted
      Stretching"; URLs, ids and class names; HTML comments (the FST-BLOCK
      markers) and CSS. This brief, REPORT.md and tools/README.md are
      working documents, not published copy, and name the service plainly
      outside the quoted sentences.
      ENFORCED: certify.py fst_trademark fails any unmarked mention in any
      swept file, attributes and schema included; functions/_lib/assistant.js
      ensureMarks adds the mark to any mention the model leaves bare, so a
      visitor never reads one.
    SCOPE: FST only. No compression boots, no percussion or massage-gun
      work, no "recovery session" naming.
    WHERE: IN-HOME ONLY. The FST page, its header and the Rates FST section
      never mention Teqneeq, a studio, or a studio price for FST. Service
      area: exactly the IN-HOME NO-FEE AREA above (the seven no-fee towns,
      Harmony Grove included since Nov 22 2026; elsewhere a travel fee
      applies; never a dollar figure).
      FST TRAVEL FEE (owner, Nov 21 2026; AMENDS the brief's "exactly
      CANON's existing in-home rule" for the fee wording only): the client
      is told the travel fee at the time of booking and it is collected at
      the visit, not with the booking payment. Verbatim on FST surfaces:
      "No travel fee in Carmel Valley, Santaluz, Fairbanks Ranch, Rancho
      Bernardo, 4S Ranch, Poway or Harmony Grove. Elsewhere in our in-home
      service area a travel fee applies: you are told the amount when you
      book, and it is collected at the visit." (Harmony Grove added Nov 22
      2026; before that "4S Ranch or Poway".) Short form: "Outside the no-fee part of our
      in-home service area a travel fee applies: you are told the amount
      when you book, and it is collected at the visit." WHY: FST is booked
      and paid in one step on Calendly, so "confirmed before you book" (the
      training wording, where a consultation comes first) cannot be true
      for it. certify.py fst_travel fails "confirmed before you book" on an
      FST surface. IN-HOME TRAINING IS UNCHANGED: every training surface
      keeps "a travel fee applies, confirmed before you book".
    WHO: open to anyone. No training program and no Performance Assessment
      required.
    RATES (in-home):
      First Visit       $150, 90 minutes. Required for every new FST
                        client. Contents: a range-of-motion check, the first
                        Fascia Stretch Therapy session on the table, and a
                        re-measure at the end.
      Single session    $225, 60 minutes.
      5-session pack    $200 per session ($1,000), expires 8 weeks from
                        purchase.
      FOUNDERS RATE (owner, Nov 22 2026; Founders run): $99 for the in-home
                        First Visit. Applies to the first 5 new in-home
                        Fascia Stretch Therapy clients, or through December
                        31, 2026, whichever comes first. First Visit only,
                        one per client. Follow-up sessions and 5-session
                        packs stay at the regular rates above. No refunds:
                        the existing First Visit payment and cancellation
                        terms apply unchanged. PUBLISHED ON ONE SURFACE: the
                        founders landing page (FOUNDERS LANDING PAGE below)
                        and its header. $99 is legal there only, beside the
                        word "founders" (certify.py fst_rates); on any other
                        FST surface it is a wrong price. The regular rates
                        on every other surface are unchanged. WHEN IT ENDS
                        (the fifth founder books, or December 31, 2026): the
                        page switches to the regular booking link and price,
                        or is retired; the owner decides.
    THE FIRST VISIT is called "First Visit". NEVER "assessment" or "FST
      assessment". It is NOT the Performance Assessment and its $150 is NOT
      credited toward anything; the FST page states that once, plainly.
    GUARANTEE: the 30-Day Fit Guarantee applies to programs only. It is
      never attached to FST.
    CANCELLATION (verbatim): "Cancellations with less than 24 hours' notice
      and no-shows forfeit the fee."
    BOOKING: ONE booking link on the site for FST, the First Visit:
      https://calendly.com/nemezio-omnifittraining/recovery-session-first-visit-assessment-in-home
      Button text "Book Your First Visit". Follow-up sessions and 5-packs
      are arranged with Nemezio after the First Visit (one line says so).
      No other Calendly page is linked for FST. (The words "recovery
      session" and "assessment" in that URL are Calendly's slug, not copy.)
      ONE EXCEPTION (owner, Nov 22 2026): the founders landing page books on
      https://calendly.com/nemezio-omnifittraining/founders-first-visit-in-home-assisted-stretching
      and on nothing else; that link appears on no other surface (certify.py
      fst_booking, both directions). The owner confirms the $99 charge on
      that Calendly event; the repo cannot see payment settings.
    FOUNDERS LANDING PAGE (owner brief, Nov 21-22 2026; Founders run):
      /in-home-stretching-founders, pages/in-home-stretching-founders.html
      and its header. A Meta ad landing page: one page, one offer, no menu.
      BUILT by build.py LANDING: logo-only header (no announcement bar, no
      nav; the logo is a plain mark, NOT a link, so a tap on it cannot carry
      the visitor off the offer to the homepage: owner, Nov 22 2026),
      legal-only footer (Terms, Privacy, copyright; no consultation
      CTA, no link grid, no Ask OmniFit loader), <meta name="robots"
      content="noindex, follow">, out of sitemap.xml and llms.txt, linked
      from no other page (build.py --check verifies each). Title "In-Home
      Assisted Stretching | Founders Rate | OmniFit Performance". The whole
      page sits inside FST-BLOCK markers, so every FST rule reads all of it.
      COPY: the owner's copy of Nov 21 2026 with these CANON forms, each an
      owner decision of Nov 22 2026: the DEFINITION sentence verbatim as the
      "What assisted stretching is" body (a sixth verbatim carrier; the
      five-places rule names where it REPLACED the older sentence); the
      "Does it hurt?" answer reads "It is designed to be comfortable, and I
      adjust to you throughout the session." (no "pain-free" outside the
      definition); the not-medical FAQ is the canonical question "Is FST™
      massage or medical treatment?" with the canonical sentence; the
      travel sentence verbatim with Harmony Grove; the DISCLAIMER block
      verbatim after the payment lines, the attribution line last; the
      credential "Precision Nutrition Level 2 Certified Master Coach"; the
      button text "Book Your First Visit", every button scrolling to the
      booking section (#fh-book), where the founders Calendly event is
      embedded inline with a plain-text fallback link; "no crowded facility"
      (the owner's "no crowded studio" trips the FST studio ban). NO reviews
      line anywhere on it (the 190+ reviews are training reviews). FIRST
      PERSON ("I bring the table to you") is the owner's voice for this page
      only; the FST page stays in the third person.
      HERO COPY (owner brief, Nov 23 2026), in order: eyebrow "In-home assisted stretching · North County
      San Diego"; the H1 "Assisted stretching that comes to your home."; the LEAD LINE "Stiff from the
      desk, the golf course or the gym?"; the SUB "A 90-minute First Visit on the table, in your own
      living room. Your range of motion is measured before and after."; the offer line and the button;
      the TRUST LINE "With Nemezio LopezPerez · NASM Elite Trainer · Fascia Stretch Practitioner –
      Level 1". Still no reviews line.
      HERO IMAGE: site/img/fst-in-home-hero.jpg. ALT TEXT: "Assisted stretching on a portable table in
      a living room". THE IMAGE IS AI-GENERATED: it is never described, in alt text, a caption or
      copy, as Nemezio, as a client, or as a real visit.
      STICKY BAR (phones): "Founders rate: $99" and a "Book Your First Visit" button. It is a second
      "$99" on this one surface, beside its "founders" label. The share image carries no price and no
      date. The page itself carries no tracking code.
    WHAT THE CLIENT NEEDS: a quiet room with floor space. The table comes
      with him. Wear clothes you can move in.
    PAYMENT TERMS (owner decisions, Nov 21 2026; verbatim sentences):
      "Payment confirms your booking. The First Visit is paid when you
      book; follow-up sessions and 5-session packs are paid in advance. No
      slot is held without payment."
      "Fees are not refunded. With 24 hours' notice or more you can
      reschedule." (Less than 24 hours and no-shows: the CANCELLATION line.)
      "A single session expires 30 days from purchase; a 5-session pack
      expires 8 weeks from purchase." Either can be rescheduled any time
      before it expires.
      Written "not refunded", never "non-refundable": that word stays the
      Foundation policy's alone (certify.py fee_language).
    DISCLAIMER (owner decision, Nov 21 2026; verbatim, one block):
      "Fascia Stretch Therapy™ is assisted stretching for mobility and
      recovery. It is not medical treatment, not physical therapy and not
      massage. Information on this website and during a visit is
      educational and is not medical advice. Consult your physician before
      booking, particularly if you have injuries, medical conditions, or
      are pregnant. A Liability Waiver and Release must be signed before
      your First Visit."
      This AMENDS "the FST page says so once, in the FAQ": the not-medical
      sentence now appears in the FAQ answer AND inside the disclaimer, and
      nowhere else on a surface.
    WHERE THE TERMS AND DISCLAIMER LIVE: the FST page (a Payment Terms
      block under the rates table; the disclaimer above the trademark
      line), Terms and Conditions (sections 2, 5, 6 and 7) and the Calendly
      First Visit booking page. The Rates FST section and the knowledge
      file carry the same facts.
STRETCH TO WIN MARKETING RULES (HARD; owner brief, Nov 20 2026. These are
the Stretch to Win Institute's conditions for marketing Fascia Stretch
Therapy. No run, and no owner override inside a run, relaxes one.)
  1. NO business or brand name containing "FST", "Fascia Stretch Therapy",
     "Fascial Stretch Therapy", "Frederick Stretch Therapy" or "Stretch to
     Win". FST is a service offered by OmniFit Performance, never part of a
     business, brand or product-line name: no "OmniFit FST", "OmniFit
     Stretch", "FST by OmniFit" or similar.
  2. NO video recorded, embedded or downloaded from the Stretch to Win
     website.
  3. NOTHING THAT TEACHES FST. Copy describes what a session is like for
     the client, never how a stretch is performed: no step-by-step
     technique, no positions, sequences or cues.
  4. VIDEO LIMITS, for any future video: Nemezio stretching a client, 1
     minute maximum; a client testimonial, 2 minutes maximum. The FST Launch
     run added no video.
  5. ATTRIBUTION, verbatim, at the foot of the FST page: "Fascia Stretch
     Therapy™ and FST™ are trademarks of the Stretch to Win Institute."
  COMPLIANCE FOR FST COPY (the two-tier screen applies in full; these are
  the FST-specific points, owner brief Nov 20 2026):
    · FST is assisted stretching for mobility and recovery. It is not
      medical treatment, not physical therapy and not massage; the FST page
      says so in the FAQ, in this sentence: "It is not medical treatment,
      not physical therapy and not massage." (AMENDED Nov 21 2026, owner:
      the sentence also sits inside the DISCLAIMER block, CANONICAL FACTS.
      Once in the FAQ, once in the disclaimer, nowhere else.)
    · No diagnose / treat / heal / cure / fix / rehabilitate claims. No
      pain-relief or injury claims. No outcome promises and no "in X
      sessions" language. The re-measure is a measurement the client sees,
      never a promised gain.
      ONE OWNER EXCEPTION (Nov 21 2026): the canonical DEFINITION says the
      stretching "is pain-free ... and improves functionality". Both
      phrases live inside that verbatim sentence and nowhere else:
      "pain-free" is how the stretching feels, not a pain-relief claim, and
      "improves functionality" is about the modality, not a promise to a
      client. Neither may be lifted out, reworded or given a timeframe.
    · "Therapy" appears only inside the method's name.
    · Persona language without a timeframe is fine (desk-bound
      professionals, golfers, people who feel stiff after travel).
    · No "free", no emoji (gold line-SVG icons from site/icons.py), no
      Pacific Beach; the reviews line only in its canonical form (the FST
      page carries no reviews line: the 190+ reviews are training reviews).
  FST SURFACES (how certify.py scopes the rules; tools/README.md has the
  detail): the FST page and its header, whole file; anything between
  <!-- FST-BLOCK --> and <!-- /FST-BLOCK --> on another page; an ld+json
  node whose "name" names the service; the section under a heading naming
  the service in assistant/knowledge.md or site/llms.txt; and any other
  mention, read in its own block, string or line. "Fascia Stretch
  Practitioner" (the credential) is not a mention.
  ENFORCED (certify.py, self-tested both ways on every run by _selftest_fst
  and negative-tested on the real files, REPORT.md FST Launch run):
    (a) fst_banned - on an FST surface: therapist, treat, heal, cure,
        compression, boots, percussion, Teqneeq, studio, "recovery session",
        "therapy" outside the method's name, diagnose, rehab, fix, pain /
        injury, guarantee, free, "in N sessions", "assessment" used for the
        First Visit (the only legal use is the Performance Assessment being
        denied), an embedded video or a stretchtowin.com URL.
    (b) fst_rates - FST prices read 150 / 225 / 200 per session (1,000 the
        pack) wherever they appear; retired_225 - $225 anywhere else;
        fst_fascial - "Fascial" only in its one FAQ sentence and the mirror;
        fst_brand - the rule 1 names and the "therapist" titles, site-wide;
        fst_trademark - the mark on EVERY mention (first mention only
        until Nov 21 2026), schema and attributes included;
        fst_session_length - 90 minutes only as the First Visit, 60 or 90
        on an FST surface; fst_booking - one Calendly link for FST;
        fst_nav - site/nav.html carries exactly the one "Assisted
        Stretching" link after Rates and never the service name, "FST",
        the mark or the badge (until Nov 21 2026 the rule failed any
        "stretch" in the nav); fst_definition_required - the DEFINITION
        verbatim as the lead in its five places, once per file;
        fst_home_block - the homepage block's copy, its single link, no
        Calendly link, no H1 / H2; fst_brand also fails "Stretch
        Practitioner" without "Fascia"; the FST page carries the
        attribution line at its foot, the First Visit / Performance
        Assessment distinction exactly once, the cancellation line, the
        canonical travel-fee sentence and the booking button; since Nov 21
        2026 also the payment, no-refund and expiry sentences and the
        disclaimer exactly once, and fst_terms_required holds Terms and
        Conditions to the same sentences so the two pages cannot drift.
    (c) the FST page's nine FAQ questions in order, the header FAQPage
        byte-identical to them, the Service node with provider
        #localbusiness-of and Offers 150 / 225 / 1000, no business or
        person node defined in the header, FST-BLOCK markers paired.
  NOT MACHINE-CHECKED (human warranties): rule 3 (copy that teaches a
  stretch) and rule 4 (video length). certify.py fails any <video>,
  <iframe>, YouTube or Vimeo URL on an FST surface, so a video cannot be
  added without the rule being revisited.
  THE FST PAGE (/fascia-stretch-therapy-san-diego): title "Fascia Stretch Therapy™ in San Diego | In-Home | OmniFit Performance". Nine FAQ questions; the header FAQPage is identical to them. No In Short block and no shared "Who this is for" block (both name pain and the training facility). Headings say "senior adults", never "older adults". Its research figures (Stathokostas et al. 2013, Wilke et al. 2019) are published third-party figures, cited with the note that they are not studies of the service and make no claim about outcomes.
  THE BADGE: site/img/fst-certified-level-1.png is the owner's "FST Certified Level 1" PNG, UNMODIFIED. Never recoloured, cropped, redrawn or resized without owner approval. It sits on a white rounded panel, never on navy. Alt text: "Fascia Stretch Therapy™ Certified Level 1 badge". Shown in EXACTLY THREE places: the FST page's practitioner block, the about credentials entry and the homepage FST block. Nowhere else: not the nav, the footer or beside the OmniFit logo.

PRICING — OCTOBER 2026 CARD (owner-confirmed Sept 13 2026). Published copy uses THIS card and
nothing else. Figures and locked sentences are VERBATIM from the full brief.

  ASSESSMENT
    Performance Assessment $150. CANONICAL CREDIT LINE (owner, Oct 17 2026): "The $150 Performance Assessment is credited toward your first purchase: a Foundation or Program cycle, an Executive Reset cycle, or a 5-session pack." Short form on CTA notes: "credited toward your first program, Reset cycle or 5-pack". Existing "credited toward your first cycle" lines stay. Territory FAQ form: "The Performance Assessment ($150 in person, $75 virtual) is credited toward your first program, Reset cycle or 5-pack."
    VIRTUAL PERFORMANCE ASSESSMENT $75 (remote / Executive Reset clients): self-measured with live video guidance, posture photos in the app, no Bodystat scan, credited toward the first purchase the same way, booked after the consultation. Single sessions: the assessment is recommended, not required; packs and programs require it.
    CONSULTATION DEPOSIT, CANONICAL (owner, Oct 17 2026): "$30 deposit, refunded the same day you attend your consultation". Never "fully refundable", never "the deposit applies to your first cycle". NEVER "free" - the consultation is 45 minutes, by video or phone, and is NOT the assessment. The movement screen happens only at the assessment.
    CANONICAL PRICING FAQ ANSWER (verbatim on its twelve carriers, in the page FAQ and the header FAQPage: the eleven territory pages and corrective-exercise-post-rehab; certify.py compares the text): "OmniFit Performance publishes its rates in full. New clients start on The Foundation: three consecutive 4-week cycles paid in full at enrollment, $560 per cycle for studio Momentum, $1,100 for studio Performance, $800 for in-home Momentum, $850 for studio couples and $1,250 for in-home couples. After that, or by direct entry, The Program bills every 4 weeks: $640 to $1,800 at the studio, $900 to $2,600+ in-home, $1,000 to $2,900 for couples. Without a program, single sessions are $205 to $275 and 5-packs run $180 to $250 per session depending on setting and membership. The fully virtual Executive Reset runs $200 to $1,100 per 4 weeks. Programs and session packs start with a Performance Assessment ($150 in person, $75 virtual), credited toward your first purchase; for a single session it's recommended, not required. Note: studio programs require a Teqneeq membership ($119 per month, billed by Teqneeq), with facility access on non-training days included. Full tables on the training rates page."
    9-POINT SCREEN ASSESSMENT SENTENCE (verbatim where the 9-point screen section opens, on the eleven pages that carry it; certify.py compares the text): "Every OmniFit program starts with a 45-minute consultation and the $150 Performance Assessment, credited toward your first cycle."

  THE FOUNDATION - new clients only. Three consecutive 4-week cycles, paid
  in full at enrolment, discounted for that reason.
    Studio Momentum (1x/wk)       560/cycle    1,680 total
    Studio Performance (2x/wk)    1,100/cycle  3,300 total
    In-home Momentum              800/cycle    2,400 total
    Studio couples Momentum       850/cycle    2,550 total
    In-home couples Momentum      1,250/cycle  3,750 total
    NOT offered on the Foundation: Peak (either setting), in-home Performance, Performance couples. Those start on The Program. A new client with prior training experience MAY start directly on The Program at any tier; the Foundation is then no longer available to them. The Foundation is a ONE-TIME ENTRY, never a step back.
    Foundation policy: non-refundable; apart from your statutory cancellation rights, the 30-Day Fit Guarantee is the only early exit; two pause weeks across the course with notice, extending the end date; sessions OmniFit cancels are credited.
    HOW IT ENDS (owner decision, Oct 18 2026): the client chooses; NO AUTOMATIC BILLING. After the third cycle the client decides whether to continue on The Program at their tier's published rate, and nothing is charged unless they confirm. Rates page wording: "After the third cycle you choose whether to continue on The Program at your tier's published rate. Nothing is charged unless you confirm." / "It ends after the third cycle. Nothing more is charged unless you choose to continue on The Program." / "After its third cycle you decide whether to continue on The Program; nothing is charged unless you confirm, and The Program can then be ended with 30 days' notice." Never "you continue on The Program" as an automatic step.

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
    Program terms (PUBLISH ON THE PAGE): 6 pause weeks per 12 months with 2 weeks' notice, credited against the next cycle; 30-day notice to cancel, remaining credit applied to the final cycle; 24-hour reschedule within the same cycle; sessions OmniFit cancels are credited.

  SESSIONS WITHOUT A PROGRAM
                            Studio member  Studio non-member  In-home
    Single session          205            235                275
    5-pack                  180/session    210/session        250/session
    Extra session (program) 160            -                  215
    Guest add-on            90             90                 90
    Studio non-member prices include the Teqneeq day pass. Singles expire 30 days from purchase; 5-packs 8 weeks. NO 10- or 20-packs. Both are retired.

  EXECUTIVE RESET (virtual): Bronze async 200 · Gold 1x/wk 500 ·
    Platinum 2x/wk 750 · Black 3x/wk 1,100. Billed every 4 weeks.

  TUNE-UP (graduates): 295 member · 325 non-member · 375 in-home. One session per cycle - reassessment on the Bodystat QuadScan 4000 and an hour of training - with programming delivered through the OmniFit app between visits. BILLED EVERY 4 WEEKS, 30 days' notice to cancel. The product is the "TUNE-UP"; "Monthly Tune-Up" is a BANNED literal term on public pages.

  TERMS
    ALL RECURRING BILLING IS EVERY 4 WEEKS. NO PRODUCT BILLS MONTHLY. The Program, the Executive Reset and the Tune-Up all bill on a 4-week cycle. There is no month-to-month option on any product and no monthly billing anywhere on the card. "month-to-month" and "billed monthly" are BANNED literal terms on public pages. The one legitimate "per month" in published copy is the TEQNEEQ MEMBERSHIP at $119/mo - that is Teqneeq's billing, not OmniFit's, and it stays. Cadence language ("monthly progress reports", "tracked monthly") describes how often something happens, not how it is billed, and stays.
    No contract exceeds $4,400. No exit fees. Round numbers only. No processing fees are added to stated prices; the 2.9% card fee stays retired.
    TRAVEL FEE (in-home training; never a dollar figure): "No travel fee in Carmel Valley, Santaluz, Fairbanks Ranch, Rancho Bernardo, 4S Ranch or Poway; elsewhere in our in-home service area a travel fee applies, confirmed before you book." Territory pages in the area: "No travel fee in [Town]; it's inside our in-home service area." Outside it (La Jolla, Del Mar, Rancho Santa Fe, Solana Beach, Encinitas, Carlsbad): "A travel fee applies in [Town], confirmed before you book." In-home page: the no-fee towns in its service-area list carry a "No travel fee" tag (4S Ranch is not on that page; Poway reads "Also serving Poway (no travel fee)"), and the page says "No travel fee for the marked areas; elsewhere a travel fee applies, confirmed before you book."
    30-DAY FIT GUARANTEE, canonical (owner, Oct 17 2026; byte-identical wherever it appears): "If OmniFit isn't the right fit within your first 30 days on The Foundation, The Program or the Executive Reset, tell us in writing and we'll refund the unused portion of your enrollment." "No compliance test" stays beside it. It promises a refund and an exit, never a result (TIER 2 item 6). WORDING CHANGES REQUIRE OWNER APPROVAL.
    The "Class IIa medical device" statement and its not-a-medical-provider note stay BYTE-IDENTICAL wherever they appear (TIER 2 item 4). "clinical-grade" and "medical-grade" are dropped SITEWIDE: device copy reads "multi-frequency bioimpedance" and the Rates assessment paragraph "a measured baseline session".
    CONTRACT VALUE CHECK (a workflow step, not a pricing cap): owner approval before filing a client on any contract whose total exceeds $4,400. Only an off-card arrangement can reach it.
    A card change is made everywhere a price is stated: the rates page and its chooser, the Fit Check page script, the assistant's knowledge file, the pricing FAQ answer above and the headers that mirror them.

  NOT ON THE CARD - do not publish
    Essential tier: unlisted. Graduates / case by case only. "Essential" is
      a banned tier name on public pages.
    Continuing-client discount 10-15%: case by case, NEVER published.
    Executive Hybrid: stays dead.

LEGACY PRICING - AUGUST 2026, CLOSED. Existing clients only; never published. A client enrolled on an August rate stays on it until they choose to move, which is a new enrolment on the October card. An August figure that is not also on the October card is stale canon wherever it is published. The figures are in the archive.
  Retired forever: Executive Hybrid (product, name, slug, $299/$500), the $175/$150/$225/$200-session era ($225 and $200 per session are canonical again in ONE meaning each, the FST single session and the FST 5-session pack rate), $225–275/mo era, $599–899 Reset era, $50/$75 travel fees, Foundation/VIP packages. $150 or $175 as a STUDIO PER-SESSION RATE is a violation. $75 is legal only as the Virtual Performance Assessment price, $140 only as a computed figure in the tier-change example, $90 only as the guest add-on.

TIER CHANGES (owner decision, Oct 17 2026)
  Tier = session frequency: Momentum (1x/wk) / Performance (2x/wk) / Peak (3x/wk). The Dial is separate from tier.
  THE PROGRAM: tier can change UP OR DOWN at any 4-week cycle boundary, with notice before the next cycle starts.
  THE FOUNDATION: NO DOWNGRADES until The Foundation is complete; the first 12 weeks are built as a block. UPGRADES are allowed. Between Foundation tiers (studio Momentum -> studio Performance): the client stays on The Foundation and pays the difference for the remaining cycles. To a tier not offered on The Foundation (Peak either setting, in-home Performance, Performance couples): The Foundation ends and the client starts The Program at the new tier at the next cycle boundary. Unused Foundation sessions are credited at the FOUNDATION PER-SESSION RATE (cycle price / sessions per cycle) against the first Program cycle; the client pays any difference. If the credit exceeds the first cycle, the remainder carries forward as SESSION CREDIT, never cash, since The Foundation is non-refundable.
  NO move from The Program into The Foundation, ever.
  PUBLISHED PLAIN-LANGUAGE COPY (verbatim, training-rates-san-diego): "On The Program you can move up or down a tier between cycles. During The Foundation you can step up, not down — the first 12 weeks are built as a block. Want more sessions mid-Foundation? Step up anytime. If your new tier is only offered on The Program, your Foundation ends there — every unused session is credited toward your first Program cycle, and you pay only the difference. You can adjust your accountability level at any cycle boundary."
  WORKED EXAMPLE (training-rates-san-diego; static text, re-derived from the card before any edit): studio Momentum Foundation client upgrades to studio Peak after cycle 1. 560 / 4 = 140 per session; 2 x 4 = 8 unused sessions; 8 x 140 = 1,120 credit; 1,800 - 1,120 = 680 due.

ACCOUNTABILITY DIAL (owner decision, Oct 17 2026)
  Three settings, in this order, INCLUDED AT EVERY TIER of The Foundation, The Program and the Executive Reset, at no price difference: FULL ACCOUNTABILITY (daily logging; coach reply within 1 business day; DEFAULT for the first cycles), COACHED (weekly written check-in with a coach reply; 1-3 habit targets; measurement review every 4 weeks), TRAIN ONLY (sessions plus the app program; one-tap weekly check-in; nutrition on request). Chosen at the Performance Assessment; changeable at any 4-week cycle boundary, INCLUDING during The Foundation.
  CORE PRINCIPLE (verbatim wherever the Dial is explained): "Tracking is a diagnostic tool, not a life sentence. We measure closely at the start so we can coach less over time. The goal is a client who no longer needs us every week."
  PATH (the published rendering): "Full Accountability -> Coached -> Train Only -> Tune-Up". The Tune-Up is graduation, never a fourth setting; it has no Dial setting.
  FLOORS at every setting: payment confirms booking · 24h reschedule notice · corrective work in every warm-up · reassessment at least every 12 weeks.
  ROLES LINE (verbatim everywhere it appears; em dash included): "Sessions are for form, load and corrective work. The app carries your individual program between sessions, your logs and your check-ins — written for you, not a template."
  Behavior-change stages: AWARENESS, REGULATION, ADAPTATION, INTEGRATION ("Identification" is retired).
  EXECUTIVE RESET BRONZE (async, no live sessions) offers COACHED or TRAIN ONLY, not Full Accountability; Gold, Platinum and Black carry all three. Copy that enumerates the settings for the Reset says so.

THE OMNIFIT METHOD (owner decision, Oct 17 2026)
  Three pillars, in this order, present throughout Assess -> Correct -> Build -> Sustain: MEASURED PROGRESS, JOINT-FIRST STRENGTH, ACCOUNTABILITY THAT TRAVELS. Written with THE METHOD AS THE SUBJECT ("The OmniFit Method measures..."), never the founder. "Every program begins with a Performance Assessment", never "Every client". Joint-First Strength keeps the post-PT bridge WITHIN SCOPE: OmniFit trains, physical therapy treats; OmniFit never diagnoses or treats. Accountability That Travels carries the Bronze exception in its definition: "included at every tier (Executive Reset Bronze offers Coached or Train Only)".
  THE TRAVEL PROTOCOL (named pathway; owner, Oct 17 2026; verbatim): "The Travel Protocol: for studio and in-home clients whose work takes them on the road. Travel-adapted programming in the app for hotel gyms and rooms, check-ins that continue at your Accountability Dial setting, and pause weeks when a trip can't hold training. During a travel week, a scheduled session can be taken live by video instead, at no extra cost. Included in every tier of The Foundation and The Program at no extra cost. Fully remote clients use the 30-Minute Executive Reset."
  USAGE: always "the Travel Protocol" (capital T and P). Never state a price for it. Never in a title, meta description, H1 or H2. Canonical phrasing on pages: "take a scheduled session live by video during a travel week, at no extra cost". Never claim ADDED or EXTRA virtual sessions, or that sessions "switch to" or are "converted to" virtual; standing live virtual sessions are the Executive Reset's. The nutrition card on behavior-change-coaching is named "Travel & Restaurant Playbooks" so it does not collide with the name.
  ONE-LINE REFERENCE: "OmniFit runs on the OmniFit Method: Measured Progress, Joint-First Strength and Accountability That Travels, carried through Assess -> Correct -> Build -> Sustain."
  SCOPE STATEMENT (verbatim, corrective-exercise-post-rehab): "Physical therapy treats; OmniFit trains. We pick up where care ends, coordinate with your clinician when you allow it, and never diagnose or treat."

OTHER DECISIONS THAT GOVERN PUBLISHED COPY (one line each; the story of each is in the archive)
  ENTRY: the front door is the 45-minute consultation at https://calendly.com/nemezio-omnifittraining/45min. Every button or link that offers a consultation, an enrolment or a booking goes there (target="_blank" rel="noopener"), as does every schema ReserveAction; links labelled "Contact" stay on /contactform.
  Announcement bar: "Limited availability for 1:1 coaching. Book a consultation". Start date: "Your start date depends on current availability and is confirmed on the consultation."
  NUTRITION is included in every program. There are no nutrition coaching add-ons.
  Comparison page: compares CATEGORIES, not local brands; competitor figures are labelled typical ranges (big-box PT $50-100 per session).
  Body composition page: InBody frequencies "Varies by model (2-3 on common gym models)"; ECW/TBW "helps explain day-to-day weight swings; read as a trend alongside how you feel and recover".
  Desk-worker page: "Budget is under $200 per 4 weeks, our lowest tier (Executive Reset Bronze)".
  Homepage: title "Personal Trainer San Diego | Diagnostic-Led Coaching" (the header WebPage name), H1 "San Diego Personal Trainer for Executives". Its partner section states NO prices.
  Fit Check: "Instant result; no answers are saved or sent; only an anonymous count of completed checks and their result is recorded." The only hold is refusing the two booking standards (payment confirms a booking; 24 hours' notice).
  404 page: "Page Not Found | OmniFit Performance", noindex, links to Home and Book Your Consultation only. The *.pages.dev preview is noindexed; production stays indexable.
  Privacy policy names Google Analytics 4, Microsoft Clarity (not used on the Fit Check), the Meta Pixel, HubSpot, Calendly, Cloudflare and Anthropic, and never Google Tag Manager or Google Ads.

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
     M., Egor B., Chad C., Alo S., Mark M., Vincent, Ken, Dave R., Mariano G.
     certify.py
     cannot verify a consent form, so it reads this list (CONSENT_LIST): a
     figure attributed to anyone else, or to an anonymised profile, is a
     consent finding until the owner adds the name here. Dave R. added by the
     owner Oct 17 2026 (follow-up run): Dave's case study and the 4S Ranch
     transformation card.
     Mariano G. added by the owner Oct 18 2026: the real 4-week progress
     report on how-we-measure-your-progress (scans on the 1500 MDD, a
     factual record, with the note that OmniFit now uses the QuadScan 4000).
     The sample QuadScan report on body-composition-testing is a single
     baseline scan, unattributed at the client's request (name, age, test
     date and serial removed); it carries no client-result figures in copy.
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

CARRIED OVER WITH THE SCREEN: no Groupon or deal content; no prenatal or postpartum content (uncertified scope, kept under TIER 1 item 3 until the owner says otherwise).

LANGUAGE RULES (Oct 17 2026)
  PRICE is framed as PROTECTING PROGRESS, always with these five facts: the assessment is credited toward the first cycle · the 30-Day Fit Guarantee (canonical wording, verbatim) · pause weeks · sessions OmniFit cancels are credited · The Foundation is a defined starter block (three 4-week cycles, one payment).
  POLICIES are framed as "standards that protect your slot and your results", never as rules the client is subject to.
  BANNED in new copy: "insurance" as a FRAMING of price or structure ("think of it as insurance", "insurance against falling off"; the ban is the metaphor, not the word: a factual payment answer is not a framing) · any results or outcome guarantee (TIER 1 item 1) · pain-reduction promises ("hurt less", "pain-free in"; describing the 3/10 pain ceiling or a corrective floor is not a promise) · perimenopause / hypermobility / prenatal positioning as a segment or a page angle.
  APPROVED SEGMENTS (persona language, no timeframe, no figures): executives and founders · desk-bound and remote professionals · active adults 50+ · professional women 35-55 with joint concerns · people returning after a long break or after physical therapy · people burned by bootcamps or big gyms · couples. The unifying audience stays "professional adults 30+".
  FRONT-DOOR LINE (verbatim): "Even if you just want to train, we can start there."
  No new client figures or stories. Case studies untouched (frozen records).

STANDING COPY RULES
  Reviews: only "4.98 average across 190+ reviews"; never "5.0", "five-star" for the total, "verified", "180+" or "133+".
  Guarantees: none beyond the 30-Day Fit Guarantee wording. "Free": never near a consultation, assessment, screen, session, call or intake.
  No emoji: icons are the gold line SVGs from site/icons.py.
  Credentials as written under BUSINESS AND ENTITY: never "ACE OES", "Orthopedic Exercise" or "Fascial Stretch Therapist".
  EM-DASHES: a voice preference, never a certification finding. New prose written by a run carries none; existing ones stay.
  "assessment" names only the Performance Assessment. "Essential", "Monthly Tune-Up", "month-to-month", "billed monthly" and "Executive Hybrid" never appear on a public page.
  RETIRED PHRASES, never published again (tools/certify.py RETIRED_LAUNCH_COPY sweeps for them): "fully refundable" · "applies to your first cycle" · "within the week" · "zero crowds" · "fully private" · "nutrition coaching add-ons" · "Strategy Session" · "133+ Reviews" · "three month program" · "3-month package" · "after your first 30 days" · "no standardized assessment" · "Typically single" · "flags inflammation" · "@gmail.com" · "g.page/r/CcePeMjnbDe9EBM/review" · "$250/month" · "diagnostic fee is credited" · "depending on location" · "varies by location" · "Iron Orr" · "Elite Training" · "paid 45-minute" · "Credentialed access only" · "Honest assessment of fit" · "45-minute movement assessment" · "seven tracked benchmarks" · "a travel fee may apply outside it" · "training throughout San Diego County" · "available throughout San Diego County" · "five-star reviews" · "5.0 rating" · "5.0 · 190+" · "Rated 5.0" · "5.0 star" · "5.0-star" · "verified reviews" · "verified five-star" · "works exclusively with" · "client tenure" · "6 months minimum" · "Unlimited coach communication" · "check-in submissions required" · "45–60 min" · "30 or 45-minute" · "30–45 min" · "is the only exit".
  RETIRED LITERALS (tools/certify.py BANNED sweeps for them): "OmniFit Personal Fitness Training" · "Pacific Beach" · "ACE OES" · "Orthopedic Exercise" · "Executive Hybrid" · "Lopez Perez" · "180+" · "Performance Diagnostic" · "month-to-month" · "billed monthly" · "Monthly Tune-Up" · every dollar figure of the August card that is not on the October card.

SITE FACTS
  REDIRECTS: the list lives in build.py REDIRECTS (public/_redirects is generated, never edited). The owner's Squarespace URL mapping of Oct 17 2026 is authoritative; booking URLs go to the Calendly consultation link; /blog is a 302 until the Journal has a post.
  MEASUREMENT: ONE setup, all in the repo, NO Google Tag Manager; loaders in pages/headers/site-header.html, every event in site/site.js. IDs: Google Analytics 4 G-0K6VLEC2VJ · Microsoft Clarity yzawpvwvdf · Meta Pixel 3596878003826620. RETIRED, never in public/: GTM-5P4CKPT2, Clarity ulpgsrkd98, AW-16616873404, G-QTG1ZLR0NQ, any "dataLayer.push". All three load on the production hostnames only; Clarity and the Meta Pixel NEVER load on /fit-check. Meta receives PageView and Schedule and nothing else: no parameters, no personal data, no advanced matching, no noscript image.
  KEY EVENTS (GA4): book_consultation_click · generate_lead · phone_click · email_click · fit_check_start · fit_check_complete (individual answers are NEVER sent) · rates_section_view · rates_chooser_result (no price is sent) · booking_cta_click · booking_section_view · booking_time_selected · booking_completed (with Meta's Schedule) · assistant_open · assistant_message · assistant_cta_click (no message text is sent). Parameters and manual steps: DEPLOY.md "Measurement".
  ROBOTS: Googlebot, Google-Extended, GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-SearchBot, PerplexityBot and Bingbot are allowed site-wide; /api/ is disallowed for every agent.

ASK OMNIFIT (the on-site AI assistant; owner brief, Oct 19 2026)
  assistant/knowledge.md is its ONLY source of facts and MUST AGREE WITH THIS FILE: public facts only (no tooling, compliance notes, payment processor, client names or legacy rates), every price from the card, the mark on every FST mention. functions/_lib/knowledge.js is generated from it by build.py. The system prompt (functions/_lib/system-prompt.js) is the owner's wording; a change needs owner approval. Setup: DEPLOY.md "Ask OmniFit".
  SPEND CAP: 30 messages an hour per visitor and 300 an hour across all visitors (ASSISTANT_GLOBAL_LIMIT_PER_HOUR); 600 characters per message; a fixed hand-off after 12 visitor turns; max_tokens 400. No raw IP, email or phone number is stored; log rows are deleted after 90 days.
  PACIFIC BEACH NOT-SERVED LINE (owner decision, Oct 21 2026): the knowledge file carries exactly one line, "- Pacific Beach (PB) is not in the in-home service area. OmniFit does not offer in-home training in Pacific Beach. Pacific Beach clients can train at the studio at Teqneeq in 4S Ranch, or virtually on the Executive Reset." It appears nowhere else.

KEYWORD OWNERSHIP — A GUIDELINE, NOT A GATE (owner decision, Nov 27 2026)
  Each tracked keyword has one owner page: the phrase belongs in the owner's title, H1, H2s and meta description and is best kept out of other pages' titles, H1s, H2s and metas; other pages cover the topic in body copy and link to the owner with the phrase as anchor text. tools/ownership.py reads the table below against the built pages and prints every departure as a WARNING. A warning never fails build.py --check and never blocks a run; the run weighs it and says in REPORT.md what it did.
  X01: the in-home page carries no "private", North County, cost, age-group or town term in its title, meta, headings, FAQ questions or JSON-LD; towns appear in its body only as links in the one service-area list (Poway as text). X02: "private" stays out of the homepage title, H1 and H2s. /personal-trainer-4s-ranch and /personal-trainer-rancho-bernardo are cited by ChatGPT as they are. K10 (cost) has no page yet: no new cost-anchor links, and /training-rates-san-diego stays transactional.

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
      cover  in[- ]home personal trainers? (?:in )?carlsbad|carlsbad in[- ]home personal trainers?
  K21 personal trainer carmel valley / in home personal trainer carmel valley
      owner  /personal-trainer-carmel-valley
      match  (?:in[- ]home )?personal trainers? (?:in )?carmel valley|carmel valley (?:in[- ]home )?personal trainers?
      cover  in[- ]home personal trainers? (?:in )?carmel valley|carmel valley in[- ]home personal trainers?
  K22 personal trainer del mar / in home personal trainer del mar
      owner  /personal-trainer-del-mar
      match  (?:in[- ]home )?personal trainers? (?:in )?del mar|del mar (?:in[- ]home )?personal trainers?
      cover  in[- ]home personal trainers? (?:in )?del mar|del mar in[- ]home personal trainers?
  K23 personal trainer encinitas / in home personal trainer encinitas
      owner  /personal-trainer-encinitas
      match  (?:in[- ]home )?personal trainers? (?:in )?encinitas|encinitas (?:in[- ]home )?personal trainers?
      cover  in[- ]home personal trainers? (?:in )?encinitas|encinitas in[- ]home personal trainers?
  K24 personal trainer fairbanks ranch / in home personal trainer fairbanks ranch
      owner  /personal-trainer-fairbanks-ranch
      match  (?:in[- ]home )?personal trainers? (?:in )?fairbanks ranch|fairbanks ranch (?:in[- ]home )?personal trainers?
      cover  in[- ]home personal trainers? (?:in )?fairbanks ranch|fairbanks ranch in[- ]home personal trainers?
  K25 personal trainer la jolla / in home personal trainer la jolla
      owner  /personal-trainer-la-jolla
      match  (?:in[- ]home )?personal trainers? (?:in )?la jolla|la jolla (?:in[- ]home )?personal trainers?
      cover  in[- ]home personal trainers? (?:in )?la jolla|la jolla in[- ]home personal trainers?
  K26 personal trainer rancho bernardo / in home personal trainer rancho bernardo
      owner  /personal-trainer-rancho-bernardo
      match  (?:in[- ]home )?personal trainers? (?:in )?rancho bernardo|rancho bernardo (?:in[- ]home )?personal trainers?
  K27 personal trainer rancho santa fe / in home personal trainer rancho santa fe
      owner  /personal-trainer-rancho-santa-fe
      match  (?:in[- ]home )?personal trainers? (?:in )?rancho santa fe|rancho santa fe (?:in[- ]home )?personal trainers?
      cover  in[- ]home personal trainers? (?:in )?rancho santa fe|rancho santa fe in[- ]home personal trainers?
  K28 personal trainer santaluz / in home personal trainer santaluz
      owner  /personal-trainer-santaluz
      match  (?:in[- ]home )?personal trainers? (?:in )?santaluz|santaluz (?:in[- ]home )?personal trainers?
      cover  in[- ]home personal trainers? (?:in )?santaluz|santaluz in[- ]home personal trainers?
  K29 personal trainer solana beach / in home personal trainer solana beach
      owner  /personal-trainer-solana-beach
      match  (?:in[- ]home )?personal trainers? (?:in )?solana beach|solana beach (?:in[- ]home )?personal trainers?
      cover  in[- ]home personal trainers? (?:in )?solana beach|solana beach in[- ]home personal trainers?
  K30 fascia stretch therapy san diego / fst san diego
      owner  /fascia-stretch-therapy-san-diego
      also   /in-home-stretching-founders
      match  fasci(?:a|al) stretch therapy|\bFST\b
  K31 assisted stretching san diego
      owner  /fascia-stretch-therapy-san-diego
      also   /in-home-stretching-founders
      match  assisted stretch(?:ing|es)?
  X01 in-home page carries no other keyword's qualifier
      page   /in-home-personal-trainer-san-diego
      in     title meta h1 h2 h3 h4 h5 h6 faq jsonld
      match  \bprivate\b|north county|older adults?|\b(?:over|after)[- ]50\b|\bseniors?\b|\bcost\b|how much|\bpric(?:e|es|ing)\b|4s ranch|carlsbad|carmel valley|del mar|encinitas|fairbanks ranch|la jolla|rancho bernardo|rancho santa fe|santaluz|solana beach|poway|del sur|olivenhain|la costa
  X02 homepage keeps "private" out of its title, H1 and H2s
      page   /
      in     title h1 h2
      match  \bprivate\b
  END OWNERSHIP TABLE

WORKFLOW
  DEPLOY = MERGE TO MAIN. main is the live site (Cloudflare Pages). Claude Code runs end with "merge to main and push main"; the owner is never handed git commands. Nothing is pasted into the site by hand: a change is edited in pages/, rebuilt, checked and merged.
  EVERY RUN: python3 build.py, python3 build.py --check and python3 tools/certify.py from the repo root, then REPORT.md. tools/README.md documents every check. A judgment call beyond the written instructions is allowed and is reported with the condition under which it would be wrong.
  CERTIFICATION reports exactly three categories: (a) compliance strikes, (b) stale canon, (c) broken structure. On a finding or an ambiguity: report file:line and STOP; never fix silently.
  If a rule here is wrong the owner changes it here, and tools/ is brought into step in the same commit. A header's FAQPage is derived from the page's FAQ (tools/faq.py), verbatim, in order.
  archive/ is never certified, corrected or brought back. Sources are pages/ (headers: pages/headers/<slug>-header.html), site/ and assistant/; public/ and functions/_lib/knowledge.js are generated.
  THE JOURNAL (/blog): posts are drafted on a schedule and publish only on the owner's "publish". Process and topics: editorial/PLAYBOOK.md and editorial/CALENDAR.md. Drafts live on a blog-NN branch. A post is a page for every check.
  SEARCH SAFETY. No run removes more than a quarter of an indexed page's visible copy, changes a title or H1, or takes a keyword phrase off a page's headings unless the brief names that change and states the ranking risk. Content cuts never ship in the same release as a platform, URL or template change. The Oct 17 2026 homepage cut is why.
