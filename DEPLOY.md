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
pages/home-0.html                 homepage hero (built for the static site; the only h1)
pages/home-1..6.html              homepage sections
site/layout.html                  the HTML document skeleton
site/nav.html                     announcement bar + site header + primary nav (single source)
site/site.css, site/site.js       shared CSS / JS
site/icons.py                     the gold line-SVG icon for every emoji the pages used
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

Only four things differ from the pasted sources, all structural:

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
4. Every emoji is swapped at build time for a gold line SVG from
   `site/icons.py` (24x24, 1.5px gold stroke, the style of the hub-card icons
   on the territory pages), sized at 1em so it takes the size the emoji had.
   249 replacements on 22 pages; the build prints the full list and fails if
   a newly pasted page carries an emoji with no icon. The `pages/` sources
   still contain the emoji. The text symbols ✓ ✗ ✕ (table ticks and CSS list
   bullets) are not emoji and stay as text.

Three source files were edited on purpose (the only copy-adjacent change):
`pages/home-2.html`, `pages/home-3.html` and `pages/home-4.html` had their
`<h1>` demoted to `<h2>` so the new hero carries the homepage's only H1. The
hero-heading CSS selectors in each file were renamed to match, and the
computed styles of all three headings were diffed before and after in
Chromium at desktop and phone widths: zero differences. Note that `home-3`
is therefore no longer byte-identical to `case-studies.html` (CANON's
duplicate rule), which only affects how `tools/certify.py` counts findings.

Small additions in `site.css` that are judgment calls, flagged here:

- `#omni-faq{background:#fff}`: the homepage FAQ section (`home-5`) is
  authored in navy text with no background of its own, i.e. for a light
  Squarespace section. On the navy body it would be unreadable.
- `main{overflow-x:clip}`: Squarespace clipped each section horizontally.
  Without it the decorative 500px hero glow on the territory pages and the
  step row on the 4S Ranch page produce a horizontal scrollbar at phone widths.
- The homepage hero card sits on a white strip (`#omni-hero{background:#fff}`)
  so its rounded corners and 40px side margins read against the white header;
  the body background elsewhere stays navy. If the live site's page
  background is white site-wide, that is one line in `site.css`.

## Header, nav and announcement bar

`site/nav.html` is the single source. Its first lines hold the one variable
for the announcement bar:

```
ANNOUNCEMENT: {"text": "At capacity for September and October — accepting November applications at updated rates →", "href": "/training-rates-san-diego"}
```

Change the text or link there and rebuild; set `"text"` to `""` to remove the
bar. It is maroon (`--omni-maroon: #7b1e2b`), white Montserrat, centred, with
an X at the right that hides it for the rest of the browser session. The link
target is a guess (the rates page); change it if the live bar links elsewhere.

The header is white and sticky: wordmark at left, two Montserrat rows
(Home, Programs, Rates, Methodology ▾, Results ▾ / More ▾, About, Fit Check,
Contact), then Instagram and LinkedIn as gold line SVGs (URLs from the
footer and the JSON-LD `sameAs`) and the "Book Your Consultation" text CTA to
Calendly in a new tab. The current page's link gets a gold underline (and the
dropdown that contains it); dropdowns open on hover on pointer devices and on
tap/click everywhere. Below 1024px the header collapses to a hamburger and a
full-height white drawer with the same items as accordions.

**No logo asset exists in the repo** (no png/svg/jpg anywhere; the JSON-LD
only references the Squarespace CDN apple-touch-icon), so the header shows the
Bebas Neue wordmark. Save the real logo as `public/assets/img/logo.png` (or
.svg) and swap the wordmark span for the `<img>` noted in `site/nav.html`.

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
2. **Add the logo** (see "Header, nav and announcement bar" above) and check
   the announcement bar's link target.
3. **Pages that live only in Squarespace** (block-built, no Code Block in the
   repo). They are linked from every page via the nav or footer and need to
   exist before launch or the links 404: `/privacy-policy` (footer),
   `/behavior-change-coaching` (nav: Methodology, plus
   how-we-measure-your-progress and outcomes), `/is-omnifit-right-for-you`
   (nav: Fit Check, plus contactform). Paste each
   live page into `pages/<slug>.html` (plus its header) and rebuild, or add a
   redirect. (`/bodybuilding` and the Energy Protocol waitlist page are no
   longer live; their headers were archived Oct 16, 2026.)
4. **Homepage hero.** `pages/home-0.html` is the new hero (navy rounded card,
   Playfair H1 "San Diego Personal Trainer for Executives", gold italic
   subhead, no CTA). If the live hero carries anything else, edit that file.
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

Every JSON-LD block on every page parses, every page has exactly one H1
except `/contactform`, and no emoji remains in any built page. All 39 pages
render in Chromium at 1366px and 390px with no horizontal overflow and no
script errors. Four findings remain, none of which this restructure was
allowed to fix:

| Finding | Where | Why it is left |
|---|---|---|
| `/privacy-policy` does not exist | footer link, every page | Page lives only in Squarespace (step 3) |
| `/behavior-change-coaching` does not exist | nav (Methodology), how-we-measure-your-progress, outcomes | Same |
| `/is-omnifit-right-for-you` does not exist | nav (Fit Check), contactform | Same |
| `/contactform` has 0 `<h1>` | `/contactform` | Its heading is a styled `div`; needs a copy decision |

Other things noticed, reported not changed:

- `pages/private-personal-trainer-san-diego.html` is byte-identical to
  `pages/training-rates-san-diego.html`; both are published at their own
  canonical URL as they were on Squarespace.
- The emoji in the `pages/` sources are replaced only in the build output
  (see "How the build works"); `python3 build.py` prints every replacement.
  The one emoji inside a CSS rule (`.hiit-locations li::before{content:'📍'}`
  on the HIIT page) becomes the same pin icon as a background image.
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
| https://www.omnifittraining.com/ | home-0 (hero), home-1, home-2, home-3, home-4, home-6, home-5 + headers/home-header | Personal Trainer San Diego \| Diagnostic-Led Coaching |
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
| https://www.omnifittraining.com/terms-and-conditions | terms-and-conditions | Terms of Service |
| https://www.omnifittraining.com/the-30-minute-executive-reset | the-30-minute-executive-reset | 30-Minute Executive Reset \| Virtual & Hybrid Coaching \| OmniFit Performance |
| https://www.omnifittraining.com/the-omnifit-method | the-omnifit-method | The OmniFit Method: Assess, Correct, Build, Sustain \| OmniFit Performance |
| https://www.omnifittraining.com/training-rates-san-diego | training-rates-san-diego | Personal Training Rates San Diego \| Published Pricing \| OmniFit Performance |
| https://www.omnifittraining.com/weight-loss | weight-loss | Sustainable Fat Loss for Busy Professionals 30+ \| OmniFit Performance San Diego |

Not published (not pages): `pages/footer.html`, `pages/home-0..6.html`
(homepage sections), everything under `archive/` (retired; redirected in
`_redirects`), including the archived headers `bodybuilding-header.html`
and `energy-protocol-waitlist-form-header.html` (pages no longer live).

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
/strength-training-1                 -> /   (page archived in the Keyword Ownership run, Oct 2026)
```
