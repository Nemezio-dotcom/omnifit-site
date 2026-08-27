# OmniFit Website Fix Radar

An internal diagnostic tool that answers one question: **what should I fix next on
omnifittraining.com to improve discoverability, AI/AIO visibility, authority, and
conversions?**

It is not a general-purpose SEO crawler. Every scan produces a ranked, heuristic
priority list ("Fix Next") rather than a wall of warnings.

## Architecture

```
fix-radar/
  backend/    FastAPI + SQLAlchemy + SQLite, Playwright/httpx+BeautifulSoup crawler
  frontend/   React + TypeScript + Vite + Tailwind + Recharts
```

- **Crawler** (`backend/app/crawler`): httpx-based fetcher (SSRF-guarded: public
  HTTP/S hosts only, unless a scan explicitly opts into a local fixture), robots.txt
  + sitemap.xml aware, BeautifulSoup/lxml extraction of titles, metadata, headings,
  links, images, JSON-LD, Open Graph.
- **Audit** (`backend/app/audit`): rule-based technical/SEO findings
  (`technical.py`) and the AIO-readiness heuristics (`aio.py`) -- entity clarity,
  expertise, evidence, geo relevance, answerability, semantic completeness, trust,
  structured data, citation-worthy passage extraction.
- **AI provider** (`backend/app/ai`): a small `AIProvider` interface with two
  implementations -- `HeuristicAIProvider` (keyword/structure based, always
  available, never fabricates) and `OpenAIProvider` (used automatically when
  `OPENAI_API_KEY` is set). Both return the same strict Pydantic schema.
- **Opportunity engine** (`backend/app/opportunities`): groups findings into
  ranked `Opportunity` records. `priority = impact * confidence * (11 - effort)`,
  normalized to 0-100. Re-scanning reconciles state: resolved issues become
  `FIXED`, reappearing issues are flagged as regressions, `IGNORED` opportunities
  never re-open on their own.
- **AI Recommendation Simulator** (`backend/app/simulator`): evidence-based
  "recommendation readiness" scoring for natural-language queries -- never claims
  to reproduce ChatGPT/Claude/Gemini/Perplexity's actual ranking behavior.
- **Competitors** (`backend/app/competitors`): crawls user-supplied competitor
  URLs and compares topical coverage, no backlink/ranking claims.
- **Integrations** (`backend/app/integrations`): PageSpeed Insights (works if the
  environment has outbound internet; no key required for light use, or set
  `GOOGLE_PAGESPEED_API_KEY`) and Search Console (import a Performance-report
  export -- there's no sane way to run per-owner OAuth headlessly here).

## Running it

### Local

```bash
# backend
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head        # or just run the app once -- it also create_all()s on startup
uvicorn app.main:app --reload --port 8000

# frontend (separate terminal)
cd frontend
npm install
npm run dev                 # http://localhost:5173, proxies /api to :8000
```

Open http://localhost:5173, click **Scan Now**.

### Docker

```bash
docker compose up --build
```

## A note on the live scan (read this before assuming something's broken)

This app was built inside a sandboxed Claude Code session whose network egress
policy **blocks outbound access to `omnifittraining.com`** (verified directly --
both a raw HTTPS request and the harness's own fetch tool returned an
egress-blocked / 403 response). The same sandbox has no `OPENAI_API_KEY` and no
general internet access for PageSpeed/Search Console either.

So that this could still be built, tested, and demonstrated with real data rather
than mocked data, **Scan Now falls back automatically**: it first tries the live
`base_url`; if that's unreachable, it retries against a local HTTP server
(`backend/app/fixture_server.py`) that serves the *actual* committed page source
from `../pages/*.html` in this repo -- including the real per-page
`<title>`/meta description/canonical/JSON-LD, which live in the
`pages/headers/*-header.html` files (the real page-head-injection code pasted
into the CMS). The dashboard clearly labels which source a scan came from and
shows a banner explaining the caveat (this repo doesn't contain every live page
as a fragment -- e.g. `/privacy-policy`, `/terms-and-conditions`, `/about` --
so broken-link findings pointing at those URLs are a fixture-completeness
artifact, not confirmed live breakage).

**Run this somewhere with real network access (your own machine, or a Claude Code
web/cloud environment whose egress policy allows `omnifittraining.com`) to get an
actual live scan.** Everything downstream of the crawler -- scoring, findings,
opportunities, the simulator -- is real logic, not a demo shim; only the network
transport was substituted.

## What's fully built vs. scaffolded

Fully built and tested: crawler, technical/SEO audit + scoring, AIO readiness
scoring, opportunity engine with regression/ignore/fixed lifecycle, Fix Next
ranking, dashboard, page-level view with on-demand AI analysis, AI Recommendation
Simulator (query analysis, evidence mapping, readiness scoring, simulated answer,
query library, cluster analysis, systemic-weakness feed into Fix Next), CSV/JSON
export, Alembic migrations, and a pytest suite covering normalization, SSRF
guards, extraction, crawling, scoring, opportunity lifecycle, and a full
create-site -> scan -> findings -> opportunities -> dashboard end-to-end flow.

Built but intentionally lighter-weight, since they depend on external systems
this environment can't reach: PDF export (works, uses reportlab, not
pixel-tuned), PageSpeed integration (real API call, untested against a live key
here), Search Console (manual CSV import rather than full OAuth), competitor
crawling (real crawler reused, untested against a live competitor site here).

Historical score tracking exists (every scan is stored; the dashboard renders a
trend line) but only has one real data point so far since this session could only
run local-fixture scans.

## Testing

```bash
cd backend && source .venv/bin/activate && python -m pytest
```

51 tests, all passing. Includes a regression test for a real bug found while
building this: `urllib.robotparser.RobotFileParser` denies-by-default when
`robots.txt` is unreachable, which would have silently zeroed out any crawl
whose robots.txt fetch failed -- `RobotsPolicy` now explicitly tracks whether
real rules were parsed before consulting the parser.

## Security notes

The crawler restricts itself to `http`/`https`, resolves hostnames and rejects
private/loopback/link-local/reserved IPs (SSRF guard) unless a scan explicitly
opts into the local fixture host. It never executes fetched page JavaScript
(Playwright is available as a dependency for future JS-rendering needs, but is
not required for this site, which is server-rendered). API keys are read from
`.env` server-side only and never sent to the frontend. Nothing is ever
auto-published to the live site -- AI-drafted titles/meta/FAQ/schema are stored
as `Recommendation` rows for manual review only.
