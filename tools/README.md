# Certification tooling

Run from the repo root. These encode CANON.md. **Use them; do not rebuild the
rules from scratch.** If a rule is wrong, fix it here and update CANON.md so the
two stay in step.

```
python3 tools/certify.py     # the three-category certification
python3 tools/mkheaders.py   # regenerate the Batch 3 page headers
```

`certify.py` reports exactly three categories — (a) compliance strikes,
(b) stale canon, (c) broken structure — and exits after printing PASSED/FAILED.
Anything else is a judgment call for a human, not a certification finding.

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

Before trusting a new rule, negative-test it in **both** directions: confirm it
flags a real violation, and confirm it passes the legitimate copy next to it.
Rules that *narrow* scope are the dangerous ones — every exemption below carries
a fixture proving a real violation in the same shape still flags.

## FAQ extraction (`faq.py`)

Pages use six different answer-container patterns. Missing one does not raise —
it silently yields a question with no answer, which is how the `null` overwrite
happened.

Question containers:

- `<summary>…</summary>`
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

## Invariants

Five, all recomputed from the files each run and compared against the hashes
recorded in CANON.md: page pricing, header pricing, credentials, archetypes,
9-point screen. A mismatch is a category (c) finding.

The credentials block is 630 bytes across 10 pages. Editing it means editing all
ten and updating the hash in CANON.md in the same commit.

## Scope

`certify.py` skips `training-rates-san-diego`, `the-30-minute-executive-reset`
and `footer` (see CANON REPO STATE). Everything else under `pages/` is in scope.
There is an assertion that the glob matched a non-zero number of files — an
earlier run passed vacuously because it was executed from the wrong directory
and matched nothing.
