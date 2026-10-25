# Deploying omnifittraining.com as a static site on Cloudflare Pages

This repo now builds a complete static site into `public/`. Nothing in
`pages/` or `pages/headers/` was rewritten: every page body, its CSS and its
JSON-LD are carried into `public/` byte-for-byte (verified at build time), and
the shared header, nav and footer are wrapped around them from one source.

## How the build works

```
pages/<slug>.html                 page body (the Squarespace Code Block)
pages/headers/<slug>-header.html  page header injection (JSON-LD etc.)
pages/headers/site-header.html    site-wide header injection (GA4 + Clarity,
                                  production only; HubSpot deferral; geo
                                  meta; entity graph)
pages/footer.html                 site-wide footer (CSS + markup + year script)
pages/home-0.html                 homepage hero (built for the static site; the only h1)
pages/home-1..6.html              homepage sections
site/layout.html                  the HTML document skeleton
site/nav.html                     announcement bar + site header + primary nav (single source)
site/site.css, site/site.js       shared CSS / JS (site.js sends every event)
site/icons.py                     the gold line-SVG icon for every emoji the pages used
site/img/logo.svg, logo.png       the brand logo (the SVG is inlined into site/nav.html)
build.py                          stdlib-only build + checks
public/                           generated output (committed)
assistant/knowledge.md            Ask OmniFit fact sheet (public facts only)
functions/                        Cloudflare Pages Functions: /api/ask, /api/assistant-log
schema.sql                        D1 tables for the assistant (paste into the D1 console)
tests/assistant.test.mjs          assistant unit tests (node --test tests/assistant.test.mjs)
```

```
python3 build.py            # rebuild public/ and print the check report
python3 build.py --check    # run only the checks against public/
```

Per page, `build.py` produces `public/<slug>.html` (homepage at
`public/index.html`; see "Trailing slash" below) containing: doctype, `<title>`, meta description,
canonical, the site-wide header injection, one Google Fonts link (union of
every weight the pages used), `/assets/site.css`, the page's
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
   (its link text already reads "4S Ranch Training"; the `_redirects` rule
   for the same slug follows Squarespace to
   `/in-home-personal-trainer-san-diego`, which is a separate decision), and on the partners page
   `/services` -> `/personal-training-services`, `/how-it-works` ->
   `/how-it-works-pricing`, `/contact` -> `/contactform`, `/hybrid-coaching`
   -> `/the-30-minute-executive-reset`.
3. `terms-and-conditions` was a Squarespace TEXT page with no CSS of its own,
   so it is wrapped in `<div class="omni-text-page">` and styled from
   `site.css` in the design system (Playfair headings, Montserrat body).
4. Every emoji is swapped at build time for a gold line SVG from
   `site/icons.py` (24x24, 1.5px gold stroke, the style of the hub-card icons
   on the territory pages), sized at 1em so it takes the size the emoji had.
   160 replacements on 13 pages as of Oct 17, 2026 (249 on 22 before the
   canon-consolidation run swapped the emoji in the touched sources for the
   same SVGs); the build prints the full list and fails if a new or edited
   page carries an emoji with no icon. Untouched `pages/` sources still
   contain their emoji. The text symbols ✓ ✗ ✕ (table ticks and CSS list
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

The header is white and sticky: logo at left, two Montserrat rows
(Home, Programs, Rates, Methodology ▾, Results ▾ / More ▾, About, Fit Check,
Contact), then Instagram and LinkedIn as gold line SVGs (URLs from the
footer and the JSON-LD `sameAs`) and the "Book Your Consultation" text CTA to
Calendly in a new tab. The current page's link gets a gold underline (and the
dropdown that contains it); dropdowns open on hover on pointer devices and on
tap/click everywhere. Below 1024px the header collapses to a hamburger and a
full-height white drawer with the same items as accordions.

The logo is the brand mark as inline SVG (`site/img/logo.svg`, generated from
`site/img/logo.png`), inlined into `site/nav.html` so its parts can animate:
once per browser session the ring draws itself, the F pops in, the letters
rise and the gold rule extends; hovering the logo turns the ring. All of it is
inert under `prefers-reduced-motion`. Sizing and motion live in `site/site.css`.

## Measurement

One setup, all in the repo, no Google Tag Manager. CANON MEASUREMENT is the
rule; this is the operating note.

| What | Value |
|---|---|
| Google Analytics 4 | Measurement ID `G-0K6VLEC2VJ`, loaded as gtag.js |
| Microsoft Clarity | project `yzawpvwvdf` |
| Single source | `pages/headers/site-header.html` loads both; `site/site.js` sends every event |
| Loads on | `www.omnifittraining.com` and `omnifittraining.com` only (`location.hostname`) |
| Anywhere else | `*.pages.dev` previews, localhost: nothing loads, `window.gtag` is undefined, and each event is one console line `[omnifit-track] <event> <json params>` |
| Clarity exclusion | never loads on `/fit-check` (GA4 still does) |
| HubSpot | untouched: the deferred tracking loader (portal 244441037) on every page, the form embed on `/contactform` and `/personal-trainer-4s-ranch` |
| Retired | GTM `GTM-5P4CKPT2` and its noscript iframe, Clarity `ulpgsrkd98`, the page-level `cta_click` / `lead_form_submit` scripts on `/personal-trainer-4s-ranch`. `build.py --check` fails if any of `GTM-5P4CKPT2`, `ulpgsrkd98`, `AW-16616873404`, `G-QTG1ZLR0NQ` or `dataLayer.push` appears anywhere in `public/`, or if either live ID appears more than once on a page |

Events (`gtag('event', name, params)` when gtag exists, else the console line;
all sent from `site/site.js` by delegated listeners, no page carries a
tracking script):

| Event | When | Params |
|---|---|---|
| `book_consultation_click` | any link to calendly.com | `cta_location` (page slug, `home` for `/`), `cta_label` (link text, trimmed, max 60), `cta_position` (`nav` \| `hero` \| `body` \| `footer` \| `sticky`, from the nearest landmark: a `sticky` class, `<footer>`, the site header or announcement bar, a `hero` class, else body; `data-cta-position` on the link or an ancestor overrides) |
| `generate_lead` | HubSpot form submitted (window `message` with `data.type === "hsFormCallback"` and `data.eventName === "onFormSubmitted"`) | `form_location` (page slug) |
| `phone_click` / `email_click` | `tel:` / `mailto:` links | `cta_location` |
| `fit_check_start` | first answer selected on `/fit-check` | none |
| `fit_check_complete` | result shown (the page marks `#result` with `data-fit-result` and, on a pass, `data-fit-setting`) | `fit_result` (`pass` \| `hold`), `fit_setting` (recommended Dial setting, pass only). Individual answers are never sent. A retake that reaches a new result counts again |
| `rates_section_view` | `/training-rates-san-diego` only, the first time each of `#rt-foundation`, `#rt-program`, `#rt-sessions`, `#rt-reset` scrolls into view (IntersectionObserver, once per section, bottom 20% of the viewport excluded) | `section` (the id) |

Completed bookings are not a site event. Calendly's own Google Analytics
integration (Calendly > Integrations > Google Analytics, the Measurement ID
above) reports Calendly's booking events to the same property, and
cross-domain measurement is configured in GA4 for `calendly.com` (Admin >
Data streams > the web stream > Configure tag settings > Configure your
domains) so a visitor who clicks through and books stays one session. Both
are GA4 / Calendly settings, not repo code; see the manual steps.

**Test-only override.** `?omnifit-track=prod` forces the production branch,
and is honoured only when `location.hostname` is `localhost` or `127.0.0.1`.
On any other host, the pages.dev preview included, the flag does nothing.
`tools/tracktest.js` uses it:

```
python3 build.py
NODE_PATH="$(npm root -g)" node tools/tracktest.js
```

The test serves `public/` locally, maps `www.omnifittraining.com` to the local
server inside Chromium to prove the real production condition, stubs gtag.js so
no hit reaches Google, intercepts google-analytics.com and clarity.ms, and
asserts every event above with its params, Clarity absent on `/fit-check`, and
no request to either service on a non-production host. Details in
`tools/README.md`; the results table is in `REPORT.md`.

## Cloudflare Pages settings

| Setting | Value |
|---|---|
| Framework preset | None |
| Build command | *(leave empty)* - `public/` is committed |
| Build output directory | `public` |
| Root directory | `/` (repo root) |
| Production branch | `main` |
| Environment variables | none required for the site; Ask OmniFit needs the secrets and D1 binding listed under "Ask OmniFit" |

Optional alternative: set the build command to `python3 build.py` so Cloudflare
regenerates `public/` on every deploy (Python 3 is in the Pages build image).
Either way the output directory is `public`.

### Deploying (since the Oct 18, 2026 cutover)

Merging to `main` is publishing. Nothing is pasted into Squarespace any more.

1. Edit the source in `pages/<slug>.html` and/or
   `pages/headers/<slug>-header.html` (or `site/`) on a branch.
2. Run `python3 build.py` and commit the regenerated `public/` with the
   source change; run `python3 tools/certify.py` (RESULT: PASSED).
3. Merge to `main` and push. Cloudflare Pages deploys `public/` from `main`
   (rebuilding it first if the build command above is set).

`public/_redirects` uses Cloudflare Pages syntax (`/old /new 301`).
`public/404.html` is written by `build.py` too (title "Page Not Found | OmniFit
Performance", `<meta name="robots" content="noindex">`, never in the sitemap,
links to Home and Book Your Consultation only); Cloudflare Pages serves it for
any route with no file and no redirect. `public/_headers` marks only the
`*.pages.dev` preview hostname `X-Robots-Tag: noindex`; the production domain
carries no such header. Every page also gets security headers (site audit,
Oct 20 2026): `X-Content-Type-Options: nosniff`, `Referrer-Policy:
strict-origin-when-cross-origin`, `X-Frame-Options: SAMEORIGIN`, a narrow
`Content-Security-Policy` (`frame-ancestors 'self'; base-uri 'self';
object-src 'none'; upgrade-insecure-requests`, no script allowlist, so GA4,
Clarity, HubSpot, Calendly and the inline page scripts are unaffected) and
`Permissions-Policy: camera=(), microphone=(), geolocation=()`. After a
deploy, check them with `curl -sI https://www.omnifittraining.com/ | grep -i
-e content-security -e x-frame -e nosniff`. `build.py --check` verifies all of it.

**Link previews.** Every page carries Open Graph and Twitter card tags
(`og:title`, `og:description`, `og:url`, `og:image` 1200x630 and the
`twitter:card` set), written by `build.py` from the page's title and meta
description. The image is `site/img/og-coach-client-cable-pulldown-1200x630.jpg`
(`SOCIAL_IMAGE` in `build.py`) except on Journal posts, whose own lead photo
`site/blog.py` sets. `build.py --check` fails a page with no preview image, a
missing image file or an `og:url` that differs from the canonical.
### Trailing slash (launch blocker, fixed Oct 18 2026)

Cloudflare Pages serves `public/<slug>/index.html` at `/<slug>/` and
redirects `/<slug>` to `/<slug>/`, while every canonical, sitemap entry,
internal link and Google-indexed URL is `/<slug>` with no slash. So
`build.py` writes FLAT files: `public/<slug>.html`, served directly at
`/<slug>` with no redirect (Pages' own `/<slug>.html` -> `/<slug>` and
`/<slug>/` -> `/<slug>` redirects then point at the canonical form). The
homepage stays `public/index.html`; `_redirects`, `404.html` and `_headers`
are unchanged. `build.py --check` fails if any `public/**/index.html` other
than the homepage's exists (its fixtures run first).

**After every deploy, verify:** open
https://omnifit-site.pages.dev/about - the address bar must STAY on `/about`
(no slash added, no redirect). `curl -sI https://omnifit-site.pages.dev/about`
must answer `200`, not `308`. Spot-check one territory page the same way.

## Ask OmniFit (AI assistant)

A chat widget ("Ask OmniFit", bottom right) answers visitor questions from
`assistant/knowledge.md` using the Anthropic API. It is **harmless until
configured**: until the Pages project has the `ANTHROPIC_API_KEY` secret and a
D1 database bound as `DB`, `/api/ask` returns 503 and the widget never appears.

| Piece | Where |
|---|---|
| Fact sheet | `assistant/knowledge.md` -> `functions/_lib/knowledge.js` (regenerated by `build.py`; commit both) |
| System prompt | `functions/_lib/system-prompt.js` (owner wording; certify.py checks its hash) |
| Chat endpoint | `functions/api/ask.js` (POST; GET is the status probe the widget uses) |
| Log export | `functions/api/assistant-log.js` (`/api/assistant-log`, last 30 days as CSV; see "Exporting the log") |
| Widget | `site/assistant.js` + `site/assistant.css` -> `public/assets/` (loaded lazily from the shared footer) |
| Database | `schema.sql` (tables `assistant_log`, `assistant_rate`, `assistant_salt`, `assistant_meta`) |
| Retention job | `workers/assistant-cleanup/` (a separate scheduled Worker; see "Daily cleanup Worker") |

`functions/` sits at the repo root next to `build.py` (the Pages root
directory), never inside `public/`. Pages finds it there with no build command.

Settings (Cloudflare dashboard -> Workers & Pages -> the project -> Settings):

| Name | Kind | Value |
|---|---|---|
| `ANTHROPIC_API_KEY` | Secret | an Anthropic API key |
| `ADMIN_KEY` | Secret | a long random string; needed only for the CSV export |
| `ASSISTANT_MODEL` | Variable (optional) | defaults to `claude-sonnet-5-5` |
| `ASSISTANT_GLOBAL_LIMIT_PER_HOUR` | Variable (optional) | messages an hour across all visitors together; defaults to `300` |
| `DB` | D1 database binding | the database created from `schema.sql` |

Limits built into `/api/ask`: requests only from omnifittraining.com,
www.omnifittraining.com and omnifit-site.pages.dev; 600 characters per
message; the conversation sent to the model is rebuilt on the server from
the log for that conversation ID (the last 4 exchanges plus the new message;
earlier turns the browser sends back are ignored, so they cannot be forged,
and a new or missing ID starts an empty conversation); after 12 visitor
messages in a conversation the reply is a fixed hand-off to booking; 30
messages an hour per visitor (keyed on a SHA-256 of the IP, or of the /64
prefix for IPv6, plus a random daily salt; no IP is stored); 300 messages an
hour across all visitors together (`ASSISTANT_GLOBAL_LIMIT_PER_HOUR`), after
which every visitor gets the same "rate limited" error, which the widget shows
as "Something went wrong" plus the Book button; emails and phone numbers
(international formats and spelled-out emails such as "name at gmail dot
com" included) are removed before anything is sent or logged; replies cut off
at the 400-token limit are trimmed to their last full sentence. `robots.txt`
disallows `/api/` for every crawler.

**90-day deletion.** Log rows older than 90 days (plus spent rate-limit
windows and old salts) are deleted by two things: every request to `/api/ask`
(including the status probe each page load makes, and error responses) and
`/api/assistant-log` triggers the cleanup, at most once every 10 minutes; and
the daily cleanup Worker below runs it whether or not anyone visits.

**Database upgrade (Oct 20 2026).** A database created from an earlier
`schema.sql` needs the new `assistant_meta` table: paste the whole
`schema.sql` into the D1 console again (every statement is `IF NOT EXISTS`,
so existing data is untouched), or run only:

```sql
CREATE TABLE IF NOT EXISTS assistant_meta (
  key          TEXT    PRIMARY KEY,
  value        TEXT    NOT NULL
);
```

Until it exists the assistant still works; it just runs the cleanup on every
request instead of every 10 minutes. No other table changed.

**Daily cleanup Worker (one time).** Pages Functions cannot run on a
schedule, so `workers/assistant-cleanup/` is a tiny separate Worker with a
daily cron (10:17 UTC) that runs the same deletion. To deploy it:

1. Find the D1 database's name and ID (dashboard -> Storage & Databases ->
   D1, or `npx wrangler d1 list`).
2. Put them in `workers/assistant-cleanup/wrangler.toml` in place of
   `REPLACE_WITH_D1_DATABASE_NAME` / `REPLACE_WITH_D1_DATABASE_ID`. Keep the
   binding name `DB`.
3. From that directory run `npx wrangler login` (once), then
   `npx wrangler deploy`. It has no public URL (`workers_dev = false`).
4. Check: dashboard -> Workers & Pages -> `omnifit-assistant-cleanup` ->
   Settings -> Trigger events shows the cron; after a day, its Logs show a
   scheduled run with no error.

Redeploy it only when `functions/_lib/assistant.js` changes `cleanup()`.

**Exporting the log.** Open `https://www.omnifittraining.com/api/assistant-log`
in a browser, enter `ADMIN_KEY` in the form, and the CSV downloads. The key is
sent in the form body, never in the address, so it does not end up in browser
history or server logs. From a script:
`curl -H "Authorization: Bearer $ADMIN_KEY" -o log.csv https://www.omnifittraining.com/api/assistant-log`.
The old `?key=` address no longer works: it shows the form instead.

## Manual steps (you)

1. **Create the Pages project** from `nemezio-dotcom/omnifit-site` with the
   settings above. Deploy once to the `*.pages.dev` preview and click through.
2. **Add the logo** (see "Header, nav and announcement bar" above) and check
   the announcement bar's link target.
3. **Pages that lived only in Squarespace** (block-built, no Code Block in the
   repo). Done before the Oct 18, 2026 cutover: `/privacy-policy` and
   `/behavior-change-coaching` are pages in `pages/`, and
   `/is-omnifit-right-for-you` 301s to `/fit-check`. (`/bodybuilding` and the Energy Protocol waitlist page are no
   longer live; their headers were archived Oct 16, 2026. Google still knows
   both URLs, so since Oct 17, 2026 they 301: `/bodybuilding` ->
   `/strength-training-1`, `/energy-protocol-waitlist-form` ->
   `/the-30-minute-executive-reset`.)
4. **Homepage hero.** `pages/home-0.html` is the new hero (navy rounded card,
   Playfair H1 "San Diego Personal Trainer for Executives", gold italic
   subhead, no CTA). If the live hero carries anything else, edit that file.
5. **BEFORE CANCELLING SQUARESPACE: replace or remove these images.** Five
   visible images are still hotlinked from `images.squarespace-cdn.com` (Oct 18,
   2026) and will break when the subscription ends. Put each in `site/img/`
   (served at `/assets/img/`) and update the reference, or remove it.
   `python3 build.py --check` prints a WARNING per remaining URL.

   | Image | Where it appears |
   |---|---|
   | Brandon testimonial (`Brandon+Testimonial.jpg`) | pages/case-studies.html (frozen record; swapping the src needs an owner override) |
   | Precision Nutrition logo (`PN+Logo+NMH.png`) | pages/about.html (credentials list) |
   | NASM CES badge (`61f78fa7-8907-4144-8033-b37ec32718d5.png`, 100px) | pages/about.html (credentials list) |
   | Thumbtack Pro screenshot, used as the coach photo (`Screenshot_20250416_132107_Thumbtack+Pro-EDIT.jpg`) | pages/about.html, pages/headers/about-header.html (schema "image"), pages/personal-trainer-4s-ranch.html (Meet Nemezio photo; locked page, the src swap needs an owner override) |
   | Dr. Damien Jackson-Ricketts headshot (`damien-jackson-ricketts.jpg`) | pages/partners.html |

   Done: the site-wide schema image (site-header) and the homepage
   primaryImageOfPage (home-header) now use
   `/assets/img/hero-coach-client-cable-pulldown-1600.jpg` instead of the
   Squarespace dumbbell photo. That URL resolves now that this build serves
   the domain (cutover Oct 18, 2026).
   The seven client transformation photos were already moved: re-branded
   (old knot logo removed, header logo added; clients untouched) and served
   from `/assets/img/`.
6. **Analytics (GA4 / Clarity, human-side settings).** The tags themselves
   are in the repo (see "Measurement"); these are the settings around them:
   (a) GA4 cross-domain: Admin > Data streams > the web stream > Configure
   tag settings > Configure your domains > add `calendly.com`. (b) Calendly >
   Integrations > Google Analytics: enter `G-0K6VLEC2VJ`, so completed
   bookings reach the property from Calendly's side; the site sends only the
   click. (c) In GA4, mark `book_consultation_click`, `generate_lead`,
   `fit_check_complete` and Calendly's scheduled event as key events.
   (d) Clarity project `yzawpvwvdf`: keep masking at Balanced or Strict so
   form fields are masked, as the privacy policy states; the project is
   never loaded on `/fit-check`. (e) Retire the old stack: unpublish or
   pause GTM container `GTM-5P4CKPT2` and stop expecting data in Clarity
   project `ulpgsrkd98`; whatever `G-QTG1ZLR0NQ` and `AW-16616873404` fired
   from inside the container stops with it. **Still not in the repo:** any
   Jotform or Trainerize embed (no iframe or script for either exists in any
   page; Trainerize appears only as text). HubSpot is preserved exactly:
   the deferred loader (portal 244441037) on every page and the form (form
   `a34ea6d0-e63f-46d1-83d4-c675a27d64bb`) on `/contactform` and
   `/personal-trainer-4s-ranch`.
7. **Squarespace URL mappings.** Done Oct 17, 2026: the owner pasted the
   live mapping list and every line is in `public/_redirects` with its
   Squarespace target (see "Redirects" below). Nothing left to export.
8. **Domain.** Add `www.omnifittraining.com` as the custom domain in Pages,
   move DNS to Cloudflare (or CNAME `www` to the `pages.dev` host), and add a
   redirect rule for the apex `omnifittraining.com` -> `https://www.omnifittraining.com`.
9. **Search Console.** Submit `https://www.omnifittraining.com/sitemap.xml`
   after launch. Squarespace's native LLMS.txt field has no equivalent here;
   add `public/llms.txt` if you want to keep one.
10. **Updating a page later.** Edit `pages/<slug>.html` and its header
    `pages/headers/<slug>-header.html` in the repo (the only source), run
    `python3 build.py` and `python3 tools/certify.py`, review both reports,
    commit, and merge to `main` (see "Deploying" above).

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
- `_redirects`: `/nutritional-coaching-pacific-beach` and `/facility` are
  now confirmed by the Squarespace mapping (same targets).
  `/personal-trainer-point-loma` is not in the mapping and stays a repo
  best guess (-> `/in-home-personal-trainer-san-diego`).

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
| https://www.omnifittraining.com/how-to-choose-a-personal-trainer-san-diego | how-to-choose-a-personal-trainer-san-diego | How to Choose a Personal Trainer: Red Flags \| San Diego |
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
| https://www.omnifittraining.com/strength-training-1 | strength-training-1 | Strength Training for Professionals 30+ \| OmniFit Performance San Diego |
| https://www.omnifittraining.com/terms-and-conditions | terms-and-conditions | Terms of Service |
| https://www.omnifittraining.com/the-30-minute-executive-reset | the-30-minute-executive-reset | 30-Minute Executive Reset \| Virtual & Hybrid Coaching \| OmniFit Performance |
| https://www.omnifittraining.com/the-omnifit-method | the-omnifit-method | The OmniFit Method: Assess, Correct, Build, Sustain \| OmniFit Performance |
| https://www.omnifittraining.com/training-rates-san-diego | training-rates-san-diego | Personal Training Rates San Diego \| Published Pricing \| OmniFit Performance |
| https://www.omnifittraining.com/weight-loss | weight-loss | Sustainable Fat Loss for Busy Professionals 30+ \| OmniFit Performance San Diego |

Not published (not pages): `pages/footer.html`, `pages/home-0..6.html`
(homepage sections), everything under `archive/` (retired; redirected in
`_redirects`), including the archived headers `bodybuilding-header.html`
and `energy-protocol-waitlist-form-header.html` (pages no longer live; both
URLs 301 since Oct 17, 2026).

## Redirects in `public/_redirects`

`public/_redirects` is generated by `build.py` from its `REDIRECTS` list.
Edit `build.py`, never the generated file. CANON.md (ARCHIVE > REDIRECTS)
carries the same rules.

**Principle (owner, Oct 17, 2026).** The Squarespace URL Mappings the owner
pasted on Oct 17, 2026 are authoritative, and their targets are copied
unchanged. There are three kinds of exception:

1. Booking URLs go to Calendly (`https://calendly.com/nemezio-omnifittraining/45min`),
   per launch decision 1, not to their Squarespace targets.
2. Three exact-match pages that did not exist when the mapping was made:
   `/nutrition-coaching`, and two `/blog/` posts whose topic now has a page.
3. Gap-fills: URLs Google knows that Squarespace never mapped.

Earlier repo rules that the mapping does not cover are kept unchanged
("existing"). Where an earlier rule disagreed with the mapping, the mapping
won: `/personal-trainer-in-pacific-beach` now goes to
`/in-home-personal-trainer-san-diego`, not `/personal-trainer-4s-ranch`.
`/blog` is a 302 because a blog is planned at that path; make it a page and
drop the rule when the blog ships.

**Check.** `python3 build.py --check` reads
`tools/gsc-known-urls-2026-10-17.txt` (every URL Google is known to have: the
sitemap pages, four retired indexed URLs, and every earlier and current
redirect source). Every path there must be a built page or a `_redirects`
source. Every internal target must be a built page, which rules out chains.
No source may repeat, and the status must be 301 or 302. Fixtures run first
and must each fail on their own defect. Add a path to the known-URL file
whenever Search Console reports a new one.

All 74 rules (44 Squarespace, 9 exception, 14 gap-fill including `/blog`,
7 existing):

| Source | Target | Status | Origin |
|---|---|---|---|
| `/executive-hybrid` | `/the-30-minute-executive-reset` | 301 | existing |
| `/personal-trainer-point-loma` | `/in-home-personal-trainer-san-diego` | 301 | existing |
| `/how-it-works` | `/how-it-works-pricing` | 301 | existing |
| `/hybrid-coaching` | `/the-30-minute-executive-reset` | 301 | existing |
| `/is-omnifit-right-for-you` | `/fit-check` | 301 | existing |
| `/consultation` | `/contactform` | 301 | existing |
| `/FAQs` | `/faqs` | 301 | existing |
| `/new-page` | `/private-personal-trainer-san-diego` | 301 | Squarespace |
| `/new-page-1` | `/` | 301 | Squarespace |
| `/home` | `/` | 301 | Squarespace |
| `/store` | `/` | 301 | Squarespace |
| `/strength-training` | `/strength-training-1` | 301 | Squarespace |
| `/nutritional-coaching-mission-bay` | `/weight-loss` | 301 | Squarespace |
| `/nutritional-coaching-mission-bat` | `/weight-loss` | 301 | Squarespace |
| `/nutritional-coaching-pacific-beach` | `/weight-loss` | 301 | Squarespace |
| `/fat-loss-training` | `/weight-loss` | 301 | Squarespace |
| `/weight-loss-training-remote-training` | `/weight-loss` | 301 | Squarespace |
| `/weight-loss-training-mission-bay` | `/weight-loss` | 301 | Squarespace |
| `/personal-trainer-pacific-beach` | `/in-home-personal-trainer-san-diego` | 301 | Squarespace |
| `/personal-trainer-in-pacific-beach` | `/in-home-personal-trainer-san-diego` | 301 | Squarespace |
| `/personal-trainer-mission-bay` | `/in-home-personal-trainer-san-diego` | 301 | Squarespace |
| `/personal-trainer-mission-valley` | `/in-home-personal-trainer-san-diego` | 301 | Squarespace |
| `/personal-trainer-clairemont` | `/in-home-personal-trainer-san-diego` | 301 | Squarespace |
| `/personal-trainer-mission-hills` | `/in-home-personal-trainer-san-diego` | 301 | Squarespace |
| `/contact` | `/contactform` | 301 | Squarespace |
| `/free-trial-copy` | `/contactform` | 301 | Squarespace |
| `/reviews` | `/case-studies` | 301 | Squarespace |
| `/personal-training` | `/personal-training-services` | 301 | Squarespace |
| `/services` | `/personal-training-services` | 301 | Squarespace |
| `/training-rates` | `/training-rates-san-diego` | 301 | Squarespace |
| `/rates` | `/training-rates-san-diego` | 301 | Squarespace |
| `/fitnessprograms` | `/training-rates-san-diego` | 301 | Squarespace |
| `/terms-conditions` | `/terms-and-conditions` | 301 | Squarespace |
| `/instructors` | `/about` | 301 | Squarespace |
| `/facility` | `/personal-trainer-4s-ranch` | 301 | Squarespace |
| `/online-coaching` | `/the-30-minute-executive-reset` | 301 | Squarespace |
| `/online-training` | `/the-30-minute-executive-reset` | 301 | Squarespace |
| `/executive-hybrid-coaching` | `/the-30-minute-executive-reset` | 301 | Squarespace |
| `/blog/benefit-of-a-personal-trainer` | `/in-home-personal-trainer-san-diego` | 301 | Squarespace |
| `/blog/best-physical-training-programs-in-mission-bay` | `/in-home-personal-trainer-san-diego` | 301 | Squarespace |
| `/blog/how-to-choose-the-right-personal-trainer-in-pacific-beach-for-your-goals` | `/in-home-personal-trainer-san-diego` | 301 | Squarespace |
| `/blog/how-a-mission-bay-personal-trainer-can-help-you-achieve-peak-physical-fitness` | `/in-home-personal-trainer-san-diego` | 301 | Squarespace |
| `/blog/common-weight-loss-mistakes-and-how-to-fix-them` | `/weight-loss` | 301 | Squarespace |
| `/blog/effective-weight-loss-programs-for-men-over-30-in-san-diego` | `/weight-loss` | 301 | Squarespace |
| `/blog/executive-fitness-in-san-diego-how-busy-professionals-over-30-can-get-results-without-burning-out` | `/about` | 301 | Squarespace |
| `/blog/maximizing-your-potential-understanding-low-testosterones-impact-on-mens-fitness` | `/about` | 301 | Squarespace |
| `/blog/functional-fitness-vs-traditional-workouts` | `/strength-training-1` | 301 | Squarespace |
| `/blog/strength-training-in-pacific-beach` | `/strength-training-1` | 301 | Squarespace |
| `/blog/understanding-personal-trainer-pricing-structures` | `/training-rates-san-diego` | 301 | Squarespace |
| `/blog/how-does-online-personal-training-work` | `/the-30-minute-executive-reset` | 301 | Squarespace |
| `/blog/q4kkx2u2vihb6kxgfepxrhfkkp60hr` | `/` | 301 | Squarespace |
| `/strategy-call` | `https://calendly.com/nemezio-omnifittraining/45min` | 301 | exception |
| `/book-online-consultation` | `https://calendly.com/nemezio-omnifittraining/45min` | 301 | exception |
| `/schedule` | `https://calendly.com/nemezio-omnifittraining/45min` | 301 | exception |
| `/schedule-1` | `https://calendly.com/nemezio-omnifittraining/45min` | 301 | exception |
| `/booking` | `https://calendly.com/nemezio-omnifittraining/45min` | 301 | exception |
| `/appointments-1` | `https://calendly.com/nemezio-omnifittraining/45min` | 301 | exception |
| `/nutrition-coaching` | `/nutrition-coaching-san-diego` | 301 | exception |
| `/blog/are-you-a-good-fit-for-working-with-a-personal-trainer` | `/fit-check` | 301 | exception |
| `/blog/how-personal-trainers-can-motivate-seniors` | `/personal-trainer-over-50-san-diego` | 301 | exception |
| `/energy-protocol-waitlist-form` | `/the-30-minute-executive-reset` | 301 | gap-fill |
| `/testimonials` | `/case-studies` | 301 | gap-fill |
| `/outdoor-fitness-mission-bay` | `/in-home-personal-trainer-san-diego` | 301 | gap-fill |
| `/hiit-personal-trainer-pacific-beach` | `/hiit-personal-trainer-san-diego` | 301 | gap-fill |
| `/hiit-training-mission-bay` | `/hiit-personal-trainer-san-diego` | 301 | gap-fill |
| `/body-building` | `/strength-training-1` | 301 | gap-fill |
| `/bodybuilding` | `/strength-training-1` | 301 | gap-fill |
| `/more` | `/personal-training-services` | 301 | gap-fill |
| `/methodology` | `/the-omnifit-method` | 301 | gap-fill |
| `/faqs-1` | `/faqs` | 301 | gap-fill |
| `/hsa-fsa` | `/hsa-fsa-personal-training` | 301 | gap-fill |
| `/in-home-personal-traning-san-diego` | `/in-home-personal-trainer-san-diego` | 301 | gap-fill |
| `/the-omnifittraining.com/the-omnifit-method` | `/the-omnifit-method` | 301 | gap-fill |
| `/blog` | `/` | 302 | gap-fill |
