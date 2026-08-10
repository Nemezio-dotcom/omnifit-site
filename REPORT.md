# Territory-Page Propagation Run — Report

**Branch:** `claude/omnfit-4s-ranch-location-mxek1x`
**Reference page:** `pages/personal-trainer-4s-ranch.html`
**Scope:** propagate the 4S Ranch canonical patch set to the territory pages, generate per-page JSON-LD headers, and certify the repo.

> **Nine pages were requested; eight exist.** `rancho-santa-fe` is not in this
> repository on any branch, though every other page links to
> `/personal-trainer-rancho-santa-fe`. It was never patched because there is no
> file to patch. Push it and it can receive an identical pass.
>
> **RESOLVED in the Final run below.** Rancho Santa Fe was hand-committed and
> verified. Sections 1 to 6 describe the propagation run as it stood at the time;
> the Final run section is the current state of the repo.

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
| `rancho-santa-fe` | **none — file absent from repo at the time of this run; see Final run** | **N at the time; Y now** |

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

> Superseded by the Final run. Current state is shown at the end of this document.

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

## Repo file tree — current

```
.
├── REPORT.md
├── corrective-exercise-post-rehab          # out of scope, unpatched
└── pages
    ├── personal-trainer-4s-ranch.html
    ├── personal-trainer-carlsbad.html
    ├── personal-trainer-carmel-valley.html
    ├── personal-trainer-del-mar.html
    ├── personal-trainer-encinitas.html
    ├── personal-trainer-fairbanks-ranch.html
    ├── personal-trainer-la-jolla.html
    ├── personal-trainer-rancho-santa-fe.html
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
        ├── personal-trainer-rancho-santa-fe-header.html
        ├── personal-trainer-santaluz-header.html
        └── personal-trainer-solana-beach-header.html
```

10 page files, 10 header files, REPORT.md. The only remaining root file is
`corrective-exercise-post-rehab`, which was never in scope. The pre-patch
originals that lived at repo root are gone; their content is in git history.

---

# Section A/B run — Who We Coach + 9-Point Movement Screen

First run governed by `CANON.md`, which was committed to the repo root at the
start of this run (`7c9f514`). Scope: add two sections to **all ten** territory
pages, 4S Ranch included.

## What was added

**Section A — Who We Coach.** Placed directly after each page's credentials block,
and after the Meet Nemezio section on 4S Ranch. Section head plus a three-card
grid using each page's own `XX-section`, `XX-section-head`, `XX-label`,
`XX-divider`, and `XX-grid`/`XX-card` classes. Intro line varies only by
neighborhood. The three archetypes are The Desk-Bound Executive, The Post-Rehab
Professional, and The 50+ Professional.

Compliance: each card was machine-checked for outcome numbers before insertion.
No pounds, percentages, or timeframes appear in any card. Situation and approach
only, as specified.

**Section B — The 9-Point Movement Screen.** Placed directly after Section A and
before the FAQ. Section head plus a full-width `XX-card` holding a
`XX-card-features` list of nine items and the closing line. The intro names the
45-minute consultation and the $110 Performance Diagnostic credited in full
toward a 3-month package, matching CANON pricing.

| Page | Section A | Section B | Inserted before line | Certification |
|---|---|---|---|---|
| `personal-trainer-4s-ranch.html` | Y | Y | 1012 | pass |
| `personal-trainer-carlsbad.html` | Y | Y | 217 | pass |
| `personal-trainer-carmel-valley.html` | Y | Y | 289 | pass |
| `personal-trainer-del-mar.html` | Y | Y | 325 | pass |
| `personal-trainer-encinitas.html` | Y | Y | 215 | pass |
| `personal-trainer-fairbanks-ranch.html` | Y | Y | 289 | pass |
| `personal-trainer-la-jolla.html` | Y | Y | 342 | pass |
| `personal-trainer-rancho-santa-fe.html` | Y | Y | 310 | pass |
| `personal-trainer-santaluz.html` | Y | Y | 217 | pass |
| `personal-trainer-solana-beach.html` | Y | Y | 289 | pass |

Ordering was verified programmatically on every page as
`credentials block < Section A < Section B < FAQ`. All ten pages parse with no
unclosed or mismatched tags. All ten header files were left untouched, since
neither section is an FAQ.

## CANON.md invariants updated

Two hashes were previously placeholders and are now set. This is a legitimate
first-time population, not a change to an existing invariant.

| Invariant | Hash | Scope |
|---|---|---|
| Archetype card bodies (Section A) | `6b1b0f4efbd4a72c` | 10 pages |
| 9-point screen body (Section B) | `bd73ea51bc9ec5eb` | 10 pages |

The definition of each hash was recorded alongside it in CANON.md, since
"byte-identical body" is ambiguous without saying which bytes: Section A hashes
the concatenation of the three card paragraph bodies in page order; Section B
hashes the intro plus the nine list items plus the closing line.

Pre-existing invariants re-verified and still holding: page pricing answer
`ae388d31c0b6149e` (10 pages), header pricing answer `7e5de5984b133663`
(10 headers), credentials body `6492e3ca1545dc26` (9 pages).

## Certification — 20 files, per CANON.md

All fourteen banned strings: **zero hits**. `$50`/`$75` as travel fees: **zero**.
Em-dashes in rendered prose: **zero violations**.

`$150`/`$175`: 46 occurrences, **all legal, zero violations**. 40 sit inside the
canonical pricing answer and 6 are the approved card bullet "Fully virtual
Executive Reset from $175/mo". CANON.md's exception (b) resolves the rule
conflict flagged in the previous run, and those six bullets are now certified
rather than merely reported.

### Em-dash tooling

CANON.md requires the exceptions be carved out by rule, not by line number. The
checker strips HTML comments and `alt` attributes, then permits an em-dash only
when it is a `-tcard-name` attribution or matches
`<li>Name — descriptor</li>` with a capitalised name of 3 to 60 characters
before the separator. It was negative-tested against six fixtures: the four legal
forms pass, a prose em-dash is caught, and — importantly — a prose em-dash placed
inside an `<li>` is still caught, so the new exception cannot be used to smuggle
prose dashes into list items.

## Judgment calls

**1. CANON.md excludes the two-sentence instruction preamble.** The message said
to commit it verbatim; the file begins at the `═══ OMNIFIT SITE` banner. The
preamble ("Commit this entire message verbatim… then proceed with the pending
Section A/B run") is a cover note for one run, and CANON.md is read by every
future run before touching anything. Left in, a later run would read "proceed
with the pending Section A/B run" as a live instruction and could redo this work.
**Wrong if** the preamble was intended as part of the permanent record, in which
case prepend it; everything from the banner down is byte-identical to the message.

**2. Section heads carry the intro paragraph.** Territory `XX-section-head` blocks
previously held only label, divider, and h2. Both intros were placed inside the
section head so they inherit its centering without an inline style, matching the
approach used for the credentials block. **Wrong if** the intros were meant to sit
full-width as body copy rather than centered under the heading.

**3. Section B renders as one full-width card, not a nine-card grid.** `XX-grid`
is a fixed three-column layout, so nine short items would have produced three
ragged rows. A single `XX-card` holding a `XX-card-features` list gives the
existing check-mark list styling. **Wrong if** the nine points were meant to read
as individual cards.

**4. Section labels were chosen, not specified.** The spec gave section names,
intro copy, and card content but not the small `XX-label` eyebrow text. "Who We
Coach" and "The Diagnostic" were used. **Wrong if** specific eyebrow text was
intended.

## Carried forward, still unresolved

- `$90` → `$110 Performance Diagnostic` rename across eight pages still rests on
  the inference that the retired $90 BodyStat assessment and the $110 Performance
  Diagnostic are the same product. CANON.md now states "$90 is the retired
  name-era price", which supports the inference but does not independently
  confirm it.
- 12 drive-time claims remain unverified against the Teqneeq FHC location.
- `corrective-exercise-post-rehab` at repo root is still unpatched, per CANON.md
  Batch 3.

---

# Batch 3, page 1 — corrective-exercise-post-rehab

Two rulings closed first, then the page. Run governed by `CANON.md`.

## Rulings applied

- **Ruling 1.** CANON.md left clean; no preamble prepended.
- **Ruling 2.** `$90 assessment = confirmed same product as the $110 Performance
  Diagnostic; rename settled.` added to the CANON.md pricing section. The item is
  closed and no longer carried forward.

## Violations fixed

The earlier report counted 11 from a narrower grep. The real count was **12 on the
banned-string list, plus 3 more `ACE Orthopedic` variants** that the earlier grep
missed because they did not contain the exact string "Orthopedic Exercise"
(`ACE Orthopedic corrective exercise` in the deploy comment, `ACE Orthopedic
certified` in a hero pill, `ACE Orthopedic Certified` in an h3).

| What | Where | Fix |
|---|---|---|
| ACE credential, 11 occurrences | lines 11, 509, 513, 532, 551, 722, 723, 726, 822, 862, 888 | ACE Corrective Exercise Specialist |
| `Nemezio Lopez Perez`, 2 | 509, 862 | Nemezio LopezPerez |
| `$90` diagnostic + `$225 to $1,275/mo` | 826 | replaced with the canonical pricing answer verbatim |
| `seven standardized metrics` / `7-metric`, 3 | 532, 666, 735 | twelve / 12 |
| em-dashes in prose, 22 | throughout | period, comma, or colon per sentence |

The five `cx-who-list` items were **kept** as em-dashes: they are
`<li><strong>Label</strong> — descriptor</li>`, which is CANON's structured-list
exception with a tag-wrapped label.

## Sections added

Placed to extend the existing structure, not reorder it. Final order: Hero,
**Why Imbalances Form**, What We Address, The Process, **Client Journey**,
What Makes OmniFit Different, **Meet Your Trainer**, Near-Me, **Scope of
Practice**, PT Coordination, **Use Cases**, FAQ, Bottom CTA, Trust Bar, Hub Links.

- **Why Sitting Creates Muscle Imbalances.** Opposing-pair mechanism at pattern
  level: what shortens, what lengthens, how joint resting position shifts, how load
  redistributes during movement. Closes with an explicit "education, not diagnosis"
  callout and a referral line. No diagnosis language, no medical claims, no
  conditions named as diagnoses.
- **What the Journey Looks Like From Your Side.** The same Assess, Correct, Build,
  Sustain arc from the client's perspective. No outcome or timeframe promises.
- **Meet Nemezio LopezPerez.** Reuses the canonical credentials body verbatim.
- **DPT, CES, DC, and CPT: Who Does What.** Four-row scope-of-practice table with a
  closing callout placing OmniFit in the CES column only, never a substitute for
  medical care, with referral back to the DPT or physician column.
- **What People Come to Corrective Training For.** Four adjacent-query use cases per
  CANON: long-term transformation, fat loss without crash protocols, desk-worker
  posture and mobility, data-driven hybrid. Situation and approach only.

## File move and header

`corrective-exercise-post-rehab` → `pages/corrective-exercise-post-rehab.html` via
`git mv`; header generated at
`pages/headers/corrective-exercise-post-rehab-header.html`, 12 FAQ nodes derived
mechanically from the on-page FAQ, JSON validated, LocalBusiness referenced by
`@id`. Repo root now holds only `CANON.md` and `REPORT.md`.

## Certification — 22 files

All 14 banned strings clean. `$50`/`$75` as travel fees clean. Em-dashes in
rendered prose: zero violations. `$150`/`$175`: 50 occurrences, all legal, zero
violations.

| Invariant | Hash | Scope |
|---|---|---|
| page pricing answer | `ae388d31c0b6149e` | 11 pages |
| header pricing answer | `7e5de5984b133663` | 11 headers |
| credentials body | `6492e3ca1545dc26` | 10 pages (was 9) |
| archetypes | `6b1b0f4efbd4a72c` | 10 pages |
| 9-point screen | `bd73ea51bc9ec5eb` | 10 pages |

The credentials invariant legitimately widened from 9 pages to 10 because this run
added the canonical body to the corrective page, as CANON.md's instruction to reuse
it directed. CANON.md was updated to match.

### Two tooling corrections worth recording

1. **A certification run passed vacuously and was caught.** The script was invoked
   from the scratchpad directory, so its glob matched **0 files** and every check
   reported clean. It was re-run from the repo root against the real 22 files. Any
   future run should treat a file count of 0 in the header line as a failure, not a
   pass.
2. **A tag-balance error was real, not cosmetic.** One insertion dropped a closing
   `</section>`, leaving 3 unclosed elements. It initially looked like a parser
   artifact from `<hr />`; correcting the parser to handle self-closing void
   elements showed the pre-patch original balanced cleanly and the patched file did
   not. Fixed, re-verified.

## Judgment calls

**1. The pricing FAQ answer was replaced with the canonical answer verbatim.**
The question is corrective-specific ("How much does corrective exercise training
cost in San Diego?") but the old answer carried two banned figures. Using the
canonical answer keeps the byte-identical invariant. **Wrong if** this page was
meant to carry a corrective-specific pricing answer, in which case the invariant
would need a documented exception.

**2. `seven standardized metrics` changed to twelve, in three places.** Not on the
banned-string list. CANON's Batch 3 line states 12 metrics, not 7, which makes 7 a
known-stale figure that I would otherwise have certified as clean. **Wrong if** 7
is correct for corrective reports specifically and 12 applies only to
the-omnifit-method.

**3. ~11 lines of scoped CSS added for the comparison table.** The page had no table
styles. Earlier runs banned new CSS; that instruction was not restated here, and a
scope table is clearer as a table than as cards. The block is scoped to
`#omni-corrective`, appended, and commented with its date. **Wrong if** the no-new-CSS
rule was meant to carry forward, in which case the table should become four cards.

**4. The client-journey section overlaps the existing process section.** The page
already had a four-phase process section. Rather than restructure what ranks, the
new section is explicitly client-POV and cross-references the method one. **Wrong if**
the intent was to replace the existing process section rather than complement it,
in which case delete the older one.

**5. The use-cases section is titled "What People Come to Corrective Training For",
not "Who This Is For".** The page already has "Who Corrective Exercise Training Is
For"; two near-identical headings would compete. CANON permits the "Use Cases"
naming. **Wrong if** the exact heading text mattered for a target query.

**6. Heading em-dashes became colons** ("Near Me: San Diego & North County",
"In-Person: Teqneeq FHC", "Virtual: Anywhere"). Headings are rendered prose and
carry no CANON exception. **Wrong if** heading dashes were intended as exempt.

## Carried forward

- 12 drive-time claims on territory pages remain unverified.
- `$90` → `$110` item is now **closed** by Ruling 2.

---

# Batch 2 run — FAQs, how-it-works-pricing, in-home, private

Ran after five rulings unblocked the pricing question. `training-rates-san-diego.html`
was designated as the pricing reference but is still the July V8 stale generation,
so every figure below comes from CANON plus the rulings, not from that page.

## Rulings applied

| Ruling | Decision |
|---|---|
| Upfront totals | 3 × the 3-month monthly rate, no discount. Every tier shows 3-month and month-to-month |
| Pack ladder | 5 @ $175 ($875), 10 @ $150 ($1,500), 20 @ $135 ($2,700), one ladder regardless of location |
| Couples | Monthly only, from $325/mo ($975 upfront). Per-person figures dropped |
| $697 Hybrid slot | Deleted. Virtual is the Reset: Bronze $175 async, Gold $449, Platinum $675, Black $995 |
| how-it-works-pricing | Converted from per-session cards to monthly tiers |
| Header naming | Standardised on `<slug>-header.html` |

The 10-pack total independently corroborates the ladder: 10 × $150 = $1,500, matching
the `$150/session ($1,500)` line on the old rates page.

## Per page

| Page | Canon fixes | Added | Header |
|---|---|---|---|
| `FAQs.html` | brand, Pacific Beach ×4, 180+, ACE, hyphenated Lopez-Perez, Hybrid FAQ deleted, pricing prose renumbered, deposit $50 → $30 | — | 14 nodes |
| `private-personal-trainer-san-diego.html` | LopezPerez, ACE ×4, $90 → $110, $225 → $250, Hybrid card and tile, paid consultation ×3 | Use Cases | 7 nodes |
| `in-home-personal-trainer-san-diego.html` | LopezPerez, ACE ×3, Hybrid tile, paid consultation | Why We Assess (9-point + RHR/BP), Desk-Posture Protocol, Conditions We Coach Around, Use Cases, pricing-structure table row | 8 nodes |
| `how-it-works-pricing.html` | Pacific Beach, Hybrid deleted throughout, 7 → 12 metrics, paid consultation, 2.9% card fee, renamed to .html | Full monthly-tier rebuild: 4 tiers, packs, Reset, couples, in-home note | 8 nodes |

Use Cases bodies are byte-identical across private and in-home
(sha256 `9f5c0770…`). They are **not** byte-identical to the corrective page's
version, which was written page-specific and shipped earlier.

## Compliance strikes found and removed

Five, none of which were on the banned-string list, so the grep alone would have
passed them:

```
FAQs.html:158                     30-Day Performance Guarantee (Reset description)
FAQs.html:248                     "20-30 pounds ... over 4-6 months" outcome claim
in-home:513                       30-Day Performance Guarantee (policy card)
how-it-works-pricing:533,592      30-Day Performance Guarantee (section + FAQ)
how-it-works-pricing:582          "The average client loses 20-30 pounds over 4-6 months"
```

The guarantee is renamed a 30-Day Fit Commitment with the outcome framing dropped;
the refund mechanics stay, since those are a commercial policy rather than a
results promise.

## Certification — 31 files in scope

All 14 banned strings clean. `$50`/`$75` as travel fees clean. Em-dashes in rendered
prose: zero. `$150`/`$175`: 75 occurrences, all legal, zero violations.

| Invariant | Hash | Scope |
|---|---|---|
| page pricing answer | `ae388d31c0b6149e` | 11 pages |
| header pricing answer | `7e5de5984b133663` | 11 headers |
| credentials body | `6492e3ca1545dc26` | 10 pages |
| archetypes | `6b1b0f4efbd4a72c` | 10 pages |
| 9-point screen | `bd73ea51bc9ec5eb` | 10 pages |

### Three uncertified files, deliberately excluded

Listed by the tooling on every run rather than silently skipped:

- **`training-rates-san-diego.html`** — the July V8 stale generation. Carries `$90`,
  `$225`, `$275`, `$599`, Executive Hybrid, the retired tier ladders, and
  body-embedded JSON-LD at line 822 that still needs moving to a header file. Blocked
  pending the hand-patched version.
- **`the-30-minute-executive-reset.html`** — Executive Hybrid at line 26. Batch 2 but
  not among the four.
- **`footer.html`** — `OmniFit Personal Fitness Training` and `Pacific Beach` at
  line 7. Site-wide, in no batch.

### Two tooling failures caught this run

1. **The checker crashed** on `&mdash;` entities, because the list-item exception
   looked up a literal em-dash character that was not present. Earlier sweeps had
   only ever seen the character form, so `&mdash;` had been passing unexamined on
   how-it-works-pricing. Fixed, and 22 entity-form em-dashes were then swept.
2. **The header-pricing invariant was over-matching.** It compared any FAQ answer
   whose question mentioned "cost", which pulled in four page-specific pricing
   answers and reported a false mismatch across five hashes. It now matches only
   answers beginning with the canonical sentence, which is what the invariant
   actually covers.

The zero-file guard added after last run's vacuous pass fired correctly when the
script was invoked from the wrong directory.

## Judgment calls

**1. CANON's `$150/$175` rule was widened.** The rungs you gave make `$175` and
`$150` canonical pack rates, which the old rule would have flagged. The exception now
covers the pack rungs and the Reset Bronze tier, and the checker judges by the
enclosing pricing card's name rather than the line. `$150` or `$175` as a **studio
per-session rate** remains a violation. **Wrong if** the intent was that those two
figures disappear entirely.

**2. The 2.9% card processing fee was removed** from two places on
how-it-works-pricing. It is not on the banned list, but the rates page's own V8
changelog reads "2.9% card fee removed everywhere", and the surrounding copy claims
"no surprise charges". **Wrong if** the fee is still charged.

**3. Billing copy was inverted.** The page said "billed monthly via auto-pay, no
large upfront payments", which contradicts Ruling 1. It now states that 3-month
programs are paid in full upfront. **Wrong if** monthly billing on 3-month plans is
still offered alongside the upfront option.

**4. The refund guarantee was reframed rather than deleted.** CANON strikes outcome
guarantees on sight, but the refund itself is a real commercial term I cannot verify
as retired. The promise language is gone; the mechanics remain. **Wrong if** the
refund policy no longer exists at all.

**5. Executive Hybrid nav tiles were removed, not retargeted,** on FAQs, private and
in-home. Retargeting each to `/the-30-minute-executive-reset` would have duplicated
an Executive Reset tile already present in the same grid. Same precedent as the
territory pages.

**6. The Reset's `30-Day Performance Guarantee` remains live** on
`the-30-minute-executive-reset.html`, which is out of scope for this run. It is the
same compliance strike removed from three in-scope pages.

## Carried forward

- `training-rates-san-diego.html` still blocked, and its body-embedded schema still
  needs moving to a header file.
- 12 drive-time claims on territory pages remain unverified.
- `footer.html` and `the-30-minute-executive-reset.html` need a pass.

---

# Deferred / future cleanup

Approved items that are deliberately **not** applied yet. Certification runs must
not flag these as violations while they remain listed here and in CANON.md's
KNOWN DEFERRED ITEMS section.

## DEFERRED-01 · Executive Reset guarantee wording (rates page)

**File:** `pages/training-rates-san-diego.html`, plus its header file.

> **Note on the header file:** it does not exist yet. That page's schema is still
> body-embedded at line 822, so the third instance currently sits in the body block
> and will move with the schema whenever it is extracted into
> `pages/headers/training-rates-san-diego-header.html`.

**Three instances, verified this session:**

| Location | Where |
|---|---|
| `pages/training-rates-san-diego.html:664` | Body callout inside the Executive Reset section |
| `pages/training-rates-san-diego.html:767` | "Does OmniFit offer a money-back guarantee?" FAQ answer |
| `pages/training-rates-san-diego.html:880` | The same answer inside the FAQPage schema |

**Current text** promises an outcome ("feel clearly stronger, more energized, and
more in control") and conditions the refund on undefined "full compliance" of a
"remaining program balance."

**Two problems:**

1. CANON bans outcome guarantees. This is named a guarantee and promises a result.
2. "Full compliance" and "remaining balance" are undefined terms in a refund promise
   under an upfront billing model.

**Approved replacement, to apply in a future cleanup pass:**

*Callout heading:*

> 30-Day Fit Guarantee

*Callout body:*

> If after your first 30 days you decide the Executive Reset isn't the right fit,
> you can stop and I'll refund the unused balance of your program. You keep the
> first month and everything you've learned. No compliance test, no negotiation.

*FAQ answer:*

> Yes, on the Executive Reset. It includes a 30-Day Fit Guarantee: if after your
> first 30 days you decide it isn't the right fit, you can cancel and receive a
> refund of the unused balance of your program. You keep the first month and
> everything you've learned. There is no compliance test to pass and nothing to
> negotiate.

**Status:** approved, not yet applied. Deliberately deferred by Nemezio. Known,
accepted exception until scheduled.

> **Why nothing broke by deferring it:** `training-rates-san-diego.html` is already
> on the uncertified list and excluded from certification runs, so this wording was
> never being flagged. The entry matters for when that page is unblocked and enters
> scope, at which point the exception must be honoured until the pass is scheduled.

## RESOLVED-02 · Statutory cap exposure on prepaid tiers · CLOSED

*Logged as DEFERRED-02, an ACTIVE CONSTRAINT, then resolved in the same session.
Retained in full because the reasoning is worth keeping; the constraint itself is
lifted.*

> **CLOSED.** Counsel (Andrew Flores) confirmed the current pricing is acceptable.
> The interim month-to-month-only rule is **lifted**: in-home Performance and Peak,
> individual and couples, may be sold and published as 3-month prepaid commitments.
> The attached condition is a **workflow rule, not a pricing cap** — contact counsel
> before filing a client on a contract exceeding $4,400. It now lives under CANON's
> WORKFLOW RULES as the CONTRACT VALUE CHECK, with the totals kept as a
> pricing-change checklist under RESOLVED ITEMS.

**Cal. Civ. Code 1812.86** caps a single health studio services contract at
**$4,400**. OmniFit's own Couples Prepaid Program Agreement cites this cap and
excludes in-home Performance and Peak couples on that basis.

### Prepaid 3-month totals against the cap

| Offer | 3-month total | vs $4,400 |
|---|---|---|
| Teqneeq Peak individual | $1,395 × 3 = **$4,185** | under, by **$215** |
| In-home Performance individual | $1,250 × 3 = $3,750 | under |
| Studio couples Performance | $1,250 × 3 = $3,750 | under |
| In-home couples Momentum | $875 × 3 = $2,625 | under |
| **In-home couples Performance** | **$1,725 × 3 = $5,175** | **OVER by $775** |
| **In-home Peak individual** | **$1,860 × 3 = $5,580** | **OVER by $1,180** (floor) |

### Open question for counsel

Whether 1812.86 reaches **in-home** personal training or only facility-based
services. That answer determines whether the two OVER rows are a real problem or a
non-issue. Both OVER rows are in-home; every facility-based offer clears.

### Interim rule

Do not publish or sell **in-home couples Performance** or **in-home Peak** as
3-month prepaid commitments. Month-to-month only. Couples Peak is already ad-hoc
only at both venues, so the in-home Peak restriction lands on the **individual**
tier.

**Status:** awaiting legal confirmation. Not a certification violation while listed.

### Verified against the repo

No certified page publishes in-home Peak or in-home Performance as a prepaid 3-month
commitment. The only repo hits are in `training-rates-san-diego.html:445` and `:552`,
which is uncertified, excluded from certification runs, and marked do-not-paste.
**Nothing live breaches the interim rule.**

### Headroom, worth watching

Teqneeq Peak individual clears by **$215**. Any rise past **$1,466/mo** crosses the
cap at 3 × monthly. In-home Peak at $1,860 is described as a **floor**, so its
overage can only grow. Both break points are recorded in CANON so a repricing run
checks before publishing.

### Also learned

The in-home **individual** ladder is now partly known and recorded: Performance
$1,250/mo and Peak $1,860/mo, alongside the existing "from $335". Momentum in-home
has not been supplied. CANON previously carried only the "from $335" entry point.

---

# CANON updates — counsel clearance and completed in-home ladder

## 1. RESOLVED-02 · cap exposure closed

Counsel (Andrew Flores) confirmed current pricing is acceptable. Applied:

- **Interim rule lifted.** In-home Performance and Peak, individual and couples, may
  now be sold and published as 3-month prepaid commitments. The
  "month-to-month ONLY" line is removed from CANON's couples block.
- **Counsel's condition recorded as a workflow rule, not a pricing constraint.** It
  sits under WORKFLOW RULES as the **CONTRACT VALUE CHECK**: contact counsel before
  filing a client on a contract exceeding $4,400. It restricts nothing about what may
  be published or sold.
- **Entry moved, not deleted.** DEFERRED-02 became RESOLVED-02 under a new
  RESOLVED ITEMS section, carrying the original 1812.86 reasoning and the open
  question about in-home versus facility-based scope. KNOWN DEFERRED ITEMS now holds
  DEFERRED-01 alone.
- **Headroom figures kept live** as a PRICING-CHANGE CHECKLIST.

## 2. In-home individual ladder completed

| Tier | 3-month | M2M | Upfront (3×) |
|---|---|---|---|
| Essential | $335 | $390 | $1,005 |
| Momentum | $650 | $755 | $1,950 |
| Performance | $1,250 | $1,425 | $3,750 |
| Peak | from $1,860 | $2,150 | $5,580 |

CANON previously held only "from $335". Momentum was the missing rung.

## Which offers now trip the CONTRACT VALUE CHECK

Recomputed across the completed ladder. **Two of eleven**, both in-home:

| Offer | 3-month total | Status |
|---|---|---|
| In-home Peak individual | $5,580 | triggers counsel call |
| In-home couples Performance | $5,175 | triggers counsel call |
| Teqneeq Peak individual | $4,185 | under, $215 clear |
| everything else | ≤ $3,750 | under |

**One number is worth remembering instead of the table:** the break point is the same
for every offer, since the total is always 3 × the monthly rate. **Any 3-month monthly
rate above $1,466 produces a total over $4,400.** Teqneeq Peak at $1,395 is the closest
under it. In-home Peak's $1,860 is a floor, so its total can only rise.

## Effect on published pages

None. No certified page publishes an in-home Peak or in-home Performance prepaid
figure, so lifting the restriction changes nothing that is live. The pages are now
*permitted* to carry those figures where previously they were not, which matters
whenever the rates page enters scope.
