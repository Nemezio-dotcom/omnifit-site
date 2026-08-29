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

---

# Tooling hardening run — em-dash re-audit and shape-based patterns

Three judgment calls confirmed and recorded in CANON with the signed Prepaid
Program Agreement as provenance: the widened `$150`/`$175` rule, removal of the
2.9% card fee (no processing fees are added to stated prices), and the upfront
billing inversion (the total is paid in a single upfront payment at signing).

## Certification now FAILS — 9 hits, none auto-fixed

Reported, not repaired, per instruction and CANON's report-and-stop rule.

### Em-dash, 4 hits, all `pages/how-it-works-pricing.html`

```
:215   You want measurable, sustainable results &mdash; not a 6-week quick fix
:223   You're looking for the cheapest option &mdash; a well-rated gym like Chuze…
:224   You want drop-in classes or a social fitness scene &mdash; F45 or Orangetheory…
:226   You want a 6-week crash program &mdash; we don't do short-term fixes
```

### lbs within 15 words of a timeframe, 5 hits

```
pages/in-home-personal-trainer-san-diego.html                   "20–30 pound"  near "4–6 weeks"
pages/headers/in-home-personal-trainer-san-diego-header.html    "20–30 pound"  near "4–6 weeks"
pages/private-personal-trainer-san-diego.html                   "20–30 lbs"    near "4–6 months"
pages/private-personal-trainer-san-diego.html                   "20–30 pounds" near "4–6 months"
pages/headers/private-personal-trainer-san-diego-header.html    "20–30 pounds" near "4–6 months"
```

These are the exact pattern CANON's compliance screen bans. **They survived Batch 2
on pages I certified as clean**, because the literal grep has no entry for them. The
header hits are the page text carried into FAQPage schema, so each page and its
header must be fixed together.

### Guarantee near an outcome promise: 0 in certified files

One hit on the excluded rates page, correctly exempted as DEFERRED-01.

## Why the em-dash re-audit needed two attempts

The first pass reported **zero**, which was wrong. Investigating the raw counts
showed 4 `&mdash;` present in a certified file, so the checker was clearing them.

The list-item exception was too permissive: it accepted any item starting with a
capital. `<li>You want X &mdash; not Y</li>` starts with a capital, so it passed as
a "Label — descriptor" item.

**First fix was also wrong.** Requiring Title Case caught the four, but then flagged
17 genuine labels — "Resting heart rate", "Desk-related posture patterns", "Acute
injury" — which are sentence-cased noun phrases.

**The working discriminator is grammatical, not typographic:** a label is a noun
phrase; the four violations are sentences beginning with a subject pronoun. The rule
now rejects items starting with `you / we / this / that / it / they / there / if /
when …` and accepts everything else that starts with a capital, plus anything
tag-wrapped in `<strong>`.

Also added: `&#8212;` and `&#x2014;` are now recognised alongside the literal
character and `&mdash;`. Both are currently zero across the repo, so this closes a
gap rather than fixing a hit.

## Rule tests

26 fixtures, both directions, all passing. Notably they now pin the cases that broke
each earlier attempt:

- genuine labels pass: `Grip Strength`, `BodyStat Body Composition`,
  `<strong>Post-PT professionals</strong>`, `Resting heart rate`,
  `Desk-related posture patterns`, `Trend, not diagnosis`, `Acute injury`
- prose is caught: `You want …`, `You're looking …`, `This is what we do …`,
  lowercase continuation, plain `<p>` prose
- `30-Day Fit Commitment` passes; `30-Day Performance Guarantee … stronger` is caught
- `20-30 lbs sustainably` passes; `20-30 pounds over 4-6 months` and
  `Dropped 27 lbs in 6 months` are caught; `Alo gained 18 lbs of lean muscle` passes

## What this says about earlier runs

Both shape classes existed in Batch 2 output and were reported as certified. The
literal grep is necessary but not sufficient: it catches known bad strings, never
bad *shapes*. Two of the five compliance strikes I found by eye during Batch 2 were
of exactly these classes, which is why the patterns were worth adding rather than
relying on manual reading.

---

# Certification simplified to three categories

Em-dashes downgraded to a silent voice preference: no longer scanned, flagged, or
reported. The four in `how-it-works-pricing.html` stay as they are. **DEFERRED-03
was never created** — it was only ever proposed in conversation, so there was
nothing to remove from CANON.

Certification now reports exactly (a) compliance strikes, (b) stale canon,
(c) broken structure. Anything else is a judgment call or handled silently.

Three compliance shapes added beyond the two already present: free-consultation
framing, prenatal/postpartum content, and uncertified specialty claims (asserting
OmniFit diagnoses, treats, prescribes, cures, rehabilitates, or provides physical
therapy or chiropractic). Negations and referral language are legal, so
"OmniFit does not diagnose conditions" and "we refer you back to your physical
therapist" both pass.

Category (c) also gained two checks that were previously done by hand: HTML
tag-balance, and header FAQPage mirroring the page FAQ in count, order and text.

**19 compliance rule fixtures pass in both directions.** Two bugs were caught by
those fixtures rather than in production:

1. Negation sitting *inside* a match was missed, because the context window
   excludes the match itself. "OmniFit does not diagnose" read as a claim.
2. `NEGATED` lacked word boundaries, so the bare alternative `no` matched inside
   **diag-no-se**, silently exempting every genuine "we diagnose" claim. A rule that
   fails open is worse than no rule; the fixtures are what surfaced it.

## Certification result

```
compliance 0 · stale canon 0 · structure 0   →  PASSED
```

30 files certified. Four remain uncertified: `training-rates-san-diego.html`,
`the-30-minute-executive-reset.html` and its header, and `footer.html`.

---

# Batch 3 — BLOCKED, not started

## All nine pages are absent from the repo

```
the-omnifit-method              ABSENT     weight-loss                      ABSENT
how-we-measure-your-progress    ABSENT     strength-training-1              ABSENT
omnifit-vs-competitors          ABSENT     hiit-personal-trainer-san-diego  ABSENT
personal-training-services      ABSENT     body-composition-testing         ABSENT
partners                        ABSENT
```

Your instruction was to list which are missing and proceed with the rest. **There is
no rest** — it is nine of nine, so no page-level work was possible.

Verified rather than assumed:

- Not on `main`, not on the working branch, and **never committed on any branch** —
  checked with `git log --all --diff-filter=A` per slug, zero results each.
- Only two refs exist on the remote, both pointing at commits that contain none of
  the nine.
- Pulling them in myself is not possible: this environment's egress proxy refuses
  all outbound hosts, re-verified this run (`CONNECT tunnel failed, response 403`).
  Files can only reach the repo by your push.

Nothing was invented, and no placeholder pages were created.

## Deferred: two repo copies are stale relative to production

`pages/training-rates-san-diego.html` and `pages/the-30-minute-executive-reset.html`
are excluded from scope and will stay excluded. The important distinction, now
recorded in CANON:

> These are **not** simply unpatched. The live versions on the domain are **ahead of
> the repo copies**. They need refreshing from live, not patching. A run that
> patched the repo copy would be carefully editing a version the site has already
> moved past, and could regress live content when pasted back.

This changes the fix from "apply the canon pass" to "replace the file from
production, then apply the canon pass". CANON's repo-state block now says so, so no
future run treats them as ordinary unpatched pages.

## Certification

Unchanged from the last run, since no page content was touched:

```
compliance 0 · stale canon 0 · structure 0   →  PASSED   (30 files)
```

## To unblock

Push or paste the nine pages. Everything else is ready: the canon pass, the Who This
Is For sections, header generation, and the shape-based compliance patterns, which
will be active from the first edit rather than retrofitted.

---

# Batch 3 — nine pages, full pass (August 2026)

Branch `claude/omnfit-4s-ranch-location-mxek1x`. Nine pages: the-omnifit-method,
how-we-measure-your-progress, omnifit-vs-competitors, weight-loss,
strength-training-1, hiit-personal-trainer-san-diego, personal-training-services,
body-composition-testing, partners.

## Certification

```
### SCOPE: 48 certified, 4 not yet certified
### (a) COMPLIANCE STRIKES   none
### (b) STALE CANON          none
### (c) BROKEN STRUCTURE     none
### RESULT: PASSED  (compliance 0 · stale canon 0 · structure 0)
```

Invariants recomputed from the files (not cached), all matching CANON:

```
9-point          10 files   1 hash   bd73ea51bc9ec5eb   matches
archetypes       10 files   1 hash   6b1b0f4efbd4a72c   matches
credentials      10 files   1 hash   6492e3ca1545dc26   matches
header pricing   11 files   1 hash   7e5de5984b133663   matches
page pricing     11 files   1 hash   ae388d31c0b6149e   matches
```

## STOPPED — two items needing your decision

### STOP-01 · The metric count cannot be reconciled without inventing product detail

CANON says 12 metrics. `how-we-measure-your-progress.html` is the page that
*enumerates* them, and it enumerates seven:

```
pages/how-we-measure-your-progress.html:168   "OmniFit tracks seven core progress metrics"
pages/how-we-measure-your-progress.html:182   "the same seven standardized metrics"
pages/how-we-measure-your-progress.html:184-190   Metric 01 … Metric 07  (seven cards)
pages/how-we-measure-your-progress.html:251   "We track seven standardized metrics: …"
```

while the same page already says twelve in four other places (lines 197, 237, 255,
256), and `the-omnifit-method.html:268` says *"across twelve metrics"* and then lists
the same **seven** categories.

The seven categories are: body composition, strength benchmarks, posture, mobility
and joint function, session adherence, nutrition compliance, subjective well-being.

I did not resolve this, because both available moves are wrong:

- Changing "seven" to "twelve" leaves a page claiming twelve and showing seven cards.
- Adding five metric cards means **inventing five products** you may not measure.
- Reverting to "seven" everywhere contradicts CANON and five other certified pages.

The likely explanation is that 12 counts individual *measures* and 7 counts
*categories* (body composition alone covers weight, body-fat %, and circumference).
If that's right, the fix is one sentence from you: either the list of 12, or
confirmation that the pages should say "twelve metrics across seven categories".

**Condition under which stopping was wrong:** if you consider the twelve already
settled and enumerable from the existing seven, this cost you a round trip.

### STOP-02 · `partners.html` offers a free training week that exists in no price list

```
pages/partners.html:1406   "Book Your Free Performance Week"
```

CANON's pricing has no free week, and the compliance screen bans free-consultation
framing. This is a bigger giveaway than the framing that was banned. I left it
exactly as-is rather than delete a promotion that might be real.

It is the only instance in the repo. Tell me whether it is a live offer, and I will
either keep it or replace the CTA with the canonical paid consultation.

## Compliance: 22 strikes cleared

All were the banned lbs-with-timeframe shape except one guarantee. The established
Batch 2 precedent was applied throughout: **the pounds figure survives as a goal
descriptor, the outcome timeframe is removed.**

| Page | Strikes |
|---|---|
| the-omnifit-method | 1 |
| how-we-measure-your-progress | 3 |
| omnifit-vs-competitors | 8 |
| weight-loss | 10 (9 lbs + 1 guarantee) |

Representative pairs:

```
- typically produces sustainable 20–30 lb fat loss … over 4–6 months
+ built for busy professionals 30+ … working toward sustainable fat loss of 20–30 lbs

- Realistic timeline … aiming for 20-30 lb fat loss:
  • Weeks 5-8: First measurable fat loss (4-6 lbs)
  • Weeks 9-16: Consistent 1-1.5 lbs/week fat loss
+ What the progression looks like … working toward sustainable fat loss:
  • Weeks 5-8: First measurable change in body composition
  • Weeks 9-16: Consistent downward trend in body composition

- Lose 20–30 pounds in 4–6 months through structured training …   (hero H1 subhead)
+ Sustainable fat loss through structured training …

- Programs that don't teach you … guarantee you'll need them forever
+ Programs that don't teach you … leave you needing them forever
```

The last one was a `guarantee` describing *competitors*, not an OmniFit promise, but
the word sat inside a fat-loss block where no reader-side parser can tell the
difference. Rewording cost nothing.

`we treat` on how-we-measure was rewritten as instructed:

```
- At OmniFit, we treat your program like a performance system.
+ At OmniFit Performance, we approach your program like a performance system.
```

## Stale canon: 4 real pricing errors found, 14 false positives ruled out

Two were caught by the rules; **two were found only by sweeping every dollar figure
on all nine pages against CANON**, which I did because the targeted rules only know
the specific tokens they were written for.

```
personal-training-services:337   $150–$175/session      → $165 studio · $195 in-home
omnifit-vs-competitors:785       $600-1200/month        → $250–$1,625/month
omnifit-vs-competitors:788       12-16 sessions (30 min) → 2-13 private 60-minute sessions
omnifit-vs-competitors:896       $1200/month ÷ 16 sessions → Performance tier, $950 ÷ ~9
```

The session-length error is worth flagging: **30 minutes is the virtual Executive
Reset format**, not in-person 1:1, which `corrective-exercise-post-rehab.html:859`
already establishes as 60 minutes.

Ruled out as legitimate: ten competitor figures inside `comp-value` blocks (F45,
Equinox, big-box PT) and four third-party device costs on body-composition-testing
(DEXA $100–200, gym scales $0–50, consumer devices $30–200).

`$90 → $110` on body-composition-testing ran to 11 instances, not the 10 expected.
Alongside it, per CANON's "rename settled": *OmniFit Performance Assessment* →
**Performance Diagnostic**, and the credit scope tightened from "any training
package" to "in full toward a 3-month package". I also removed *"making the
assessment effectively free for clients who train with us"* — a full credit is not
the same claim as free, and free-offer framing on a consultation-class product is
what the screen exists to stop.

## Structure

Document-wrapper stripping, exactly what was removed:

**omnifit-vs-competitors.html** — `<!DOCTYPE html>`, `<html lang="en">`, `<head>`,
`<meta charset>`, `<meta viewport>`, `<title>`, `<meta description>`, fonts
`<link>`, `</head>`, `<body>`, `</body>`, `</html>`.

**partners.html** — the same, plus `<link rel="canonical">`, and the `<body>` tag
carried `style="margin:0;padding:0;background:#0a1628"`.

Two things were preserved rather than dropped:

- On vs-competitors the **entire 423-line `<style>` block lived inside `<head>`**. A
  naive head-strip deletes all the page CSS. My first attempt did exactly that and
  crashed before writing (the fragment then had no `<style>` to anchor to), which is
  the only reason it was caught. The style block is now re-emitted at the top of the
  fragment.
- Both pages loaded fonts via a `<head>` `<link>`, which cannot survive in a Code
  Block. Each is now an `@import` at the top of the style block, matching every other
  certified page.
- The dropped `<body>` background on partners changes nothing: `#omnifit-partners`
  already sets `background: var(--navy-deepest) !important`, the same `#0a1628`.

SEO title, description, and canonical are preserved as `SQUARESPACE PAGE SETTINGS`
comments at the top of each fragment, since they belong in page settings, not the
Code Block.

Schema extraction: **8 inline `ld+json` blocks** removed from page bodies —
weight-loss 1, hiit 1, partners 6 — each page now carries a comment saying where the
markup went.

The partners `HealthAndBeautyBusiness` node was **not** carried into the header: it
redefined the business (`@id …/#organization`, and on the wrong host — no `www`),
which CANON forbids in a page header. The header references the homepage
`#localbusiness-of` like every other page. The two `Person` nodes **were** carried
over; they are partner facts that exist nowhere else.

Partner details verified against the page body, nothing invented: Dr. Damien
Jackson-Ricketts, DPT, OCS, of Stoke Physical Therapy, and Celeste Esposito, LMT, of
Serenity Massage. Schema and prose agree.

## Headers

Nine generated. FAQ counts: method 6, how-we-measure 6, vs-competitors 7,
weight-loss 8, strength 7, hiit 5, body-composition 8, partners 6.
`personal-training-services` has **no FAQ section at all**, so its header carries
WebPage and BreadcrumbList only — no empty FAQPage.

Three pages' FAQs were invisible to the old extractor, which knew three markup
patterns and needed five. vs-competitors uses `faq-question` divs and partners uses
`op-faq-q` buttons; both reported **zero FAQs** before I checked the markup directly.
Had I trusted the count, two headers would have shipped with their FAQs silently
missing. The new extractor was regression-tested against **all 16 existing headers**
and still mirrors every one.

## Use Cases

Added to all nine. The four card bodies are byte-identical to the private and
in-home pages — sha256 `9f5c077075371e0d…`, matching the recorded invariant. Only
the surrounding markup varies, because these pages use four different CSS
conventions (`fl`/`st`/`hiit`/`sv`/`bc` standard framework, `s-mid`+`dg`/`mg` on the
two dark pages, `comparison-grid` on vs-competitors, `op-*` on partners). Heading is
"What People Come to Coaching For" rather than the private-page "…Private Coaching…".

Verified against real CSS rather than assumed: only `bc` defines `-grid-2`, so the
others use their base grid class; `op-partners-grid` is a plain container, not a
grid, so the cards stack as the partner cards do.

## HIIT

Option 1 completed. Beyond the venue removals already reported, four residual
outdoor references were still live and are now gone:

```
:561  "…in 4S Ranch, outdoors, or virtually"      → "…in your home across North County, or virtually"
:569  "Studio, outdoor, or virtual"               → "Studio, in-home, or virtual"
:663  "Studio or outdoor"                         → "Studio or in-home"
:773  "What should I bring to an outdoor HIIT session?" → "…in-home HIIT session?"
:659  <!-- PACIFIC BEACH LOCATIONS -->            → <!-- WHERE HIIT SESSIONS HAPPEN -->
```

The Pacific Beach comment banner is the notable one: the *content* under it had been
replaced, but the banner survived and would have shipped a Pacific Beach reference
into a file CANON says must have zero.

## Judgment calls, each with the condition that makes it wrong

1. **Kept the pounds figure, dropped the timeframe.** Follows Batch 2 precedent.
   *Wrong if* you wanted pounds gone entirely from modality pages.

2. **Rewrote the sample progress report** on how-we-measure rather than deleting it.
   "Month 3 typically looks like… 225 → 204 lbs" is the strongest implied promise on
   the page. It is now a labelled sample layout, with the two lbs rows showing what
   is reported ("Weight & body-fat %", "Estimated 1RM") instead of a delta.
   *Wrong if* those were real, defensible figures you wanted shown.

3. **Removed "21.5 Pounds Lost"** from the client-outcomes block and dropped "at 4
   Months" from its heading, replacing the stat with "12 Metrics Tracked Monthly".
   *Wrong if* you have documentation for that average and want it public.

4. **Renamed the assessment to Performance Diagnostic** on body-composition-testing.
   CANON says "rename settled", but your instruction only said $90→$110.
   *Wrong if* the rename is not meant to reach this page yet.

5. **Derived the $110/session equivalent** on vs-competitors from the Performance
   tier ($950 ÷ ~9 sessions/month at 2/week). *Wrong if* you count sessions per
   month differently, which would shift the figure by a few dollars.

6. **Left four outcome claims that carry a timeframe but no pounds**, because the
   written screen bans lbs-with-timeframe specifically and I am not widening a rule
   past what CANON says:
   ```
   how-we-measure:168        "achieves sustainable body recomposition results within 4–6 months"
   how-we-measure:188/220    "90%+ session adherence", "87% Pain Reduction"
   strength-training-1:323   "Over 4–6 months: measurable increases in all major lifts"
   omnifit-vs-competitors:886 "measurable body composition changes within 6-8 weeks"
   ```
   `87% Pain Reduction` is the one I would look at hardest: it is an outcome stat in
   the shape of a clinical result, published by a non-clinician. *Wrong if* you want
   the screen read by intent rather than by letter, in which case say so and I will
   widen it.

## Certification rules changed this run

Four changes, each negative-tested in both directions before use.

1. **Timeframes must be quantified.** `years of inactivity` was firing the
   lbs-with-timeframe rule against legitimate persona copy. A timeframe now counts
   only when numerically bounded (`4-6 months`, `Weeks 5-8`, `Month 3`) or rate-framed
   (`per week`, `/week`).

2. **Contrastive timeframes are exempt.** `lose 20–30 pounds … Unlike 6-week
   challenges` describes what OmniFit is *not*. The marker must sit within two words
   of the timeframe, and **every other timeframe in the window is still checked** — so
   `Lose 20-30 lbs in 6 months, not a 6-week challenge` still flags. That fixture is
   in the suite specifically to prove the exemption cannot fail open.

3. **Travel-fee rule tightened** from "`$50`/`$75` anywhere on a line mentioning
   travel" to the figure being adjacent to the word. It was firing on
   `$50-80/session … no travel support`.

4. **`comp-value` blocks exempted** from the `$150`/`$175` check — competitor pricing
   on a comparison page is not OmniFit pricing. Deliberately *not* a
   range-based exemption, which would have hidden the real
   `In-studio $150–$175/session` error on personal-training-services.

Changes 2–4 all *narrow* the rules, which is the direction that risks failing open,
so each carries a fixture proving a real violation in the same shape still flags.

---

# Consultation correction + rule gap (August 2026)

Triggered by a human correction, not by a certification failure. That is the
finding: **the strike had already passed my own certification that morning.**

## The three checks that reported success while not looking

Recorded here because it is now a pattern, not an incident. All three are closed,
and `tools/README.md` carries the lesson forward.

| # | Check | Reported | Actually true |
|---|---|---|---|
| 1 | Header regression | "every header mirrors its page" | Compared **questions only**, never answers |
| 2 | Header re-mirror | "7 answers re-mirrored" | Wrote `null` over all 7, destroying the canonical pricing block |
| 3 | Free-framing rule | how-we-measure **certified clean** | Page said `free 45-minute assessment`; rule only knew the literal word `consultation` |

**#2 is the most serious**: a script I wrote silently replaced seven real answers
with `null`, including the canonical pricing block that is a hash-verified
invariant. It was caught by reading the diff, not by any check. The cause was the
FAQ extractor missing the `-faq-body` answer pattern used by every territory page
— a missing pattern does not raise, it yields a question with no answer. Reverted
from git; `qa_strict()` now refuses to emit a null answer at all.

**#3 is the reason for this run.** A literal-string rule is only as wide as the
vocabulary someone happened to think of. The page did not say "consultation", so
nothing fired.

The shared shape: a green result is worth nothing until the check has been seen to
fail on purpose. Every rule touched in this run was negative-tested in both
directions, and the new answer-mirror check was verified by deliberately
tampering with a header answer and confirming it was caught.

## TASK 1 — the strike

`pages/how-we-measure-your-progress.html`, inside `<section class="cta">`:

```
- Book a free 45-minute assessment and get your baseline metrics. No commitment. Just clarity on where you stand.
+ Book a paid 45-minute consultation, by video or phone. A $30 refundable deposit reserves your time. No commitment beyond that, just clarity on where you stand.
- Book Your Assessment          (anchor text; href unchanged)
+ Book Your Consultation
```

Two faults in one sentence: free-framing, and conflating the consultation with
the $110 Performance Diagnostic.

**Correction to the task's premise, verified rather than assumed:** that header
*does* carry a FAQPage (6 Q/A pairs). The stated reason for skipping the
re-mirror was wrong, but the conclusion holds — the header contains neither
`free` (0 occurrences) nor `Book Your Assessment` (0), because the CTA is not
part of the FAQ. No re-mirror required.

## TASK 2 — the widened rule

CANON (a) free-framing now reads: `free` within ~6 words of **consultation ·
assessment · screen · screening · session · diagnostic · call · intake**.

Negative-tested both directions. The old string flags; the replacement passes.
Two exemptions were needed once the rule met real copy, each tested:

- `feel free` — idiom, exempt only when "feel" immediately precedes, so
  `Book a free session` still flags.
- **hyphenated compound adjectives** — `distraction-free`, `injury-free`,
  `pain-free`. A real offer is written unhyphenated.

### Sweep across all files

The user reported exactly one instance, found by grep from outside the repo. My
sweep found **two more**, and both were rule defects rather than content:

```
pages/personal-trainer-4s-ranch.html:839   "every session happens in a private, distraction-free space"
pages/personal-trainer-carlsbad.html:210   "...and injury-free. Assessment-Driven Precision"
```

Neither is an offer. **No content was changed on either page** — the rule was
corrected instead. Hits in `CANON.md` and `REPORT.md` are the rule text and this
report describing themselves; documentation is not in certification scope.

After the TASK 1 fix: **0 free-framing hits across all 52 page/header files.**

## TASK 3 — consultation delivery mode

CANON now records: 45 minutes, always video or phone, never in person, preceded
by a client intake form, $30 refundable deposit, and **not** the movement screen.

`pages/corrective-exercise-post-rehab.html`, three edits. Neither CTA note sits
inside a FAQ answer and the header contains none of the strings, so **no
re-mirror was required** — verified, not assumed.

```
- 45-minute consultation · Includes movement assessment · No obligation        (:534)
- 45-minute consultation · Movement assessment included · No obligation        (:1063)
+ 45-minute consultation by video or phone · Movement screen booked separately · No obligation
```

Third edit, one line above the second CTA note, the same conflation in prose:

```
- We'll assess your movement, review your history, and build a corrective plan designed for your body.
+ We'll review your history and goals, and map out the corrective plan; the in-person movement screen is booked separately as part of the $110 Performance Diagnostic.
```

## STOPPED — the same conflation is inside a hash-verified invariant

Not fixed. Reporting and stopping, per workflow rules.

The credentials block contains:

> "Every program he builds starts with a **45-minute movement assessment** and
> follows the Assess, Correct, Build, Sustain framework..."

The 45 minutes belongs to the virtual consultation; the movement assessment is
the separate in-person Diagnostic. This is exactly what the new CANON line bans,
and it is **inside the 630-byte credentials invariant, hash `6492e3ca1545dc26`**.

14 pages carry the string; 10 of those are the invariant block:

```
inside credentials invariant (10):
  pages/corrective-exercise-post-rehab.html:830
  pages/personal-trainer-carlsbad.html:210        pages/personal-trainer-carmel-valley.html:282
  pages/personal-trainer-del-mar.html:318         pages/personal-trainer-encinitas.html:208
  pages/personal-trainer-fairbanks-ranch.html:282 pages/personal-trainer-la-jolla.html:335
  pages/personal-trainer-rancho-santa-fe.html:303 pages/personal-trainer-santaluz.html:210
  pages/personal-trainer-solana-beach.html:282
outside the invariant (4):
  pages/omnifit-vs-competitors.html:843,927       pages/personal-trainer-4s-ranch.html:690
  pages/strength-training-1.html:142              pages/the-30-minute-executive-reset.html:454
```

Fixing it means editing 14 pages, re-hashing the credentials invariant, and
updating CANON in the same commit — and it would put all 10 territory pages back
on the re-paste list. That is a decision, not a cleanup.

## Where intake-form copy would belong

Flagged only, not added, as instructed. The natural homes are the pages that
already describe booking: `how-it-works-pricing` (the process section),
`FAQs` (a "what happens after I book" answer), `the-omnifit-method` (Step 1, the
45-minute video consultation), and the CTA notes on the territory pages. The
territory-page CTA notes are the highest-value spot and the highest-cost, since
they would re-paste all ten.

## TASK 4 — tooling versioned

`tools/certify.py`, `tools/faq.py`, `tools/mkheaders.py`, `tools/README.md`.
CANON WORKFLOW RULES now points runs at it.

Two defects fixed in the move, both of which had been masked by monkeypatching:

- `certify.py` carried its **own three-pattern** FAQ extractor and was being
  patched at runtime to use the six-pattern one. It now imports `faq.py`, so
  certification and header generation cannot disagree about what a page's FAQ is.
- The mirror check compared **questions only**. CANON (c) requires "count, order
  **and text**", so answers were never checked — the same blind spot as incident
  #1, sitting in the certification tool itself. Answers are now compared, with
  whitespace normalised before punctuation (stripping `<a>` tags leaves a space
  before the period; that is an extraction artifact, not a mirroring failure).

Verified by tampering with one answer in the del-mar header and confirming
`[FAQPage answers do not mirror page] differing index=[1]`, then restoring.

---

# Rates Page Correction + Canon Pack Fix (August 2026)

`training-rates-san-diego.html` corrected and certified in. CANON's session-pack
line — wrong, not the live page — fixed first, since TASK 1 explicitly said so.

## TASK 1 — CANON's pack line was the error, not the page

CANON had a single ladder (5 @ $175, 10 @ $150, 20 @ $135) that turned out to be
a mangled merge: the in-home 5-pack rung and the studio 20-pack rung, with the
other four lost. The live page uses two ladders by venue:

```
Studio  — 5 @ 145/session (725) · 10 @ 140 (1,400) · 20 @ 135 (2,700)
In-home — 5 @ 175/session (875) · 10 @ 170 (1,700) · 20 @ 165 (3,300)
```

CANON's (b) exception list updated to match, and `$150` is now retired as a pack
rung outright — it belongs to neither ladder.

### The corrected rule immediately exposed a live pricing error

Widening the $150/$175 check to the real two-ladder structure surfaced **8
instances of the old single ladder on three other, already-certified,
already-pasted pages** — not touched by this run, since it was scoped to
`training-rates-san-diego.html` only, but too serious to fix silently or ignore.

```
pages/FAQs.html:183                                       FAQ answer text
pages/headers/FAQs-header.html:86                          schema mirror
pages/how-it-works-pricing.html:200                        quotable block
pages/how-it-works-pricing.html:399   <div class="pc-price">$150<span>/session</span></div>
pages/how-it-works-pricing.html:580                        FAQ answer text
pages/headers/how-it-works-pricing-header.html:54           schema mirror
pages/private-personal-trainer-san-diego.html:535           FAQ answer text
pages/headers/private-personal-trainer-san-diego-header.html:62  schema mirror
```

**`how-it-works-pricing.html:399` is not a mention — it is a rendered price
card.** The "10 Sessions" pack card on that live page currently displays
`$150/session` as the actual price, for a rung that exists in neither ladder
(studio 10-pack is $140, in-home is $170). This has very likely been showing an
incorrect price to real visitors since the page was pasted. **Reported here,
not fixed** — outside this run's scope, and a decision for a human, not
something to fix as a side effect of a documentation correction.

### Rule change, negative-tested

`$150` now gets no exemption beyond competitor pricing (`comp-value` divs) —
never via markers, cards, or the new packs-table context. `$175` gained a
`<table class="...packs...">` context for the in-home pack column. Eight
fixtures, both directions: the in-home $175 pack rung passes; a hypothetical
$150 inside the *same* packs table still flags, proving the new exemption
cannot be walked back onto the retired figure; legacy `pc-name` card and
`Bronze` marker regressions still pass; a bare unattributed $175 studio claim
still flags as the retired violation CANON already named.

## TASK 2 — guest add-on $50 → $75

Three named places, plus a fourth found and fixed as a judgment call (below).
Travel-fee rule checked against the corrected text — no false positive, since
the word "travel" never shares a line with the guest-addon price anywhere on
this page. No rule change needed.

```
pages/training-rates-san-diego.html
  :382   studio footnote        "Guest add-on: $50/session" → "$75/session"
  :492   in-home footnote       "Guest add-on: $50/session" → "$75/session"
  :689   add-ons grid card      "$50 /session" → "$75 /session"
  :777   FAQ answer (4th)       "guest for $50 per session" → "$75 per session"
pages/headers/training-rates-san-diego-header.html
  :395   FAQPage answer mirror  same change, to keep the header mirroring the page
```

**Judgment call — the fourth instance.** TASK 2 named three places; the FAQ
answer "Can I bring a guest to my training session?" states the same $50 price
a fourth time and is not one of them. Left alone, the page would say $75 in
three places and $50 in a fourth, on the same page, about the same thing.
Fixed it, and mirrored the header FAQPage answer to match, since leaving the
header at $50 would have broken the count/order/text mirror the moment the
page changed. **Wrong if** the FAQ price was meant to stay a legacy/grandfathered
rate distinct from the named-package guest add-on — nothing in the task or
CANON suggests that, but it's the reading under which this call fails.

The referral credit card ("$50 off your next month") is a **different, separate
offer** and was correctly left untouched — confirmed by content, not by line
number, since the two $50 figures sit four lines apart in the add-ons grid.

## TASK 3 — add-on prices recorded in CANON

```
Add-ons: extra session 115 studio / 155 in-home · guest add-on 75/session
Referral credit: 50 off next month — UNVERIFIED, not yet confirmed
```

The referral credit is recorded but not applied to anything — it was already
published at $50 and nothing about it needed changing; it is flagged so a
future run does not treat it as silently confirmed.

## TASK 4 — DEFERRED-01 applied verbatim, then resolved

**Correction to the task's premise, verified rather than assumed:** CANON said
the page's schema was "still body-embedded" with the third instance living in
the body block. It was not — the schema had already been extracted to
`pages/headers/training-rates-san-diego.html` (the live refresh landed it
there). All three instances located by content, since line numbers from the
old copy were stale as warned:

```
pages/training-rates-san-diego.html
  :663-664   body callout, heading + body    Executive Section
  :767       "Does OmniFit offer a money-back guarantee?" FAQ answer
pages/headers/training-rates-san-diego-header.html
  :379       the same FAQ answer, mirrored in the header's FAQPage schema
             (not "the body-embedded schema" — already in the header)
```

CANON's approved text applied exactly, no re-drafting. Callout heading became
"30-Day Fit Guarantee". Verified negative and positive: the old wording, tested
in isolation, still trips `guarantee_near_outcome` ('Guarantee' near
'stronger'); the resolved text produces zero hits on its own — it does not pair
"guarantee" with an outcome word, so it needs no exemption at all.

DEFERRED-01 moved to RESOLVED ITEMS with the full history retained. The
`DEFERRED-01 is exempt` line removed from (a), and the matching `DEFERRED_01`
regex and carve-out removed from `tools/certify.py` — an orphaned exemption for
an item that no longer needs one is a latent blind spot for whatever text
happens to match the pattern next.

## TASK 5 — "Class IIa medical device" removed

One instance, in the FAQ answer describing the Performance Assessment, mirrored
in the header. Both removed; surrounding "clinical-grade diagnostic session ...
using the BodyStat 1500 MDD for body composition analysis" reads cleanly
without the parenthetical.

**Count correction:** the task said "clinical-grade" appears four times; the
actual count is **five** (lines 242, 252, 737, 742, 772). Reported, not silently
corrected in the task text. Per instruction, none of the five were touched —
only the Class IIa descriptor.

**Judgment call.** Removed the regulatory-shaped claim exactly as instructed
and nothing more. **Wrong if** "clinical-grade" itself should also be reduced
given the corrected count is higher than assumed — that's explicitly a separate
decision per the task, not made here.

## TASK 6 — certified in, header renamed, two more premise corrections

**Correction #1.** TASK 6 said the page's schema "is still body-embedded" and
asked me not to extract it — same stale premise as TASK 4. There was nothing to
extract; it already lives in the header. No schema-extraction work was done or
skipped, because none was needed.

**Correction #2.** While updating CANON's REPO STATE for the sibling stale-page
entry (`the-30-minute-executive-reset.html`), checked rather than assumed: a
header file *already exists* for it
(`pages/headers/the-30-minute-executive-reset-header.html`, v1 August 2026,
complete WebPage/BreadcrumbList/FAQPage graph) — not "no header file yet" as
CANON previously read. Corrected that line while touching it; did not otherwise
investigate or change that file, per the explicit DO NOT.

**Naming fix sequencing, seen firsthand.** Brought the page into certification
scope, then ran certification *before* renaming the header — deliberately, to
test whether CANON's "fix naming after content certifies" rule is doing real
work. It is: with the header still named `training-rates-san-diego.html` (no
`-header` suffix), the header/page mirror check computed the wrong slug and
reported a **false structural error** — `[no matching page
pages/training-rates-san-diego.html.html]` — even though compliance and stale
canon were already clean. Renamed the header, re-ran: zero structural findings.
Fixing the name first would have hidden that check behind a filename bug
instead of a real pass.

**Additional fix, found by bringing the page into scope, not asked for
directly.** A leftover build-changelog comment at the top of the page named the
retired "Executive Hybrid" product ("V8 CHANGES: Executive Hybrid removed...").
It documented its own removal, not a reintroduction, but no other certified
page in the repo carries this style of dev-changelog comment, and Batch 3's
canon pass established precedent for scrubbing "Executive Hybrid" from
comments, not just rendered copy. Replaced with a one-line dated note.
**Judgment call — wrong if** that build history was wanted for internal
reference despite naming the retired product.

**Two rule gaps found and fixed, not content reworded.** Bringing the page in
exposed two `$175` instances the existing exemptions didn't recognise:

- `pages/training-rates-san-diego.html:619` — the Reset Bronze feature price
  sits one line below its `<h3>Bronze — Async Training</h3>` title, not on the
  same line. The marker check was same-line only. Widened to a 2-line lookback
  (`_marker_nearby`), which also correctly still flags a `$175` three lines
  after an unrelated "Bronze" mention, and still flags a `$150` sitting next to
  "Bronze" — proving the widened window doesn't accidentally rehabilitate the
  retired figure.
- `pages/headers/training-rates-san-diego-header.html:17` — the page's meta
  description says "virtual from $175/month", accurately describing the
  canonical Bronze tier, but matches no existing marker phrase. Added
  `"virtual from $175"` as a literal marker, consistent with the existing
  approach of specific marker phrases rather than a broader heuristic.

Both changes negative-tested; six fixtures, all passing in both directions.

`OUT_OF_SCOPE` in `tools/certify.py` updated to drop `training-rates-san-diego`.

## Certification

```
### SCOPE: 50 certified, 3 not yet certified
   not certified: pages/footer.html
   not certified: pages/headers/the-30-minute-executive-reset-header.html
   not certified: pages/the-30-minute-executive-reset.html

### (a) COMPLIANCE STRIKES   none
### (b) STALE CANON          8 hit(s) — all three pre-existing pages above,
                              none on training-rates-san-diego
### (c) BROKEN STRUCTURE     none
### RESULT: FAILED  (compliance 0 · stale canon 8 · structure 0)
```

Isolated: `pages/training-rates-san-diego.html` and its header individually
report **zero** compliance strikes and **zero** banned-string hits.

Invariants — unaffected by this run, training-rates-san-diego carries none of
the five shared blocks (it's the standalone rates table, not a territory page
or the summarized pricing FAQ):

```
9-point          10 files   1 hash   bd73ea51bc9ec5eb   matches CANON
archetypes       10 files   1 hash   6b1b0f4efbd4a72c   matches CANON
credentials      10 files   1 hash   6492e3ca1545dc26   matches CANON
header pricing   11 files   1 hash   7e5de5984b133663   matches CANON
page pricing     11 files   1 hash   ae388d31c0b6149e   matches CANON
```

---

# Ingest Consolidation Run — Report

**Branch:** `claude/consolidate-ingest-certification-njmhvr`
**Date:** Aug 2026
**Scope:** reconcile the repo with what is actually live — archive the retired
pages, bring the corrected pages into certification scope, teach the tooling
the ingest's structural exceptions, and report (not fix) every defect on the
newly scoped files.

> **This run fixed no page content.** Task 4 was explicitly report-only, and
> CANON's workflow rule is to report `file:line` and stop. Certification
> therefore ends **FAILED**, with a full inventory below. Nothing in `archive/`
> was modified, no previously certified page was edited, no canonical tags were
> added, no orphan header or changelog comment was deleted.

## 1. Certification result and invariant hashes

```
### SCOPE: 67 certified, 4 not yet certified
   not certified: pages/footer.html
   not certified: pages/headers/the-30-minute-executive-reset-header.html
   not certified: pages/llms-txt-page-retired.html
   not certified: pages/the-30-minute-executive-reset.html

...
### (c) BROKEN STRUCTURE
   (known orphan header, no page to mirror: pages/headers/bodybuilding-header.html)
   (known orphan header, no page to mirror: pages/headers/energy-protocol-waitlist-form-header.html)
   pages/headers/home-header.html  [FAQPage questions do not mirror page] page=11 schema=0
   pages/headers/home-header.html  [FAQPage answers do not mirror page] differing index=[]
   2 problem(s)

### INVARIANT HASHES
   page pricing     ae388d31c0b6149e
   header pricing   7e5de5984b133663
   credentials      6492e3ca1545dc26
   archetypes       6b1b0f4efbd4a72c
   9-point          bd73ea51bc9ec5eb

### RESULT: FAILED  (compliance 97 · stale canon 22 · structure 2)
```

All five invariants recomputed from the files and **matching CANON.md** — no
invariant was changed by this run, so no hash in CANON needed updating.

| Invariant | Hash | CANON |
|---|---|---|
| page pricing | `ae388d31c0b6149e` | matches |
| header pricing | `7e5de5984b133663` | matches |
| credentials | `6492e3ca1545dc26` | matches (`6492e3ca`, 630 bytes) |
| archetypes | `6b1b0f4efbd4a72c` | matches |
| 9-point screen | `bd73ea51bc9ec5eb` | matches |

`certify.py` now prints these every run rather than only on mismatch — a silent
invariant is how a check reports success without looking.

`python3 tools/negative_tests.py` — **27 fixtures, all passing**, each new
exemption paired with a case proving the check it exempts still fires.

## 2. Per-file table: what moved, what changed

### Moved to `archive/` (contents byte-identical, sha256 verified either side)

| From | To | sha256 |
|---|---|---|
| `pages/personal-trainer-mission-hills.html` | `archive/personal-trainer-mission-hills.html` | `6a79892d…` unchanged |
| `pages/headers/personal-trainer-mission-hills-header.html` | `archive/headers/personal-trainer-mission-hills-header.html` | `8349b81f…` unchanged |
| `pages/executive-hybrid-coaching.html` | `archive/executive-hybrid-coaching.html` | `612449d8…` unchanged |
| `pages/headers/executive-hybrid-coaching-header.html` | `archive/headers/executive-hybrid-coaching-header.html` | `391cfc80…` unchanged |
| `pages/online-training.html` | `archive/online-training.html` | `71fb7c6f…` unchanged |
| `pages/headers/online-training-header.html` | `archive/headers/online-training-header.html` | `6509aa97…` unchanged |

`online-training` and its header were present and were archived the same way.
`archive/README.md` added.

### Changed

| File | Change |
|---|---|
| `archive/README.md` | new — retired, never certified, never pasted, never corrected, URLs redirect |
| `CANON.md` | REPO STATE: ten pages into scope; archive recorded; `llms-txt-page-retired` recorded; "26 pairs" corrected to 25. New STRUCTURAL EXCEPTIONS section. New ACCEPTED-01/-02. DEFERRED-01 gains an OPEN DISCREPANCY note |
| `tools/certify.py` | structural exceptions encoded; multi-block JSON-LD; `file:line` on compliance findings; invariant hashes printed; accepted-exception mechanism; new page→header presence check |
| `tools/faq.py` | `<summary>` widened to `<summary …>` |
| `tools/negative_tests.py` | new — 27 both-directions fixtures |
| `tools/README.md` | two new failing-check incidents; exemption and matching rules documented |
| `REPORT.md` | this section |

**No page or header content was edited anywhere.** `git diff` over `pages/` and
`archive/` for this run is empty apart from the six renames.

## 3. Defect inventory — newly scoped files (report only, nothing fixed)

105 findings. **Read the count with this caveat:** `pages/case-studies.html`
and `pages/home-3.html` are **byte-identical** (`c82d5f32…`) — home-3 *is* the
case-studies block, duplicated as a homepage Code Block. Their 45 findings each
are the same 45 defects counted twice. Distinct defects: **60**.

| class | count | where |
|---|---|---|
| (a) lbs near timeframe | 91 | case-studies 45 · home-3 45 (same file) · desk-worker 1 |
| (a) result promised within a window | 1 | home-2 |
| (b) stale canon | 13 | all 13 inside changelog comments — see §4 |
| (c) broken structure | 2 | home-header |
| accepted exceptions excused | 0 | ACCEPTED-01/-02 are dormant; neither fires |

### (c) broken structure

| file:line | defect | detail |
|---|---|---|
| `pages/headers/home-header.html` | FAQPage questions do not mirror page | page = 11 questions (home-2 × 6, home-5 × 5), header schema = 0. The homepage FAQ is not in structured data at all. |
| `pages/headers/home-header.html` | FAQPage answers do not mirror page | same cause |

Everything else structural is clean: tag balance passes on all 67 in-scope
files, no invalid JSON, no LocalBusiness redefined outside the homepage, every
`about` reference that exists points at `#localbusiness-of`, and every in-scope
page has a header or a recorded reason not to.

### (a) + (b), full table

| file | defect class | file:line | exact string |
|---|---|---|---|
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:20` | '17 lbs' near '40-Year' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:20` | '17 pounds' near '4 Months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:20` | '248 to 231 lbs' near '4 Months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:21` | '18 lbs' near '12 Months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:21` | '18 pounds' near '12 Months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:24` | '27 pounds' near '6 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:24` | '225 to 198 lbs' near '6 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:25` | '21 pounds' near '6 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:25` | '181 to 160 lbs' near '6 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:26` | '14 lbs' near '3 Months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:26` | '14 pounds' near '3 Months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:26` | '162 to 148 lbs' near '3 Months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:27` | '11 pounds' near '6 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:28` | '2 lbs' near '29-Year' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:28` | '6 lbs' near 'a Week' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:237` | '17 lbs' near '40-Year' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:244` | '17 lbs' near '4-month' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:253` | '17 lbs' near '4 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:253` | '231 lbs' near '4 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:255` | '17 pounds' near '40-year' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:268` | '18 lbs' near '12 Months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:275` | '18 lbs' near '12-month' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:284` | '18 lbs' near '12 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:286` | '18 pounds' near '12 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:361` | '27 lbs' near '6-month' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:368` | '27 lbs' near '6-month' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:394` | '27 lbs' near '6 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:394` | '198 lbs' near '6 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:404` | '27 pounds' near '6 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:425` | '21 lbs' near '6-month' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:452` | '21 lbs' near '6 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:452` | '160 lbs' near '6 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:462` | '21 pounds' near '6 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:476` | '14 lbs' near '3-month' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:483` | '14 lbs' near '3-month' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:510` | '14 lbs' near '3 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:510` | '148 lbs' near '3 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:520` | '14 pounds' near '3 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:541` | '11 lbs' near '6-month' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:542` | '6 lbs' near '6-month' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:578` | '11 pounds' near '6 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:578` | '6 pounds' near '6 months' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:605` | '2 lbs' near 'week 12' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:612` | '2 lb' near '12-week' |
| `pages/case-studies.html` | (a) lbs near timeframe | `pages/case-studies.html:623` | '6 lb' near '12 weeks' |
| `pages/desk-worker-posture-pain.html` | (a) lbs near timeframe | `pages/desk-worker-posture-pain.html:409` | '18 lbs' near '/week' |
| `pages/headers/home-header.html` | (b) stale canon | `pages/headers/home-header.html:6` | [OmniFit Personal Fitness Training] - Brand: "OmniFit Personal Fitness Training" → "OmniFit Performance" |
| `pages/headers/home-header.html` | (b) stale canon | `pages/headers/home-header.html:13` | [Orthopedic Exercise] - Credentials: ACE "Orthopedic Exercise Specialist" → ACE CES (confirmed); |
| `pages/headers/home-header.html` | (b) stale canon | `pages/headers/home-header.html:16` | [Pacific Beach] - areaServed: Pacific Beach/Mission Bay → 4S Ranch + North County corridor. |
| `pages/home-1.html` | (b) stale canon | `pages/home-1.html:7` | [$90 ] - CTA Step 1 wording cleaned; $90 Performance Diagnostic FLAGGED pending canonical pricing doc |
| `pages/home-1.html` | (b) stale canon | `pages/home-1.html:8` | [Executive Hybrid] - Executive Hybrid CONFIRMED dead: Card 6 relinked to /the-30-minute-executive-reset; add 301 for old slug |
| `pages/home-1.html` | (b) stale canon | `pages/home-1.html:9` | [$90 ] - PRICING (Aug 2026 canonical doc): Performance Diagnostic $90 → $110, credited in full toward a 3-month packa |
| `pages/home-1.html` | (b) stale canon | `pages/home-1.html:15` | [$90 ] - CTA: consultation kept primary; $90 Performance Diagnostic added as Step 2 |
| `pages/home-1.html` | (b) stale canon | `pages/home-1.html:422` | [Executive Hybrid] <!-- Executive Hybrid retired: card now links to the live Executive Reset page. 301 /executive-hybrid-coaching |
| `pages/home-2.html` | (b) stale canon | `pages/home-2.html:10` | [$90 ] - PRICING (Aug 2026 canonical doc): Performance Diagnostic $90 → $110, credited in full toward a 3-month packa |
| `pages/home-2.html` | (b) stale canon | `pages/home-2.html:13` | [ACE OES] - Cred chip: "ACE CES" → "ACE OES" (superseded: ACE later reissued as CES, see v3) |
| `pages/home-2.html` | (a) result promised within a window | `pages/home-2.html:288` | 'produces measurable change' near '30 days' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:20` | '17 lbs' near '40-Year' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:20` | '17 pounds' near '4 Months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:20` | '248 to 231 lbs' near '4 Months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:21` | '18 lbs' near '12 Months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:21` | '18 pounds' near '12 Months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:24` | '27 pounds' near '6 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:24` | '225 to 198 lbs' near '6 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:25` | '21 pounds' near '6 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:25` | '181 to 160 lbs' near '6 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:26` | '14 lbs' near '3 Months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:26` | '14 pounds' near '3 Months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:26` | '162 to 148 lbs' near '3 Months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:27` | '11 pounds' near '6 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:28` | '2 lbs' near '29-Year' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:28` | '6 lbs' near 'a Week' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:237` | '17 lbs' near '40-Year' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:244` | '17 lbs' near '4-month' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:253` | '17 lbs' near '4 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:253` | '231 lbs' near '4 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:255` | '17 pounds' near '40-year' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:268` | '18 lbs' near '12 Months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:275` | '18 lbs' near '12-month' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:284` | '18 lbs' near '12 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:286` | '18 pounds' near '12 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:361` | '27 lbs' near '6-month' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:368` | '27 lbs' near '6-month' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:394` | '27 lbs' near '6 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:394` | '198 lbs' near '6 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:404` | '27 pounds' near '6 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:425` | '21 lbs' near '6-month' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:452` | '21 lbs' near '6 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:452` | '160 lbs' near '6 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:462` | '21 pounds' near '6 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:476` | '14 lbs' near '3-month' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:483` | '14 lbs' near '3-month' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:510` | '14 lbs' near '3 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:510` | '148 lbs' near '3 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:520` | '14 pounds' near '3 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:541` | '11 lbs' near '6-month' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:542` | '6 lbs' near '6-month' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:578` | '11 pounds' near '6 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:578` | '6 pounds' near '6 months' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:605` | '2 lbs' near 'week 12' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:612` | '2 lb' near '12-week' |
| `pages/home-3.html` | (a) lbs near timeframe | `pages/home-3.html:623` | '6 lb' near '12 weeks' |
| `pages/home-4.html` | (b) stale canon | `pages/home-4.html:11` | [180+] - Reviews: 180+ → 190+ everywhere (schema reviewCount, description, quotable, stats bar) |
| `pages/home-4.html` | (b) stale canon | `pages/home-4.html:30` | [OmniFit Personal Fitness Training] - Business name: OmniFit Personal Fitness Training → OmniFit Performance |
| `pages/home-4.html` | (b) stale canon | `pages/home-4.html:31` | [Pacific Beach] - Location: Pacific Beach (2123 Garnet Ave) → 4S Ranch / Teqneeq (10772 Thornmint Rd) |

TOTAL ROWS: 105  (accepted: 0)

## 4. Changelog comments — inventory only, nothing deleted

The `v2`/`v3` comment blocks restate previously removed claims **verbatim**, and
they ship in the production HTML source where crawlers read them. A crawler
reading `pages/home-4.html` finds the string `OmniFit Personal Fitness Training
→ OmniFit Performance` and `Pacific Beach (2123 Garnet Ave)` in the page source,
which is precisely what the brand and NAP sweeps were for.

**35 lines across 10 files.** Every one of the 13 stale-canon hits on the newly
scoped files is one of these — there is not a single stale-canon hit in
customer-visible copy on any newly scoped page.

| file:line | restated removed claim(s) | verbatim comment text |
|---|---|---|
| `pages/footer.html:6` | BNI | `<!-- Changelog v2: removed footer-badges block (NASM / ACE / BNI) and its CSS;` |
| `pages/footer.html:7` | OmniFit Personal Fitness Training, Pacific Beach | `replaced legacy "OmniFit Personal Fitness Training" Pacific Beach GBP link` |
| `pages/headers/home-header.html:6` | OmniFit Personal Fitness Training | `- Brand: "OmniFit Personal Fitness Training" → "OmniFit Performance"` |
| `pages/headers/home-header.html:8` | Garnet | `- NAP: 2123 Garnet Ave, PB 92109 → 10772 Thornmint Rd, San Diego 92127 + geo updated` |
| `pages/headers/home-header.html:9` | 142/151 | `- Reviews: 142/151 → 190+ (aggregateRating reviewCount 190; description says 190+)` |
| `pages/headers/home-header.html:10` | $80-$125 | `- Pricing: "$80-$125 per session" era is DEAD. priceRange + offer catalog rebuilt` |
| `pages/headers/home-header.html:11` | Foundation Monthly | `from the Aug 2026 canonical doc. Retired product names (Foundation Monthly,` |
| `pages/headers/home-header.html:12` | VIP 6-Month | `Performance 3-Month, VIP 6-Month) removed.` |
| `pages/headers/home-header.html:13` | Orthopedic Exercise | `- Credentials: ACE "Orthopedic Exercise Specialist" → ACE CES (confirmed);` |
| `pages/headers/home-header.html:16` | Pacific Beach | `- areaServed: Pacific Beach/Mission Bay → 4S Ranch + North County corridor.` |
| `pages/headers/training-rates-san-diego-header.html:8` | $50 | `V2 CHANGES: guest add-on FAQ answer corrected $50 -> $60 per session` |
| `pages/home-1.html:7` | $90  | `- CTA Step 1 wording cleaned; $90 Performance Diagnostic FLAGGED pending canonical pricing doc` |
| `pages/home-1.html:8` | Executive Hybrid | `- Executive Hybrid CONFIRMED dead: Card 6 relinked to /the-30-minute-executive-reset; add 301 for old slug` |
| `pages/home-1.html:9` | $90  | `- PRICING (Aug 2026 canonical doc): Performance Diagnostic $90 → $110, credited in full toward a 3-month package; starting-at line added ($250/mo = Teqneeq Esse` |
| `pages/home-1.html:11` | 100+, BNI | `- Trust strip: 100+ → 190+ 5-Star Reviews; "BNI Del Mar" removed` |
| `pages/home-1.html:15` | $90  | `- CTA: consultation kept primary; $90 Performance Diagnostic added as Step 2` |
| `pages/home-1.html:422` | Executive Hybrid | `<!-- Executive Hybrid retired: card now links to the live Executive Reset page. 301 /executive-hybrid-coaching to /the-30-minute-executive-reset in Squarespace ` |
| `pages/home-2.html:6` | 20–30 | `- COMPLIANCE: "20–30 lb over 4–12 months" outcome claim removed from quotable (attorney screen: no lbs-in-timeframe claims)` |
| `pages/home-2.html:7` | free consultation | `- COMPLIANCE: all "free consultation" framing removed ($30 refundable deposit is the qualification filter, not a free offer)` |
| `pages/home-2.html:9` | lose 25 lbs | `- "lose 25 lbs" sample goal replaced with non-numeric example` |
| `pages/home-2.html:10` | $90  | `- PRICING (Aug 2026 canonical doc): Performance Diagnostic $90 → $110, credited in full toward a 3-month package; $30 deposit CONFIRMED` |
| `pages/home-2.html:13` | ACE OES | `- Cred chip: "ACE CES" → "ACE OES" (superseded: ACE later reissued as CES, see v3)` |
| `pages/home-4.html:11` | 180+ | `- Reviews: 180+ → 190+ everywhere (schema reviewCount, description, quotable, stats bar)` |
| `pages/home-4.html:15` | 20–30 | `- COMPLIANCE: "most clients lose 20–30 pounds over 4–6 months" outcome claim removed` |
| `pages/home-4.html:18` | 97.8% | `- Stats bar: "97.8% Client Satisfaction" REPLACED with "3/10 Pain Ceiling Rule".` |
| `pages/home-4.html:19` | 97.8% | `(97.8% is Gemini sentiment share from Semrush, not a client satisfaction survey.` |
| `pages/home-4.html:30` | OmniFit Personal Fitness Training | `- Business name: OmniFit Personal Fitness Training → OmniFit Performance` |
| `pages/home-4.html:31` | Garnet, Pacific Beach | `- Location: Pacific Beach (2123 Garnet Ave) → 4S Ranch / Teqneeq (10772 Thornmint Rd)` |
| `pages/home-5.html:5` | 20-30 | `- COMPLIANCE: "1-2 lb/week ... 20-30+ lbs in 4-6 months" results answer replaced` |
| `pages/the-30-minute-executive-reset.html:12` | $175 | `built around travel and packed calendars. From $175/month. NASM Elite Trainer.` |
| `pages/the-30-minute-executive-reset.html:16` | $175 | `A. TIER FREQUENCIES CONFIRMED (Aug 2026): Bronze $175 async, Gold $449 = 1 live` |
| `pages/the-30-minute-executive-reset.html:26` | Executive Hybrid | `Executive Hybrid was retired and 301s here. Confirm the framing reads right.` |
| `pages/training-rates-san-diego.html:4` | 2.9%, Executive Hybrid | `<!-- V8 CHANGES: Executive Hybrid removed (both venues + FAQ + schema) · 2.9% card fee removed everywhere · Monthly Tune-Up added after Session Packages · Tune-` |
| `pages/training-rates-san-diego.html:5` | $50 | `<!-- V9 CHANGES: Guest add-on corrected $50 → $60 in 4 locations (studio footer · in-home footer · add-on card · guest FAQ). NOTE: apply same fix to FAQ JSON-LD` |
| `pages/weight-loss.html:9` | 20-30 | `without crash dieting," "losing 20-30 lbs sustainably,"` |

TOTAL LINES: 35 across 10 files

Three notes on that table:

- `pages/weight-loss.html:9` is **not** a defect. It restates persona language
  ("losing 20-30 lbs sustainably") which CANON explicitly keeps legal — persona
  language without a timeframe. Listed for completeness only.
- `pages/training-rates-san-diego-header.html:8` and
  `pages/training-rates-san-diego.html:5` both record the guest add-on as
  corrected **`$50 → $60`**. CANON says the guest add-on is **$75** ("was $50,
  corrected in the Rates Page Correction run"). The comments record a figure
  that is in neither the old nor the current canon. Reported, not touched.
- `pages/footer.html` and `pages/the-30-minute-executive-reset.html` are out of
  certification scope but their comments ship all the same, so they are listed.

## 5. `JJ4E LLC`

One occurrence, repo-wide:

```
pages/llms-txt-page-retired.html:42
# OmniFit Training © 2025 JJ4E LLC (DBA OmniFit Personal Fitness Training)
```

Not changed — a legal entity question, not a canon one. The same file also
carries, at the same lines, three things a future run will want to decide on
together with it:

```
pages/llms-txt-page-retired.html:31   Pacific Beach, Mission Bay, Kate Sessions Park…
pages/llms-txt-page-retired.html:37   Contact: hello@omnifittraining.com   (canon: nemezio@)
pages/llms-txt-page-retired.html:42   DBA OmniFit Personal Fitness Training
```

## 6. Pre-existing failures on previously certified pages

**The previously certified pages do not currently pass.** Run in isolation over
the 25 certified page/header pairs: structure **0**, all five invariants
matching, but **14 findings** — every one of them present in the baseline run
before this run changed anything, and none of them introduced by it.

| file:line | class | detail |
|---|---|---|
| `pages/training-rates-san-diego.html:664` | (a) outcome guarantee | `'Guarantee' near 'energized'` |
| `pages/training-rates-san-diego.html:767` | (a) outcome guarantee | `'guarantee' near 'stronger'` |
| `pages/training-rates-san-diego.html:768` | (a) outcome guarantee | `'Guarantee' near 'stronger'` |
| `pages/headers/training-rates-san-diego-header.html:378` | (a) outcome guarantee | `'guarantee' near 'stronger'` |
| `pages/headers/training-rates-san-diego-header.html:381` | (a) outcome guarantee | `'Guarantee' near 'stronger'` |
| `pages/training-rates-san-diego.html:4` | (b) Executive Hybrid | in the V8 changelog comment |
| `pages/FAQs.html:183` | (b) $150 | pre-existing, documented in tools/README.md |
| `pages/headers/FAQs-header.html:86` | (b) $150 | pre-existing |
| `pages/how-it-works-pricing.html:200` | (b) $150 | pre-existing |
| `pages/how-it-works-pricing.html:399` | (b) $150 | pre-existing — a rendered `$150/session` price card |
| `pages/how-it-works-pricing.html:580` | (b) $150 | pre-existing |
| `pages/headers/how-it-works-pricing-header.html:54` | (b) $150 | pre-existing |
| `pages/private-personal-trainer-san-diego.html:535` | (b) $150 | pre-existing |
| `pages/headers/private-personal-trainer-san-diego-header.html:62` | (b) $150 | pre-existing |

The eight `$150` hits are the ones `tools/README.md` already records as
surfaced-but-unfixed by the pack-rule widening.

**The five guarantee strikes are new information.** CANON records DEFERRED-01 as
CLOSED with the approved rewording applied. History says it was applied
(`7b8f6c8` on the page, `e288599` on the header) and then **overwritten on 23
Aug 2026** by `6a0fd2a` and `1e3d88e`, two "Update training-rates-san-diego"
commits that re-pasted the live version over the corrected copy:

```
-  <h4>30-Day Fit Guarantee</h4>
+  <h4>30-Day Executive Performance Guarantee</h4>
-  …you decide it isn't the right fit, you can cancel and receive a refund of
-  the unused balance… There is no compliance test to pass…
+  …if after 30 days of full compliance you don't feel clearly stronger, more
+  energized, and more in control…
```

The implication is not repo hygiene: the approved text never reached
Squarespace, so **the live rates page still carries the banned wording**.
Fixing the repo copy alone will not fix the site — the corrected text has to be
pasted. Left unfixed here because previously certified pages were out of this
run's scope; recorded in CANON under DEFERRED-01 as an OPEN DISCREPANCY.

## 7. Judgment calls, each with the condition under which it is wrong

1. **Headers archived to `archive/headers/`, not flat `archive/`.** The
   instruction said "move to `archive/`". Nesting mirrors the source layout and
   keeps each page/header pair obvious. *Wrong if* anything downstream expects a
   flat `archive/` directory.

2. **`llms-txt-page-retired.html` put out of certification scope rather than
   archived or certified.** It was in `certify.py`'s glob but has never been in
   CANON's REPO STATE, so tool and brief disagreed. It is a retired `llms.txt`
   body, not a page, and the task named it nowhere. Excluding it keeps 20-odd
   phantom stale-canon hits out of the real inventory; its contents are reported
   in §5 instead. *Wrong if* this is meant to be a live page — then it belongs in
   scope and needs a brand, NAP, contact-address and entity pass.

3. **The homepage FAQ mirror is reported as a structural defect, not exempted.**
   Task 3 said `home-header.html` is the header for all five blocks, which the
   tooling now encodes. It does not say the homepage FAQ is exempt from
   mirroring, and 11 questions with no FAQPage in the header is a real
   structured-data gap. *Wrong if* the homepage FAQ is deliberately unmarked-up,
   in which case `home` belongs in a mirror-exempt list next to the orphans.

4. **A new page→header presence check was added.** Task 3 required the tooling
   to know that `case-studies` and `home-3` are not missing headers. Nothing
   checked page→header at all, so the exemption had nothing to attach to; the
   check gives it meaning and is negative-tested. It flags nothing else in the
   repo. *Wrong if* headerless pages are common and intended, in which case the
   check produces noise rather than signal.

5. **The two hsa-fsa accepted exceptions were recorded but are dormant.** Under
   the rules as they stand, neither string fires: `RESULT` does not match "so
   timing matters", and the `diagnose` pattern requires a subject within two
   words and treats the negation as legal already. They are recorded as
   instructed so a future widening cannot re-flag settled copy. *Wrong if* the
   intent was for the rules to be widened until those strings DO fire and only
   then be excused — that would be a rule change this run was not asked to make.

6. **The 91 `lbs near timeframe` hits on case-studies/home-3 are reported, not
   excused.** CANON's CANONICAL TRUTH block lists the case-study figures *with*
   their timeframes ("Mark −17 lbs (248→231, 4mo)") as canonical, while the
   COMPLIANCE SCREEN bans lbs-with-timeframe outright. The page publishes them
   as "Dropped 17 lbs (248 → 231 lbs) in 4 months". **CANON contradicts itself
   here and this run did not resolve it** — that is an attorney question, not a
   tooling one. *Wrong if* documented historical client results are considered
   outside the screen, in which case case-studies needs a named accepted
   exception rather than 45 open findings.

7. **The ingest was described as 20 files; 24 were found** outside certification
   scope (14 pages, 10 headers, counting `llms-txt-page-retired` and the two
   orphan headers). All 24 are accounted for above. *Wrong if* a specific
   20-file manifest exists that this run should have reconciled against instead
   of the repo's own contents.
