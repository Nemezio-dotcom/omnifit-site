from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from app.models.integrations import SearchConsolePage, SearchConsoleQuery


def import_rows(db: Session, site_id: int, rows: list[dict]) -> int:
    """Import GSC performance rows exported from Search Console (Performance report CSV/API export).

    We don't run a live OAuth flow in this internal tool -- Search Console requires
    per-property OAuth consent that doesn't make sense to automate headlessly here.
    Export the Performance report from search.google.com/search-console and import
    it; this keeps the integration genuinely optional per the spec.
    """
    count = 0
    page_agg: dict[str, dict] = {}
    for row in rows:
        clicks = int(row.get("clicks", 0) or 0)
        impressions = int(row.get("impressions", 0) or 0)
        ctr = float(row.get("ctr", 0) or 0)
        position = float(row.get("position", row.get("avg_position", 0)) or 0)
        page_url = row.get("page") or row.get("page_url")

        db.add(
            SearchConsoleQuery(
                site_id=site_id,
                query=row.get("query", ""),
                page_url=page_url,
                clicks=clicks,
                impressions=impressions,
                ctr=ctr,
                avg_position=position,
                date_range_start=row.get("date_range_start"),
                date_range_end=row.get("date_range_end"),
            )
        )
        count += 1
        if page_url:
            agg = page_agg.setdefault(page_url, {"clicks": 0, "impressions": 0, "ctr_sum": 0.0, "pos_sum": 0.0, "n": 0})
            agg["clicks"] += clicks
            agg["impressions"] += impressions
            agg["ctr_sum"] += ctr
            agg["pos_sum"] += position
            agg["n"] += 1

    for page_url, agg in page_agg.items():
        db.add(
            SearchConsolePage(
                site_id=site_id,
                page_url=page_url,
                clicks=agg["clicks"],
                impressions=agg["impressions"],
                ctr=round(agg["ctr_sum"] / agg["n"], 4),
                avg_position=round(agg["pos_sum"] / agg["n"], 1),
            )
        )
    db.commit()
    return count


def derive_opportunities(db: Session, site_id: int) -> list[dict]:
    """Surface content opportunities from imported GSC data. Advisory only --
    these aren't auto-injected as Opportunity rows because they depend on a
    manual import step the owner controls."""
    pages = db.query(SearchConsolePage).filter(SearchConsolePage.site_id == site_id).all()
    if not pages:
        return []

    out = []
    for p in pages:
        if p.impressions >= 50 and p.ctr < 0.02:
            out.append(
                {
                    "type": "LOW_CTR_HIGH_IMPRESSIONS",
                    "page_url": p.page_url,
                    "detail": f"{p.impressions} impressions but only {p.ctr:.1%} CTR -- the title/description may not be compelling for what people are searching.",
                }
            )
        if 4 <= p.avg_position <= 20:
            out.append(
                {
                    "type": "STRIKING_DISTANCE",
                    "page_url": p.page_url,
                    "detail": f"Averaging position {p.avg_position:.1f} -- close enough that on-page improvements could meaningfully move rank.",
                }
            )
    return out
