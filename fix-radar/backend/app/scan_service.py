from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.audit.aio import run_aio_audit
from app.audit.base import RawFinding, score_from_findings
from app.audit.technical import run_technical_audit
from app.business_context import business_context_summary
from app.core.config import get_settings
from app.crawler.crawler import CrawledPage, CrawlResult, Crawler
from app.models.core import Finding, Page, Scan, Site
from app.opportunities.engine import generate_opportunity_drafts
from app.opportunities.service import sync_opportunities

WEIGHTS = {
    "technical_score": 0.20,
    "seo_score": 0.20,
    "local_score": 0.10,
    "aio_score": 0.20,
    "authority_score": 0.15,
    "conversion_score": 0.15,
}


def run_scan_for_local_fixture(db: Session, site: Site, root_url: str, **crawler_kwargs) -> Scan:
    """Same pipeline as a live scan, but explicitly allows a private/local host.
    Used only for the repo's own local-fixture demo server, never for user-supplied URLs."""
    return _run_scan(db, site, root_url, allow_private_hosts=True, source="local_fixture", **crawler_kwargs)


def run_scan(db: Session, site: Site, **crawler_kwargs) -> Scan:
    return _run_scan(db, site, site.base_url, allow_private_hosts=False, source="live", **crawler_kwargs)


def _run_scan(
    db: Session,
    site: Site,
    root_url: str,
    *,
    allow_private_hosts: bool,
    source: str,
    max_pages: int | None = None,
    max_depth: int | None = None,
) -> Scan:
    settings = get_settings()
    scan = Scan(site_id=site.id, status="RUNNING", source=source)
    db.add(scan)
    db.commit()
    db.refresh(scan)

    try:
        crawler = Crawler(
            root_url,
            user_agent=settings.crawler_user_agent,
            max_pages=max_pages or settings.crawler_max_pages,
            max_depth=max_depth or settings.crawler_max_depth,
            timeout_ms=settings.crawler_request_timeout_ms,
            allow_private_hosts=allow_private_hosts,
            check_external_links=not allow_private_hosts,
        )
        result = crawler.crawl()

        reachable_pages = [p for p in result.pages if p.status_code and p.status_code < 400]
        if not reachable_pages:
            raise RuntimeError(
                f"Could not reach any page at {root_url} -- the root URL itself returned "
                f"{'an error' if not result.pages else f'HTTP {result.pages[0].status_code} / {result.pages[0].fetch_error}'}. "
                "This usually means the target is unreachable from this environment (network policy, DNS, or the "
                "site being down), not that the site has zero working pages."
            )

        page_rows = _persist_pages(db, scan, result)

        technical_findings, technical_score, seo_score = run_technical_audit(result.pages, result)
        aio_findings, profiles, aio_scores = run_aio_audit(result.pages)

        all_findings = technical_findings + aio_findings
        _persist_findings(db, scan, page_rows, all_findings)
        _apply_page_scores(page_rows, result.pages, profiles, all_findings)

        scan.pages_crawled = len(result.pages)
        scan.technical_score = technical_score
        scan.seo_score = seo_score
        scan.local_score = aio_scores["local_score"]
        scan.aio_score = aio_scores["aio_score"]
        scan.authority_score = aio_scores["authority_score"]
        scan.conversion_score = aio_scores["conversion_score"]
        scan.overall_score = round(
            sum(getattr(scan, key) * weight for key, weight in WEIGHTS.items()), 1
        )
        scan.status = "COMPLETE"
        scan.finished_at = datetime.now(timezone.utc)
        db.commit()

        drafts = generate_opportunity_drafts(all_findings)
        sync_opportunities(db, site, drafts)

    except Exception as exc:  # pragma: no cover - defensive path, surfaced via scan.error
        scan.status = "FAILED"
        scan.error = str(exc)
        scan.finished_at = datetime.now(timezone.utc)
        db.commit()
        raise

    db.refresh(scan)
    return scan


def _persist_pages(db: Session, scan: Scan, result: CrawlResult) -> dict[str, Page]:
    rows: dict[str, Page] = {}
    for p in result.pages:
        row = Page(
            scan_id=scan.id,
            url=p.url,
            normalized_url=p.normalized_url,
            status_code=p.status_code,
            response_time_ms=p.response_time_ms,
            content_type=p.content_type,
            final_url=p.final_url,
            redirect_chain=p.redirect_chain,
            title=p.title,
            meta_description=p.meta_description,
            canonical=p.canonical,
            h1=p.h1,
            h2=p.h2,
            h3=p.h3,
            word_count=p.word_count,
            internal_links=p.internal_links,
            external_links=p.external_links,
            images=p.images,
            json_ld=p.json_ld,
            open_graph=p.open_graph,
            robots_meta=p.robots_meta,
            is_indexable=p.is_indexable,
            in_sitemap=p.in_sitemap,
            inbound_internal_link_count=p.inbound_internal_link_count,
            is_orphan=p.is_orphan,
            depth=p.depth,
            text_content=p.text_content,
        )
        db.add(row)
        rows[p.url] = row
    db.commit()
    for url, row in rows.items():
        db.refresh(row)
    return rows


def _persist_findings(db: Session, scan: Scan, page_rows: dict[str, Page], findings: list[RawFinding]) -> None:
    for f in findings:
        page = page_rows.get(f.affected_url) if f.affected_url else None
        db.add(
            Finding(
                scan_id=scan.id,
                page_id=page.id if page else None,
                code=f.code,
                category=f.category,
                severity=f.severity,
                affected_url=f.affected_url,
                evidence=f.evidence,
                explanation=f.explanation,
                recommended_action=f.recommended_action,
                estimated_effort=f.estimated_effort,
                estimated_impact=f.estimated_impact,
                confidence=f.confidence,
                fingerprint=f.fingerprint,
            )
        )
    db.commit()


def _apply_page_scores(page_rows: dict[str, Page], crawled: list[CrawledPage], profiles: dict, findings: list[RawFinding]) -> None:
    findings_by_url: dict[str, list[RawFinding]] = {}
    for f in findings:
        if f.affected_url:
            findings_by_url.setdefault(f.affected_url, []).append(f)

    for cp in crawled:
        row = page_rows.get(cp.url)
        if not row:
            continue
        page_findings = findings_by_url.get(cp.url, [])
        row.technical_score = score_from_findings(
            [f for f in page_findings if f.category.value in ("TECHNICAL",)], 1
        )
        row.seo_score = score_from_findings(
            [f for f in page_findings if f.category.value in ("SEO", "INTERNAL_LINKING", "STRUCTURED_DATA")], 1
        )
        profile = profiles.get(cp.url)
        if profile:
            row.aio_score = round((profile.entity_clarity + profile.semantic_completeness + profile.answerability) / 3 * 10, 1)
            row.local_score = round(profile.geo_relevance * 10, 1)
            row.trust_score = round(profile.trust * 10, 1)
            row.conversion_score = round(profile.conversion * 10, 1)


def business_context_for_ai() -> str:
    return business_context_summary()
