# archive/ — retired pages, historical records only

These files describe pages that **no longer exist on the live site**. Each URL
now 301s elsewhere via Squarespace URL Mappings.

## Rules for this directory

- **Never certified.** Nothing here is in certification scope and nothing here
  ever enters it. `tools/certify.py` globs `pages/**/*.html` only; `archive/`
  is outside that glob by construction, not by an exemption list.
- **Never pasted.** No file here is a paste source. The live site has moved on.
- **Never corrected.** These are historical records. They contain retired
  pricing, the Garnet Ave / Pacific Beach address, the retired brand name
  "OmniFit Personal Fitness Training", and the retired Executive Hybrid
  product. That is expected and correct for an archive. Fixing them would
  destroy the record of what was actually published.
- **Never deleted.** They are kept so the reasoning behind later corrections
  survives.
- Contents are byte-identical to the `pages/` copies at the moment of
  archiving (Aug 2026 consolidation run). Verified by sha256 before and after
  the move.

## What is here and where its URL goes

| Archived file | Retired URL | Redirects to |
|---|---|---|
| `personal-trainer-mission-hills.html` + `headers/personal-trainer-mission-hills-header.html` | `/personal-trainer-mission-hills` | 301, per Squarespace URL Mappings |
| `executive-hybrid-coaching.html` + `headers/executive-hybrid-coaching-header.html` | `/executive-hybrid-coaching` | 301 → `/the-30-minute-executive-reset` |
| `online-training.html` + `headers/online-training-header.html` | `/online-training` | 301, per Squarespace URL Mappings |

Headers keep the `headers/<slug>-header.html` shape so each page/header pair
stays obvious. The `pages/headers/<slug>-header.html` naming standard in
CANON.md applies to `pages/`, not here.
