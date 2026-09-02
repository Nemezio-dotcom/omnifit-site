# Certification tooling

Run from the repo root. These encode CANON.md. **Use them; do not rebuild the
rules from scratch.** If a rule is wrong, fix it here and update CANON.md so the
two stay in step.

```
python3 tools/certify.py     # the three-category certification
python3 tools/mkheaders.py   # regenerate the Batch 3 page headers
```

`certify.py` reports exactly three categories — (a) compliance strikes,
(b) stale canon, (c) broken structure — then the five invariant hashes, then
the checks that could not run, then `PASSED` / `FAILED` / `INCOMPLETE`.
Anything else is a judgment call for a human, not a certification finding.
`INCOMPLETE` means no findings but at least one check was not applied; it is
never reported as a pass.

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

## Compliance rules (a)

- **outcome guarantees** — "guarantee" within ~30 words of an outcome promise.
- **lbs near a timeframe** — a pounds figure within ~15 words of a *quantified*
  window. Bare duration nouns ("after years of inactivity") do not count. A
  timeframe preceded within two words by a contrastive marker ("unlike 6-week
  challenges") is exempt, but every other timeframe in the window is still
  checked, so `Lose 20-30 lbs in 6 months, not a 6-week challenge` still flags.
- **free-framing** — "free" within ~6 words of any bookable first session:
  consultation · assessment · screen · screening · session · diagnostic ·
  call · intake. Widened Aug 2026 after the literal `consultation`-only version
  passed `free 45-minute assessment`. Two exemptions, both tested: `feel free`
  (idiom, only when "feel" immediately precedes) and hyphenated compound
  adjectives (`distraction-free`, `injury-free`, `pain-free`) — a real offer is
  written unhyphenated.
- **prenatal / postpartum** — exempt when attributed to a partner via
  `knowsAbout` markup, or inside an explicit out-of-scope disclaimer.
- **uncertified specialty claims** — asserting OmniFit diagnoses, treats,
  prescribes, cures, rehabilitates, or provides physical therapy or
  chiropractic. Negations and referral language are legal. Note `\b` boundaries
  on the negation list: without them, a bare `no` matched inside "diag**no**se"
  and exempted every genuine claim — a rule failing open.
- **quantified clinical outcome statistics** — a percentage attached to a
  clinical result (pain, injury, recovery, healing, rehab, range of motion)
  *with* an outcome framing (reduced, improved, relief…). Behavioural and
  business stats are not clinical and stay: adherence, compliance, rating,
  reviews. Process statements ("100% of clients get an injury screen") lack the
  outcome framing and pass.
- **results promised within a window** — the general case of the lbs rule, in
  any units. Results must be framed against the client's own baseline, never a
  calendar. Negation is checked on the **preceding** words only, so a trailing
  "…and we don't cut corners" cannot exempt a real promise.
- **DOCUMENTED CASE-STUDY EXCEPTION** (Andrew Flores, Sept 2026) — the only
  exemption on `lbs_near_timeframe` and `result_near_timeframe`. CANON's
  CANONICAL TRUTH recorded documented client figures *with* timeframes as
  canonical fact while the compliance screen banned that shape outright; both
  could not hold. An attributed, documented individual outcome is a fact about
  a named person; a claim about what a prospective client can expect is a
  projection, and only the projection is what the rule prevents.
  Three gates, all in `_case_study_exempt()`:
  1. **attribution** — a named client beside a role noun (`Mark ·`,
     `Annie, a registered nurse`, `Dave Rendo, owner of…`), or an explicit
     anonymisation *with a stated profile* (`Anonymized client · Male, 29`).
     Bare "anonymized client" is not enough. The role noun is required: without
     it, `San Diego, lost 27 pounds` would read as an attribution and condition
     1 would be decorative.
  2. **page disclaimer** — `_has_results_disclaimer()` requires the phrase
     "individual result(s)" *plus* a variation clause (vary / depend / not a
     projection) within 40 words. **Keyed off the disclaimer text on the page,
     never off the filename** — that is what makes condition 2 enforceable.
     The same figure on a page without the disclaimer is still a strike.
  3. **not aggregate** — `typical`, `average`, `most clients`, `you can expect`
     and friends within the window are never exempt, on any page.
  Condition 3 of CANON's exception (substantiation on file) is not
  machine-checkable and remains a human warranty.
  Fails **closed**: anything the attribution test cannot confirm stays a strike.
  Negative-tested in all four required directions plus four more — see the
  Sept 2026 entry in REPORT.md.

## Stale-canon rules (b)

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

## Invariants

Five, all recomputed from the files each run and compared against the hashes
recorded in CANON.md: page pricing, header pricing, credentials, archetypes,
9-point screen. A mismatch is a category (c) finding. All five are now
**printed every run**, not only on mismatch, and an invariant that matched no
file at all is reported as not-verified rather than silently absent.

The credentials block is 630 bytes across 10 pages. Editing it means editing all
ten and updating the hash in CANON.md in the same commit.

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
