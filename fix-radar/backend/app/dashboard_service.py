from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.core import Finding, Opportunity, Page, Scan, Site
from app.models.enums import OpportunityStatus
from app.opportunities.service import top_fix_next

CATEGORY_LABELS = {
    "technical_score": "Technical",
    "seo_score": "SEO",
    "local_score": "Local",
    "aio_score": "AIO",
    "authority_score": "Authority",
    "conversion_score": "Conversion",
}

STRENGTH_COPY = {
    "technical_score": "The site is technically sound: crawlable, mostly free of broken links and redirect chains.",
    "seo_score": "On-page SEO fundamentals (titles, descriptions, headings) are in solid shape.",
    "local_score": "San Diego / service-area relevance is clearly and repeatedly signaled across the site.",
    "aio_score": "Pages give an AI system a genuinely clear, answerable picture of who OmniFit is and does.",
    "authority_score": "Expertise and evidence signals (credentials, results, methodology) come through clearly.",
    "conversion_score": "Pages give a ready visitor a clear next step.",
}

WEAKNESS_COPY = {
    "technical_score": "Technical issues (broken links, errors, redirects) are holding the site back.",
    "seo_score": "On-page SEO fundamentals need attention.",
    "local_score": "The site under-signals its actual San Diego service area.",
    "aio_score": "Pages don't yet give an AI system enough to confidently understand or cite OmniFit.",
    "authority_score": "Expertise and evidence (credentials, results, third-party validation) are the weakest link.",
    "conversion_score": "Pages don't give ready visitors a clear next step.",
}


def build_dashboard(db: Session, site: Site) -> dict:
    latest_scan = (
        db.query(Scan)
        .filter(Scan.site_id == site.id, Scan.status == "COMPLETE")
        .order_by(Scan.finished_at.desc())
        .first()
    )

    fix_next = top_fix_next(db, site.id, limit=3)

    biggest_strength = biggest_weakness = None
    if latest_scan:
        scores = {k: getattr(latest_scan, k) for k in CATEGORY_LABELS if getattr(latest_scan, k) is not None}
        if scores:
            best_key = max(scores, key=scores.get)
            worst_key = min(scores, key=scores.get)
            biggest_strength = f"{CATEGORY_LABELS[best_key]} ({scores[best_key]}/100): {STRENGTH_COPY[best_key]}"
            biggest_weakness = f"{CATEGORY_LABELS[worst_key]} ({scores[worst_key]}/100): {WEAKNESS_COPY[worst_key]}"

    recently_fixed = (
        db.query(Opportunity)
        .filter(Opportunity.site_id == site.id, Opportunity.status == OpportunityStatus.FIXED)
        .order_by(Opportunity.updated_at.desc())
        .limit(5)
        .all()
    )

    site_health = {}
    if latest_scan:
        findings = db.query(Finding).filter(Finding.scan_id == latest_scan.id).all()
        pages = db.query(Page).filter(Page.scan_id == latest_scan.id).all()
        site_health = {
            "pages_crawled": latest_scan.pages_crawled,
            "broken_links": len([f for f in findings if f.code in ("BROKEN_INTERNAL_LINK", "BROKEN_EXTERNAL_LINK")]),
            "indexability_issues": len([f for f in findings if f.code == "NOINDEX_PAGE"]),
            "schema_issues": len([f for f in findings if f.code in ("NO_STRUCTURED_DATA", "MISSING_LOCALBUSINESS_SCHEMA", "NO_FAQ_SCHEMA")]),
            "thin_pages": len([f for f in findings if f.code == "THIN_CONTENT"]),
            "missing_metadata": len([f for f in findings if f.code in ("MISSING_TITLE", "MISSING_META_DESCRIPTION")]),
            "orphan_pages": len([p for p in pages if p.is_orphan]),
        }

    aio_opportunities = (
        db.query(Opportunity)
        .filter(Opportunity.site_id == site.id, Opportunity.category.in_(["AIO", "STRUCTURED_DATA"]), Opportunity.status == OpportunityStatus.OPEN)
        .order_by(Opportunity.priority_score.desc())
        .limit(5)
        .all()
    )
    authority_opportunities = (
        db.query(Opportunity)
        .filter(Opportunity.site_id == site.id, Opportunity.category == "AUTHORITY", Opportunity.status == OpportunityStatus.OPEN)
        .order_by(Opportunity.priority_score.desc())
        .limit(5)
        .all()
    )

    score_trend = [
        {
            "scan_id": s.id,
            "date": s.finished_at.isoformat() if s.finished_at else None,
            "overall_score": s.overall_score,
            "technical_score": s.technical_score,
            "seo_score": s.seo_score,
            "local_score": s.local_score,
            "aio_score": s.aio_score,
            "authority_score": s.authority_score,
            "conversion_score": s.conversion_score,
        }
        for s in db.query(Scan).filter(Scan.site_id == site.id, Scan.status == "COMPLETE").order_by(Scan.finished_at.asc()).all()
    ]

    network_notice = None
    if latest_scan and latest_scan.source == "local_fixture":
        network_notice = (
            "This scan ran against a local copy of the site's own committed page source, not the live URL -- "
            "this environment's network policy currently blocks outbound access to the live domain. "
            "Content-based findings (headings, word count, links between the pages present here, images, "
            "JSON-LD, titles/descriptions read from the real per-page head-injection files) reflect genuine "
            "OmniFit content. However, this repo does not contain every live page as a fragment (e.g. privacy "
            "policy, terms, about, and some legacy URLs aren't committed here), so broken-link findings pointing "
            "at those URLs are an artifact of this fixture's incompleteness, not necessarily real breakage on the "
            "live site -- verify them against the live site before treating them as confirmed. "
            "Run Fix Radar somewhere with network access to omnifittraining.com for a true live scan."
        )

    return {
        "site": site,
        "latest_scan": latest_scan,
        "fix_next": fix_next,
        "biggest_strength": biggest_strength,
        "biggest_weakness": biggest_weakness,
        "recently_fixed": recently_fixed,
        "site_health": site_health,
        "aio_opportunities": aio_opportunities,
        "authority_opportunities": authority_opportunities,
        "competitor_gaps": [],
        "simulator_summary": None,
        "score_trend": score_trend,
        "network_notice": network_notice,
    }
