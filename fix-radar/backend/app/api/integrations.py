from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.integrations.pagespeed import fetch_pagespeed
from app.integrations.search_console import derive_opportunities, import_rows
from app.models.integrations import PageSpeedResult, SearchConsolePage, SearchConsoleQuery
from app.models.core import Site

router = APIRouter(prefix="/api/integrations", tags=["integrations"])


@router.post("/search-console/connect")
def search_console_connect(site_id: int = Body(...), rows: list[dict] = Body(default_factory=list), db: Session = Depends(get_db)):
    """"Connect" here means: import a Search Console Performance export.
    There's no headless OAuth flow for a per-owner Search Console property in
    this internal tool -- export the Performance report and paste/upload rows.
    An empty `rows` list just confirms the site exists and returns current status."""
    if not db.query(Site).get(site_id):
        raise HTTPException(404, "Site not found")
    imported = import_rows(db, site_id, rows) if rows else 0
    total = db.query(SearchConsoleQuery).filter(SearchConsoleQuery.site_id == site_id).count()
    return {"imported_this_request": imported, "total_rows": total, "connected": total > 0}


@router.get("/search-console/opportunities")
def search_console_opportunities(site_id: int, db: Session = Depends(get_db)):
    return derive_opportunities(db, site_id)


@router.post("/pagespeed/connect")
def pagespeed_connect(site_id: int = Body(...), url: str = Body(...), strategy: str = Body("mobile"), db: Session = Depends(get_db)):
    if not db.query(Site).get(site_id):
        raise HTTPException(404, "Site not found")
    try:
        result = fetch_pagespeed(db, site_id, url, strategy)
    except Exception as exc:
        raise HTTPException(
            502,
            f"Could not reach PageSpeed Insights ({exc}). This is optional -- Fix Radar works fully without it; "
            "try again from an environment with outbound internet access.",
        ) from exc
    return {
        "id": result.id,
        "performance": result.performance,
        "accessibility": result.accessibility,
        "best_practices": result.best_practices,
        "seo": result.seo,
    }


@router.get("/pagespeed/results")
def pagespeed_results(site_id: int, db: Session = Depends(get_db)):
    rows = db.query(PageSpeedResult).filter(PageSpeedResult.site_id == site_id).order_by(PageSpeedResult.fetched_at.desc()).all()
    return [
        {
            "id": r.id, "page_url": r.page_url, "strategy": r.strategy, "performance": r.performance,
            "accessibility": r.accessibility, "best_practices": r.best_practices, "seo": r.seo,
            "fetched_at": r.fetched_at.isoformat(),
        }
        for r in rows
    ]
