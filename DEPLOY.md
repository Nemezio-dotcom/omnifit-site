# Deploying omnifittraining.com as a static site on Cloudflare Pages

This repo now builds a complete static site into `public/`. Nothing in
`pages/` or `pages/headers/` was rewritten: every page body, its CSS and its
JSON-LD are carried into `public/` byte-for-byte (verified at build time), and
the shared header, nav and footer are wrapped around them from one source.

## How the build works

```
pages/<slug>.html                 page body (the Squarespace Code Block)
pages/headers/<slug>-header.html  page header injection (JSON-LD etc.)
pages/headers/site-header.html    site-wide header injection (GTM, Clarity,
                                  HubSpot deferral, geo meta, entity graph)
pages/footer.html                 site-wide footer (CSS + markup + year script)
pages/home-1..6.html              homepage sections
site/layout.html                  the HTML document skeleton
site/nav.html                     site header + primary nav (single source)
site/site.css, site/site.js       shared CSS / JS
build.py                          stdlib-only build + checks
public/                           generated output (committed)
```

```
python3 build.py            # rebuild public/ and print the check report
python3 build.py --check    # run only the checks against public/
```

Per page, `build.py` produces `public/<slug>/index.html` (homepage at
`public/index.html`) containing: doctype, `<title>`, meta description,
canonical, the site-wide header injection, one Google Fonts link (union of
every weight the pages used, plus Bebas Neue), `/assets/site.css`, the page's
header injection verbatim, the page's own `<style>` blocks (moved from the body
into `<head>`, with their Google Fonts `@import` lines dropped because the
layout already loads the fonts), then nav, `<main>` with the page body, footer,
and `/assets/site.js`.

The page-level `#wrapper-id ... !important` scoping was left in place on
purpose: it is what guarantees the rendered result is identical, and with no
Squarespace template to fight it is harmless. De-scoping it page by page can be
a later pass.

Only three things differ from the pasted sources, all structural:

1. `<style>` / `<link>` tags lifted from body to head (see above).
2. Internal links to slugs that exist nowhere in the repo are repointed at
   build time (`LINK_FIXES` in `build.py`; the `pages/` sources are untouched):
   `/personal-trainer-in-pacific-beach` -> `/personal-trainer-4s-ranch`
   (its link text already reads "4S Ranch Training"), and on the partners page
   `/services` -> `/personal-training-services`, `/how-it-works` ->
   `/how-it-works-pricing`, `/contact` -> `/contactform`, `/hybrid-coaching`
   -> `/the-30-minute-executive-reset`.
3. `terms-and-conditions` was a Squarespace TEXT page with no CSS of its own,
   so it is wrapped in `<div class="omni-text-page">` and styled from
   `site.css` in the design system (Playfair headings, Montserrat body).

Two small additions in `site.css` are judgment calls, flagged here:

- `#omni-faq{background:#fff}`: the homepage FAQ section (`home-5`) is
  authored in navy text with no background of its own, i.e. for a light
  Squarespace section. On the navy body it would be unreadable.
- `main{overflow-x:clip}`: Squarespace clipped each section horizontally.
  Without it the decorative 500px hero glow on the territory pages and the
  step row on the 4S Ranch page produce a horizontal scrollbar at phone widths.

## Cloudflare Pages settings

| Setting | Value |
|---|---|
| Framework preset | None |
| Build command | *(leave empty)* - `public/` is committed |
| Build output directory | `public` |
| Root directory | `/` (repo root) |
| Production branch | `main` |
| Environment variables | none required |

Optional alternative: set the build command to `python3 build.py` so Cloudflare
regenerates `public/` on every deploy (Python 3 is in the Pages build image).
Either way the output directory is `public`.

`public/_redirects` uses Cloudflare Pages syntax (`/old /new 301`).
Cloudflare serves `public/<slug>/index.html` at `/<slug>` and 308-redirects
`/<slug>/` to `/<slug>`, which matches the canonical URLs.

## Manual steps (you)

1. **Create the Pages project** from `nemezio-dotcom/omnifit-site` with the
   settings above. Deploy once to the `*.pages.dev` preview and click through.
2. **Review the nav.** The Squarespace template's header/nav was never in this
   repo and the live site could not be fetched from the build environment, so
   `site/nav.html` is a placeholder built in the design system (Bebas Neue
   wordmark, Montserrat links, gold CTA). Match its labels, order, dropdowns
   and CTA to the live header, then `python3 build.py`.
3. **Pages that live only in Squarespace** (block-built, no Code Block in the
   repo). They are linked from the repo and need to exist before launch or the
   links 404: `/privacy-policy` (footer, every page), `/behavior-change-coaching`
   (how-we-measure-your-progress, outcomes), `/is-omnifit-right-for-you`
   (contactform). Also `/bodybuilding` and `/energy-protocol-waitlist` have
   headers in the repo but no page. Paste each live page into
   `pages/<slug>.html` (plus its header) and rebuild, or add a redirect.
4. **Homepage hero.** The repo holds the homepage only as the six section
   fragments (`home-1`..`home-6`). Whatever sits above `home-1` on the live
   homepage (Squarespace hero / H1) is not here; paste it in as `home-0` and
   add it to `HOME_ORDER` in `build.py`.
5. **Images are hotlinked from Squarespace.** 25 distinct
   `images.squarespace-cdn.com` URLs are referenced across 39 pages. They will
   break when the Squarespace subscription ends. Download them, put them under
   `public/assets/img/`, and update the references before cancelling.
6. **Analytics / embeds.** Preserved exactly: GTM `GTM-5P4CKPT2`, Microsoft
   Clarity `ulpgsrkd98` and the HubSpot loader (portal 244441037) on every
   page; the HubSpot form (portal 244441037, form
   `a34ea6d0-e63f-46d1-83d4-c675a27d64bb`) on `/contactform` and
   `/personal-trainer-4s-ranch`; Calendly links on every page. **Not in the
   repo:** a direct GA4 tag for property 392866825 (it must be firing from the
   GTM container, confirm in GTM), and any Jotform or Trainerize embed (no
   iframe or script for either exists in any page; Trainerize appears only as
   text). If those were Squarespace-injected, add them to
   `pages/headers/site-header.html` and rebuild.
7. **Squarespace URL mappings.** Everything found in the repo is in
   `public/_redirects`. Export the live Squarespace URL Mappings list and add
   any extra lines.
8. **Domain.** Add `www.omnifittraining.com` as the custom domain in Pages,
   move DNS to Cloudflare (or CNAME `www` to the `pages.dev` host), and add a
   redirect rule for the apex `omnifittraining.com` -> `https://www.omnifittraining.com`.
9. **Search Console.** Submit `https://www.omnifittraining.com/sitemap.xml`
   after launch. Squarespace's native LLMS.txt field has no equivalent here;
   add `public/llms.txt` if you want to keep one.
10. **Updating a page later.** Paste the live page into `pages/<slug>.html`
    and its header into `pages/headers/<slug>-header.html`, run
    `python3 build.py`, review the check report, commit.

## Check report (from `python3 build.py`)

Every JSON-LD block on every page parses. Five findings remain, none of which
this restructure was allowed to fix:

| Finding | Where | Why it is left |
|---|---|---|
| `/privacy-policy` does not exist | footer link, every page | Page lives only in Squarespace (step 3) |
| `/behavior-change-coaching` does not exist | how-we-measure-your-progress, outcomes | Same |
| `/is-omnifit-right-for-you` does not exist | contactform | Same |
| Homepage has 3 `<h1>` | `/` | home-2, home-3 and home-4 each carry one; needs a copy decision |
| `/contactform` has 0 `<h1>` | `/contactform` | Its heading is a styled `div`; needs a copy decision |

Other things noticed, reported not changed:

- `pages/private-personal-trainer-san-diego.html` is byte-identical to
  `pages/training-rates-san-diego.html`; both are published at their own
  canonical URL as they were on Squarespace.
- Pre-existing emoji characters are in the page sources (trust strips and
  feature lists on the territory, service and FAQ pages; roughly 11-15 per
  territory page, 3 on FAQs). None were introduced by the build; the footer,
  nav and every icon added here are gold line SVGs.
- `pages/home-5.html` uses an older palette (`#002147`, `#DAA520`) than the
  rest of the site.
- Titles and descriptions come from each header's `WebPage` node, else the
  page's `SEO Title` / `SEO Description` comments. Three pages had neither and
  use derived values set in `META_FALLBACK` in `build.py`: `case-studies`,
  `contactform`, `desk-worker-posture-pain`. `terms-and-conditions` keeps the
  bare title "Terms of Service" that its header records (Squarespace appended
  the site title at render time).
- `_redirects` targets for `/nutritional-coaching-pacific-beach` (-> `/weight-loss`,
  the target REPORT.md recorded) and for the archive-only slugs
  `/personal-trainer-point-loma` and `/facility` are best guesses; change them
  if the live mappings differ.

## Pages by URL

Compare against the live site. Source = the file(s) under `pages/`.

| URL | Source | Title |
|---|---|---|
| https://www.omnifittraining.com/ | home-1, home-2, home-3, home-4, home-6, home-5 + headers/home-header | Personal Trainer San Diego \| Diagnostic-Led Coaching |
| https://www.omnifittraining.com/about | about | About Nemezio LopezPerez \| NASM Elite Trainer, San Diego |
| https://www.omnifittraining.com/body-composition-testing | body-composition-testing | Body Composition Testing in San Diego \| Bodystat QuadScan 4000 \| OmniFit Performance |
| https://www.omnifittraining.com/case-studies | case-studies | Client Case Studies \| Real Results From Real Professionals \| OmniFit Performance (derived) |
| https://www.omnifittraining.com/contactform | contactform | Request Your Consultation \| OmniFit Performance San Diego (derived) |
| https://www.omnifittraining.com/corrective-exercise-post-rehab | corrective-exercise-post-rehab | Corrective Exercise Specialist in San Diego \| Post-Rehab Training \| OmniFit Performance |
| https://www.omnifittraining.com/couples-personal-training-san-diego | couples-personal-training-san-diego | Couples Personal Training San Diego \| Train Together, Programmed Separately |
| https://www.omnifittraining.com/desk-worker-posture-pain | desk-worker-posture-pain | Desk Worker Posture & Pain Correction \| OmniFit Performance San Diego (derived) |
| https://www.omnifittraining.com/faqs | FAQs | OmniFit Performance FAQs \| Personal Training in San Diego |
| https://www.omnifittraining.com/glp-1-personal-training-san-diego | glp-1-personal-training-san-diego | GLP-1 Personal Training San Diego \| Keep the Muscle, Lose the Fat |
| https://www.omnifittraining.com/hiit-personal-trainer-san-diego | hiit-personal-trainer-san-diego | HIIT Personal Training in San Diego \| OmniFit Performance |
| https://www.omnifittraining.com/how-it-works-pricing | how-it-works-pricing | How It Works & Pricing \| OmniFit Performance San Diego |
| https://www.omnifittraining.com/how-we-measure-your-progress | how-we-measure-your-progress | How We Measure Your Progress \| OmniFit Performance San Diego |
| https://www.omnifittraining.com/hsa-fsa-personal-training | hsa-fsa-personal-training | HSA & FSA Eligible Personal Training \| How It Works |
| https://www.omnifittraining.com/in-home-personal-trainer-san-diego | in-home-personal-trainer-san-diego | In-Home Personal Trainer in San Diego \| OmniFit Performance |
| https://www.omnifittraining.com/nutrition-coaching-san-diego | nutrition-coaching-san-diego | Nutrition Coaching San Diego \| Habit-Based, Not a Meal Plan You Abandon |
| https://www.omnifittraining.com/omnifit-vs-competitors | omnifit-vs-competitors | OmniFit vs F45, Orangetheory, Big Box Gyms & Equinox \| San Diego Personal Training Comparison |
| https://www.omnifittraining.com/outcomes | outcomes | Client Outcomes \| OmniFit Performance San Diego |
| https://www.omnifittraining.com/partners | partners | Trusted Clinical Partners \| OmniFit Performance — San Diego |
| https://www.omnifittraining.com/personal-trainer-4s-ranch | personal-trainer-4s-ranch | Personal Trainer 4S Ranch \| In-Home & Studio \| OmniFit Performance |
| https://www.omnifittraining.com/personal-trainer-carlsbad | personal-trainer-carlsbad | Personal Trainer Carlsbad \| In-Home & Studio \| OmniFit Performance |
| https://www.omnifittraining.com/personal-trainer-carmel-valley | personal-trainer-carmel-valley | Personal Trainer Carmel Valley \| In-Home & Studio \| OmniFit Performance |
| https://www.omnifittraining.com/personal-trainer-del-mar | personal-trainer-del-mar | Personal Trainer Del Mar \| In-Home & Studio \| OmniFit Performance |
| https://www.omnifittraining.com/personal-trainer-encinitas | personal-trainer-encinitas | Personal Trainer Encinitas \| In-Home & Studio \| OmniFit Performance |
| https://www.omnifittraining.com/personal-trainer-fairbanks-ranch | personal-trainer-fairbanks-ranch | Personal Trainer Fairbanks Ranch \| In-Home & Studio \| OmniFit Performance |
| https://www.omnifittraining.com/personal-trainer-la-jolla | personal-trainer-la-jolla | Personal Trainer La Jolla \| In-Home & Studio \| OmniFit Performance |
| https://www.omnifittraining.com/personal-trainer-over-50-san-diego | personal-trainer-over-50-san-diego | Personal Trainer for Over 50 in San Diego \| Strength Training After 50 |
| https://www.omnifittraining.com/personal-trainer-rancho-bernardo | personal-trainer-rancho-bernardo | Personal Trainer Rancho Bernardo \| In-Home & Studio \| OmniFit Performance |
| https://www.omnifittraining.com/personal-trainer-rancho-santa-fe | personal-trainer-rancho-santa-fe | Personal Trainer Rancho Santa Fe \| In-Home & Studio \| OmniFit Performance |
| https://www.omnifittraining.com/personal-trainer-santaluz | personal-trainer-santaluz | Personal Trainer Santaluz \| In-Home & Studio \| OmniFit Performance |
| https://www.omnifittraining.com/personal-trainer-solana-beach | personal-trainer-solana-beach | Personal Trainer Solana Beach \| In-Home & Studio \| OmniFit Performance |
| https://www.omnifittraining.com/personal-training-services | personal-training-services | Personal Training Services for Professionals 30+ \| OmniFit Performance San Diego |
| https://www.omnifittraining.com/private-personal-trainer-san-diego | private-personal-trainer-san-diego (identical to training-rates) | Private Personal Trainer in San Diego \| OmniFit Performance |
| https://www.omnifittraining.com/strength-training-1 | strength-training-1 | Strength Training for Professionals Over 30 \| OmniFit Performance San Diego |
| https://www.omnifittraining.com/terms-and-conditions | terms-and-conditions | Terms of Service |
| https://www.omnifittraining.com/the-30-minute-executive-reset | the-30-minute-executive-reset | 30-Minute Executive Reset \| Virtual & Hybrid Coaching \| OmniFit Performance |
| https://www.omnifittraining.com/the-omnifit-method | the-omnifit-method | The OmniFit Method: Assess, Correct, Build, Sustain \| OmniFit Performance |
| https://www.omnifittraining.com/training-rates-san-diego | training-rates-san-diego | Personal Training Rates San Diego \| Published Pricing \| OmniFit Performance |
| https://www.omnifittraining.com/weight-loss | weight-loss | Sustainable Fat Loss for Busy Professionals 30+ \| OmniFit Performance San Diego |

Not published (not pages): `pages/footer.html`, `pages/home-1..6.html`
(homepage sections), everything under `archive/` (retired; redirected in
`_redirects`), and the orphan headers `bodybuilding-header.html`,
`energy-protocol-waitlist-form-header.html` (their pages exist only in
Squarespace).

## Redirects in `public/_redirects`

```
/executive-hybrid                    -> /the-30-minute-executive-reset
/executive-hybrid-coaching           -> /the-30-minute-executive-reset
/online-training                     -> /the-30-minute-executive-reset
/personal-trainer-mission-hills      -> /in-home-personal-trainer-san-diego
/nutritional-coaching-pacific-beach  -> /weight-loss
/personal-trainer-in-pacific-beach   -> /personal-trainer-4s-ranch
/personal-trainer-point-loma         -> /in-home-personal-trainer-san-diego
/facility                            -> /personal-trainer-4s-ranch
/services                            -> /personal-training-services
/how-it-works                        -> /how-it-works-pricing
/contact                             -> /contactform
/hybrid-coaching                     -> /the-30-minute-executive-reset
/consultation                        -> /contactform
/FAQs                                -> /faqs
```
