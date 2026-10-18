# Certification tooling

Run from the repo root. These encode CANON.md. **Use them; do not rebuild the
rules from scratch.** If a rule is wrong, fix it here and update CANON.md so the
two stay in step.

```
python3 tools/certify.py     # the three-category certification
python3 tools/mkheaders.py   # regenerate the Batch 3 page headers
python3 tools/ownership.py   # keyword ownership on public/ (also run by build.py --check)
python3 tools/ownership.py --selftest   # its must-fail / must-pass fixtures
python3 build.py --check     # site checks incl. redirects vs tools/gsc-known-urls-*.txt and the tracking rule
NODE_PATH="$(npm root -g)" node tools/tracktest.js   # measurement test on the built site (Playwright)
NODE_PATH="$(npm root -g)" node tools/mobileaudit.js [--open-details] [--shots DIR]   # 390/412px layout audit (Playwright)
NODE_PATH="$(npm root -g)" node tools/choosertest.js [--shots DIR]   # rates chooser vs CANON card, keyboard/ARIA, 390/412 layout
```

`certify.py` reports exactly three categories — (a) compliance strikes,
(b) stale canon, (c) broken structure — then the five invariant hashes, then
the checks that could not run, then `PASSED` / `FAILED` / `INCOMPLETE`.
Anything else is a judgment call for a human, not a certification finding.
`INCOMPLETE` means no findings but at least one check was not applied; it is
never reported as a pass.

## The standing rule

**Every check must fail loudly rather than return empty, and any run that does
not print a `RESULT:` line is an incomplete run, not a pass.** Four incidents
in this repo share one shape — the null overwrite, the questions-only
regression, the literal-string free-framing miss, and the `KeyError` abort that
killed the run before its result line. In each, something reported success, or
reported nothing, while not actually looking. A check that cannot look must say
so: raise, or record itself under CHECKS THAT COULD NOT RUN. Silence and an
empty comparison are the two failure modes that have actually bitten, and
neither of them is green.

## Why this exists

Three separate checks have reported success while not actually looking at the
thing they claimed to check. Each is now closed by something in this directory.
The pattern is the point: **a green result means nothing until you have seen the
check fail on purpose.**

| Incident | What it reported | What was true |
|---|---|---|
| Header regression | "every header mirrors its page" | It compared **questions only**, never answers |
| Header re-mirror | 7 answers "re-mirrored" | It wrote `null` over all 7, destroying the canonical pricing block |
| Free-framing rule | how-we-measure certified clean | Page said `free 45-minute assessment`; rule only knew `consultation` |
| Session-pack rule | CANON authorised `10 @ $150` as a pack rung | $150 belonged to neither venue's ladder — a mangled merge of the studio and in-home figures |
| FAQ extractor coverage | `online-training` header mirrored its page | Page FAQ uses `<button class="faq-q">`; extractor read **0 questions**, schema had 0 FAQ entries, so the check compared `[]` to `[]` and passed |

The pack-rule incident is the odd one out: CANON itself was wrong, not the tool.
Widening `certify.py`'s $150/$175 check to match the corrected CANON immediately
surfaced 8 pre-existing hits on three *other*, already-certified, already-pasted
pages (FAQs, how-it-works-pricing, private-personal-trainer-san-diego) — a
customer-facing pricing error (a rendered `$150/session` price card) that had been
live and certifying clean the whole time. Fixing a rule can expose a violation the
old rule was never written to see; that is a finding to report, not a bug in the
new rule.

Before trusting a new rule, negative-test it in **both** directions: confirm it
flags a real violation, and confirm it passes the legitimate copy next to it.
Rules that *narrow* scope are the dangerous ones — every exemption below carries
a fixture proving a real violation in the same shape still flags.

## FAQ extraction (`faq.py`)

**Pages with no FAQ (`NO_FAQ` in certify.py, CANON "PAGES WITH NO FAQ").** An
empty mirror used to be recorded as "compared nothing" and kept certification
at INCOMPLETE forever, because six pages simply have no FAQ. A declared page now
passes only after a positive scan: no `<details>`, `<summary>`, `faq`/`accordion`
class, `fq` button or "Frequently Asked Questions" in the page body, and no
FAQPage in the header. Negative tests (Oct 16, 2026): adding a `<details>` FAQ to
fit-check flags `[declared no-FAQ page carries FAQ markup]`; dropping fit-check
from the list brings back the not-run entry. An undeclared page with no FAQ is
still NOT RUN, never a silent pass.

**Page node subtypes (`PAGE_TYPES`).** AboutPage and ContactPage count as the
page node for the `about` → #localbusiness-of check.

Decorative toggle icons (`<span class="…icon">+</span>`) inside a question
container are stripped before comparison (home-5 carries one per question).

Pages use six question-container patterns and six answer-container patterns.
A missing question pattern yields no question at all; a missing answer pattern
yields a question with no answer. Neither used to raise, which is how the `null`
overwrite happened and how `online-training` passed a mirror check against a
header with no FAQPage at all.

Question containers:

- `<summary …>…</summary>` — with or without a class attribute. The
  attribute-less form matched only the territory pages; `hsa-fsa` uses
  `<summary class="hsa-faq-q">` and read as zero questions.
- `<div class="…faq-q">…</div>` — cx / fl / st / hiit / desk-worker
- `<button class="fq" …>…<span` — how-it-works-pricing, the-omnifit-method
  (how-we-measure-your-progress also uses it for its six FAQs. Its Results-section
  "How these figures were calculated" toggle is marked `class="fq fq-method"`
  on purpose: it is a method disclosure, not an FAQ, and counting it shifted
  every FAQ index by one - the "7 vs 6 mirror drift" that mkheaders.py
  "fixed" by copying the method block into FAQPage. Fixed Oct 16, 2026.)
- `<button class="…faq-q" …>…</button>` — online-training
- `<div class="faq-question">…</div>` — omnifit-vs-competitors
- `<button class="op-faq-q" …>…<svg` — partners (now subsumed by the generic
  `…faq-q` button pattern; kept as documentation)

Answer containers:

1. `<div class="…faq-a" …>…</div>` — covers `faq-a`, `of-faq-a`, `cx-faq-a`,
   `bc-faq-a`, `fl-faq-a`, `st-faq-a`, `hiit-faq-a`, `op-faq-a`
2. `<div class="…faq-body" …>…</div></details>` — the territory pages, plus
   `hsa-faq-body`, `rt-faq-body`, `er-faq-body`, `sz-faq-body`
3. `<div class="fa"><p>…</p></div>`
4. `<div class="faq-answer">…</div></div>`
5. `<div class="op-faq-a-inner">…</div>` (subsumed by 1; kept)
6. `<div class="answer" …>…</div>` — home-5, the only container with no `faq`
   in its class name at all

Questions and answers are paired by document position, so a new question
pattern needs its answer pattern added at the same time.

`qa()` returns ordered `(question, answer)` pairs. `qa_strict()` is the same but
**asserts no answer is None** — use it anywhere the result gets written to a
file. `questions()` returns questions only.

### The zero-answer guard (Sept 2026)

`qa()` now **raises `faq.ExtractorFailure`** when a page yields questions and
*not one* extractable answer. That combination is always an unknown
answer-container class, never a page that legitimately has no answers, and
returning the pairs anyway is what let a mirror check compare `[]` to `[]` and
report success. `certify.py` catches it and records the pair under CHECKS THAT
COULD NOT RUN — an unverified mirror, never a pass. Negative-tested both ways:
an unknown container raises, `of-faq-a` next to it returns the pair.

### Patterns added Sept 2026

| Pattern | Kind | Page it was missing on | Was |
|---|---|---|---|
| `<summary class="…">` | question | hsa-fsa-personal-training | only attribute-less `<summary>` matched — 9 questions read as 0 |
| `<button class="[a-z-]*faq-q">` | question | online-training | 7 questions read as 0, mirror passed vacuously |
| `<div class="answer">` | answer | home-5 | 5 questions, 0 answers |

`of-faq-a` was **already covered** by `<div class="[a-z-]*faq-a">`, which also
covers `faq-a`, `cx-faq-a`, `bc-faq-a`, `fl-faq-a`, `st-faq-a` and `hiit-faq-a`.
It was verified rather than added: dropping that pattern breaks FAQs,
in-home-personal-trainer-san-diego, private-personal-trainer-san-diego and
online-training, so the coverage is load-bearing and proven, not assumed.

`_hits()` now deduplicates containers on their **start offset, shortest match
wins**. Two patterns can read the same element — `op-faq-q` matches both the
`<svg` pattern and the generic `</button>` one — and without dedup that one
container yields two questions and the pairing walks off by one for the rest of
the page (it did, on `partners`: 6 questions became 12 with 6 unanswered).

Every pattern is negative-tested for load-bearing: removing it must break a
named page. Two are now subsumed by the generic prefixed patterns
(`op-faq-q…<svg`, `op-faq-a-inner`) and are kept as documentation of the shape;
removing them changes nothing.

## Header mirroring

CANON (c) requires the FAQPage to mirror the page FAQ in **count, order and
text**. `certify.py` checks all three, answers included. Comparison normalises
whitespace before punctuation, because stripping `<a>` tags leaves a space
before the period — an extraction artifact, not a mirroring failure.

`certify.py` delegates extraction to `faq.py` rather than carrying its own copy,
so certification and header generation cannot disagree about what a page's FAQ
is. They previously did.

**Every `<script type="application/ld+json">` block is read, not just the
first.** A header may spread its nodes across several blocks:
`desk-worker-posture-pain-header` carries `Service` in block 1 and its
6-question `FAQPage` in block 2. `re.search` stopped at block 1, so the mirror
compared 6 page questions against 0 schema questions and reported the **header**
broken — the checker not looking, blamed on the file it failed to read. Nodes
from all blocks are now merged (flattening `@graph` where present) before any
structural check runs, and invalid JSON names which block it was in. It was the
only multi-block header in the repo; fixing it changed exactly one pair's status
and no others. Negative-tested both ways: a matching second-block FAQPage
mirrors, an altered one still flags.

## Compliance rules (a) — the two tiers

Rewritten Sept 2026 when outside counsel disengaged and the owner became the
sole compliance decision-maker. The old screen was aimed at projections and
caught measured facts in the same net; the owner judged that a mistake. See
CANON **COMPLIANCE SCREEN — TWO TIERS**.

**TIER 1 rules report a violation. TIER 2 rules report a MISSING CONDITION.**
A Tier 2 rule that flags conditioned copy is a defect in the rule, not a
finding — that inversion is the single most important thing to keep straight
when editing this file.

| # | Rule | Tier | Status |
|---|---|---|---|
| 1 | `guarantee_any` | T1-1 | **changed** — "guarantee" with a result noun in the same sentence (narrowed Sept 12; see below) |
| 2 | `lbs_near_timeframe` | T1-2 | **changed** — inches and body-fat % added; disclaimer relaxed to same-page |
| 3 | `result_near_timeframe` | T1-2 | **changed** — same-page disclaimer; conditioned surfaces exempt |
| 4 | `uncertified_claims` | T1-3 | **changed** — assess/manage a medical condition, and device-used-to |
| 5 | `prenatal_postpartum` | T1-3 | unchanged — carried over, see CANON's note |
| 6 | `free_consultation` | T1-4 | unchanged |
| 7 | `phase_angle_result` | T1-5 | **new** |
| 8 | `population_clinical_claim` | T1-6 | **new** — the surviving half of `clinical_stat` |
| 9 | `aggregate_metric_conditions` | T2-1 | **new** — replaces `clinical_stat`'s blanket ban |
| 10 | `class_iia_note` + cross-file wording | T2-4 | **new** |
| 11 | BANNED literal terms | (b) | unchanged — stale canon, not the compliance screen |
| 12 | travel-fee adjacency | (b) | unchanged — and still carries its known defect, below |
| 13 | `$150`/`$175` context | (b) | unchanged |
| 14 | tag balance · ld+json validity | (c) | unchanged |
| 15 | LocalBusiness `@id` · `about` reference · FAQ mirror · orphan page | (c) | unchanged |
| 16 | invariant mismatch · canon hash stale | (c) | unchanged |
| 17 | `attributed_outcome_conditions` | T2-2a | **new** (Oct 17 2026) — the Outcome Claims Amendment's conditions 3, 4, 5 and the consent list; counted since the Oct 17 follow-up (`AMENDMENT_COUNTS = True`); page-scoped /outcomes short disclosure |
| 18 | `data_backed_figures` | T2-2g | **new** (Oct 17 2026) — unattributed client figures must be on /outcomes; adherence % on sight; same reporting rule |
| 19 | `positioning_line_verbatim` | (b) | **new** (Oct 17 2026) — the POSITIONING LINE verbatim, never in title/meta/H1 |
| 20 | `travel_protocol_usage` | (b) | **new** (Oct 17 2026) — "the Travel Protocol" casing, no price |
| — | `clinical_stat` | **RETIRED** | split into 8 (hard ban, force unchanged) and 9 (conditional). Nothing is lost: the population-scope clinical case it existed for is 8. |
| — | dedicated-block disclaimer test | **RETIRED for T2-2** | written to counsel's standard; T2-2 asks only for a same-page disclaimer. Still governs nothing else — T2-1 states its own three conditions. |

### What the tiers changed, rule by rule

- **`guarantee_any` (T1-1).** Two draftings, each wrong once, and the pair is
  worth keeping as a lesson in what the rule is actually for:
  **v1** flagged "guarantee" within ~30 words of an outcome word, and missed
  the DEFERRED-01 wording, which was written not to sit near one.
  **v2** flagged the word itself, and caught that wording along with
  everything else — including a refund policy that promises no result at all.
  **v3 (Sept 12, owner decision)** asks whether a RESULT NOUN is the object of
  the guarantee or sits in the same sentence. What makes a guarantee a Tier 1
  violation is the result it promises, not that it is called a guarantee; a
  promise about money is CANON Tier 2 item 6 and is legal.
  The window is the **sentence**, not a word count: "guarantee" and its promise
  sit either side of a colon in `30-Day Guarantee: you will be stronger`, and a
  fixed window either clips the promise or reaches into the next sentence.
  Negation still reads the preceding words only, so `Reimbursement is not
  guaranteed` on hsa-fsa stays legal.
  Fixture both ways: the approved 30-Day Fit Guarantee callout and FAQ answer
  must pass; `guarantee you'll lose 20 lbs` must fire.
- **`lbs_near_timeframe` (T1-2).** Inches and body-fat percentage added.
  Condition 2 of the case-study exemption relaxed from a dedicated block to
  anywhere on the page. Attribution and the never-exempt aggregate test are
  untouched, which is why neither how-we-measure-your-progress nor
  desk-worker-posture-pain gains an exemption from the relaxation — both fail
  attribution on their own.
- **`uncertified_claims` (T1-3).** "Assesses" and "manages" are new and are
  **scoped to a medical condition**. Unscoped they would flag "every client
  starts with a movement assessment" across most of the site — a rule failing
  closed so hard it stops being read.
- **`aggregate_metric_conditions` (T2-1).** The rule that carries the point of
  the rewrite. A figure presented as an aggregate is a finding **only** when
  its surface is missing a method line, the not-independently-audited note, or
  the individual-results disclaimer, and the finding names which. Surface = the
  innermost enclosing `<section>`, falling back to the page. The fixture is the
  Results section of `how-we-measure-your-progress.html`: it passes with all
  three present and flags with any one removed.
  The machine-checkable half of "method" is sample size **and** period. "What
  was measured" is prose beside the figure and stays a human warranty, like
  substantiation in T2-2 — stated here so nobody later reads a green result as
  proof the method line is good.
- **`class_iia_note` (T2-4).** Two conditions, two findings. Per-file: the fact
  must sit beside the not-a-medical-provider note. Cross-file: one
  byte-identical wording everywhere, collected in `run()` the way an invariant
  is, because that is the shape of the check.
  The cross-file comparison is on **the sentence** the fact sits in. It was a
  12-word window first, and that window also compared the prose on either side:
  once the canonical block was appended correctly to a second page, three
  different words in the *preceding* sentence (`no additional cost.` against
  `a population average.`) read as two different wordings of an identical
  claim. A checker reporting correct copy as a violation — the Tier 2 inversion
  this file warns about, arriving in the one rule written to be exact.
  The window existed because an earlier sentence split, run while the fact sat
  mid-sentence inside a header's `ld+json`, swept up `" } }, { "@type":
  "Question"`. That is no longer the shape. Negative-tested: changing one word
  *inside* the block (`certification` → `approval` on one of three surfaces)
  still fires and names the odd file out.

### Three defects this rewrite introduced, and how they surfaced

Recorded because each is a shortcut the next editor will also reach for, and
none was caught by reading the code.

| Shortcut | What broke | Caught by |
|---|---|---|
| Strip `<script>` bodies as "not copy" | A header file **is** one `ld+json` block. Every header went blank and ten rules reported nothing on it — the null overwrite in a new costume | the widened guarantee rule going silent on `training-rates-san-diego-header` |
| Add `"` as an inch unit | Every ld+json price (`"325.00"`) read as `00 inches`: 20 invented findings across three headers | running the suite and reading the output |
| `\bmedical condition\b` | Does not match "medical condition**s**" — the device rule passed the exact sentence T1-3 names | the negative test, not the regex |

Thirty-eight negative tests were run across the changed and new rules, both
directions on each. Two failed on the first pass: the plural above (a real
bug) and one badly written fixture (it removed one of the two audit phrases and
expected a flag).

## Stale-canon rules (b)

**The signal inverted on 13 Sept 2026.** August prices were canonical; they are
now the stale-canon marker, and the October card's figures are canonical. Three
figures changed sides and had to be REMOVED from `BANNED`, not added to it:
`$90` (was the retired name-era assessment price, now the guest add-on), `$275`
(was an August month-to-month rate, now the in-home single) and `$500/mo` (was
Executive Hybrid, and Reset Gold is now $500).

Banning a bare figure is only safe when it appears in **no** October product.
The safe set was computed by differencing the two CANON blocks, not read off by
eye: sixteen figures collide, and each would have been a false positive on
correct copy.

Two matching rules exist because both were learned the hard way in one run:

- **Figures need a right boundary.** Plain substring matching fired `$50` inside
  `$500` and `$75` inside `$750`, both October Reset tiers.
- **A hyphenated range is third-party pricing.** `$50-80/session` and
  `$150-250/month` are competitor rates on the comparison page. The card's rule
  is round numbers only, so every OmniFit figure is a single number — which
  gives the same exemption the August `$150` rule carried as a `comp-value`
  class whitelist, without needing to know the class names.

`assessment_as_session_rate` replaces the August `$150`/`$175` context rule.
`$150` is now canonical — it is the Performance Assessment — so the rule checks
the **meaning** rather than the number: `$150` published as a per-session rate
is the October equivalent of the old mangled pack rung.

`BANNED_TIERS` holds `Essential`, unlisted on the card, matched
case-sensitively so "essential movement patterns" stays prose.
`fee_language` flags `exit fee`, `cancellation fee` and `non-refundable`
**scoped to the sentence**, with the Foundation policy sentence as the single
exemption and the negative test.

Retired with the August card, kept as a note rather than code: `_marker_nearby`,
`_inside_packs_table`, `CANON_MARKERS`, `CANON_CARDS`. All four carved `$175`
out as a legal pack rung; it appears in no October product and is a plain
banned literal now. A dormant exemption is how a retired figure gets
grandfathered back in through a context nobody re-reads.

### The old $150/$175 rules

- **$150 is retired everywhere.** Neither ladder uses it (studio 5/10/20 @
  $145/$140/$135; in-home @ $175/$170/$165). The only exemption is competitor
  pricing on the comparison page (`comp-value` divs) — there is no packs-table,
  marker, or card exemption for $150, by design, so it can never be
  grandfathered back in through a context meant for $175.
- **$175 is legal** inside: the canonical pricing FAQ answer, a marker phrase
  on the same line or within 2 lines above (`_marker_nearby`, covers a title
  and its price sitting on adjacent lines — e.g. a `<h3>Bronze</h3>` line
  followed by the price div), a `pc-name` card lookback matching a canonical
  card name, or inside a `<table class="...packs...">` block
  (`_inside_packs_table` — the in-home pack column).
- **DEFERRED-01 is resolved**, not exempted. There is no `DEFERRED_01`
  carve-out in `certify.py` any more — the approved replacement text does not
  pair "guarantee" with an outcome word, so it passes `guarantee_near_outcome`
  on its own merit. If the old banned wording ever reappears anywhere, it now
  flags like any other violation.

### Launch decisions 18-20 (Oct 17 2026)

- **`booking_cta_to_contactform`** extends `consultation_cta_to_contactform`
  (item 15) to every enrolment or booking label: an anchor to `/contactform`
  whose tag-stripped label starts "Start", "Get Started", "Book" or "Stay".
  "Contact" (and "Contact us to start") stays quiet.
- **`reserve_action_to_contactform`** parses every `ld+json` block and walks
  it: a `ReserveAction` whose `target` (a URL string or an `EntryPoint`)
  names `/contactform` fires. A `WebPage` `url` naming the contact page does
  not: the contact page's own address is not an entry action.
- **`ken_muscle_claim`** fires on `+6 lb(s)`, `6 pounds of muscle` and
  `6 lbs of muscle` on the flattened copy of EVERY file, frozen records
  included (the owner overrode their exemption for Ken's card, which is
  where the figure lived). A digit guard keeps `16 lbs of muscle` and
  `+6.2 lbs` quiet.
- **`RETIRED_LAUNCH_COPY`** gains `depending on location` and `varies by
  location` (item 19). The clean fixture now carries the canonical travel
  sentence, a territory sentence and the pricing answer's "depending on
  setting and membership", which must stay quiet.
- All four self-test both ways on every run. Negative test: the new
  `certify.py` against the pre-change tree reported 54 stale-canon hits (31
  travel phrases, 11 booking CTAs, 5 ReserveActions, 7 Ken figures) and
  FAILED; the changed tree reports none.

### Two exemption defects, fixed Oct 17 2026

The owner-dictated over-50 proof card "−11 lb bodyweight, 6 months" beside
"Ken · CTO · 50s" fired T1-2 although TIER 2 item 2 exempts it (attributed,
page disclaimed). Two defects, each enough on its own:

| Defect | Shape that broke it | Fix |
|---|---|---|
| `DISCLAIMER_ANYWHERE` read one sentence only | "Individual results. Outcomes depend on ... and vary between clients." stopped at the first period: page read as undisclaimed | the condition word may sit in the same sentence or the next one (one period, 160 chars each side) |
| `AGGREGATE` matched bare `everyone` | "years of putting everyone else first" in Vincent's card, 45 words away, read as population framing | `everyone(?!\s+else)`, `anyone(?!\s+else)` |

`_selftest_case_study_exempt()` runs before the compliance screen on every
run: the disclaimed attributed card must pass; the same card with no
disclaimer, "Everyone loses 11 lb in 6 months" and an unattributed "Clients
lose 11 lb in 6 months" must all fire, and "Individual results. Call us
today." must not count as a disclaimer.

## Outcome Claims Amendment (Oct 17, 2026)

CANON TIER 2 items 2a and 2g (owner-approved Oct 1 2026, applied Oct 17 2026)
and the TIER 1 item 2 carve-out. The amendment was recorded before any page
was brought to it, so the two new rules **report in full under `(a') OUTCOME
CLAIMS AMENDMENT` and did not count toward the result** while
`AMENDMENT_COUNTS = False`. The follow-up run the same day brought the copy to
zero findings and set `AMENDMENT_COUNTS = True` (owner): they count now. The
`RESULT:` line always carries their count.

**`attributed_outcome_conditions` (T2-2a).** Scans the raw file with
comments, `<style>`, non-ld+json `<script>` bodies and `style="…"` attributes
blanked to spaces (positions and line numbers survive), so CSS bar widths
(`width:94%`) never read as figures. A figure is pounds / inches / body-fat %
(`_T1_UNITS`) or a bare percentage. It is *attributed* when, within 80 words,
there is a consent-list first name or a case-sensitive name shape: `Name,
<role>` / `Name · <role>` / `Name — <role>`, `Name is a <role>`, or `Name,
<age>`. Case-sensitive on purpose: the first draft used `re.I` and read "That
is a…", "This… client" and "Illustrative example, not client data" as
people. The nearest *preceding* name within 12 words wins (the /outcomes
profile table puts three clients on one line; a figcaption puts the name
first), else the nearest name either side (a stat card puts the name under
the figure). Then, per figure:

- consent — the first name must be in `CONSENT_LIST` (anonymised profiles
  fail too: no list vouches for them);
- (3) — `in just` / `in only` / `in as little as` beside the figure;
- (4) — `DISCLOSURE_2A` verbatim on the figure's surface (`_surface`: the
  enclosing `<section>`, else the page), compared after flattening,
  entity-unescaping and `_norm`, so a link-wrapped URL still matches. On
  /outcomes only (`outcomes.html` and its header, by basename via the
  `page` argument) the disclosure is `DISCLOSURE_2A_OUTCOMES`, the first
  sentence alone, and must NOT be followed by "How clients typically
  progress" (`_has_disclosure`): the full line there, and the short line
  anywhere else, are both findings (owner, Oct 17 2026);
- (5) — in the figure's *block* sentence (innermost p/h/li/td/div…, then
  sentence-split): second person, first person singular (`I`, `my`, `me`,
  case-sensitive on `I`), a projection word (`will`, `can`, `expect…`,
  `typical…`, `up to`) or a present-tense outcome verb. The block scope
  exists because a stat card's label ("+18 lbs Lean Muscle") has no period
  and the first draft ran it into the next card's "You…".

Figures inside tag attributes (alt, aria-label, data-tip) are skipped
(`_in_tag`): `_flat()` drops attributes, so no other rule sees them either.
Deduplicated on (line, client, condition).

**`data_backed_figures` (T2-2g).** Unattributed figures only. A figure is a
*client result* when, within 20 words, a client word (`client(s)`, `client
base`, `of those`, `cohort` — not `members`, a gym word: "80% of members
quit by month 3" is a big-box statistic) sits beside a past-tense result verb
or statistic word (`lost`, `achieved`, `rose`, `median`, `average`…). Skipped:
goal framing before the figure (`want to lose 20–30 lbs`, TIER 2 item 3),
trial words (`trial`, `study`, `participants`, `DXA` — the GLP-1 page),
illustrative surfaces (TIER 2 item 5). A client result must appear on
`pages/outcomes.html` (`_published_on_outcomes`: the number with its unit
class, sign dropped, lb/lbs/pounds unified). A percentage within 20 words of
`adherence` / `attendance` / `sessions completed` is a finding on sight.

**TIER 1 item 2 carve-out.** `lbs_near_timeframe` now breaks before reporting
when `_published_with_method(figure)` is true: the figure appears on
/outcomes on a surface carrying a sample size (`_C_SAMPLE`) and the page
carries a date range (`_DATE_RANGE`; page-wide, because /outcomes states it
once in its meta line). `outcomes=` overrides the live page for self-tests;
the Oct 17 case-study self-test passes `outcomes=''` so it can never be
satisfied by a figure that happens to be on the live page.

**Negative tests, both directions, every run (`_selftest_amendment`).** A
compliant card passes; a link-wrapped disclosure passes; "in just" fires and
"over 6 months" does not; the near-verbatim "…; see aggregate outcomes
above." fires; the disclosure on another surface fires; "you", "I added", 
"will add" and "gains … every year" each fire; an unlisted name ("Marco,
business owner"; Dave R. joined the list Oct 17 2026 and now passes) and an
anonymised profile fail consent, "Ken · CTO" passes it; the /outcomes
exemption both ways (short line passes on outcomes.html and its header,
fails on another page and with no page; the full line and the
"; see aggregate outcomes above." near-miss fail on /outcomes, the full
line passes elsewhere; the short line on another surface fails); an unattributed
figure is not a 2a finding. 2g: an off-outcomes aggregate fires, the same
figure on a synthetic /outcomes passes, a persona goal passes, a trial
figure passes, an adherence % fires and an illustrative adherence % passes,
an attributed figure is not a 2g finding. Carve-out: the aggregate fires
with the figure absent, with no sample size, and with no date range, and
passes when all three are there.

**First live run (Oct 17 2026): 17 findings, all genuine, listed in
REPORT.md.** The three false-positive classes the drafts produced and what
closed them: sentence-start words read as names (case-sensitive shapes +
`_NONPERSON`); the 1200-character window reaching from /outcomes' retention
table into its profiles section (80-word window, nearest-preceding rule);
alt text read as copy while the rest of the screen ignores it (`_in_tag`).

**`positioning_line_verbatim` (b).** Keyed on two fragments no other copy
uses (`diagnostic-led coaching system`, `pain or plateau`); CANON's
DESCRIPTION says "diagnostic-led personal training practice" and is quiet.
Each fragment hit must have `POSITIONING_LINE` verbatim within 220
characters (not sentence equality: inside ld+json the "sentence" before a
slogan is an email address). Separately reports the fragment inside
`<title>`, `<h1>`, a `<meta name="description">`, or a header's WebPage
`name` / `description` (build.py reads those as the title and meta).
Self-tested: verbatim, in a summary, and as an ld+json slogan pass; two
paraphrases, the DESCRIPTION, and each banned placement behave as expected.

**`travel_protocol_usage` (b).** `travel protocol` in any casing but
`Travel Protocol`, and a `$` figure in the same sentence as the name. Live on
the travel-support pages since the Oct 17 follow-up run. The price test reads
the sentence inside its block element (`_block_sentence`): splitting on
punctuation alone ran an unpunctuated `<li>` on omnifit-vs-competitors back
into the `$640–$2,900 per 4 weeks` paragraph above the list. Self-tested: a
price in the block above passes, a price in the same `<li>` fires.

**T2-1 vs the 2a disclosure (Oct 17 follow-up).** `aggregate_metric_conditions`
read "How clients typically progress" in the disclosure as aggregate framing
and struck Vincent's −8% card on the over-50 page once the disclosure went
on. That verbatim pointer (link-wrapped or not) is blanked, same length, for
the framing test only. Self-tested: the card beside the disclosure passes,
the card beside "Clients typically see this." still fires.

**T1-2 vs the 2a disclosure (owner decision, homepage rebuild, Oct 17 2026).**
The same misreading in `lbs_near_timeframe`'s named-individual exemption
(`_case_study_exempt`): a named case card carrying the verbatim disclosure
lost its exemption because "typically" sat inside the 45-word window, which
struck all seven figures on the new homepage case cards. Only the exact
sentence "How clients typically progress: omnifittraining.com/outcomes."
(`DISCLOSURE_2A_POINTER`; link-wrapped reads "outcomes ." once flattened) is
blanked, same length, on the whole text **before** the window is cut — a first
version blanked it inside the window and missed the cases where the window
edge split the sentence, leaving a bare "typically". Self-tested both ways in
`_selftest_case_study_exempt`: (1) a named card with the verbatim disclosure
passes, at every window offset from 25 to 54 words of padding; (2) a named
card beside "Our clients typically lose 10 lbs in 3 months" still fires on the
named figure; (3) the disclosure with one word changed ("typically improve")
is not exempt.

**Teqneeq on-site PT (`teqneeq_onsite_pt`, stale canon, Oct 17 2026).** Teqneeq
has no on-site physical therapy clinic (CANON ENTITY BLOCK). A sentence naming
Teqneeq, or the sentence after it, that places a PT / physical therapy /
rehab clinic on site or in-house is a finding; negations pass. Every file in
the glob, frozen records included. Self-tested both ways
(`_selftest_teqneeq_pt`: the old /about line, a clinic in the next sentence,
"PT clinic on site" and "in-house rehab" fire; the canonical negation, an
external partner and a claim in the sentence before Teqneeq pass), and
negative-tested on the real tree by restoring the removed /about sentence in
memory (1 finding).

## Known checker defects, unfixed

- **travel-fee rule, `$75` adjacency.** `travel[^.<]{0,30}\$(?:50|75)` fires on
  `…Extra guest add-on: $75/session · A travel fee may apply…`
  (`couples-personal-training-san-diego.html:274`). The `$75` is the canonical
  guest add-on and the travel sentence carries no figure, which CANON
  explicitly permits. Two unrelated facts sitting either side of a `·` are read
  as one claim. Reported, not fixed — the fix is to require the dollar figure
  and the word *travel* inside the same `·`-delimited clause.

## Byte-identical duplicates

Where two in-scope files are byte-identical, `certify.py` certifies one and
references the other: it sha256-hashes every in-scope file, keeps the
alphabetically first of each identical group so the choice is deterministic,
and **prints the pairing** in the SCOPE block rather than applying it silently.
`pages/home-3.html` was the `case-studies` block pasted into the homepage
(sha256 `c82d5f32…`); certifying both double-counted every finding on it. Since
the homepage rebuild (Oct 17 2026) it is three short case cards, no longer a
duplicate and no longer frozen; there is no byte-identical pair in `pages/`.

`archive/` never enters the glob, and an assertion enforces that: retired pages
keep their retired pricing, old address and unmirrored headers on purpose.

## Invariants

Five, all recomputed from the files each run and compared against the hashes
recorded in CANON.md: page pricing, header pricing, credentials, archetypes,
9-point screen. All five are now **printed every run**, not only on mismatch,
and an invariant that matched no file at all is reported as not-verified rather
than silently absent.

### Two mismatch classes, both category (c)

Until Sept 2026 this section described a comparison that did not happen. The
check only asserted that the files carrying an invariant agreed with **each
other**; it never opened CANON.md. An invariant edited consistently across all
its pages therefore passed in silence while CANON still recorded the old hash —
the null overwrite again, a comparison reporting success without looking at the
thing it claimed to check. The hashes are now parsed out of CANON's INVARIANTS
block and compared, and the two failures are reported as two classes because
they mean different things:

| Finding | What is true |
|---|---|
| `[invariant mismatch]` | the files carrying the invariant disagree with **each other** |
| `[canon hash stale]` | the files agree, and what they agree on is **not what CANON.md records** |

Files agreeing with one another proves only that an edit was applied
consistently. The Device Swap run is the case in point: retiring the 1500 MDD
rewrote the Body Composition `<li>` on every territory page at once, so the
9-point hash moved from `bd73ea51bc9ec5eb` to `ba590a09107ffda0` with all pages
still in perfect agreement. Under the old check that was indistinguishable from
no change at all.

The recorded hashes are **parsed, never hard-coded** — a copy in `certify.py`
would be a second place to forget to update, and CANON being the single
recorded source is the whole point. Each invariant's bullet anchor and hash
pattern are matched inside **one `- ` bullet** of the INVARIANTS block. The
first version searched the whole block with `.*?` under `re.S`, which let a
blanked hash match forward into the *next* bullet and report a neighbouring
invariant's value as its own — a parser failing open, in the exact shape the
check exists to close. It was caught by negative-testing a blanked archetypes
hash, which "parsed" as the 9-point value.

Fails loudly, never open. An unreadable CANON.md, a missing INVARIANTS block,
or a block where not one hash parses raises `certify.CanonParseFailure`;
`run()` catches it and records the run under CHECKS THAT COULD NOT RUN, so an
invariant that was never compared can never read as one that matched. A single
unparseable hash is reported per-invariant the same way. Both paths are
negative-tested, and so is the parse of a live CANON.md.

Negative-tested in both directions, as every rule here must be: altering the
recorded 9-point hash in CANON.md fires
`[canon hash stale] 9-point: files agree on …, CANON.md records …` and moves
the structure count; reverted, all five read `ok` and the count returns.

The credentials block is 630 bytes across 10 pages. Editing it means editing all
ten and updating the hash in CANON.md in the same commit. CANON recorded this
one truncated to 8 hex while the others were 16, so comparison is on the
**recorded prefix** — a shorter recorded value is a weaker check, not a
mismatch. The entry was widened to the full `6492e3ca1545dc26` in the Device
Swap merge, closing that weakness; the prefix rule stays, with an 8-hex floor,
because nothing stops a future entry being written short again.

## CHECKS THAT COULD NOT RUN

Not a fourth category — CANON says a run reports exactly three. This block
lists checks that were **not applied**, so a green result can never mean
"nothing was looked at". A run with zero findings but a non-empty block prints
`RESULT: INCOMPLETE`, not `PASSED`.

What lands here: a header whose ld+json is a single bare node rather than an
`@graph` document (the homepage header *is* the LocalBusiness definition, and
several uploaded headers are one bare node — that shape is outside what CANON
specifies for page headers, so calling it a violation would be inventing a
rule and calling it a pass is how three earlier checks came to report success
without looking); an `@graph` with no `WebPage` node; a page whose FAQ the
extractor could not read; a header/page pair where both sides have zero FAQ
entries so the mirror compared nothing; an invariant that matched no file.

Before Sept 2026 the first of these did not report anything at all — it raised
`KeyError: 'WebPage'` and killed the run part-way through category (c), so no
mirror check, no invariant hash and no result line was produced. Certification
had been aborting rather than certifying since the uploads that followed commit
`4b3f5f7`.

## Scope

`certify.py` skips `the-30-minute-executive-reset` and `footer` (see CANON
REPO STATE). `training-rates-san-diego` entered scope in the Rates Page
Correction run (Aug 2026) once its content certified; the naming fix (its
header lacked the `-header.html` suffix) was applied *after* content passed,
per CANON's naming-fix rule — doing it first would have hidden a real
structural check behind a filename mismatch instead of a genuine pass.
Everything else under `pages/` is in scope.
There is an assertion that the glob matched a non-zero number of files — an
earlier run passed vacuously because it was executed from the wrong directory
and matched nothing.

```
python3 tools/mkterritory.py   # regenerate the eleven territory page headers
```

`mkterritory.py` keeps each territory header's own WebPage and breadcrumb,
mirrors the on-page FAQ verbatim (tags stripped) in page order, and asserts the
pricing answer is byte-identical across all eleven before writing.

## Keyword ownership (`ownership.py`, Oct 2026)

Reads the OWNERSHIP TABLE in CANON's KEYWORD OWNERSHIP section and fails when
an owned phrase sits in the title, H1, H2s or meta description of a page other
than its owner (or an `also` page), plus the page-specific X rules (the
in-home page's banned qualifiers, the homepage's "private"). It reads the
**rendered** pages in `public/`, because title and meta are only resolved at
build time, and it is run by `build.py --check`, not `certify.py`: CANON caps
certification at three finding categories and this is none of them.

It fails closed the same way the rest of this directory does: a missing,
empty or malformed table, a regex that does not compile, or an owner page that
was not built is a problem, never a skipped check. An unassigned keyword
(owner `-`) is printed as NOT enforced rather than passing silently.

Fixtures: `fixtures/ownership/fail/*.html` must each produce a problem,
`fixtures/ownership/pass/*.html` must each produce none; each carries a
`<!-- fixture-path: /slug -->` line saying which page it pretends to be.
`build.py --check` runs them before checking the site. Negative-tested by
mutation when written: disabling longest-match attribution breaks four pass
fixtures, dropping comment stripping breaks one, and dropping H2 from the
scanned surfaces lets five fail fixtures through.

## Redirect check (`build.py --check`, Oct 17, 2026)

Lives in `build.py` (`check_redirects`, `redirect_selftest`), not here, because
it reads the built `public/`. CANON ARCHIVE > REDIRECTS has the principle and
the rules. Every path in `tools/gsc-known-urls-2026-10-17.txt` must be a built
page or a `public/_redirects` source; every internal target must be a built
page (so no chains); no source repeats; status 301 or 302. Fixtures mutate
the real rule set (drop a rule whose source is a known URL, add a chain, a
duplicate, a missing target, a 308) and each must raise exactly its own
problem kind, or the run fails. Negative-tested when written: removing the
`/testimonials` line from `public/_redirects` reports it unresolved, adding
`/old-chain /home 301` reports the chain, and disabling the chain rule in the
checker trips the "add a chain" fixture.

Known drift, recorded so the next run is not surprised: `mkheaders.py` is NOT
a no-op on `pages/headers/how-we-measure-your-progress-header.html`, but since
Oct 16, 2026 only its leading comment differs (the file carries a hand-written
Oct 2 comment; mkheaders writes its Batch 3 template comment). The JSON-LD is
identical. The old 7-vs-6 FAQ "drift" was the method toggle being read as an
FAQ, fixed by marking it `fq fq-method`. Keep the Oct 2 comment if it rewrites.

## Tracking check (`build.py --check`, Oct 17, 2026)

Lives in `build.py` (`check_tracking`, `tracking_selftest`), beside the redirect
check, because it reads the RENDERED output: the site-wide header is the single
source of the GA4 and Clarity loaders, and only `public/` shows what a page
actually ships. CANON MEASUREMENT is the rule.

- **Banned anywhere in `public/`** (every text file, pages and assets alike):
  `GTM-5P4CKPT2`, `ulpgsrkd98`, `AW-16616873404`, `G-QTG1ZLR0NQ` and the
  literal `dataLayer.push`. The last one is why the GA4 shim in
  `pages/headers/site-header.html` holds the data layer in a local
  (`dl.push(arguments)`): it is Google's snippet, spelled so the ban can be
  absolute.
- **At most once per built page:** `G-0K6VLEC2VJ` and `yzawpvwvdf`. A second
  occurrence means a page or header grew its own copy of the loader.
- **Fixtures first**, on mutated copies of the real `public/` text: each banned
  string appended to a page and to `assets/site.js` must raise exactly
  `banned`; a second copy of each live ID appended to a page must raise exactly
  `repeated`; the untouched set must raise nothing; and the first page must
  carry each live ID exactly once. Any fixture that misbehaves is a PROBLEM in
  the report, so a broken checker cannot report green.
- **Negative-tested on the real output** (Oct 17, 2026; restored by rebuild):
  `GTM-5P4CKPT2` in a page comment -> `banned`; a second `G-0K6VLEC2VJ` in a
  page -> `repeated`; `window.dataLayer.push({})` in `site.js` -> `banned`;
  the `repeated` rule disabled inside the checker -> both of its fixtures fail.

## Measurement test (`tools/tracktest.js`, Oct 17, 2026)

Playwright against the built site, served from `public/` on 127.0.0.1 the way
Cloudflare Pages serves it (`/slug` -> `public/slug/index.html`). It needs Node
18+ and the `playwright` package with Chromium (`npm i -g playwright && npx
playwright install chromium`), and is run after `python3 build.py`:

```
NODE_PATH="$(npm root -g)" node tools/tracktest.js
```

What it proves (46 assertions, the table is in REPORT.md):

- The production branch runs on the real hostname: Chromium is launched with
  `--host-resolver-rules` mapping `www.omnifittraining.com` to the local
  server, so `http://www.omnifittraining.com:<port>/` loads gtag.js and Clarity
  with no override. The same mapping for a fake preview host with the override
  proves the flag is ignored off localhost.
- The test-only override `?omnifit-track=prod` forces the production branch on
  `localhost` and `127.0.0.1` only (DEPLOY.md "Measurement").
- Every event in CANON MEASUREMENT fires with its params: Calendly clicks from
  the nav, announcement bar, homepage hero, footer, rates hero, a ladder CTA,
  the Fit Check result and the 4S Ranch sticky bar (position per landmark);
  `tel:` and `mailto:`; HubSpot `onFormSubmitted` (and not `onFormReady` or a
  string message); a full Fit Check to pass (`fit_setting` present) and to hold
  (no `fit_setting`, no answer in any param), plus a retake; the four rates
  sections once each and never twice.
- Clarity never loads on `/fit-check` (production hostname and override alike);
  GA4 still does.
- On a non-production host nothing is requested from googletagmanager.com,
  google-analytics.com or clarity.ms before or after events, `window.gtag` is
  undefined, HubSpot still loads, and each event is one console line
  `[omnifit-track] <event> <json params>`.

**No hit reaches Google or Microsoft.** The request for gtag.js is answered with
a stub that forwards each `gtag('event', ...)` to
`google-analytics.com/g/collect` in GA4's own shape (`en=<event>`,
`ep.<param>=<value>`); requests to google-analytics.com, clarity.ms and the
HubSpot loaders are intercepted and answered locally; fonts, images and every
other external host are blocked. The test therefore proves what the site sends
into gtag and how, not what the GA4 property does with it afterwards.

## Mobile audit (`tools/mobileaudit.js`, Oct 17, 2026)

CANON LAUNCH DECISIONS item 22, committed for the first time in the homepage
rebuild run (the earlier run described its method in REPORT.md but did not
commit the script). Serves `public/` locally and loads each built page (or the
paths given) at 390×900 and 412×900, `isMobile`. Reports `scrollWidth` past the
viewport, grid items / card elements under 240px ("narrow", printed for
review: 2-up tiles and table cells are narrow by design), and content clipped
past the right edge that no scrollable ancestor contains (`<main>` has
`overflow-x:clip`, so `scrollWidth` alone cannot see it). `aria-hidden`
decorative layers are excluded from the clip test: the homepage hero's photo
frames are zoomed 1.2× inside the clipped card on purpose. Exit 1 on any
overflow or clip. `--shots DIR` also saves the homepage hero and In Short
block at both widths.

## Rates restructure run (Oct 17, 2026)

- **`faq.py`: `<summary class="... section-toggle">` is not a question.** The
  rates page (V16) keeps seven sections in `<details>` with the section H2 in
  the `<summary>`. The bare `<summary>` pattern read those as seven questions
  with no answer, which would have broken the FAQPage mirror. The pattern now
  skips a summary whose class carries the `section-toggle` token, and only
  that token (`section-toggled` still reads). `faq.selftest()` runs from
  certify.py on every run and proves both directions: a section toggle yields
  nothing, and FAQ summaries beside it (bare and classed) still pair with
  their answers. Negative-tested: with the old pattern, or without the `\b`,
  the self-test fails. `ownership.py` applies the same exclusion to its FAQ
  read (it only matters for X01).
- **`choosertest.js`** (new) parses the OCTOBER 2026 CARD out of CANON.md, not
  the page's data attributes, then selects all 16 chooser combinations in the
  built page and checks every figure, the offer and the event attributes. It
  also checks the ARIA shape, operates the chooser by keyboard alone, checks
  the no-JavaScript fallback, measures every state at 390 and 412px, and with
  `--shots` saves the three 390px screenshots.
- **`mobileaudit.js --open-details`** opens every `<details>` before
  measuring, so the content of closed sections is audited too.
- **`tracktest.js`** covers `rates_chooser_result` (production and console
  paths), the seven sections closed by default, a jump-bar anchor and a URL
  hash each opening a closed section, and the Foundation CTA inside one.


## Coaching tenure rule (Oct 18 2026)

`coaching_tenure_claim` (stale canon) encodes the owner fact in CANON's ENTITY
BLOCK: Nemezio started coaching in 2016, a hobby before it was his profession,
and copy never claims a number of professional years. It fires on "10+ years",
"over / more than a decade" or "over / more than ten years" in a sentence that
also carries a coaching / experience / helping / training word. Stat badges
flatten to "10+ Years Coaching" and are caught. A sentence naming a partner or
another practitioner (Celeste, Esposito, Serenity, Damien, Jackson-Ricketts,
Stoke, "therapist", "Dr.") passes, so a partner's own experience is not read
as Nemezio's. Self-tested both ways on every run (`_selftest_coaching_tenure`).
Negative test on real copy: run against the files as they stood at e6ddff4,
it reported all nine old claims (about x2, about-header, contactform, 4S Ranch
x2, Rancho Santa Fe, corrective page and header) and nothing on partners.
