#!/usr/bin/env python3
"""Build public/ (the Cloudflare Pages output directory) from the repo sources.

    python3 build.py            # build public/ and print the check report
    python3 build.py --strict   # same, exit 1 if any check fails
    python3 build.py --check    # only run the checks against an existing public/

The checks include keyword ownership (tools/ownership.py, reading the
KEYWORD OWNERSHIP table in CANON.md): no owned phrase in the title, H1, H2s
or meta description of a page other than its owner. Its pass/fail fixtures
run first, so a broken check cannot report green. They also include the
measurement rule (CANON MEASUREMENT): no retired tracking ID or dataLayer
push anywhere in public/, and the GA4 / Clarity IDs at most once per page;
its fixtures run first too.

Sources
  pages/<slug>.html                 page body (one Squarespace Code Block each)
  pages/headers/<slug>-header.html  per-page header injection (JSON-LD, etc.)
  pages/headers/site-header.html    site-wide header injection (GA4 + Clarity,
                                    production only; HubSpot deferral; geo
                                    meta; entity graph)
  pages/footer.html                 site-wide footer (style + markup + script)
  pages/home-1..6.html              homepage sections, concatenated in HOME_ORDER
  site/layout.html, site/nav.html, site/site.css, site/site.js
  site/img/*                        static images, copied to public/assets/img/

Ask OmniFit (the on-site AI assistant): functions/_lib/knowledge.js is
regenerated from assistant/knowledge.md on every build, site/assistant.js and
site/assistant.css are copied to public/assets/, and a small loader is added to
the shared footer on every page. The widget stays hidden until the Pages
Functions in functions/ are configured (see DEPLOY.md, "Ask OmniFit").

Also written: public/_redirects, robots.txt, llms.txt (from site/llms.txt), the favicon set
(favicon.ico, apple-touch-icon.png, icon-192.png, icon-512.png from site/), sitemap.xml, 404.html (noindex,
not in the sitemap, links to Home and Book Your Consultation only) and
_headers (X-Robots-Tag: noindex on the *.pages.dev preview hostname only,
plus security headers on every page). Every page also gets Open Graph /
Twitter card tags (SOCIAL_IMAGE unless its header sets its own).

Nothing here rewrites page copy, schema or CSS rules. The only edits made to
page markup are structural: <style>/<link> tags are lifted out of the body into
<head>, Google Fonts @imports are dropped in favour of the single font link in
the layout, the hrefs listed in LINK_FIXES (links to slugs that do not exist)
are repointed, and every emoji is swapped for a gold line SVG from
site/icons.py. Standard library only.
"""
import datetime
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "pages"
HEADERS = PAGES / "headers"
SITE = ROOT / "site"
PUBLIC = ROOT / "public"
BASE = "https://www.omnifittraining.com"

sys.path.insert(0, str(SITE))
import icons  # noqa: E402  (site/icons.py)
import blog  # noqa: E402  (site/blog.py - the Journal at /blog)
sys.path.insert(0, str(ROOT / "tools"))
import ownership  # noqa: E402  (tools/ownership.py)

# Source files under pages/ that are not standalone pages.
NOT_PAGES = {"footer", "home-0", "home-1", "home-2", "home-3", "home-4", "home-5", "home-6", "home-motion"}

# Homepage = these fragments, in page order. home-0 is the hero built for the
# static site (the only h1); CANON: home-6 sits after the programs section and
# before the FAQ. home-motion is the scroll-reveal layer (CSS lifted to head,
# script runs after every section exists).
HOME_ORDER = ["home-0", "home-1", "home-2", "home-3", "home-4", "home-6", "home-5", "home-motion"]

# Repo file name -> live slug, where they differ. Squarespace slugs are
# lower-case and every internal link in the repo uses /faqs.
SLUG_MAP = {"FAQs": "faqs"}

# Internal links whose target slug has no page anywhere in the repo, repointed
# at build time to the page the repo's own link graph uses for that topic.
# Applied to page bodies only; pages/ sources are left untouched.
LINK_FIXES = {
    "/personal-trainer-in-pacific-beach": "/personal-trainer-4s-ranch",  # link text reads "4S Ranch Training"
    "/services": "/personal-training-services",
    "/how-it-works": "/how-it-works-pricing",
    "/contact": "/contactform",
    "/hybrid-coaching": "/the-30-minute-executive-reset",
}

# Title / meta description for pages with no WebPage node in their header and
# no "SEO Title" comment in the page. Derived from the page's own H1 and the
# description already carried in its header or body schema.
META_FALLBACK = {
    "case-studies": (
        "Client Case Studies | OmniFit Performance San Diego",
        "Documented individual client outcomes from busy professionals in San Diego using the "
        "Assess-Correct-Build-Sustain method. Individual results; outcomes vary.",
    ),
}

# Title / meta description that override whatever the header or page carries.
# fit-check: the uploaded header's WebPage.name is the on-page question; the
# SEO title and description set for the page in October 2026 are these.
META_OVERRIDE = {
    "fit-check": (
        "OmniFit Fit Check | Are You Ready for Coaching?",
        "Seven questions, three minutes. See if you're ready and able for OmniFit's diagnostic-led "
        "coaching in San Diego, and which accountability setting fits you.",
    ),
}

# <title> only (description, header JSON-LD and page body untouched). Squarespace
# appended the site name to every title on render; the static build does not, so
# these 15 pages lost the brand at the Oct 18, 2026 cutover. Owner-approved
# Oct 25, 2026: brand restored, every title kept at 61 characters or fewer.
TITLE_OVERRIDE = {
    "home": "Personal Trainer San Diego | OmniFit Performance",
    "about": "About Nemezio LopezPerez | OmniFit Performance, San Diego",
    "body-composition-testing": "Body Composition Testing San Diego | OmniFit Performance",
    "corrective-exercise-post-rehab": "Corrective Exercise San Diego | Post-Rehab | OmniFit",
    "couples-personal-training-san-diego": "Couples Personal Training San Diego | OmniFit Performance",
    "glp-1-personal-training-san-diego": "GLP-1 Personal Training San Diego | OmniFit Performance",
    "how-to-choose-a-personal-trainer-san-diego": "How to Choose a Personal Trainer: Red Flags | OmniFit",
    "hsa-fsa-personal-training": "HSA & FSA Eligible Personal Training | OmniFit Performance",
    "nutrition-coaching-san-diego": "Nutrition Coaching San Diego | OmniFit Performance",
    "personal-trainer-fairbanks-ranch": "Personal Trainer Fairbanks Ranch | OmniFit Performance",
    "personal-trainer-rancho-santa-fe": "Personal Trainer Rancho Santa Fe | OmniFit Performance",
    "personal-training-services": "Personal Training for Professionals 30+ | OmniFit Performance",
    "strength-training-1": "Strength Training for Professionals 30+ | OmniFit Performance",
    "the-30-minute-executive-reset": "30-Minute Executive Reset | OmniFit Performance",
    "weight-loss": "Sustainable Fat Loss for Professionals 30+ | OmniFit",
}

CALENDLY = "https://calendly.com/nemezio-omnifittraining/45min"

# Open Graph / Twitter card tags on every page, so a link shared by text,
# Facebook or LinkedIn shows a photo, title and description. A page whose
# header already carries og:image (a Journal post, via site/blog.py) keeps its
# own; everything else gets the site default below at the recommended
# 1200x630. Made from hero-coach-client-cable-pulldown-1600.jpg (top-weighted
# crop so both faces stay in frame).
SOCIAL_IMAGE = {
    "src": "/assets/img/og-coach-client-cable-pulldown-1200x630.jpg",
    "width": 1200,
    "height": 630,
    "alt": "Coach Nemezio LopezPerez coaching a client through a cable exercise for the upper back",
}


def social_tags(title, desc, url):
    """Default og:/twitter: tags for a page without its own."""
    e = lambda v: html.escape(str(v), quote=True)
    img = SOCIAL_IMAGE
    tags = [
        ("property", "og:type", "website"),
        ("property", "og:site_name", "OmniFit Performance"),
        ("property", "og:title", title),
        ("property", "og:description", desc),
        ("property", "og:url", url),
        ("property", "og:image", BASE + img["src"]),
        ("property", "og:image:width", img["width"]),
        ("property", "og:image:height", img["height"]),
        ("property", "og:image:alt", img["alt"]),
        ("name", "twitter:card", "summary_large_image"),
        ("name", "twitter:image", BASE + img["src"]),
    ]
    return "".join(f'<meta {a}="{k}" content="{e(v)}">\n' for a, k, v in tags)

# Ask OmniFit. The knowledge file is the assistant's only source of facts;
# knowledge.js is generated from it and never edited by hand.
KNOWLEDGE_MD = ROOT / "assistant" / "knowledge.md"
KNOWLEDGE_JS = ROOT / "functions" / "_lib" / "knowledge.js"
ASSISTANT_ASSETS = ("assistant.js", "assistant.css")
# Appended to the shared footer on every page. Loads the widget only after the
# page has finished loading (and the browser is idle), so it costs nothing on
# first paint; the widget itself is position:fixed, so nothing shifts.
ASSISTANT_LOADER = (
    '<script>(function(){function go(){var s=document.createElement("script");'
    's.src="/assets/assistant.js";s.async=true;document.body.appendChild(s)}'
    'function idle(){"requestIdleCallback" in window?requestIdleCallback(go,{timeout:3000}):setTimeout(go,1500)}'
    'document.readyState==="complete"?idle():window.addEventListener("load",idle)})();</script>'
)

# robots.txt (owner, Oct 2026): search and AI crawlers named and allowed
# site-wide; /api/ (the assistant's functions) disallowed for every agent.
ROBOTS_AGENTS = ("Googlebot", "Google-Extended", "GPTBot", "OAI-SearchBot", "ChatGPT-User",
                 "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Bingbot")
ROBOTS_TXT = (
    "".join(f"User-agent: {a}\nAllow: /\nDisallow: /api/\n\n" for a in ROBOTS_AGENTS)
    + "User-agent: *\nAllow: /\nDisallow: /api/\n\n"
    + f"Sitemap: {BASE}/sitemap.xml\n"
)


def knowledge_js(md_text):
    """assistant/knowledge.md -> the text of functions/_lib/knowledge.js.
    HTML comments (maintainer notes) are dropped, so they never reach the model."""
    body = re.sub(r"<!--.*?-->\s*", "", md_text, flags=re.S).strip() + "\n"
    return ("// GENERATED by build.py from assistant/knowledge.md. Do not edit; edit the .md and rebuild.\n"
            "export const KNOWLEDGE = " + json.dumps(body, ensure_ascii=False) + ";\n")

# Images still hotlinked from Squarespace (build.py --check prints a WARNING per URL).
SQSP_CDN_RE = re.compile(r"https?://[a-z0-9.-]*squarespace-cdn\.com/[^\s\"'<>)]+")

# Cloudflare Pages _redirects: (source, target, status, origin); a None target
# is a comment line. PRINCIPLE (owner, Oct 17 2026; CANON ARCHIVE > REDIRECTS):
# the Squarespace URL Mappings the owner pasted on Oct 17, 2026 are
# authoritative. The only departures are (1) booking URLs -> Calendly (LAUNCH
# DECISIONS item 1), (2) three exact-match pages that did not exist when the
# mapping was made, (3) gap-fills for URLs Google knows that Squarespace never
# mapped. Origins: Squarespace / exception / gap-fill / existing (an earlier
# repo rule kept as it was). `build.py --check` verifies every path in
# tools/gsc-known-urls-2026-10-17.txt resolves, every internal target is a
# built page (so no chains), and no source repeats.
REDIRECTS = [
    ("# OmniFit Performance - Cloudflare Pages redirects (generated by build.py; edit REDIRECTS there)", None, None, None),
    ("# Earlier repo rules, kept unchanged (not in the Squarespace mapping)", None, None, None),
    ('/executive-hybrid', '/the-30-minute-executive-reset', 301, 'existing'),
    ('/personal-trainer-point-loma', '/in-home-personal-trainer-san-diego', 301, 'existing'),
    ('/how-it-works', '/how-it-works-pricing', 301, 'existing'),
    ('/hybrid-coaching', '/the-30-minute-executive-reset', 301, 'existing'),
    ('/is-omnifit-right-for-you', '/fit-check', 301, 'existing'),
    ('/consultation', '/contactform', 301, 'existing'),
    ('/FAQs', '/faqs', 301, 'existing'),
    ("# Squarespace URL Mappings, pasted by the owner Oct 17 2026 (authoritative, targets unchanged)", None, None, None),
    ('/new-page', '/private-personal-trainer-san-diego', 301, 'Squarespace'),
    ('/new-page-1', '/', 301, 'Squarespace'),
    ('/home', '/', 301, 'Squarespace'),
    ('/store', '/', 301, 'Squarespace'),
    ('/strength-training', '/strength-training-1', 301, 'Squarespace'),
    ('/nutritional-coaching-mission-bay', '/weight-loss', 301, 'Squarespace'),
    ('/nutritional-coaching-mission-bat', '/weight-loss', 301, 'Squarespace'),
    ('/nutritional-coaching-pacific-beach', '/weight-loss', 301, 'Squarespace'),
    ('/fat-loss-training', '/weight-loss', 301, 'Squarespace'),
    ('/weight-loss-training-remote-training', '/weight-loss', 301, 'Squarespace'),
    ('/weight-loss-training-mission-bay', '/weight-loss', 301, 'Squarespace'),
    ('/personal-trainer-pacific-beach', '/in-home-personal-trainer-san-diego', 301, 'Squarespace'),
    ('/personal-trainer-in-pacific-beach', '/in-home-personal-trainer-san-diego', 301, 'Squarespace'),
    ('/personal-trainer-mission-bay', '/in-home-personal-trainer-san-diego', 301, 'Squarespace'),
    ('/personal-trainer-mission-valley', '/in-home-personal-trainer-san-diego', 301, 'Squarespace'),
    ('/personal-trainer-clairemont', '/in-home-personal-trainer-san-diego', 301, 'Squarespace'),
    ('/personal-trainer-mission-hills', '/in-home-personal-trainer-san-diego', 301, 'Squarespace'),
    ('/contact', '/contactform', 301, 'Squarespace'),
    ('/free-trial-copy', '/contactform', 301, 'Squarespace'),
    ('/reviews', '/case-studies', 301, 'Squarespace'),
    ('/personal-training', '/personal-training-services', 301, 'Squarespace'),
    ('/services', '/personal-training-services', 301, 'Squarespace'),
    ('/training-rates', '/training-rates-san-diego', 301, 'Squarespace'),
    ('/rates', '/training-rates-san-diego', 301, 'Squarespace'),
    ('/fitnessprograms', '/training-rates-san-diego', 301, 'Squarespace'),
    ('/terms-conditions', '/terms-and-conditions', 301, 'Squarespace'),
    ('/instructors', '/about', 301, 'Squarespace'),
    ('/facility', '/personal-trainer-4s-ranch', 301, 'Squarespace'),
    ('/online-coaching', '/the-30-minute-executive-reset', 301, 'Squarespace'),
    ('/online-training', '/the-30-minute-executive-reset', 301, 'Squarespace'),
    ('/executive-hybrid-coaching', '/the-30-minute-executive-reset', 301, 'Squarespace'),
    ('/blog/benefit-of-a-personal-trainer', '/in-home-personal-trainer-san-diego', 301, 'Squarespace'),
    ('/blog/best-physical-training-programs-in-mission-bay', '/in-home-personal-trainer-san-diego', 301, 'Squarespace'),
    ('/blog/how-to-choose-the-right-personal-trainer-in-pacific-beach-for-your-goals', '/in-home-personal-trainer-san-diego', 301, 'Squarespace'),
    ('/blog/how-a-mission-bay-personal-trainer-can-help-you-achieve-peak-physical-fitness', '/in-home-personal-trainer-san-diego', 301, 'Squarespace'),
    ('/blog/common-weight-loss-mistakes-and-how-to-fix-them', '/weight-loss', 301, 'Squarespace'),
    ('/blog/effective-weight-loss-programs-for-men-over-30-in-san-diego', '/weight-loss', 301, 'Squarespace'),
    ('/blog/executive-fitness-in-san-diego-how-busy-professionals-over-30-can-get-results-without-burning-out', '/about', 301, 'Squarespace'),
    ('/blog/maximizing-your-potential-understanding-low-testosterones-impact-on-mens-fitness', '/about', 301, 'Squarespace'),
    ('/blog/functional-fitness-vs-traditional-workouts', '/strength-training-1', 301, 'Squarespace'),
    ('/blog/strength-training-in-pacific-beach', '/strength-training-1', 301, 'Squarespace'),
    ('/blog/understanding-personal-trainer-pricing-structures', '/training-rates-san-diego', 301, 'Squarespace'),
    ('/blog/how-does-online-personal-training-work', '/the-30-minute-executive-reset', 301, 'Squarespace'),
    ('/blog/q4kkx2u2vihb6kxgfepxrhfkkp60hr', '/', 301, 'Squarespace'),
    ("# Exception: booking URLs -> Calendly (LAUNCH DECISIONS item 1)", None, None, None),
    ('/strategy-call', CALENDLY, 301, 'exception'),
    ('/book-online-consultation', CALENDLY, 301, 'exception'),
    ('/schedule', CALENDLY, 301, 'exception'),
    ('/schedule-1', CALENDLY, 301, 'exception'),
    ('/booking', CALENDLY, 301, 'exception'),
    ('/appointments-1', CALENDLY, 301, 'exception'),
    ("# Exception: exact-match pages that did not exist when the mapping was made", None, None, None),
    ('/nutrition-coaching', '/nutrition-coaching-san-diego', 301, 'exception'),
    ('/blog/are-you-a-good-fit-for-working-with-a-personal-trainer', '/fit-check', 301, 'exception'),
    ('/blog/how-personal-trainers-can-motivate-seniors', '/personal-trainer-over-50-san-diego', 301, 'exception'),
    ("# Gap-fills: URLs Google knows that Squarespace never mapped", None, None, None),
    ('/energy-protocol-waitlist-form', '/the-30-minute-executive-reset', 301, 'gap-fill'),
    ('/testimonials', '/case-studies', 301, 'gap-fill'),
    ('/outdoor-fitness-mission-bay', '/in-home-personal-trainer-san-diego', 301, 'gap-fill'),
    ('/hiit-personal-trainer-pacific-beach', '/hiit-personal-trainer-san-diego', 301, 'gap-fill'),
    ('/hiit-training-mission-bay', '/hiit-personal-trainer-san-diego', 301, 'gap-fill'),
    ('/body-building', '/strength-training-1', 301, 'gap-fill'),
    ('/bodybuilding', '/strength-training-1', 301, 'gap-fill'),
    ('/more', '/personal-training-services', 301, 'gap-fill'),
    ('/methodology', '/the-omnifit-method', 301, 'gap-fill'),
    ('/faqs-1', '/faqs', 301, 'gap-fill'),
    ('/hsa-fsa', '/hsa-fsa-personal-training', 301, 'gap-fill'),
    ('/in-home-personal-traning-san-diego', '/in-home-personal-trainer-san-diego', 301, 'gap-fill'),
    ('/the-omnifittraining.com/the-omnifit-method', '/the-omnifit-method', 301, 'gap-fill'),
    ("# Temporary: a blog is planned at this path", None, None, None),
    ('/blog', '/', 302, 'gap-fill'),
]

GSC_KNOWN = ROOT / "tools" / "gsc-known-urls-2026-10-17.txt"

# public/404.html. Standalone (no nav, no footer): the page carries exactly two
# links, Home and Book Your Consultation, and a noindex meta. Cloudflare Pages
# serves /404.html for every unmatched route.
NOT_FOUND_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page Not Found | OmniFit Performance</title>
<meta name="robots" content="noindex">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/montserrat-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/playfair-display-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<style>
/* Self-hosted fonts (Oct 25 2026): Montserrat + Playfair Display variable, latin
   subset, served from this site instead of Google Fonts. Same families, every
   weight 100-900 and italics; removes the render-blocking Google Fonts request. */
@font-face{{font-family:'Montserrat';font-style:normal;font-weight:100 900;font-display:swap;src:url(/assets/fonts/montserrat-latin-wght-normal.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD;}}
@font-face{{font-family:'Montserrat';font-style:italic;font-weight:100 900;font-display:swap;src:url(/assets/fonts/montserrat-latin-wght-italic.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD;}}
@font-face{{font-family:'Playfair Display';font-style:normal;font-weight:400 900;font-display:swap;src:url(/assets/fonts/playfair-display-latin-wght-normal.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD;}}
@font-face{{font-family:'Playfair Display';font-style:italic;font-weight:400 900;font-display:swap;src:url(/assets/fonts/playfair-display-latin-wght-italic.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD;}}
</style>
<style>
  html,body{{margin:0;min-height:100%;background:#0a1628;color:#fff;font-family:'Montserrat',sans-serif}}
  .nf{{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:48px 20px;text-align:center}}
  .nf h1{{font-family:'Playfair Display',serif;font-size:clamp(30px,5vw,48px);margin:0 0 16px}}
  .nf p{{color:rgba(255,255,255,.7);font-size:17px;line-height:1.7;max-width:520px;margin:0 auto 28px}}
  .nf-row{{display:flex;flex-wrap:wrap;gap:14px;justify-content:center}}
  .nf-btn{{display:inline-block;padding:14px 32px;border-radius:6px;font-weight:700;font-size:12px;letter-spacing:1.5px;text-transform:uppercase;text-decoration:none;color:#fff;border:1px solid rgba(255,255,255,.3)}}
  .nf-btn--primary{{background:#c9a84c;border-color:#c9a84c;color:#0a1628}}
</style>
</head>
<body class="page page--404">
<main id="main" class="nf">
  <div>
    <h1>Page Not Found</h1>
    <p>That page isn't here. It may have moved when the site was rebuilt, or the address has a typo.</p>
    <div class="nf-row">
      <a class="nf-btn" href="/">Home</a>
      <a class="nf-btn nf-btn--primary" href="{CALENDLY}" target="_blank" rel="noopener">Book Your Consultation</a>
    </div>
  </div>
</main>
</body>
</html>
"""

# public/_headers (Cloudflare Pages). Only the preview hostname is marked
# noindex; www.omnifittraining.com gets no X-Robots-Tag.
# Security headers on every page (site audit, Oct 20 2026). The CSP is
# deliberately narrow: it stops other sites framing the pages (clickjacking),
# plugins, and <base> hijacking, and upgrades any stray http:// asset. It does
# NOT allowlist scripts: every page runs inline scripts (and GA4, Clarity,
# HubSpot, Calendly), so a script-src policy would need 'unsafe-inline' and
# buy little for the breakage risk. Permissions-Policy leaves payment alone
# (Calendly takes the consultation deposit).
# Browser caching (Oct 25 2026): fonts never change (a year, immutable); images
# keep their file names when replaced, so they get 30 days rather than a year.
# site.css / site.js stay on Cloudflare's default so edits show up immediately.
HEADERS_TXT = """https://:project.pages.dev/*
  X-Robots-Tag: noindex

/*
  Strict-Transport-Security: max-age=31536000
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
  Content-Security-Policy: frame-ancestors 'self'; base-uri 'self'; object-src 'none'; upgrade-insecure-requests
  Permissions-Policy: camera=(), microphone=(), geolocation=()

/assets/fonts/*
  Cache-Control: public, max-age=31536000, immutable

/assets/img/*
  Cache-Control: public, max-age=2592000, stale-while-revalidate=86400
"""

STYLE_RE = re.compile(r"<style\b[^>]*>.*?</style>", re.S | re.I)
LINK_RE = re.compile(r"<link\b[^>]*>", re.I)
IMPORT_RE = re.compile(r"^[ \t]*@import\s+url\([^)]*\)\s*;?[ \t]*\r?\n?", re.M)
LDJSON_RE = re.compile(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', re.S)
H1_RE = re.compile(r"<h1\b", re.I)
HREF_RE = re.compile(r'href="(/[^"#?]*)')


def read(p):
    return Path(p).read_text(encoding="utf-8")


def git_date(*paths):
    """Last commit date (YYYY-MM-DD) touching any of the given source files."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", *[str(p) for p in paths]],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        if out:
            return out
    except Exception:
        pass
    return datetime.date.today().isoformat()


def header_nodes(text):
    """Every node across every ld+json block in a header file."""
    nodes = []
    for block in LDJSON_RE.findall(text):
        d = json.loads(block)
        if isinstance(d, dict) and "@graph" in d:
            nodes.extend(d["@graph"])
        elif isinstance(d, list):
            nodes.extend(d)
        else:
            nodes.append(d)
    return nodes


def page_meta(slug, page_text, header_text):
    t, d, src = _page_meta(slug, page_text, header_text)
    if slug in TITLE_OVERRIDE:
        return TITLE_OVERRIDE[slug], d, src + " + TITLE_OVERRIDE"
    return t, d, src


def _page_meta(slug, page_text, header_text):
    """(title, description) - header WebPage node, else the page's SEO
    comments, else META_FALLBACK. Returns the source label too."""
    if slug in META_OVERRIDE:
        return (*META_OVERRIDE[slug], "build.py META_OVERRIDE")
    if header_text:
        for n in header_nodes(header_text):
            if n.get("@type") == "WebPage" and n.get("name"):
                return n["name"], n.get("description", ""), "header WebPage node"
    t = re.search(r"<!--\s*SEO Title:\s*(.*?)\s*-->", page_text)
    d = re.search(r"<!--\s*SEO Description:\s*(.*?)\s*-->", page_text)
    if t:
        return html.unescape(t.group(1)), html.unescape(d.group(1)) if d else "", "page SEO comment"
    if slug in META_FALLBACK:
        return (*META_FALLBACK[slug], "build.py META_FALLBACK (derived)")
    raise SystemExit(f"{slug}: no title source (add it to META_FALLBACK)")


COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def split_body(body):
    """Lift <style> and <link> tags out of the page body.
    Returns (body, styles, links). Google Fonts links/imports are dropped
    because the layout loads one font stylesheet covering every weight.
    HTML comments are masked first: a paste note such as "Paste everything
    from <style> to the end" must not be taken as the start of a style block
    (it swallowed the comment's closing "-->", which left the page's wrapper
    div commented out in the browser and its scoped CSS unapplied)."""
    comments = []

    def stash(m):
        comments.append(m.group(0))
        return f"\x00C{len(comments) - 1}\x00"

    body = COMMENT_RE.sub(stash, body)
    styles = []

    def take_style(m):
        css = IMPORT_RE.sub("", m.group(0))
        styles.append(css)
        return ""

    body = STYLE_RE.sub(take_style, body)
    links = []

    def take_link(m):
        tag = m.group(0)
        if "fonts.googleapis.com" in tag or "fonts.gstatic.com" in tag:
            return ""
        links.append(tag)
        return ""

    body = LINK_RE.sub(take_link, body)
    body = re.sub(r"\x00C(\d+)\x00", lambda m: comments[int(m.group(1))], body)
    return body, styles, links


def fix_links(body):
    for old, new in LINK_FIXES.items():
        body = body.replace(f'href="{old}"', f'href="{new}"')
    return body


CSS_CONTENT_EMOJI_RE = re.compile(r"content:\s*(['\"])(" + icons.EMOJI_RE.pattern + r")\1\s*;")


def replace_emoji(body, styles, where):
    """Emoji in markup -> inline SVG; emoji in a CSS content: string -> the
    same icon as a background image on a 1em box. Returns the new body, the
    new styles and {char: count}."""
    body, counts = icons.replace(body, where)
    new_styles = []
    for css in styles:
        def sub(m):
            ch = m.group(3)
            if ch in icons.KEEP:
                return m.group(0)
            counts[ch] = counts.get(ch, 0) + 1
            return (f"content: ''; width: 1em; height: 1em; "
                    f"background: {icons.css_data_uri(ch)} center / contain no-repeat;")
        css = CSS_CONTENT_EMOJI_RE.sub(sub, css)
        left = icons.find(css)
        if left:
            raise icons.UnmappedEmoji(f"{where}: emoji still in CSS outside a content: string: {left}")
        new_styles.append(css)
    return body, new_styles, counts


def load_nav():
    """site/nav.html with the ANNOUNCEMENT line applied.
    Returns the nav HTML (announcement bar removed when its text is empty)."""
    nav = read(SITE / "nav.html").strip()
    m = re.search(r"^ANNOUNCEMENT:\s*(\{.*\})\s*$", nav, re.M)
    if not m:
        raise SystemExit("site/nav.html: ANNOUNCEMENT line missing")
    ann = json.loads(m.group(1))
    text, href = ann.get("text", "").strip(), ann.get("href", "/").strip()
    if text:
        nav = nav.replace("{{announce_text}}", html.escape(text, quote=True))
        nav = nav.replace("{{announce_href}}", html.escape(href, quote=True))
    else:
        nav = re.sub(r'<div class="site-announce".*?</div>\s*', "", nav, count=1, flags=re.S)
    return nav


def mark_active(nav, url_path):
    """aria-current on the nav link for this page; is-active on the dropdown
    that contains it (so the trigger is underlined too)."""
    target = f'href="{url_path}"'
    if target not in nav:
        return nav
    nav = nav.replace(f"<a {target}>", f'<a {target} aria-current="page">', 1)
    # Walk the <li class="has-menu"> blocks and flag the one holding the link.
    def flag(m):
        block = m.group(0)
        return block.replace('<li class="has-menu">', '<li class="has-menu is-active">', 1) if 'aria-current="page"' in block else block
    return re.sub(r'<li class="has-menu">.*?</ul>\s*</li>', flag, nav, flags=re.S)


def footer_parts():
    """pages/footer.html -> (css, markup, js)."""
    text = read(PAGES / "footer.html")
    css = "\n".join(m.group(0) for m in STYLE_RE.finditer(text))
    css = re.sub(r"</?style[^>]*>", "", css).strip()
    js = "\n".join(re.findall(r"<script>(.*?)</script>", text, re.S)).strip()
    markup = STYLE_RE.sub("", text)
    markup = re.sub(r"<script>.*?</script>", "", markup, flags=re.S).strip()
    return css, markup, js


def render(layout, **kw):
    out = layout
    for k, v in kw.items():
        out = out.replace("{{" + k + "}}", v)
    leftover = re.findall(r"{{\w+}}", out)
    if leftover:
        raise SystemExit(f"unfilled placeholders: {leftover}")
    return out


def build():
    layout = read(SITE / "layout.html")
    nav = load_nav()
    site_header = read(HEADERS / "site-header.html").strip()
    footer_css, footer_html, footer_js = footer_parts()
    # The Journal (site/blog.py). With no post in pages/blog/ the build output
    # is unchanged: no /blog page, the /blog 302 stays, no CSS, no footer link.
    posts = blog.load_posts(PAGES / "blog", SITE / "img")
    footer_html = footer_html.replace("<!--BLOG_LINK-->", blog.FOOTER_LINK if posts else "")
    footer_html += "\n" + ASSISTANT_LOADER

    # Ask OmniFit knowledge, regenerated on every build.
    KNOWLEDGE_JS.parent.mkdir(parents=True, exist_ok=True)
    KNOWLEDGE_JS.write_text(knowledge_js(read(KNOWLEDGE_MD)), encoding="utf-8")

    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    (PUBLIC / "assets").mkdir(parents=True)
    # Static images: site/img/<file> is served at /assets/img/<file>.
    if (SITE / "img").is_dir():
        shutil.copytree(SITE / "img", PUBLIC / "assets" / "img")
    # Self-hosted web fonts: site/fonts/<file> is served at /assets/fonts/<file>.
    if (SITE / "fonts").is_dir():
        shutil.copytree(SITE / "fonts", PUBLIC / "assets" / "fonts")
    (PUBLIC / "assets" / "site.css").write_text(
        read(SITE / "site.css").rstrip() + "\n\n/* ===== Footer (source: pages/footer.html) ===== */\n" + footer_css + "\n"
        + ("\n" + read(SITE / "blog.css") if posts else ""),
        encoding="utf-8",
    )
    for name in ASSISTANT_ASSETS:
        shutil.copyfile(SITE / name, PUBLIC / "assets" / name)
    (PUBLIC / "assets" / "site.js").write_text(
        read(SITE / "site.js").rstrip() + "\n\n/* ===== Footer year (source: pages/footer.html) ===== */\n" + footer_js + "\n",
        encoding="utf-8",
    )

    pages = []  # (url_path, title, meta_source, lastmod)
    emoji_report = {}  # url_path -> {char: count}

    def emit(slug, url_path, body_text, sources, header_path, title, desc, meta_source,
             header_text=None, lastmod=None):
        if header_text is None:
            header_text = read(header_path).strip() if header_path else ""
        # The layout sets the canonical; drop a duplicate carried by a header.
        header_text = re.sub(r'<link rel="canonical"[^>]*>\s*', "", header_text)
        body, styles, links = split_body(body_text)
        body = fix_links(body)
        body, styles, counts = replace_emoji(body, styles, url_path)
        if counts:
            emoji_report[url_path] = counts
        canonical = BASE + ("/" if url_path == "/" else url_path)
        social = "" if 'property="og:image"' in header_text else social_tags(title, desc, canonical)
        doc = render(
            layout,
            title=html.escape(title, quote=True),
            description=html.escape(desc, quote=True),
            canonical=canonical,
            social=social,
            site_header=site_header,
            page_header_source=str(header_path.relative_to(ROOT)) if header_path else ("site/blog.py" if header_text else "none"),
            page_header=header_text or "<!-- (this page has no header file) -->",
            page_links="\n".join(links),
            page_source=", ".join(str(s.relative_to(ROOT)) for s in sources),
            page_styles="\n".join(styles),
            slug=slug,
            nav=mark_active(nav, url_path),
            body=body.strip("\n"),
            footer=footer_html,
        )
        # Flat files (CANON / DEPLOY.md "Trailing slash"): Cloudflare Pages
        # serves public/<slug>.html at /<slug> directly, whereas
        # public/<slug>/index.html is served at /<slug>/ with a redirect from
        # /<slug> - and every canonical, sitemap entry and internal link uses
        # /<slug>. The homepage stays public/index.html.
        out = PUBLIC / ("index.html" if url_path == "/" else url_path.strip("/") + ".html")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(doc, encoding="utf-8")
        pages.append((url_path, title, meta_source,
                      lastmod or git_date(*sources, *([header_path] if header_path else []))))

    # Homepage
    home_sources = [PAGES / f"{f}.html" for f in HOME_ORDER]
    home_header = HEADERS / "home-header.html"
    title, desc, src = page_meta("home", "", read(home_header))
    emit("home", "/", "\n\n".join(read(p) for p in home_sources), home_sources, home_header, title, desc, src)

    # Every other page
    for p in sorted(PAGES.glob("*.html")):
        name = p.stem
        if name in NOT_PAGES:
            continue
        slug = SLUG_MAP.get(name, name)
        header = HEADERS / f"{name}-header.html"
        header = header if header.exists() else None
        text = read(p)
        title, desc, src = page_meta(name, text, read(header) if header else "")
        if name == "terms-and-conditions":
            # Squarespace TEXT page: no wrapper or CSS of its own.
            text = '<div id="omni-terms" class="omni-text-page">\n' + text + "\n</div>"
        emit(slug, f"/{slug}", text, [p], header, title, desc, src)

    # The Journal: one page per post at /blog/<slug> (public/blog/<slug>.html),
    # plus the index at /blog (public/blog.html). Dates come from each post's
    # metadata, not git, so the sitemap carries the real publish/update date.
    if posts:
        for post in posts:
            emit(f"blog-{post['slug']}", f"/blog/{post['slug']}", blog.post_body(post), [post["path"]], None,
                 post["title"], post["description"], "pages/blog POST metadata",
                 header_text=blog.post_header(post, BASE), lastmod=post["updated"])
        emit("blog", "/blog", blog.index_body(posts), [p["path"] for p in posts], None,
             blog.INDEX_TITLE, blog.INDEX_DESC, "site/blog.py",
             header_text=blog.index_header(posts, BASE), lastmod=max(p["updated"] for p in posts))

    # _redirects (the /blog 302 placeholder drops out once the Journal has a post)
    lines = []
    for old, new, status, _origin in REDIRECTS:
        if posts and old == "/blog":
            continue
        lines.append(old if new is None else f"{old} {new} {status}")
    (PUBLIC / "_redirects").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # robots.txt
    (PUBLIC / "robots.txt").write_text(ROBOTS_TXT, encoding="utf-8")

    # llms.txt - AI-assistant summary of the site, copied verbatim from site/llms.txt
    shutil.copyfile(SITE / "llms.txt", PUBLIC / "llms.txt")
    # favicon set (site/favicon.ico etc.), served from the site root where browsers look for it
    for icon in ("favicon.ico", "apple-touch-icon.png", "icon-192.png", "icon-512.png"):
        shutil.copyfile(SITE / icon, PUBLIC / icon)
    if posts:
        with open(PUBLIC / "llms.txt", "a", encoding="utf-8") as fh:
            fh.write(blog.llms_lines(posts, BASE))

    # 404.html - Cloudflare Pages serves it for any route with no file and no
    # redirect. Not a page: it is never appended to `pages`, so it stays out of
    # the sitemap; noindex; links to Home and Book Your Consultation only.
    (PUBLIC / "404.html").write_text(NOT_FOUND_HTML, encoding="utf-8")

    # _headers - the *.pages.dev preview hostname is never indexed. The
    # production domain carries no X-Robots-Tag and stays indexable.
    (PUBLIC / "_headers").write_text(HEADERS_TXT, encoding="utf-8")

    # sitemap.xml
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url_path, _t, _s, lastmod in sorted(pages, key=lambda r: (r[0] != "/", r[0])):
        loc = BASE + ("/" if url_path == "/" else url_path)
        sm.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n  </url>")
    sm.append("</urlset>")
    (PUBLIC / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")

    return pages, emoji_report


def read_redirects(text):
    """public/_redirects text -> [(source, target, status, line_no)]."""
    rules = []
    for i, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        rules.append((parts[0], parts[1] if len(parts) > 1 else "",
                      parts[2] if len(parts) > 2 else "", i))
    return rules


def read_known(path):
    """tools/gsc-known-urls-*.txt -> [path], comments and blanks skipped."""
    return [l.strip() for l in Path(path).read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.strip().startswith("#")]


def norm(path):
    return path.rstrip("/") or "/"


def check_redirects(rules, built, known):
    """The redirect rules (CANON ARCHIVE > REDIRECTS), as problem strings:
      unresolved  a known path that is neither a built page nor a rule source
      missing     a rule whose internal target is not a built page
      chain       a rule whose target is itself a rule source (a target must
                  be a built page or an external https:// URL)
      duplicate   the same source on two lines
      status      a status other than 301 or 302
    `built` is the set of built page paths; `known` the known-URL list."""
    problems = []
    sources = {}
    for src, tgt, status, ln in rules:
        if src in sources:
            problems.append(f"duplicate: {src} on _redirects lines {sources[src]} and {ln}")
        else:
            sources[src] = ln
    target_of = {}
    for src, tgt, _status, _ln in rules:
        target_of.setdefault(src, tgt)
    for src, tgt, status, ln in rules:
        if status not in ("301", "302"):
            problems.append(f"status: {src} -> {tgt} has status {status or '(none)'!r} (line {ln})")
        if tgt.startswith("https://"):
            continue
        if not tgt.startswith("/"):
            problems.append(f"missing: {src} -> {tgt!r} is neither an internal path nor an https:// URL (line {ln})")
        elif tgt in sources or norm(tgt) in sources:
            hop = tgt if tgt in sources else norm(tgt)
            problems.append(f"chain: {src} -> {tgt} -> {target_of[hop]} (line {ln}); target a built page directly")
        elif norm(tgt) not in built:
            problems.append(f"missing: {src} -> {tgt} targets no built page (line {ln})")
    for path in known:
        if norm(path) not in built and path not in sources:
            problems.append(f"unresolved: known URL {path} is neither a built page nor a _redirects source")
    return problems


def redirect_selftest(rules, built, known):
    """Each fixture mutates the real rule set and must raise exactly its own
    problem kind. Returns a list of fixtures that misbehaved (empty = OK)."""
    base = set(check_redirects(rules, built, known))
    kinds = lambda probs: sorted({p.split(":", 1)[0] for p in set(probs) - base})
    bad = []
    droppable = next((r for r in rules if r[0] in known and norm(r[0]) not in built), None)
    page = next(iter(sorted(built)))
    fixtures = [
        ("remove one rule", [r for r in rules if r is not droppable], "unresolved"),
        ("add a chain", rules + [("/zz-selftest-chain", rules[0][0], "301", 0)], "chain"),
        ("add a duplicate source", rules + [(rules[0][0], page, "301", 0)], "duplicate"),
        ("add a missing target", rules + [("/zz-selftest-missing", "/zz-no-such-page", "301", 0)], "missing"),
        ("add a bad status", rules + [("/zz-selftest-status", page, "308", 0)], "status"),
    ]
    if droppable is None:
        bad.append("no rule whose source is a known URL to drop")
    for name, mutated, want in fixtures:
        got = kinds(check_redirects(mutated, built, known))
        if got != [want]:
            bad.append(f"{name}: expected [{want}], got {got}")
    return bad


# Measurement (CANON MEASUREMENT). The retired trackers must appear nowhere in
# public/ (any file), and the live IDs at most once per built page: the
# site-wide header is their single source, so a second occurrence means a page
# or header grew its own copy.
TRACKING_BANNED = ("GTM-5P4CKPT2", "ulpgsrkd98", "AW-16616873404", "G-QTG1ZLR0NQ", "dataLayer.push")
TRACKING_ONCE = ("G-0K6VLEC2VJ", "yzawpvwvdf")


def check_tracking(files):
    """files: {relative path: text} for everything under public/.
    Problems: 'banned: <needle> in <file>' and 'repeated: <id> x<n> in <page>'."""
    problems = []
    for rel in sorted(files):
        text = files[rel]
        for needle in TRACKING_BANNED:
            if needle in text:
                problems.append(f"banned: {needle} in {rel}")
        if rel.endswith(".html"):
            for ident in TRACKING_ONCE:
                n = text.count(ident)
                if n > 1:
                    problems.append(f"repeated: {ident} x{n} in {rel}")
    return problems


def tracking_selftest(files):
    """Each fixture mutates a copy of the real public/ text and must raise
    exactly its own problem kind (and nothing on the untouched set).
    Returns the fixtures that misbehaved (empty = OK)."""
    base = set(check_tracking(files))
    kinds = lambda probs: sorted({p.split(":", 1)[0] for p in set(probs) - base})
    page = next((r for r in sorted(files) if r.endswith(".html") and "/" not in r and r != "404.html"), None)
    if page is None:
        return ["no built page to mutate"]
    bad = []
    if base:
        bad.append(f"real public/ already fails: {sorted(base)[:3]}")
    for needle in TRACKING_BANNED:
        for where in (page, "assets/site.js"):
            if where not in files:
                bad.append(f"{where} missing from public/")
                continue
            mutated = dict(files)
            mutated[where] = files[where] + "\n<!-- " + needle + " -->\n"
            got = kinds(check_tracking(mutated))
            if got != ["banned"]:
                bad.append(f"{needle} in {where}: expected [banned], got {got}")
    for ident in TRACKING_ONCE:
        if files[page].count(ident) != 1:
            bad.append(f"{page} should carry {ident} exactly once, has {files[page].count(ident)}")
        mutated = dict(files)
        mutated[page] = files[page] + "\n<!-- " + ident + " -->\n"
        got = kinds(check_tracking(mutated))
        if got != ["repeated"]:
            bad.append(f"second {ident} in {page}: expected [repeated], got {got}")
    return bad


def check_flat(rels):
    """Trailing slash (DEPLOY.md): rels = every file path under public/,
    relative. A nested <dir>/index.html would be served at /<dir>/ and
    /<dir> would redirect to it, so any index.html other than the homepage's
    is a problem."""
    return [f"nested: {r} exists; a page must be public/<slug>.html so /<slug> is served without a redirect"
            for r in sorted(rels) if r.endswith("index.html") and r != "index.html"]


def flat_selftest(rels):
    """Adding a nested index.html to the real file list must raise exactly
    one 'nested' problem, and a flat layout none. Returns the fixtures that misbehaved."""
    bad = []
    # Fixtures run on the real list minus anything the real check reports, so
    # a real nested file is reported once (by the check), not as a fixture.
    rels = {r for r in rels if not check_flat({r})}
    for fx in ("about/index.html", "personal-trainer-del-mar/index.html"):
        got = check_flat(rels | {fx})
        if len(got) != 1 or not got[0].startswith("nested: " + fx):
            bad.append(f"adding {fx}: expected one nested problem, got {got}")
    if check_flat({"index.html", "about.html", "assets/site.css"}):
        bad.append("a flat layout was flagged")
    return bad


def page_path(f):
    """public/index.html -> '/', public/<slug>.html -> '/<slug>',
    public/blog/<slug>.html -> '/blog/<slug>'."""
    return ownership._url_path(PUBLIC, f)


def check():
    """Every internal link resolves, exactly one H1 per page, JSON-LD parses."""
    files = ownership.built_pages(PUBLIC)
    redirects = {}
    rules = read_redirects((PUBLIC / "_redirects").read_text(encoding="utf-8"))
    for a, b, _status, _ln in rules:
        redirects.setdefault(a, b)
    existing = {page_path(f) for f in files}
    built = set(existing)  # built pages only (no static files)
    for f in PUBLIC.rglob("*"):
        if f.is_file() and f not in files:
            existing.add("/" + f.relative_to(PUBLIC).as_posix())

    problems = []
    notes = []
    broken = {}
    for f in files:
        page = page_path(f)
        text = f.read_text(encoding="utf-8")
        n_h1 = len(H1_RE.findall(re.sub(r"<!--.*?-->", "", text, flags=re.S)))
        if n_h1 != 1:
            problems.append(f"{page}: {n_h1} <h1> elements")
        left = icons.find(text.split("<body", 1)[1])
        if left:
            problems.append(f"{page}: emoji still present: {' '.join(left)}")
        if page != "/404":
            # Social preview: one og:image + twitter:card, og:url = canonical,
            # and the image is a file this build ships.
            ogi = re.findall(r'<meta property="og:image" content="([^"]*)"', text)
            ogu = re.findall(r'<meta property="og:url" content="([^"]*)"', text)
            canon = re.findall(r'<link rel="canonical" href="([^"]*)"', text)
            n_tc = text.count('name="twitter:card"')
            if len(ogi) != 1 or n_tc != 1:
                problems.append(f"{page}: expected one og:image and one twitter:card, found {len(ogi)} / {n_tc}")
            elif not ogi[0].startswith(BASE + "/") or not (PUBLIC / ogi[0][len(BASE) + 1:]).is_file():
                problems.append(f"{page}: og:image {ogi[0]} is not a file in public/")
            if ogu != canon:
                problems.append(f"{page}: og:url {ogu} does not match canonical {canon}")
        for i, block in enumerate(LDJSON_RE.findall(text), 1):
            try:
                json.loads(block)
            except json.JSONDecodeError as e:
                problems.append(f"{page}: JSON-LD block {i} does not parse: {e}")
        for href in sorted(set(HREF_RE.findall(text))):
            target = href.rstrip("/") or "/"
            if target in existing:
                continue
            if target in redirects and (redirects[target].rstrip("/") or "/") in existing:
                notes.append(f"{href} resolves via _redirects -> {redirects[target]}")
                continue
            broken.setdefault(href, []).append(page)
    for href, on in broken.items():
        where = "every page (nav or footer link)" if len(on) == len(files) else ", ".join(on)
        problems.append(f"broken internal link {href} on {where}")
    # Launch plumbing: 404.html (noindex, out of the sitemap, two links) and
    # _headers (preview hostname noindex, production domain untouched).
    nf = PUBLIC / "404.html"
    if not nf.exists():
        problems.append("404.html missing")
    else:
        t = nf.read_text(encoding="utf-8")
        if '<meta name="robots" content="noindex">' not in t:
            problems.append("404.html: no noindex meta")
        if "<title>Page Not Found | OmniFit Performance</title>" not in t:
            problems.append("404.html: wrong title")
        hrefs = re.findall(r'href="([^"]+)"', t.split("<body", 1)[1])
        if hrefs != ["/", CALENDLY]:
            problems.append(f"404.html: links must be Home and Book Your Consultation only, got {hrefs}")
    if "404" in (PUBLIC / "sitemap.xml").read_text(encoding="utf-8"):
        problems.append("sitemap.xml lists the 404 page")
    hd = (PUBLIC / "_headers")
    if not hd.exists() or hd.read_text(encoding="utf-8") != HEADERS_TXT:
        problems.append("_headers: preview-hostname noindex rule or security headers missing or altered")
    elif "omnifittraining.com" in HEADERS_TXT:
        problems.append("_headers: production domain must not carry X-Robots-Tag")
    # Ask OmniFit: knowledge.js in step with knowledge.md, widget assets built
    # from site/, the loader on every page, robots.txt as written above.
    if not KNOWLEDGE_JS.exists() or KNOWLEDGE_JS.read_text(encoding="utf-8") != knowledge_js(read(KNOWLEDGE_MD)):
        problems.append("assistant: functions/_lib/knowledge.js is not what assistant/knowledge.md generates (run python3 build.py)")
    for name in ASSISTANT_ASSETS:
        built_asset = PUBLIC / "assets" / name
        if not built_asset.exists() or built_asset.read_bytes() != (SITE / name).read_bytes():
            problems.append(f"assistant: public/assets/{name} missing or differs from site/{name}")
    no_loader = [page_path(f) for f in files if ASSISTANT_LOADER not in f.read_text(encoding="utf-8")]
    if no_loader:
        problems.append(f"assistant: loader missing on {len(no_loader)} page(s): {', '.join(sorted(no_loader)[:5])}")
    robots = (PUBLIC / "robots.txt").read_text(encoding="utf-8") if (PUBLIC / "robots.txt").exists() else ""
    if robots != ROBOTS_TXT:
        problems.append("robots.txt: missing or not what build.py writes (named crawlers allowed, /api/ disallowed)")
    if (ROOT / "public" / "functions").exists():
        problems.append("assistant: functions/ must sit at the project root next to build.py, not inside public/")
    notes.append(f"assistant: knowledge.js in step with knowledge.md; widget assets and loader on {len(files)} pages; "
                 f"robots.txt names {len(ROBOTS_AGENTS)} crawlers and disallows /api/")
    # Redirects (CANON ARCHIVE > REDIRECTS). Fixtures first, then the real set
    # against every URL Google is known to have (tools/gsc-known-urls-*.txt).
    if not GSC_KNOWN.exists():
        problems.append(f"redirects: {GSC_KNOWN.relative_to(ROOT)} missing")
    else:
        known = read_known(GSC_KNOWN)
        problems += [f"redirect check fixture misbehaved: {b}" for b in redirect_selftest(rules, built, known)]
        problems += [f"redirects: {p}" for p in check_redirects(rules, built, known)]
        n301 = sum(1 for r in rules if r[2] == "301")
        notes.append(f"redirects: {len(rules)} rules ({n301} x 301, {len(rules) - n301} x 302); "
                     f"{len(known)} known URLs checked; fixtures OK")
    # Measurement (CANON MEASUREMENT). Fixtures first, then every file under
    # public/: retired trackers nowhere, live IDs at most once per page.
    tracked = {}
    for f in PUBLIC.rglob("*"):
        if f.is_file():
            try:
                tracked[f.relative_to(PUBLIC).as_posix()] = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue  # images
    problems += [f"tracking check fixture misbehaved: {b}" for b in tracking_selftest(tracked)]
    problems += [f"tracking: {p}" for p in check_tracking(tracked)]
    n_pages = len(files)
    # Trailing slash (DEPLOY.md): flat <slug>.html only. Fixtures first.
    problems += [f"trailing-slash check fixture misbehaved: {b}" for b in flat_selftest(set(tracked) | {"index.html"})]
    flat = check_flat({f.relative_to(PUBLIC).as_posix() for f in PUBLIC.rglob("*") if f.is_file()})
    problems += [f"trailing slash: {p}" for p in flat]
    notes.append(f"trailing slash: {n_pages} pages are public/index.html or public/<slug>.html, "
                 f"no nested index.html; fixtures OK")
    notes.append(f"tracking: {len(tracked)} files scanned for {len(TRACKING_BANNED)} retired strings; "
                 f"{', '.join(TRACKING_ONCE)} once on each of {n_pages} pages; fixtures OK")
    # Keyword ownership (CANON KEYWORD OWNERSHIP). Fixtures first: if a fixture
    # that must fail passes, the site result below means nothing.
    try:
        bad = ownership.selftest(verbose=False)
    except ownership.TableError as e:
        bad = [f"CANON table not read: {e}"]
    problems += [f"ownership check fixture misbehaved: {b}" for b in bad]
    own_problems, own_notes = ownership.check_site(PUBLIC)
    problems += [f"keyword ownership: {p}" for p in own_problems]
    notes += [f"keyword ownership: {n}" for n in own_notes]
    # Squarespace-hosted images (CANON "BEFORE CANCELLING SQUARESPACE"). A
    # WARNING, never a problem: these URLs work today and break the day the
    # Squarespace subscription ends. Listed per URL with the pages carrying it.
    warnings = []
    cdn = {}
    for rel, text in tracked.items():
        for url in set(SQSP_CDN_RE.findall(text)):
            page = page_path(Path(rel)) if (rel.endswith(".html") and "/" not in rel and rel != "404.html") else rel
            cdn.setdefault(url, set()).add(page)
    for url in sorted(cdn):
        warnings.append(f"squarespace-cdn.com image still referenced: {url.split('/')[-1].split('?')[0]} "
                        f"on {', '.join(sorted(cdn[url]))}")
    return problems, notes, warnings


def main():
    argv = sys.argv[1:]
    if "--check" not in argv:
        pages, emoji_report = build()
        print(f"Built {len(pages)} pages into {PUBLIC.relative_to(ROOT)}/")
        for url_path, title, src, lastmod in sorted(pages, key=lambda r: (r[0] != "/", r[0])):
            print(f"  {url_path:45s} {title}  [{src}; lastmod {lastmod}]")
        total = sum(sum(c.values()) for c in emoji_report.values())
        print(f"\nEMOJI -> SVG: {total} replacements on {len(emoji_report)} pages")
        for url_path in sorted(emoji_report, key=lambda u: (u != "/", u)):
            items = ", ".join(f"{ch} x{n} -> {icons.ICONS[ch][0]}" for ch, n in sorted(emoji_report[url_path].items(), key=lambda kv: -kv[1]))
            print(f"  {url_path:45s} {items}")
    problems, notes, warnings = check()
    print("\nCHECK: internal links, one H1 per page, social preview tags, JSON-LD parses, no emoji, 404/_headers, redirects, tracking, keyword ownership, Squarespace images (warning only)")
    for n in sorted(set(notes)):
        print("  note    ", n)
    for w in warnings:
        print("  WARNING ", w)
    if not warnings:
        print("  note     no squarespace-cdn.com references remain")
    for p in problems:
        print("  PROBLEM ", p)
    print(f"RESULT: {'PASSED' if not problems else str(len(problems)) + ' problem(s)'}")
    if problems and "--strict" in argv:
        sys.exit(1)


if __name__ == "__main__":
    main()
