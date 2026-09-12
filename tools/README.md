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
| 1 | `guarantee_any` | T1-1 | **changed** — any guarantee, not just one near an outcome word |
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
| — | `clinical_stat` | **RETIRED** | split into 8 (hard ban, force unchanged) and 9 (conditional). Nothing is lost: the population-scope clinical case it existed for is 8. |
| — | dedicated-block disclaimer test | **RETIRED for T2-2** | written to counsel's standard; T2-2 asks only for a same-page disclaimer. Still governs nothing else — T2-1 states its own three conditions. |

### What the tiers changed, rule by rule

- **`guarantee_any` (T1-1).** The old rule required an outcome word within ~30
  words. The DEFERRED-01 replacement wording passes that test *by design* — it
  was written not to pair "guarantee" with an outcome — and Tier 1 bans
  guarantees of any kind. Negation is still read, on the preceding words only,
  so `Reimbursement is not guaranteed` on hsa-fsa stays legal.
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
`pages/home-3.html` is the `case-studies` block pasted into the homepage
(sha256 `c82d5f32…`); certifying both double-counted every finding on it. It is
the only such pair in `pages/` as of Sept 2026.

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
