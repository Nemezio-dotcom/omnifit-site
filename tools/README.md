# Certification tooling

Run from the repo root. These encode CANON.md. **Use them; do not rebuild the
rules from scratch.** If a rule is wrong, fix it here and update CANON.md so the
two stay in step.

```
python3 tools/certify.py         # the three-category certification
python3 tools/mkheaders.py       # regenerate the Batch 3 page headers
python3 tools/negative_tests.py  # both-directions tests for every exemption
```

`certify.py` reports exactly three categories — (a) compliance strikes,
(b) stale canon, (c) broken structure — and exits after printing PASSED/FAILED.
Anything else is a judgment call for a human, not a certification finding.

## Why this exists

Six separate checks have now reported success while not actually looking at the
thing they claimed to check. Each is now closed by something in this directory.
The pattern is the point: **a green result means nothing until you have seen the
check fail on purpose.**

| Incident | What it reported | What was true |
|---|---|---|
| Header regression | "every header mirrors its page" | It compared **questions only**, never answers |
| Header re-mirror | 7 answers "re-mirrored" | It wrote `null` over all 7, destroying the canonical pricing block |
| Free-framing rule | how-we-measure certified clean | Page said `free 45-minute assessment`; rule only knew `consultation` |
| Session-pack rule | CANON authorised `10 @ $150` as a pack rung | $150 belonged to neither venue's ladder — a mangled merge of the studio and in-home figures |
| Header structure check | ran on every header under `pages/` | it read only the FIRST `ld+json` block and assumed an `@graph` with a `WebPage` node; the first hand-built header it met raised `KeyError: 'WebPage'` and the whole section reported nothing |
| FAQ question extraction | hsa-fsa "has no FAQ" | `<summary>` was matched bare, so `<summary class="hsa-faq-q">` yielded ZERO of its nine questions |

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

Pages use six different answer-container patterns. Missing one does not raise —
it silently yields a question with no answer, which is how the `null` overwrite
happened.

Question containers:

- `<summary …>…</summary>` — attributes allowed; the bare-tag-only version
  returned zero questions for `hsa-fsa-personal-training`
- `<div class="…faq-q">…</div>`
- `<button class="fq" …>…<span`
- `<div class="faq-question">…</div>` — omnifit-vs-competitors
- `<button class="op-faq-q" …>…<svg` — partners

Answer containers:

1. `<div class="…faq-a" …>…</div>`
2. `<div class="fa"><p>…</p></div>`
3. `<div class="faq-answer">…</div></div>`
4. `<div class="op-faq-a-inner">…</div>`
5. `<div class="…faq-body" …>…</div></details>` — **the territory pages**, the
   one that was missing
6. (questions and answers are paired by document position, so a new question
   pattern needs its answer pattern added at the same time)

`qa()` returns ordered `(question, answer)` pairs. `qa_strict()` is the same but
**asserts no answer is None** — use it anywhere the result gets written to a
file. `questions()` returns questions only.

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
9-point screen. A mismatch is a category (c) finding.

The credentials block is 630 bytes across 10 pages. Editing it means editing all
ten and updating the hash in CANON.md in the same commit.

## Scope

`certify.py` skips `the-30-minute-executive-reset`, `footer` and
`llms-txt-page-retired` (see CANON REPO STATE). `training-rates-san-diego` entered scope in the Rates Page
Correction run (Aug 2026) once its content certified; the naming fix (its
header lacked the `-header.html` suffix) was applied *after* content passed,
per CANON's naming-fix rule — doing it first would have hidden a real
structural check behind a filename mismatch instead of a genuine pass.
Everything else under `pages/` is in scope. `archive/` is not under `pages/`,
so the retired pages are out of scope by construction rather than by an
exemption list — nothing there can be reached by widening a rule.
There is an assertion that the glob matched a non-zero number of files — an
earlier run passed vacuously because it was executed from the wrong directory
and matched nothing.

## Structural exceptions (Ingest Consolidation run, Aug 2026)

These are facts about how the site is built, not tolerated violations. Each has
a fixture in `negative_tests.py` proving the check it exempts still fires.

- `KNOWN_ORPHAN_HEADERS` — `bodybuilding`, `energy-protocol-waitlist-form`. Their
  pages are Squarespace blocks with no Code Block to retrieve, so no
  `pages/<slug>.html` will ever exist. Noted, never flagged, never deleted. A
  header with a genuinely missing page still reports `[no matching page]`.
- `BODY_EMBEDDED_SCHEMA` — `case-studies`, `home-3` carry their JSON-LD in the
  body and have no header. An unexempted headerless page still reports
  `[no header file]`. The two files are byte-identical, so their findings
  double-count by design.
- `HEADER_PAGES` — the homepage is five Code Blocks, `home-1`…`home-5`, sharing
  `home-header.html`. The map points the mirror check at all five bodies
  concatenated; it does **not** switch the check off, and the check currently
  reports the homepage FAQ (11 questions) as absent from that header's schema.
- `LOCALBUSINESS_DEFINER` — the homepage header is where `LocalBusiness` is
  defined. CANON (c) bans *re*definition, which still flags in any other header.
- `WEBPAGE_TYPES` / `ld_nodes()` — every `ld+json` block is read, `@graph` or
  bare object, and the `about` reference is only checked where a WebPage-shaped
  node exists. Inventing a finding for a header that carries only a `Service`
  node would be a new rule, not this one. Invalid JSON in *any* block flags.

## Accepted exceptions

`ACCEPTED` entries are matched on slug **and** rule kind **and** an exact phrase
in the surrounding flattened text. All three must match, so an exemption cannot
swallow a different violation of the same shape on the same page — there is a
fixture for exactly that. The two hsa-fsa entries are currently **dormant**:
neither fires under the rules as they stand. They are recorded so a future
widening cannot re-flag settled copy, not because they are suppressing anything
today.

## file:line on compliance findings

Compliance rules run on flattened text, which has no line numbers. `_flatmap()`
returns that same flattened text plus a source offset per character; `run()`
asserts it is byte-identical to `_flat()` on every file, every run. If the two
ever drift the assertion fires rather than the report quietly pointing at lines
the rule never looked at.
