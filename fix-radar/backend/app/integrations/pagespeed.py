from __future__ import annotations

import httpx
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.integrations import PageSpeedResult

PSI_ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"


def fetch_pagespeed(db: Session, site_id: int, url: str, strategy: str = "mobile") -> PageSpeedResult:
    settings = get_settings()
    params = {"url": url, "strategy": strategy, "category": ["PERFORMANCE", "ACCESSIBILITY", "BEST_PRACTICES", "SEO"]}
    if settings.google_pagespeed_api_key:
        params["key"] = settings.google_pagespeed_api_key

    with httpx.Client(timeout=30) as client:
        resp = client.get(PSI_ENDPOINT, params=params)
        resp.raise_for_status()
        data = resp.json()

    categories = data.get("lighthouseResult", {}).get("categories", {})
    audits = data.get("lighthouseResult", {}).get("audits", {})

    def cat_score(key: str) -> float | None:
        val = categories.get(key, {}).get("score")
        return round(val * 100, 1) if val is not None else None

    def audit_value(key: str) -> float | None:
        return audits.get(key, {}).get("numericValue")

    row = PageSpeedResult(
        site_id=site_id,
        page_url=url,
        strategy=strategy,
        performance=cat_score("performance"),
        accessibility=cat_score("accessibility"),
        best_practices=cat_score("best-practices"),
        seo=cat_score("seo"),
        lcp_ms=audit_value("largest-contentful-paint"),
        cls=audit_value("cumulative-layout-shift"),
        inp_ms=audit_value("interaction-to-next-paint") or audit_value("experimental-interaction-to-next-paint"),
        fcp_ms=audit_value("first-contentful-paint"),
        raw={"categories": categories},
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
