# Territory-Page Propagation Run — Report

**Branch:** `claude/omnfit-4s-ranch-location-mxek1x`
**Reference page:** `pages/personal-trainer-4s-ranch.html`
**Scope:** propagate the 4S Ranch canonical patch set to the territory pages, generate per-page JSON-LD headers, and certify the repo.

> **Nine pages were requested; eight exist.** `rancho-santa-fe` is not in this
> repository on any branch, though every other page links to
> `/personal-trainer-rancho-santa-fe`. It was never patched because there is no
> file to patch. Push it and it can receive an identical pass.

---

## 1. Summary table

| Page | Patches applied | Header generated |
|---|---|---|
| `pages/personal-trainer-carlsbad.html` | 1, 2, 4, 5, 7, 11, 12 | Y |
| `pages/personal-trainer-carmel-valley.html` | 1, 2, 4, 5, 7, 11, 12 | Y |
| `pages/personal-trainer-del-mar.html` | 1, 2, 4, 5, 7, 11, 12 | Y |
| `pages/personal-trainer-encinitas.html` | 1, 2, 4, 5, 7, 11, 12 | Y |
| `pages/personal-trainer-fairbanks-ranch.html` | 1, 2, 4, 5, 7, 11, 12 | Y |
| `pages/personal-trainer-la-jolla.html` | 1, 2, 4, 5, 7, 11, 12 | Y |
| `pages/personal-trainer-santaluz.html` | 1, 2, 4, 5, 7, 11, 12 | Y |
| `pages/personal-trainer-solana-beach.html` | 1, 2, 4, 5, 7, 11, 12 | Y |
| `pages/personal-trainer-4s-ranch.html` (reference) | A1–A3 + deploy-comment cleanup | Y |
| `rancho-santa-fe` | **none — file absent from repo** | **N** |

### Rules that were no-ops on every territory page

These are recorded as flags, not silently skipped. Nothing was invented to satisfy them.

| Rule | Why it did not fire |
|---|---|
| 3 — 90-day results FAQ | No territory page has a results/timeframe FAQ. Adding one would have invented copy and broken the Part 2 rule that FAQPage contain **only** on-page questions. |
| 6 — Vincent = 59 / 8% BF, Alo = 18 lbs | No territory page has a transformation gallery, caption, or alt text. |
| 8 — "10+ Years in San Diego" | Territory stat rows read "12 Certifications Held". No San Diego-tenure claim exists. |
| 9 — stale `$50`/`$75` travel fees | No territory page carries those figures. See §5 for the vaguer wording that remains. |
| 10 — Pacific Beach studio references | Zero occurrences repo-wide. All pages already reference Teqneeq FHC, 4S Ranch. |

### Rule 4 (timeframe-attached lbs claims)

No territory page attached a timeframe to a pound figure. Persona language without a
timeframe was preserved as instructed, e.g. `pages/personal-trainer-carmel-valley.html:205`
— "Lose 20–30+ lbs sustainably."

---

## 2. Rule-10 drive-time flags

Every drive-time and proximity claim tied to the studio. **None were changed and none were invented.** Each needs human verification against the Teqneeq FHC location.

| File:line | Sentence as it now stands |
|---|---|
| `pages/personal-trainer-carlsbad.html:215` | "Our studio inside Teqneeq FHC at 10772 Thornmint Rd in 4S Ranch is about 25 minutes from most Carlsbad locations, doable for weekly sessions but not ideal for 2–3x/week frequency." |
| `pages/personal-trainer-carmel-valley.html:157` | "Train 1:1 inside Teqneeq FHC, a members-only functional health and performance lab in 4S Ranch, a quick drive up the 56." |
| `pages/personal-trainer-carmel-valley.html:295` | "Studio sessions are available inside Teqneeq FHC, a members-only functional health and performance lab at 10772 Thornmint Rd in 4S Ranch, San Diego, about 15 minutes from most Carmel Valley locations via the 56." |
| `pages/personal-trainer-del-mar.html:193` | "Train 1:1 inside Teqneeq FHC, a members-only functional health and performance lab in 4S Ranch, an easy drive from Del Mar via the 56." |
| `pages/personal-trainer-del-mar.html:331` | "Studio sessions are available inside Teqneeq FHC, a members-only functional health and performance lab at 10772 Thornmint Rd in 4S Ranch, San Diego, about 20 minutes from Del Mar via the 56." |
| `pages/personal-trainer-fairbanks-ranch.html:157` | "Train 1:1 inside Teqneeq FHC, a members-only functional health and performance lab in nearby 4S Ranch, about 15 minutes via Del Dios Highway." |
| `pages/personal-trainer-la-jolla.html:348` | "Studio sessions are available inside Teqneeq FHC, a members-only functional health and performance lab at 10772 Thornmint Rd in 4S Ranch, San Diego, about 30 minutes from La Jolla." |
| `pages/personal-trainer-santaluz.html:87` | "In-home sessions in your estate gym, private studio training at Teqneeq FHC, just minutes away in neighboring 4S Ranch, or hybrid coaching designed for professionals who demand privacy, structure, and measurable results." |
| `pages/personal-trainer-santaluz.html:117` | "Train 1:1 inside Teqneeq FHC, a members-only functional health and performance lab in neighboring 4S Ranch, roughly 10 minutes from the Santaluz gates." |
| `pages/personal-trainer-solana-beach.html:157` | "Train 1:1 inside Teqneeq FHC, a members-only functional health and performance lab in 4S Ranch, an easy drive inland via Lomas Santa Fe." |
| `pages/personal-trainer-solana-beach.html:267` | "In-home sessions at your Solana Beach residence, studio sessions a quick drive inland at Teqneeq FHC, or outdoor training at nearby parks." |
| `pages/personal-trainer-solana-beach.html:295` | "Studio sessions are available inside Teqneeq FHC, a members-only functional health and performance lab at 10772 Thornmint Rd in 4S Ranch, San Diego, about 20 minutes inland via Lomas Santa Fe and the 56." |

`encinitas` carries no drive-time claim.

---

## 3. Page-specific content with no 4S Ranch counterpart

Flagged, **not normalized**. Each item is local positioning, a local persona, or a local FAQ that has no equivalent on the reference page. All of it was left intact and swept for voice only.

### Structural gaps

| File | Item |
|---|---|
| `pages/personal-trainer-encinitas.html` | **No hybrid/virtual service card.** Only the Related Pages tile existed, and it was retargeted. Rule 1 says kill an existing card; nothing was added. |
| `pages/personal-trainer-la-jolla.html` | Same — no hybrid/virtual service card. |
| `pages/personal-trainer-solana-beach.html` | Same — no hybrid/virtual service card. |
| all eight | 7-question FAQ set vs. 4S Ranch's 10. No testimonials, transformations, "Meet Nemezio," "What's Included," or 90-day timeline sections. |

### Local service cards absent from 4S Ranch

| File:line | Card |
|---|---|
| `pages/personal-trainer-carlsbad.html:186` | Performance Beyond the Gym |
| `pages/personal-trainer-carlsbad.html:196` | Designed for Busy Families |
| `pages/personal-trainer-carmel-valley.html:254` | Efficiency for Busy Schedules |
| `pages/personal-trainer-carmel-valley.html:266` | More Than Physical Training |
| `pages/personal-trainer-del-mar.html:296` | In-Home Convenience |
| `pages/personal-trainer-del-mar.html:302` | Travel-Ready Hybrid Format |
| `pages/personal-trainer-encinitas.html:184` | Complements Yoga & Active Recovery |
| `pages/personal-trainer-encinitas.html:194` | Olivenhain & Encinitas Coverage |
| `pages/personal-trainer-fairbanks-ranch.html:254` | Privacy-First Training |
| `pages/personal-trainer-fairbanks-ranch.html:260` | Your Home Gym, Fully Utilized |
| `pages/personal-trainer-fairbanks-ranch.html:266` | Pain Resolution, Not Pain Management |
| `pages/personal-trainer-la-jolla.html:313` | Corrective-First Philosophy |
| `pages/personal-trainer-santaluz.html:186` | Gated Community Convenience |
| `pages/personal-trainer-santaluz.html:191` | Golf Performance Foundation |
| `pages/personal-trainer-solana-beach.html:254` | Complements Your Active Lifestyle |
| `pages/personal-trainer-solana-beach.html:266` | Flexible Coastal Convenience |

### Local FAQs absent from 4S Ranch

| File:line | Question |
|---|---|
| `pages/personal-trainer-carlsbad.html:211` | Do you serve the La Costa area specifically? |
| `pages/personal-trainer-carlsbad.html:214` | I play golf regularly and have lower back stiffness. Can you help? |
| `pages/personal-trainer-carlsbad.html:215` | Is Carlsbad too far from your studio for regular training? |
| `pages/personal-trainer-carmel-valley.html:309` | I sit at a desk all day and have chronic back and neck pain. Can you help? |
| `pages/personal-trainer-del-mar.html:350` | What if I have chronic pain or a previous injury? |
| `pages/personal-trainer-encinitas.html:209` | Do you serve Olivenhain? |
| `pages/personal-trainer-encinitas.html:212` | I practice yoga regularly. How does strength training fit with that? |
| `pages/personal-trainer-encinitas.html:213` | I've had a shoulder injury that flares up with certain movements. Can you work around that? |
| `pages/personal-trainer-fairbanks-ranch.html:294` | What equipment do I need at home? |
| `pages/personal-trainer-fairbanks-ranch.html:314` | Is there a difference between OmniFit and the trainers at my country club? |
| `pages/personal-trainer-la-jolla.html:362` | How is OmniFit different from a big-box gym or boutique fitness studio? |
| `pages/personal-trainer-santaluz.html:211` | Do I need a fully equipped home gym? |
| `pages/personal-trainer-santaluz.html:214` | Will this help my golf game? |
| `pages/personal-trainer-santaluz.html:215` | How is OmniFit different from the trainers at the club? |
| `pages/personal-trainer-solana-beach.html:309` | I surf and cycle regularly. Will strength training complement that? |
| `pages/personal-trainer-solana-beach.html:314` | Can I train outdoors in Solana Beach? |

Each page also carries a "What certifications does your trainer hold?" FAQ with a
full credential list, which 4S Ranch handles inside its "What makes OmniFit
different" answer instead. Both now read **ACE Corrective Exercise Specialist**.

---

## 4. Part 3 certification grep

Run across `pages/**` **and** the out-of-scope root file `corrective-exercise-post-rehab`.

### Zero-hit terms

| Term | `pages/` | Hits elsewhere |
|---|---|---|
| `OmniFit Personal Fitness Training` | clean | none |
| `Pacific Beach` | clean | none |
| `ACE OES` | clean | none |
| `Orthopedic Exercise` | clean | **8 — out of scope, see below** |
| `180+` | clean | none |
| `Executive Hybrid` | clean | none |
| `$225` | clean | **1 — out of scope, see below** |
| `$299` | clean | none |
| `$500` | clean | none |
| `$599` | clean | none |
| `free consultation` | clean | none |
| `Lopez Perez` | clean | **2 — out of scope, see below** |
| em-dashes in rendered copy | clean | n/a |

Only remaining `—` in `pages/` is a CSS comment banner inside the 4S Ranch
`<style>` block, plus HTML comments and the three `— Name, Title` testimonial
attribution dashes, all excluded by rule 11.

### Out-of-scope hits — `corrective-exercise-post-rehab`

This page was never in the patch list and was **not** modified. It violates the
same canon and needs its own pass.

```
Orthopedic Exercise   corrective-exercise-post-rehab:509
Orthopedic Exercise   corrective-exercise-post-rehab:532
Orthopedic Exercise   corrective-exercise-post-rehab:551
orthopedic exercise   corrective-exercise-post-rehab:723
Orthopedic Exercise   corrective-exercise-post-rehab:726
Orthopedic Exercise   corrective-exercise-post-rehab:822
Orthopedic Exercise   corrective-exercise-post-rehab:862
Orthopedic Exercise   corrective-exercise-post-rehab:888
Lopez Perez           corrective-exercise-post-rehab:509
Lopez Perez           corrective-exercise-post-rehab:862
$225                  corrective-exercise-post-rehab:826
```

### `$150` / `$175` breakdown

**`$150` — zero hits repo-wide.** It does not appear in the canonical answer
(which reads "$135 to $175 per session") or anywhere else.

**`$175` — 23 lines, 41 occurrences. 36 canonical, 5 needing review.**

CANONICAL — inside the byte-identical pricing answer, two occurrences per line
("Session packs run $135 to **$175** per session…" and "…async programming tier
at **$175** per month"):

```
pages/headers/personal-trainer-4s-ranch-header.html:62         x2
pages/headers/personal-trainer-carlsbad-header.html:62         x2
pages/headers/personal-trainer-carmel-valley-header.html:62    x2
pages/headers/personal-trainer-del-mar-header.html:62          x2
pages/headers/personal-trainer-encinitas-header.html:62        x2
pages/headers/personal-trainer-fairbanks-ranch-header.html:62  x2
pages/headers/personal-trainer-la-jolla-header.html:62         x2
pages/headers/personal-trainer-santaluz-header.html:62         x2
pages/headers/personal-trainer-solana-beach-header.html:62     x2
pages/personal-trainer-4s-ranch.html:1021                      x2
pages/personal-trainer-carlsbad.html:210                       x2
pages/personal-trainer-carmel-valley.html:290                  x2
pages/personal-trainer-del-mar.html:326                        x2
pages/personal-trainer-encinitas.html:208                      x2
pages/personal-trainer-fairbanks-ranch.html:290                x2
pages/personal-trainer-la-jolla.html:343                       x2
pages/personal-trainer-santaluz.html:210                       x2
pages/personal-trainer-solana-beach.html:290                   x2
```

REVIEW — outside the canonical answer. All five are the Hybrid & Virtual Coaching
card bullet **"Fully virtual Executive Reset from $175/mo"**, which is the exact
string specified in patch-sheet item 1 and agrees with the canonical answer's
async tier at $175/month. **Assessed as correct, not stale-era.**

```
pages/personal-trainer-4s-ranch.html:658         x1
pages/personal-trainer-carlsbad.html:141         x1
pages/personal-trainer-carmel-valley.html:197    x1
pages/personal-trainer-fairbanks-ranch.html:197  x1
pages/personal-trainer-santaluz.html:141         x1
```

### Other invariants

- Pricing FAQ answer: **one** sha256 across all 9 pages and all 9 headers (`ae388d31c0b6149e`, 972 bytes).
- Reviews: 21 occurrences of `190+`, no other review count anywhere.
- All 9 headers parse under `json.loads`, reference `https://www.omnifittraining.com/#localbusiness-of` by `@id`, and define no `LocalBusiness`.
- Every header's FAQ questions match its page's questions in count, order, and text.

---

## 5. Judgment calls beyond the written instructions

**1. `$90 BodyStat assessment` → `$110 Performance Diagnostic` (8 pages, 4–6 spots each).**
Rule 12 says "$110 Performance Diagnostic credited toward a 3-month package
wherever priced," but these pages priced the intake at $90 under the older name,
including a service card titled "BodyStat Diagnostics" and a FAQ "What is the
BodyStat assessment?". They were treated as the same product renamed and
repriced: card title and FAQ renamed to Performance Diagnostic, price moved to
$110, credit wording changed to "credited in full toward a 3-month package,"
and **BodyStat 1500 MDD kept as the named measurement device**.
**If the $90 BodyStat scan is a separate, still-current product, this is wrong on eight pages.**

**2. Regenerated the FAQPage node in the supplied 4S Ranch v2 header.**
The delivered file was hand-authored, so several answers — including the pricing
answer — did not match the visible page. It omitted "Note:" and the closing
"Full tables on the training rates page." sentence, which broke both the
byte-identical rule and the requirement that schema mirror on-page text. The
FAQPage is now derived mechanically like the other eight. Its WebPage `name` and
`description` are untouched. **The as-delivered file is intact in commit `b80619d`.**

**3. Hybrid card descriptions kept local; title, bullets, and link normalized.**
Rule 1 said match 4S Ranch. The 4S Ranch title (`Hybrid & Virtual Coaching`),
three bullets, and `/the-30-minute-executive-reset` link were applied verbatim,
but each page's own descriptive sentence was kept, since it names the local
persona and carried no retired pricing.

**4. No hybrid card added to the three pages that lack one** (encinitas, la-jolla,
solana-beach). Rule 1 says kill an existing card; creating one would be inventing
a section. Their Related Pages tiles were retargeted.

**5. Em-dash sweep resolved per sentence, not globally.**
130 unique em-dash contexts were catalogued first. A blanket comma would have
produced comma splices, so each was resolved to a period, comma, or colon by the
following clause — e.g. "…concierge territory. We also serve…" (period),
"Credentialed access only: no walk-ins" (colon), "…virtual programming, ideal
for…" (comma). Numeric en-dashes (`45–60`, `2–3x`, `20–30`), HTML comments, alt
attributes, and testimonial attribution dashes were left untouched.

**6. Repo layout normalized.** The eight pages moved from repo root to
`pages/personal-trainer-<slug>.html` via `git mv`, matching the reference page and
the Part 2 header path. The pre-patch root `4s-ranch` file was removed as
superseded by the patched copy; its content remains in git history.

**7. Retired rate figures removed from the 4S Ranch deploy comment.**
The comment quoted the old rate card and "180+" as things to check for, which
tripped the certification grep from inside a comment. It now describes the checks
without embedding the stale literals.

**8. Residual travel-fee language left in place (not a rule-9 hit, but flagged).**
All eight pages still read "A travel fee may apply for in-home sessions depending
on location." No figures, so rule 9 did not fire — but 4S Ranch now points to the
rates page instead, and these may want the same treatment.

```
pages/personal-trainer-carlsbad.html:209
pages/personal-trainer-carmel-valley.html:285
pages/personal-trainer-del-mar.html:321
pages/personal-trainer-encinitas.html:207
pages/personal-trainer-fairbanks-ranch.html:285
pages/personal-trainer-la-jolla.html:338
pages/personal-trainer-santaluz.html:209
pages/personal-trainer-solana-beach.html:285
```

---

## 6. Repo file tree

```
.
├── REPORT.md
├── corrective-exercise-post-rehab          # out of scope, unpatched, see §4
└── pages
    ├── personal-trainer-4s-ranch.html
    ├── personal-trainer-carlsbad.html
    ├── personal-trainer-carmel-valley.html
    ├── personal-trainer-del-mar.html
    ├── personal-trainer-encinitas.html
    ├── personal-trainer-fairbanks-ranch.html
    ├── personal-trainer-la-jolla.html
    ├── personal-trainer-santaluz.html
    ├── personal-trainer-solana-beach.html
    └── headers
        ├── personal-trainer-4s-ranch-header.html
        ├── personal-trainer-carlsbad-header.html
        ├── personal-trainer-carmel-valley-header.html
        ├── personal-trainer-del-mar-header.html
        ├── personal-trainer-encinitas-header.html
        ├── personal-trainer-fairbanks-ranch-header.html
        ├── personal-trainer-la-jolla-header.html
        ├── personal-trainer-santaluz-header.html
        └── personal-trainer-solana-beach-header.html
```

**Missing vs. requested:** `pages/personal-trainer-rancho-santa-fe.html` and
`pages/headers/personal-trainer-rancho-santa-fe-header.html`.

Nothing in this run was published to Squarespace. This repo is the source of
truth; approved output is pasted by hand.

---

# Final run — credentials block, RSF intake, close-out

Run immediately before hand-off to Squarespace. Scope: verify the two
hand-committed Rancho Santa Fe files, add a "Meet Your Trainer" credentials
section to the nine territory pages, re-certify, and merge to `main`.

## RSF intake verification

Both files were committed **without the `.html` extension**, so nothing existed at
the paths given (`pages/personal-trainer-rancho-santa-fe.html`,
`pages/headers/personal-trainer-rancho-santa-fe-header.html`). Content was
certified **before** any change and passed every check; the files were then
renamed with `git mv` in commit `bea9dec`. **Content is byte-for-byte unchanged.**
This was a naming slip, not a certification failure, so the run continued.

| Check | Result |
|---|---|
| All 14 banned strings, page + header | clean, zero hits |
| Pricing FAQ answer byte-identical to other nine | yes, `ae388d31c0b6149e` |
| Header JSON valid | yes |
| `about` references homepage `#localbusiness-of`, no `LocalBusiness` redefined | yes |
| FAQPage matches page questions in count, order, text | yes, 6 of 6 |
| Hybrid & Virtual Coaching card present | yes |

**Structural note:** RSF carries **6** FAQs where the other eight territory pages
carry 7. Its schema matches its page exactly, so this is not a defect, but it
means RSF has no "Do you only serve X" territory-scope FAQ. Its six questions:

```
pages/personal-trainer-rancho-santa-fe.html:320  How does in-home personal training work in Rancho Santa Fe?
pages/personal-trainer-rancho-santa-fe.html:325  What does a personal trainer in Rancho Santa Fe cost?
pages/personal-trainer-rancho-santa-fe.html:330  Do I need a fully equipped home gym?
pages/personal-trainer-rancho-santa-fe.html:335  What certifications does your trainer hold?
pages/personal-trainer-rancho-santa-fe.html:340  I split time between San Diego and another city. Can this work?
pages/personal-trainer-rancho-santa-fe.html:345  How is this different from other in-home trainers in Rancho Santa Fe?
```

## Credentials block additions

Added to nine pages, placed after the services grid and before the FAQ section.
4S Ranch was left untouched — it already has its own Meet Nemezio section with a
portrait.

Markup uses each page's own `XX-section`, `XX-section-head`, `XX-label`,
`XX-divider`, `XX-card`, `XX-card-link`, and `XX-spacer` classes. **No CSS was
added and no inline styles were used.** The card sits as a direct child of the
section rather than inside `XX-grid`, because `XX-grid` is a fixed three-column
layout and a lone card would render at one-third width.

| Page | Prefix | Inserted before line | Order verified |
|---|---|---|---|
| carlsbad | `cb` | 202 | grid < coach < FAQ |
| carmel-valley | `cv` | 274 | grid < coach < FAQ |
| del-mar | `dm` | 310 | grid < coach < FAQ |
| encinitas | `en` | 200 | grid < coach < FAQ |
| fairbanks-ranch | `fb` | 274 | grid < coach < FAQ |
| la-jolla | `lj` | 327 | grid < coach < FAQ |
| rancho-santa-fe | `rs` | 295 | grid < coach < FAQ |
| santaluz | `sz` | 202 | grid < coach < FAQ |
| solana-beach | `sb` | 274 | grid < coach < FAQ |

Body text sha256 — **one hash across all nine**:

```
6492e3ca1545dc260e88d05f10a9c40d93cee90bd800283c71ef063e6c014477   (630 bytes)
```

Zero em-dashes in the new content. All ten pages pass HTML tag-balance parsing
with no unclosed tags and no mismatches. Header files were not touched in this
part, since the credentials section is not an FAQ and FAQPage schema is unchanged.

## Final certification grep — 20 files

`pages/**` and `pages/headers/**`, all ten pages and all ten headers.

| Term | Result |
|---|---|
| `OmniFit Personal Fitness Training` | clean |
| `Pacific Beach` | clean |
| `ACE OES` | clean |
| `Orthopedic Exercise` | clean |
| `Executive Hybrid` | clean |
| `Lopez Perez` | clean |
| `180+` | clean |
| `free consultation` | clean |
| `$90 ` | clean |
| `$225` | clean |
| `$275` | clean |
| `$299` | clean |
| `$500/mo` | clean |
| `$599` | clean |

**Total banned-string hits: 0.**

### `$150` / `$175`

`$150` — zero hits. `$175` — 46 occurrences: **40 inside the canonical pricing
answer** (two per answer across 10 pages and 10 headers), **6 outside it**.

```
pages/personal-trainer-4s-ranch.html:658
pages/personal-trainer-carlsbad.html:141
pages/personal-trainer-carmel-valley.html:197
pages/personal-trainer-fairbanks-ranch.html:197
pages/personal-trainer-rancho-santa-fe.html:218
pages/personal-trainer-santaluz.html:141
```

**Reported, not removed.** All six are the identical Hybrid & Virtual Coaching
card bullet **"Fully virtual Executive Reset from $175/mo"**, which is the exact
string specified in patch-sheet item 1 and agrees with the canonical answer's
"async programming tier at $175 per month". Read strictly, the Part 3 rule
("legal only inside the canonical pricing FAQ answer") would flag them; read
against item 1, they are required. This is a rule conflict, not a stale-era
violation, so nothing was deleted. **Decide which rule wins before paste.**

### Other invariants

- Page pricing answer: one hash, `ae388d31c0b6149e`, across all 10 pages.
- Header pricing answer: one hash, `7e5de5984b133663`, across all 10 headers.
- All 10 headers parse under `json.loads`.

## Judgment calls in this run

**1. Renamed the RSF files rather than stopping.** The stop condition was a
certification failure; content passed everything. A missing file extension is a
naming slip with a deterministic fix, and stopping the final run over it would
have blocked hand-off. The rename is its own commit and is reported here rather
than folded into another change.

**2. Credentials card placed outside `XX-grid`.** See above — a single card in a
fixed three-column grid renders at one-third width. Placing it directly in the
section gives a full-width card using only existing classes.

**3. Omitted a card icon and `h3` sub-heading.** The card pattern on these pages
normally carries `XX-card-icon` and an `h3`. The content spec listed only a label,
heading, body, and link, so nothing extra was invented.

**4. The six `$175` card bullets were left in place.** See the rule conflict above.

## Carried forward, still unresolved

- **`$90` → `$110 Performance Diagnostic`** rename across eight pages rests on the
  inference that the retired $90 BodyStat assessment and the canonical $110
  Performance Diagnostic are the same product. Unverified.
- **12 drive-time claims** remain unverified against the Teqneeq FHC location.
- **`corrective-exercise-post-rehab`** at repo root is still unpatched and still
  violates the canon (8× "Orthopedic Exercise", 2× "Lopez Perez", 1× `$225`).
