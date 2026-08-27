from __future__ import annotations

from sqlalchemy.orm import Session

from app.crawler.crawler import Crawler
from app.crawler.fetcher import SSRFBlockedError
from app.models.competitors import Competitor, CompetitorPage
from app.models.core import Page, Scan, Site

TOPIC_KEYWORDS: dict[str, list[str]] = {
    "corrective_exercise": ["corrective exercise", "post-rehab", "post rehab"],
    "executive_health": ["executive health", "executive coaching", "executive fitness", "executive performance"],
    "in_home_training": ["in-home training", "in home training", "in-home personal training"],
    "virtual_coaching": ["virtual coaching", "online coaching", "remote coaching"],
    "nutrition_coaching": ["nutrition coaching", "nutrition plan", "meal plan"],
    "strength_training": ["strength training"],
    "weight_loss": ["weight loss", "fat loss"],
}
FAQ_HEADING_RE = "?"
TESTIMONIAL_KEYWORDS = ["testimonial", "review", "client says", "success story", "case study"]
CREDENTIAL_KEYWORDS = ["certified", "certification", "cscs", "nasm", "nsca", "credential", "licensed", "degree"]


def crawl_competitor(db: Session, competitor: Competitor, *, max_pages: int = 40) -> list[CompetitorPage]:
    from datetime import datetime, timezone

    crawler = Crawler(
        competitor.base_url,
        user_agent="OmniFitFixRadar/1.0 (+internal competitor audit)",
        max_pages=max_pages,
        max_depth=4,
        allow_private_hosts=False,
        check_external_links=False,
    )
    try:
        result = crawler.crawl()
    except SSRFBlockedError as exc:
        raise ValueError(f"Refused to crawl {competitor.base_url}: {exc}") from exc

    db.query(CompetitorPage).filter(CompetitorPage.competitor_id == competitor.id).delete()

    rows = []
    for p in result.pages:
        if not p.status_code or p.status_code >= 400 or "html" not in (p.content_type or ""):
            continue
        text = (p.text_content or "").lower()
        headings = (p.h1 or []) + (p.h2 or []) + (p.h3 or [])
        topics = [topic for topic, kws in TOPIC_KEYWORDS.items() if any(kw in text for kw in kws)]
        schema_types = sorted({str(item.get("@type", "")) for item in (p.json_ld or []) if isinstance(item, dict) and item.get("@type")})

        row = CompetitorPage(
            competitor_id=competitor.id,
            url=p.url,
            title=p.title,
            word_count=p.word_count,
            headings=headings,
            has_schema=bool(p.json_ld),
            schema_types=schema_types,
            faq_count=sum(1 for h in headings if "?" in h),
            testimonial_signals=sum(1 for kw in TESTIMONIAL_KEYWORDS if kw in text),
            credential_signals=sum(1 for kw in CREDENTIAL_KEYWORDS if kw in text),
            topics=topics,
        )
        db.add(row)
        rows.append(row)

    competitor.last_crawled_at = datetime.now(timezone.utc)
    db.commit()
    return rows


def _omnifit_topic_coverage(pages: list[Page]) -> set[str]:
    covered = set()
    for p in pages:
        text = (p.text_content or "").lower()
        for topic, kws in TOPIC_KEYWORDS.items():
            if any(kw in text for kw in kws):
                covered.add(topic)
    return covered


def compute_gap_analysis(db: Session, site: Site) -> dict:
    latest_scan = (
        db.query(Scan)
        .filter(Scan.site_id == site.id, Scan.status == "COMPLETE")
        .order_by(Scan.finished_at.desc())
        .first()
    )
    omnifit_pages = db.query(Page).filter(Page.scan_id == latest_scan.id).all() if latest_scan else []
    omnifit_topics = _omnifit_topic_coverage(omnifit_pages)
    omnifit_testimonials = sum(1 for p in omnifit_pages if any(kw in (p.text_content or "").lower() for kw in TESTIMONIAL_KEYWORDS))
    omnifit_schema_pages = sum(1 for p in omnifit_pages if p.json_ld)

    competitors = db.query(Competitor).filter(Competitor.site_id == site.id).all()
    if not competitors:
        return {
            "summary": ["No competitors added yet. Add competitor URLs to unlock gap analysis."],
            "top_opportunities": [],
            "comparison_table": [],
        }

    comp_data = []
    for c in competitors:
        pages = db.query(CompetitorPage).filter(CompetitorPage.competitor_id == c.id).all()
        topics = set()
        for p in pages:
            topics.update(p.topics or [])
        comp_data.append(
            {
                "competitor": c,
                "pages": pages,
                "topics": topics,
                "page_count": len(pages),
                "faq_pages": sum(1 for p in pages if p.faq_count > 0),
                "testimonial_pages": sum(1 for p in pages if p.testimonial_signals > 0),
                "credential_pages": sum(1 for p in pages if p.credential_signals > 0),
                "schema_pages": sum(1 for p in pages if p.has_schema),
            }
        )

    n = len(comp_data)
    summary = []
    for topic in TOPIC_KEYWORDS:
        count = sum(1 for cd in comp_data if topic in cd["topics"])
        label = topic.replace("_", " ")
        summary.append(f"{count}/{n} competitors have a dedicated {label} page.")
        if topic not in omnifit_topics and count > 0:
            summary.append(f"OmniFit does not currently have clearly identifiable {label} content that competitors do.")

    if omnifit_testimonials > 0 and sum(cd["testimonial_pages"] for cd in comp_data) == 0:
        summary.append("OmniFit has stronger client-evidence content (testimonials/case studies) than any crawled competitor.")
    elif omnifit_testimonials == 0 and any(cd["testimonial_pages"] > 0 for cd in comp_data):
        summary.append("OmniFit is weaker than at least one competitor in visible client evidence (testimonials/case studies).")

    if omnifit_schema_pages > 0 and sum(cd["schema_pages"] for cd in comp_data) == 0:
        summary.append("OmniFit is ahead on structured data -- no crawled competitor page carries JSON-LD schema.")

    top_opportunities = []
    for topic in TOPIC_KEYWORDS:
        count = sum(1 for cd in comp_data if topic in cd["topics"])
        if topic not in omnifit_topics and count >= max(1, n // 2):
            top_opportunities.append(
                {
                    "title": f"Build a dedicated {topic.replace('_', ' ')} page",
                    "why": f"{count}/{n} competitors already have this; OmniFit doesn't have clearly identifiable content for it.",
                }
            )
    if sum(cd["testimonial_pages"] for cd in comp_data) > 0 and omnifit_testimonials == 0:
        top_opportunities.append(
            {"title": "Publish client testimonials/case studies", "why": "Competitors show visible client evidence that OmniFit currently doesn't."}
        )
    top_opportunities = top_opportunities[:5]

    comparison_table = [
        {
            "name": "OmniFit (this site)",
            "page_count": len(omnifit_pages),
            "topics_covered": sorted(omnifit_topics),
            "testimonial_signal_pages": omnifit_testimonials,
            "schema_pages": omnifit_schema_pages,
        }
    ] + [
        {
            "name": cd["competitor"].name,
            "page_count": cd["page_count"],
            "topics_covered": sorted(cd["topics"]),
            "testimonial_signal_pages": cd["testimonial_pages"],
            "schema_pages": cd["schema_pages"],
        }
        for cd in comp_data
    ]

    return {"summary": summary, "top_opportunities": top_opportunities, "comparison_table": comparison_table}
