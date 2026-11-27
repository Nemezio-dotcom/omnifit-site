# Run reports

This file holds the most recent runs, newest last. Everything up to and including the Fascia + Seniors run (43 run sections, 9,160 lines, Territory-Page Propagation of Aug 2026 through Nov 27, 2026) is in `archive/REPORT-through-2026-11-26.md`, byte-identical to how it stood here. A citation of an earlier run by name or item number ("Homepage rebuild run", "item 22", "FST Launch run") points there. The full brief the earlier runs cite is `archive/CANON-full-2026-11-27.md`. Nothing in `archive/` is certified, corrected or read on a run.

# Homepage San Diego run — San Diego section, two FAQ questions, eleven links back to the homepage (owner brief Nov 27, 2026)

Part A of the owner's brief of Nov 27, 2026. **Why:** the homepage owns "personal trainer san diego" (K01), and since the Oct 17 rebuild it carried that phrase on the title and H1 only; every keyword-bearing H2 pointed at North County, 4S Ranch or executive coaching. Search Console shows Google swapping in the in-home page for the query since Oct 20. This run puts San Diego depth back on the homepage without undoing the rebuild.

**Locked and unchanged** (compared on the built page before and after): the title, meta description, H1, canonical, hero, positioning line, In Short list, proof strip, every existing section and all seven existing FAQ answers. The built homepage differs from the previous build only by additions: the new section, two FAQ items, two FAQPage entries, and comments. `/personal-trainer-4s-ranch` and `/personal-trainer-rancho-bernardo` and their headers are untouched (`git diff` empty).

## What changed

| File | Change |
|---|---|
| `pages/home-7.html` (new) | Section `#omh-sd`, label "San Diego", H2 "A San Diego Personal Trainer Who Measures First", lede and three cards, the owner's copy verbatim. Existing `.omh` classes and the home-2 card pattern; no CSS of its own. Icons: `scales`, `pin`, `users` from `site/icons.py`. |
| `build.py` | `home-7` in `HOME_ORDER` directly after `home-1`, in `NOT_PAGES`, and in the docstring. |
| `pages/home-5.html` | Two questions appended after "Is nutrition coaching included?": "Where in San Diego does OmniFit train clients?" and "What should I look for in a personal trainer in San Diego?". Nine questions; the first seven are byte-identical. |
| `pages/headers/home-header.html` | v6. FAQPage regenerated from `pages/home-5.html` with `faq.qa_strict`; the first seven entries came out byte-identical, two were added. WebPage name and description unchanged. |
| `pages/home-motion.html` | Comment only. The shared selectors (`.omh .omh-inner > .omh-label, h2, .omh-lede` and `.omh .omh-grid > .omh-card`) already tag the new section; confirmed in a browser (label, H2, lede and the three cards all receive `omni-rv`). |
| `pages/in-home-personal-trainer-san-diego.html` | One sentence at the end of the first body paragraph after In Short. |
| `pages/private-personal-trainer-san-diego.html` | One sentence at the end of the first body paragraph after In Short. |
| Nine town pages (La Jolla, Del Mar, Carmel Valley, Rancho Santa Fe, Fairbanks Ranch, Encinitas, Solana Beach, Santaluz, Carlsbad) | One sentence, as its own paragraph in the "Meet Nemezio LopezPerez" card, after the bio paragraph. |
| `tools/certify.py`, `DEPLOY.md` | Fragment list reads home-0..7 (comments and the file table). |
| `CANON.md` | home-7 in the fragment list, the nine-question homepage FAQ, header v6. Two short edits; Part B rewrites the file. |
| `public/` | Rebuilt; sitemap lastmod moves to the commit date for the twelve pages touched. |

No heading, title, meta description, FAQ question or JSON-LD changed on any of the eleven linking pages.

## Homepage numbers

| Measure | Before | After |
|---|---|---|
| Visible words in `<main>` (tags, comments, styles and scripts stripped) | 2,098 | 2,518 |
| H1 | 1 | 1 |
| Homepage FAQ questions (page and FAQPage) | 7 | 9 |
| K01 on a homepage H2 | 0 | 1 ("A San Diego Personal Trainer Who Measures First") |
| Body-copy links to `/` with the anchor "personal trainer in San Diego", site-wide | 0 | 11 |

The brief quotes 2,008 words for the Oct 17 rebuild; 2,098 is today's starting point by the same method, because the FST block and the longer coach line were added since. The new copy is 420 words.

## Checks (as they stood before this run; no rule was changed)

| Check | Result |
|---|---|
| `python3 build.py` then `python3 build.py --check` | RESULT: PASSED. Output identical to the pre-run baseline, line for line: no new problem or note on any key. |
| `python3 tools/ownership.py` and `--selftest` | PASSED. K01 now matches a homepage H2. X02 holds: "private" in no homepage title, H1 or H2. No K05-K09 or K20-K31 phrase on a homepage H2 (the H2 matches are K01, K02, K03 and K04, all homepage-owned). |
| `python3 tools/certify.py` | RESULT: PASSED (compliance 0, stale canon 0, structure 0, not-run 0, amendment 0). 102 files certified (101 + `home-7`). All five invariant hashes unchanged, the credentials block included. |
| Home-header FAQPage mirror | Passes with nine questions. Negative test: one word changed in the eighth header answer gave `[FAQPage answers do not mirror page] differing index=[7]` and RESULT: FAILED; restored, PASSED. |
| `python3 tools/mkheaders.py --check` | PASSED (9 headers reproduce byte-for-byte). |
| Rendered `public/index.html` | One H1. The new H2 is inside `<main>`, between the proof strip and "Who It's For". All 17 links in the new copy point at a built page that is not a redirect source (no 404, no hop). No em-dash, no dollar figure and no "private" in the new copy. |
| `node --test tests/assistant.test.mjs`, `tools/widgettest.js`, `tools/choosertest.js`, `tools/tracktest.js` | All pass (4 hand-offs; 30 checks, 16 combinations; 89 assertions). |
| `node tools/mobileaudit.js --open-details` (every page, 390 and 412px) | RESULT: PASSED, no overflow and nothing clipped. |
| `node tools/bandcontrast.js public` | 0 low-contrast text nodes in light bands. |

## Judgment calls (each with the condition under which it is wrong)

1. **"across San Diego County" in the lede stays as written.** CANON says the service area is described as North County San Diego, never "throughout San Diego County". The lede says who the practice is built for, and the second card states the in-home area as North County and the county-wide reach as live video, so no published fact disagrees. `certify.py` passes it (its retired phrases are "training throughout San Diego County" and "available throughout San Diego County"). WRONG IF the owner reads the CANON rule as ruling out any county-wide description; then the lede should say "in San Diego".
2. **The travel-fee sentence is not repeated in the "Where we train" card**, as the brief asked. No certify rule required it there; `home-4` carries it.
3. **Town pages: the sentence is its own paragraph in the Meet Nemezio card, not inside the bio paragraph.** The bio paragraph is the hash-locked credentials block; a sentence inside it would have changed that hash on nine of its eleven carriers. WRONG IF the owner wanted it in the closing section instead.
4. **In-home and private pages: the sentence closes the first body paragraph after In Short.** For the private page, "the opening section" was read as the first body section, not the hero. WRONG IF the owner meant the hero subhead.
5. **The eleven links carry each page's existing link style.** Those paragraphs had no link rule, so the anchor rendered in browser-default blue. In-home and private use the pages' own `.of-link` class; the town pages use an inline style with the same declarations as their FAQ links (gold, underlined). No stylesheet rule was added. WRONG IF the owner wants unstyled anchors.
6. **No selector was added to the reveal layer.** The section is animated the same way the other `.omh` sections are, through the shared selectors. WRONG IF a section-specific effect was wanted.

# CANON slim-down — CANON.md cut to facts, owner rules and workflow; the rest archived (owner brief Nov 27, 2026)

Part B of the owner's brief of Nov 27, 2026. No page copy changed: `public/` is byte-identical to the build that shipped with the Homepage San Diego run.

## Size

| | Lines | Bytes |
|---|---|---|
| CANON.md before (as it stood after Part A; 3,051 before Part A's nine added lines) | 3,060 | 206,135 |
| CANON.md now | 826 | 80,132 |
| `archive/CANON-full-2026-11-27.md` (byte-identical copy of the "before" file, `cmp` clean) | 3,060 | 206,135 |

634 of the 826 lines are byte-identical blocks of the archive (the six blocks listed under gate 6). **Read this before taking 826 at face value:** in the 192 lines that were rewritten, each fact or rule is one line, not hard-wrapped, and 99 of them are longer than 100 characters (the longest, the pricing FAQ answer, is 1,209). Wrapped at 100 columns the same file is 1,146 lines; at the old file's 78 columns, 1,276. The byte count is the honest measure of what a run now reads: 61% less.

## What moved to the archive, by section

| Section of the full brief | Lines | In the new CANON |
|---|---|---|
| CANONICAL FACTS, consultation to HSA / FSA | 64 | Kept, byte-identical (60 lines; the 4-line header rewritten) |
| CANONICAL FACTS > FASCIA STRETCH THERAPY | 282 | Kept, byte-identical, except the founders landing page's layout notes (70 lines: hero image dimensions, crops, phone layout, sticky bar styling, share image build, Meta tracking narrative), cut to 11 lines of copy rules |
| REPO STATE (certified list, not-yet-certified, ORPHAN HEADERS, DUPLICATE RULE) | 269 | Archived. Carried as single lines: the FST page facts, the badge rules, "the business is defined once in site-header.html", the homepage title and H1, "the partner section states no prices" |
| ARCHIVE | 26 | One WORKFLOW line: archive/ is never certified, corrected or brought back |
| REDIRECTS (principle, the check, the 74 rules) | 120 | One line under SITE FACTS: the list lives in `build.py` REDIRECTS |
| MEASUREMENT | 208 | IDs, the production-only rule, what Meta receives, the key event names. Parameters and manual steps are in DEPLOY.md "Measurement" |
| ASK OMNIFIT | 100 | The essentials: the knowledge file is the only source and must agree with CANON, the prompt is the owner's wording, the spend cap, the Pacific Beach not-served line verbatim |
| WORKFLOW RULES | 39 | Rewritten as WORKFLOW, with the owner's new SEARCH SAFETY rule verbatim. The CONTRACT VALUE CHECK is one line under the card's TERMS |
| CANONICAL TRUTH (brand, NAP, reviews, credentials) | 24 | BUSINESS AND ENTITY |
| PRICING — OCTOBER 2026 CARD | 160 | Kept: every table row byte-identical, every locked sentence verbatim; run history removed. Two sentences added so the checks can read them (see "Hash locks") |
| LEGACY PRICING | 33 | One paragraph: closed, existing clients only, never published, figures in the archive |
| Case-study figures, DEVICE, Retired forever | 38 | Carried, one line each |
| ACCOUNTABILITY DIAL | 45 | Names, order and locked sentences |
| THE OMNIFIT METHOD (incl. the Travel Protocol) | 64 | Names, order and locked sentences |
| ENTITY BLOCK | 104 | BUSINESS AND ENTITY: the description, founder bio, entity line and positioning line verbatim |
| LANGUAGE RULES | 41 | Kept |
| STRETCH TO WIN MARKETING RULES | 88 | Kept whole, byte-identical |
| TIER CHANGES | 46 | Kept: the rules, the published copy verbatim, the worked example's figures |
| LAUNCH DECISIONS (22 items, RETIRED LAUNCH COPY) | 206 | One line per decision that still governs copy (OTHER DECISIONS, the card, BUSINESS AND ENTITY); the retired phrases as one line under STANDING COPY RULES |
| COMPLIANCE SCREEN, TIER 1 and TIER 2 | 186 | Kept whole, byte-identical |
| CARRIED OVER, NOT RE-TIERED | 10 | One line |
| EM-DASH RULES | 7 | One line under STANDING COPY RULES |
| CERTIFICATION (a) (b) (c) rule descriptions | 238 | Archived (how the checker works; `tools/README.md` documents it). WORKFLOW keeps "exactly three categories" |
| PAGE HEADER SHAPE | 8 | Archived; rule removed |
| PAGES WITH NO FAQ | 22 | Archived; rule removed |
| KEYWORD OWNERSHIP (rules, table, changelog) | 229 | A guideline: one paragraph, the X rules in one, and the table byte-identical |
| INVARIANTS | 103 | Archived; hash locks removed |
| BEFORE CANCELLING SQUARESPACE | 40 | Archived (DEPLOY.md keeps its manual step; `build.py --check` still warns per image) |
| THE JOURNAL | 19 | One WORKFLOW line |
| KNOWN DEFERRED / RESOLVED ITEMS, PRICING-CHANGE CHECKLIST | 89 | Archived |
| NEXT RUNS | 72 | Archived. One fact carried: never add ratings through Product or ItemList markup |
| CHANGE LOG | 78 | Archived |

## Rules removed or downgraded (each with its reason)

| Rule | Was | Now | Reason |
|---|---|---|---|
| Keyword ownership: owned phrase on a non-owner title, H1, H2 or meta; X01; X02; table unreadable; owner page not built | PROBLEM, failed `build.py --check` | WARNING, never fails | Owner decision: a guideline |
| Keyword ownership "cover" (owner page must carry the in-home variant) | PROBLEM | WARNING | Same decision, named in the brief |
| Ownership fixture misbehaving | PROBLEM | WARNING (`ownership.py --selftest` alone still exits 1) | A guideline's tool cannot block a run |
| `[invariant mismatch]` and `[canon hash stale]` for the five hashes (page pricing, header pricing, credentials, archetypes, 9-point) | structure finding | removed | Owner decision: no hash locks on wording. Three plain checks replace the part that guarded prices and credentials (below) |
| Archetype card bodies byte-identical on 11 pages | hash-locked | free | Wording only: no price, policy or credential in it |
| 9-point screen items and closing line byte-identical on 11 pages | hash-locked | free | Wording only (its one price sentence is still checked) |
| Meet Nemezio bio outside the credentials sentence | hash-locked | free | Wording only |
| Assistant system prompt sha256 | stale-canon finding | removed | Named in the brief. The prompt carries no price; it is still screened for compliance, stale canon and the FST mark |
| `[LocalBusiness redefined]`, `[site-header LocalBusiness must carry @id #localbusiness-of]`, `[about not referencing homepage LocalBusiness]` | structure finding | removed | PAGE HEADER SHAPE left CANON |
| `[no ld+json block]` in a header | structure finding | removed as its own finding | Header shape. A page FAQ with no FAQPage still fails the mirror |
| "bare node, not an @graph document" and "no WebPage node" | check-could-not-run (INCOMPLETE) | removed | Header shape |
| `[declared no-FAQ page carries FAQ markup]` and the `NO_FAQ` list | structure finding | removed | PAGES WITH NO FAQ left CANON. A readable FAQ without a FAQPage still fails the mirror; FAQ-shaped markup that cannot be read still gives INCOMPLETE; a page with no FAQ on either side is no longer anything |

**Not removed.** All 19 self-tests that ran before still run (one added). The compliance rule list is unchanged. Every TIER 1 and TIER 2 rule, every Stretch to Win rule, the FAQPage mirror (count, order, text), invalid JSON, tag balance, placeholder copy, the pricing FAQ carrier list, `[no matching page]`, and in `build.py --check` links, one H1, no nested `index.html`, redirects and tracking are as they were. The FST badge keeps its sha256: it pins an image file, not wording, and lives beside its test in `certify.py`.

**Made stricter, once.** The negative test for gate 5 wrote "Clients rate us 5.0 stars." on a page and certify said nothing, before Part B as well as after: the retired phrases were "Rated 5.0", "5.0 rating" and "5.0 · 190+". `"5.0 star"` and `"5.0-star"` joined `RETIRED_LAUNCH_COPY` (48 phrases, each self-tested). No published page contains either.

## Hash locks replaced by plain checks

The hash was the only guard on three published price or credential sentences, so each is now written out in CANON.md and compared as text (tags dropped, entities decoded, whitespace collapsed):

| CANON label | Replaces | Carriers | Check |
|---|---|---|---|
| CANONICAL PRICING FAQ ANSWER | page pricing and header pricing hashes | 24 files: the page FAQ and header FAQPage of the twelve carriers | the answer must be CANON's sentence |
| CREDENTIALS SENTENCE ("He holds fourteen certifications ...") | credentials hash | 11 pages | the Meet Nemezio block must contain it |
| 9-POINT SCREEN ASSESSMENT SENTENCE ("... the $150 Performance Assessment, credited toward your first cycle.") | 9-point hash | 11 pages | the section's intro must contain it |

A label that is missing, doubled or unquoted in CANON gives RESULT: INCOMPLETE, never PASSED. Negative tests on a scratch copy, each restored afterwards: "fourteen" changed to "thirteen" on one page, the assessment price changed to $160 on one page, and a price changed in one header each failed on their own check; a renamed CANON label gave INCOMPLETE; a price changed in CANON itself failed all 24 carriers.

## Parsers changed

| Tool | What it reads from CANON | Change | Proof |
|---|---|---|---|
| `tools/certify.py` `_canon_card_numbers` (knowledge-file price check) | every figure in CANONICAL FACTS and the OCTOBER 2026 CARD | The first block now ends at STRETCH TO WIN MARKETING RULES (it ended at REPO STATE). The card block is found as before | `_selftest_assistant` passes ($640, $1,680 and $119 allowed; $475 and $1,050 refused). The set of allowed figures went from 93 to 72 and every one of the 72 was allowed before, so the check is no looser |
| `tools/certify.py` `canon_hashes` | the INVARIANTS block | Removed. `canon_sentences` reads the three labelled sentences instead | `_selftest_canon_sentences`, both ways, every run |
| `tools/ownership.py` | the OWNERSHIP TABLE | Table byte-identical, parser unchanged. Findings are warnings; exit code is 0. Fixture folder `fail/` renamed `warn/` | `--selftest`: 20 warn fixtures warn, 13 pass fixtures are quiet, a site built from the warn fixtures draws 66 WARNING lines with exit code 0, and an unreadable table is a warning with exit code 0 |
| `build.py` | CANON through `ownership.py` only | Ownership findings go to the WARNING list, never to problems | A keyword phrase put on a non-owner H2 in a scratch build: `build.py --check` printed the WARNING, RESULT: PASSED, exit 0 with `--strict` |
| `tools/choosertest.js` | the card tables and four figures by pattern | None needed: the rows and the lines it matches are byte-identical | RESULT: PASSED (30 checks, 16 combinations) |

References to sections that no longer exist were re-pointed in `tools/certify.py`, `build.py`, `tools/ownership.py`, `tools/README.md` (its Invariants, no-FAQ, keyword ownership and not-run sections were rewritten to say what the tools do now), `DEPLOY.md`, `editorial/PLAYBOOK.md` and `tools/mobileaudit.js`. `assistant/knowledge.md` refers only to CANON.md and to checks that still exist, so it is unchanged. **Left as they are, on purpose:** the comment line "(LAUNCH DECISIONS item 1)" that `build.py` writes into `public/_redirects`, and the comments inside `pages/` and `site/` that name old sections. They are part of the built site, and Part B may not change `public/`.

## Gates

| # | Gate | Result |
|---|---|---|
| 1 | `public/` byte-identical to `public/` after Part A | PASS. `diff -r` against the snapshot taken after Part A: no difference. `git diff main -- public` is empty. `functions/_lib/knowledge.js` is unchanged too |
| 2 | `build.py --check` exits clean; ownership prints warnings only | PASS. RESULT: PASSED, 0 problems; "keyword ownership (guideline): no warnings" on the real site |
| 3 | `certify.py` runs to the end with zero findings and its self-tests pass | PASS. RESULT: PASSED (compliance 0, stale canon 0, structure 0, not-run 0, amendment 0). 20 self-tests ran, each asserting both directions |
| 4 | Node tests | PASS. `tests/assistant.test.mjs`, `tools/widgettest.js` (4 hand-offs), `tools/choosertest.js` (30 checks, 16 combinations), `tools/tracktest.js` (89 assertions) |
| 5 | Negative test, run then reverted | PASS, with the fix above. On a scratch copy of the La Jolla page: "5.0 stars" gave `[retired launch copy: 5.0 star]`; "Guaranteed results: you will lose 20 lbs." gave `[outcome guarantee (T1-1)]`; the Program price changed from $640 to $660 gave `[pricing FAQ answer does not match CANON]` and the mirror finding. RESULT: FAILED (1, 1, 2). The same test on `main` before Part B caught the guarantee and the price but not "5.0 stars" |
| 6 | Every dollar figure and locked sentence of the old rate card and policies is in the new CANON | PASS. 17 of 17 dollar figures and 31 of 31 table figures. 80 of 88 quoted strings of 25 characters or more; the other 8 are retired wording or labels the old brief quoted in passing, listed below |
| 7 | New CANON.md under 900 lines | PASS at 826 lines, on the format disclosed under "Size". No fact or owner rule was dropped to get there |

The 8 quoted strings not carried, all deliberately: ", so you can compare the two yourself" (the cut tail of the founders sub); "Every client starts with a $150 Performance Assessment" (replaced Oct 18 2026); "Monthly Tune-Up: 199/250/295" (the August card); "No travel fee inside our in-home service area; a travel fee may apply outside it." (retired Oct 18 2026; its tail is on the retired phrases list); "a clinical-grade diagnostic session" (replaced); "fully refundable $30 deposit" (replaced; "fully refundable" is on the retired list); "Data-Driven Hybrid Coaching" and "The assessment is credited" (names of a card and a policy line, not rules).

## Needs the owner

Nothing. Both items that stood here (the "ACE CES" line of the brief, and the line count) were decided by the owner on Nov 27, 2026 and are recorded in the Wrap-up run below, with the seven judgment calls that follow.

## Judgment calls (each with the condition under which it is wrong)

1. **One fact per line in the rewritten sections.** The brief asks three times for "one line"; the verbatim blocks keep their original wrapping. WRONG IF the owner wants wrapped text throughout (see "Needs the owner", 2).
2. **Founders landing page layout notes cut from the FST facts** (image dimensions, crop positions, phone layout, sticky bar styling, how the share image is built). The brief says FST facts stay verbatim and also that per-page version notes leave. Every rule about the page's copy stayed: the hero copy, the alt text, "the image is AI-generated", the second "$99" beside "founders", no price or date on the share image. WRONG IF the owner counts the layout notes as FST facts; they are in the archive, lines 249 to 318.
3. **STRETCH TO WIN MARKETING RULES kept whole**, including its description of what certify enforces, although descriptions of checkers leave everywhere else. The brief says verbatim for this section. WRONG IF the owner wants the ENFORCED list out (41 lines).
4. **`[no ld+json block]` and `[no matching page]`.** The first was treated as header shape and removed; the second was kept, because a header that cannot find its page is a mirror that was never checked. WRONG IF the owner reads REPO STATE's orphan-header rule as retired too.
5. **The pricing FAQ answer is written into CANON in full** (the hash was the only guard on about twenty figures in one sentence). A lighter check, each figure against the card, would have let a studio price sit in the in-home clause. WRONG IF the owner wants that sentence free to be reworded page by page.
6. **The credentials sentence is checked, not the whole bio.** WRONG IF the owner wanted the Meet Nemezio block entirely free; then the credentials count on those eleven pages has no guard.
7. **Two phrases added to the retired list** ("5.0 star", "5.0-star"). It is the one place Part B makes certify stricter. WRONG IF the owner wants no rule added in a run that removes rules; then gate 5 fails on "5.0 stars", as it would have before this run.

# Wrap-up run — owner decisions recorded, run report archived, SEARCH SAFETY made visible (owner brief Nov 27, 2026)

Closes out the Homepage San Diego run and the CANON slim-down. **This run changed no page.** Nothing in `pages/` or `site/` was touched, no redirect changed, and `public/` is byte-identical to main, sitemap included (`git diff main -- public pages site functions` is empty). Search Console is rechecked on Dec 11; nothing a search engine reads moved.

## 1. Owner decisions on the slim-down's open items (Nov 27, 2026)

| Item | Decision |
|---|---|
| Line count | 826 stands (827 with this run's one line). One fact per line stays; no re-wrapping. |
| "ACE CES" | Stays published exactly as it is on the 20 pages. The brief's "ACE CES out of site copy" line was stale. CANON's existing rule, banning "ACE OES" and "Orthopedic Exercise", is the right one. No page change, no new rule. |
| Judgment calls 1 to 7 of the slim-down report | Accepted as made. |
| Part A, town pages | The sentence stays its own paragraph in the Meet Nemezio card. |
| Part A, the eleven links | They keep each page's gold link style. |

The "Needs the owner" list in the slim-down section above is cleared.

## 2. Run report archived

| | Lines |
|---|---|
| REPORT.md before | 9,343 |
| Moved to `archive/REPORT-through-2026-11-26.md` (everything above "# Homepage San Diego run": 43 run sections) | 9,160 |
| REPORT.md now (a short header, the Homepage San Diego run, the CANON slim-down, this run) | 282 |

Proof: `cmp` of the archive against lines 1 to 9,160 of REPORT.md on main reports no difference, and the archive followed by the kept sections is the old file byte for byte.

Citations re-pointed to the archive: eight in `tools/README.md` (the Oct 17 findings list, the measurement tables, the mobile audit method, the FST Launch and FST Reach negative tests, the founders hero figures, the Meta Pixel negative tests), one in `DEPLOY.md` (the measurement results table) and one in `tools/mobileaudit.js` ("item 22"). Nothing in `build.py` or `editorial/` cited an archived section.

CANON's WORKFLOW block gained one line: "REPORT.md holds the five most recent runs. At the start of a run, older sections move byte-identical to archive/REPORT-<through date>.md." REPORT.md holds three today; five is the cap.

Left as they are, and why:
- `pages/home-1.html` has a comment citing REPORT.md, "Homepage rebuild run". It is inside `pages/` and is carried into `public/`.
- CANON's Stretch to Win block cites "REPORT.md FST Launch run". CANON could gain one line and lose none. Its opening paragraph already says that such citations point into the archive.
- `tools/choosertest.js` and `tools/ownership.py` mention REPORT.md as the place a run writes to, not a section of it.

## 3. SEARCH SAFETY made visible

New: `tools/searchsafety.py`, run by `python3 build.py --check` (and by `python3 build.py`). It compares each built page with the same file on origin/main and prints a WARNING, never a failure, when the visible copy inside `<main>` shrinks by more than a quarter, the `<title>` or the H1 changes, or a KEYWORD OWNERSHIP phrase that was on one of the page's headings on main is on none of them now. Each warning names the page, the before and the after, and ends "name this change and its ranking risk in the brief (CANON SEARCH SAFETY)". Nothing it finds is added to the check's problems; with `--strict` the exit code is still 0.

On the real site today: 49 built pages compared with origin/main, 1 not compared (the founders landing page, noindex), no warnings.

**Self-test** (runs inside `build.py --check` first, and its result is printed): nine fixture pairs in `tools/fixtures/searchsafety/`.

| Fixture | Result |
|---|---|
| a page cut from 2,000 to 1,400 words | warns |
| cut from 2,000 to 1,600 | quiet |
| cut from 2,000 to 1,500 (exactly a quarter) | quiet |
| grown from 2,000 to 2,400 | quiet |
| changed H1 | warns |
| changed title | warns |
| keyword phrase taken off the headings | warns |
| keyword phrase moved from one heading to another | quiet |
| unchanged page | quiet |

The self-test counts the words in the copy fixtures against their names, checks every warning ends with the sentence above, and proves that a new page is a note, that a missing origin/main is one note, and that a warning leaves the exit code at 0.

**Replay** (the homepage built at the last commit of Oct 16, 2026, `9bbf8a4`, as "main"; the homepage built at `05fdafe`, Oct 18, 2026, as the build). It fires on the copy cut:

```
  WARNING  /: visible copy inside <main> went from 6,431 to 2,023 words (69% removed, more than a quarter); name this change and its ranking risk in the brief (CANON SEARCH SAFETY)
SEARCH SAFETY: 1 warning(s); nothing fails
```

It printed that one warning and no other. The title and the H1 were the same on both days. The keyword warning did not fire: the rebuild took "personal trainer San Diego" off the H2s, but the H1 still carried it, so the phrase never left the page's headings (see judgment call 3). The rebuild run's own table counted 6,849 and 2,008 words by source fragment; this check counts everything inside `<main>` of the built page.

**Through `build.py`, on a scratch copy of the repo, then discarded:** a page cut to 39% of its copy, a changed H1, a changed title, a keyword phrase removed from the homepage's headings and one new page gave four WARNING lines and one note, RESULT: PASSED, exit 0 with `--strict`.

## 4. Left alone

`tools/README.md`, `DEPLOY.md` and `tools/certify.py` apart from the re-pointing above (`certify.py` needed none). The two squarespace-cdn.com badge images on /about: `build.py --check` still prints its two warnings. Every redirect.

## Gates

| # | Gate | Result |
|---|---|---|
| 1 | `public/` byte-identical to main | PASS. `git diff main -- public` is empty after a full rebuild; `pages/`, `site/` and `functions/` are untouched too |
| 2 | `python3 build.py --check` | PASS. RESULT: PASSED. It prints "search safety: self-test passed (9 fixture cases: a 2,000 to 1,400 word cut, a changed title, a changed H1 and a keyword phrase off the headings each warn; 2,000 to 1,600 does not)" |
| 3 | `tools/certify.py` | PASS. RESULT: PASSED (0, 0, 0, not-run 0); its 20 self-tests ran |
| 4 | Node tests | PASS. `tests/assistant.test.mjs`; `tools/widgettest.js` (4 hand-offs); `tools/choosertest.js` (30 checks, 16 combinations); `tools/tracktest.js` (89 assertions) |
| 5 | The report archive is byte-identical to the lines it replaced | PASS (`cmp`, 9,160 lines) |
| 6 | CANON.md gained one line and lost none | PASS. `git diff --numstat`: 1 added, 0 removed. 827 lines |

## Needs the owner

1. **`tools/README.md` does not describe the new check.** The brief says to leave that file alone, and CANON says it documents every check. The check is documented in the module itself and in `build.py`'s header. A short README entry belongs in the next run that may touch the file.

## Judgment calls (each with the condition under which it is wrong)

1. **A page that was on main and is not built any more also warns.** The brief names three conditions; a deleted page is the largest copy cut there is. WRONG IF the owner wants exactly three.
2. **A page that is noindex on main is not compared** (today, the founders landing page). The rule speaks of an indexed page. WRONG IF ad landing pages should be watched too.
3. **"On the page's headings" means any heading, H1 to H6.** So a phrase that leaves the H2s but stays on the H1, which is what happened to the homepage in October, does not draw the keyword warning; the copy cut drew its own. WRONG IF the owner wants a warning whenever a phrase is on fewer heading levels than before.
4. **Exactly a quarter does not warn.** The rule says more than a quarter.
5. **The check does not fetch.** It compares with the origin/main the checkout already has and prints that commit and its date, so an old reference is visible. A run that starts by fetching main, as runs do, compares with the live site. WRONG IF the owner wants the check to go to the network itself.
6. **The replay needed history this checkout did not have** (it was a shallow copy that began on Oct 18). The local copy was deepened to Oct 1 to read the Oct 16 build. Nothing in the repository changed.
