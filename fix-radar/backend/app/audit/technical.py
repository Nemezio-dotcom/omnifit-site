from __future__ import annotations

from collections import defaultdict

from app.audit.base import RawFinding, score_from_findings
from app.crawler.crawler import CrawledPage, CrawlResult
from app.models.enums import FindingCategory as Cat
from app.models.enums import Severity as Sev

THIN_CONTENT_HARD_MIN = 60
THIN_CONTENT_SOFT_MIN = 150
SLOW_RESPONSE_MS = 3000
TITLE_MIN = 15
TITLE_MAX = 65
META_MIN = 50
META_MAX = 160


def run_technical_audit(pages: list[CrawledPage], crawl: CrawlResult) -> tuple[list[RawFinding], float, float]:
    """Returns (findings, technical_score, seo_score). Both scores are heuristic 0-100."""
    findings: list[RawFinding] = []
    ok_pages = [p for p in pages if p.status_code and p.status_code < 400 and "html" in (p.content_type or "html")]

    findings += _status_findings(pages)
    findings += _link_findings(crawl)
    findings += _redirect_findings(ok_pages)
    findings += _metadata_findings(ok_pages)
    findings += _heading_findings(ok_pages)
    findings += _thin_content_findings(ok_pages)
    findings += _image_alt_findings(ok_pages)
    findings += _orphan_findings(ok_pages)
    findings += _indexability_findings(ok_pages)
    findings += _sitemap_findings(crawl, ok_pages)
    findings += _performance_findings(ok_pages)
    findings += _schema_presence_findings(ok_pages)

    technical_codes = {
        "BROKEN_INTERNAL_LINK", "BROKEN_EXTERNAL_LINK", "REDIRECT_CHAIN", "SLOW_RESPONSE",
        "NO_SITEMAP", "NOT_IN_SITEMAP", "SERVER_ERROR", "CLIENT_ERROR", "NOINDEX_PAGE",
    }
    seo_codes = {
        "MISSING_TITLE", "DUPLICATE_TITLE", "TITLE_LENGTH", "MISSING_META_DESCRIPTION",
        "DUPLICATE_META_DESCRIPTION", "META_LENGTH", "MISSING_H1", "MULTIPLE_H1",
        "THIN_CONTENT", "MISSING_ALT_TEXT", "ORPHAN_PAGE", "POOR_INTERNAL_LINKING",
        "MISSING_CANONICAL", "NO_STRUCTURED_DATA",
    }

    technical_findings = [f for f in findings if f.code in technical_codes]
    seo_findings = [f for f in findings if f.code in seo_codes]

    technical_score = score_from_findings(technical_findings, len(pages))
    seo_score = score_from_findings(seo_findings, len(ok_pages))
    return findings, technical_score, seo_score


def _status_findings(pages: list[CrawledPage]) -> list[RawFinding]:
    out = []
    for p in pages:
        if p.fetch_error and not p.status_code:
            out.append(
                RawFinding(
                    code="SERVER_ERROR", category=Cat.TECHNICAL, severity=Sev.HIGH,
                    affected_url=p.url, evidence=p.fetch_error,
                    explanation="The page could not be fetched at all.",
                    recommended_action="Confirm the URL resolves and the server responds; check hosting/DNS if this persists.",
                    estimated_effort=5, estimated_impact=8, confidence=8,
                )
            )
        elif p.status_code and p.status_code >= 500:
            out.append(
                RawFinding(
                    code="SERVER_ERROR", category=Cat.TECHNICAL, severity=Sev.CRITICAL,
                    affected_url=p.url, evidence=f"HTTP {p.status_code}",
                    explanation="The server returned an error for this URL.",
                    recommended_action="Investigate server logs for this route; this blocks both users and crawlers.",
                    estimated_effort=5, estimated_impact=9, confidence=9,
                )
            )
        elif p.status_code and p.status_code >= 400:
            out.append(
                RawFinding(
                    code="CLIENT_ERROR", category=Cat.TECHNICAL, severity=Sev.HIGH,
                    affected_url=p.url, evidence=f"HTTP {p.status_code}",
                    explanation="This URL is linked or listed but returns a client error.",
                    recommended_action="Fix the link/URL, restore the page, or 301-redirect it to the correct location.",
                    estimated_effort=2, estimated_impact=6, confidence=9,
                )
            )
    return out


def _link_findings(crawl: CrawlResult) -> list[RawFinding]:
    out = []
    for link in crawl.broken_internal_links:
        out.append(
            RawFinding(
                code="BROKEN_INTERNAL_LINK", category=Cat.TECHNICAL, severity=Sev.HIGH,
                affected_url=link["from_url"],
                evidence=f"Links to {link['to_url']} which returns HTTP {link['status_code']}",
                explanation="An internal link points to a broken page, wasting crawl budget and link equity, and breaking navigation.",
                recommended_action=f"Update or remove the link to {link['to_url']}, or fix the destination page.",
                estimated_effort=1, estimated_impact=5, confidence=9,
            )
        )
    for check in crawl.external_link_checks:
        if not check["ok"]:
            out.append(
                RawFinding(
                    code="BROKEN_EXTERNAL_LINK", category=Cat.TECHNICAL, severity=Sev.LOW,
                    affected_url=check["from_url"],
                    evidence=f"External link to {check['to_url']} returned {check['status_code'] or 'no response'} ({check.get('error') or 'n/a'})",
                    explanation="A broken external link is a minor trust/UX issue; it is outside your control to fix the destination.",
                    recommended_action=f"Remove or replace the link to {check['to_url']}.",
                    estimated_effort=1, estimated_impact=2, confidence=6,
                )
            )
    return out


def _redirect_findings(pages: list[CrawledPage]) -> list[RawFinding]:
    out = []
    for p in pages:
        if len(p.redirect_chain) >= 2:
            out.append(
                RawFinding(
                    code="REDIRECT_CHAIN", category=Cat.TECHNICAL, severity=Sev.MEDIUM,
                    affected_url=p.url, evidence=" -> ".join(p.redirect_chain + [p.final_url]),
                    explanation="Multiple chained redirects slow page delivery and dilute link equity.",
                    recommended_action="Point the original link directly at the final destination URL.",
                    estimated_effort=2, estimated_impact=3, confidence=8,
                )
            )
    return out


def _metadata_findings(pages: list[CrawledPage]) -> list[RawFinding]:
    out = []
    titles: dict[str, list[CrawledPage]] = defaultdict(list)
    descs: dict[str, list[CrawledPage]] = defaultdict(list)

    for p in pages:
        if not p.title:
            out.append(
                RawFinding(
                    code="MISSING_TITLE", category=Cat.SEO, severity=Sev.HIGH,
                    affected_url=p.url, evidence="No <title> tag found.",
                    explanation="Search engines and AI systems rely on the title tag to understand what a page is about.",
                    recommended_action="Add a unique, descriptive title (roughly 15-65 characters) that states the page's topic and location if relevant.",
                    estimated_effort=1, estimated_impact=6, confidence=9,
                )
            )
        else:
            titles[p.title.strip().lower()].append(p)
            length = len(p.title)
            if length < TITLE_MIN or length > TITLE_MAX:
                out.append(
                    RawFinding(
                        code="TITLE_LENGTH", category=Cat.SEO, severity=Sev.LOW,
                        affected_url=p.url, evidence=f'Title is {length} characters: "{p.title}"',
                        explanation="Titles far outside ~15-65 characters risk truncation in search results or reading as vague.",
                        recommended_action="Tighten or expand the title to clearly state the page topic within roughly 15-65 characters.",
                        estimated_effort=1, estimated_impact=2, confidence=5,
                    )
                )

        if not p.meta_description:
            out.append(
                RawFinding(
                    code="MISSING_META_DESCRIPTION", category=Cat.SEO, severity=Sev.MEDIUM,
                    affected_url=p.url, evidence="No meta description found.",
                    explanation="A missing meta description means search engines auto-generate a snippet, which usually converts worse.",
                    recommended_action="Write a specific, benefit-led meta description (roughly 50-160 characters).",
                    estimated_effort=1, estimated_impact=4, confidence=8,
                )
            )
        else:
            descs[p.meta_description.strip().lower()].append(p)
            length = len(p.meta_description)
            if length < META_MIN or length > META_MAX:
                out.append(
                    RawFinding(
                        code="META_LENGTH", category=Cat.SEO, severity=Sev.LOW,
                        affected_url=p.url, evidence=f"Meta description is {length} characters.",
                        explanation="Meta descriptions far outside ~50-160 characters get truncated or look thin in results.",
                        recommended_action="Rewrite to roughly 50-160 characters, leading with the specific value to the reader.",
                        estimated_effort=1, estimated_impact=2, confidence=5,
                    )
                )

        if not p.canonical:
            out.append(
                RawFinding(
                    code="MISSING_CANONICAL", category=Cat.TECHNICAL, severity=Sev.LOW,
                    affected_url=p.url, evidence="No canonical link tag found.",
                    explanation="Without a canonical tag, search engines must guess which URL variant is authoritative.",
                    recommended_action="Add a self-referencing canonical link tag to this page.",
                    estimated_effort=1, estimated_impact=2, confidence=6,
                )
            )

    for title, group in titles.items():
        if len(group) > 1:
            for p in group:
                out.append(
                    RawFinding(
                        code="DUPLICATE_TITLE", category=Cat.SEO, severity=Sev.MEDIUM,
                        affected_url=p.url,
                        evidence=f'Same title as {len(group)-1} other page(s): "{p.title}"',
                        explanation="Duplicate titles make it hard for search engines (and users) to tell pages apart in results.",
                        recommended_action="Give each page a distinct title that reflects its specific topic, service, or location.",
                        estimated_effort=1, estimated_impact=5, confidence=8,
                    )
                )

    for desc, group in descs.items():
        if len(group) > 1:
            for p in group:
                out.append(
                    RawFinding(
                        code="DUPLICATE_META_DESCRIPTION", category=Cat.SEO, severity=Sev.LOW,
                        affected_url=p.url,
                        evidence=f"Same meta description as {len(group)-1} other page(s).",
                        explanation="Duplicate descriptions reduce differentiation in search results.",
                        recommended_action="Write a unique description for this page.",
                        estimated_effort=1, estimated_impact=3, confidence=7,
                    )
                )
    return out


def _heading_findings(pages: list[CrawledPage]) -> list[RawFinding]:
    out = []
    for p in pages:
        if len(p.h1) == 0:
            out.append(
                RawFinding(
                    code="MISSING_H1", category=Cat.SEO, severity=Sev.MEDIUM,
                    affected_url=p.url, evidence="No <h1> found on the page.",
                    explanation="The H1 is the clearest on-page signal of what the page is about, for both users and AI systems.",
                    recommended_action="Add a single, specific H1 that states the page's main topic.",
                    estimated_effort=1, estimated_impact=4, confidence=7,
                )
            )
        elif len(p.h1) > 1:
            out.append(
                RawFinding(
                    code="MULTIPLE_H1", category=Cat.SEO, severity=Sev.LOW,
                    affected_url=p.url, evidence=f"{len(p.h1)} H1 tags found: {p.h1}",
                    explanation="Multiple H1s dilute the page's primary topic signal.",
                    recommended_action="Keep one H1 for the page's main topic; demote the rest to H2/H3.",
                    estimated_effort=1, estimated_impact=2, confidence=6,
                )
            )
    return out


def _thin_content_findings(pages: list[CrawledPage]) -> list[RawFinding]:
    out = []
    for p in pages:
        if p.word_count < THIN_CONTENT_HARD_MIN:
            out.append(
                RawFinding(
                    code="THIN_CONTENT", category=Cat.CONTENT, severity=Sev.MEDIUM,
                    affected_url=p.url, evidence=f"{p.word_count} words of visible text.",
                    explanation="Very little text gives search engines and AI systems almost nothing to understand or cite from this page.",
                    recommended_action="Expand the page with specific, useful content answering what a visitor to this page would actually want to know.",
                    estimated_effort=4, estimated_impact=5, confidence=6,
                )
            )
        elif p.word_count < THIN_CONTENT_SOFT_MIN:
            out.append(
                RawFinding(
                    code="THIN_CONTENT", category=Cat.CONTENT, severity=Sev.LOW,
                    affected_url=p.url, evidence=f"{p.word_count} words of visible text.",
                    explanation="This page is on the thin side; context matters (a simple contact page is fine thin) but if it's meant to rank, it likely needs more substance.",
                    recommended_action="Consider whether this page should be more comprehensive for its purpose.",
                    estimated_effort=3, estimated_impact=3, confidence=4,
                )
            )
    return out


def _image_alt_findings(pages: list[CrawledPage]) -> list[RawFinding]:
    out = []
    for p in pages:
        missing = [img for img in p.images if not img.get("has_alt")]
        if missing:
            severity = Sev.MEDIUM if len(missing) / max(len(p.images), 1) > 0.5 else Sev.LOW
            out.append(
                RawFinding(
                    code="MISSING_ALT_TEXT", category=Cat.SEO, severity=severity,
                    affected_url=p.url, evidence=f"{len(missing)} of {len(p.images)} images have no alt text.",
                    explanation="Alt text is how screen readers and AI systems understand images; it's also an accessibility requirement.",
                    recommended_action="Add descriptive alt text to each image (empty alt=\"\" is fine for purely decorative images).",
                    estimated_effort=2, estimated_impact=3, confidence=8,
                )
            )
    return out


def _orphan_findings(pages: list[CrawledPage]) -> list[RawFinding]:
    out = []
    for p in pages:
        if p.is_orphan:
            out.append(
                RawFinding(
                    code="ORPHAN_PAGE", category=Cat.INTERNAL_LINKING, severity=Sev.MEDIUM,
                    affected_url=p.url, evidence="No other crawled page links to this URL.",
                    explanation="Orphan pages are hard for search engines to discover through normal crawling and get little internal authority.",
                    recommended_action="Add at least one contextual internal link to this page from a relevant, already-linked page.",
                    estimated_effort=1, estimated_impact=4, confidence=7,
                )
            )
        elif p.inbound_internal_link_count == 1:
            out.append(
                RawFinding(
                    code="POOR_INTERNAL_LINKING", category=Cat.INTERNAL_LINKING, severity=Sev.LOW,
                    affected_url=p.url, evidence="Only one crawled page links to this URL.",
                    explanation="Pages with very few inbound internal links are weakly supported in the site's structure.",
                    recommended_action="Link to this page from 1-2 more relevant pages (e.g. related service or location pages).",
                    estimated_effort=1, estimated_impact=2, confidence=5,
                )
            )
    return out


def _indexability_findings(pages: list[CrawledPage]) -> list[RawFinding]:
    out = []
    for p in pages:
        if not p.is_indexable:
            out.append(
                RawFinding(
                    code="NOINDEX_PAGE", category=Cat.TECHNICAL, severity=Sev.INFO,
                    affected_url=p.url, evidence=f"robots meta: {p.robots_meta}",
                    explanation="This page is explicitly excluded from search indexing. This may be intentional.",
                    recommended_action="Confirm this is intentional; if not, remove the noindex directive.",
                    estimated_effort=1, estimated_impact=1, confidence=5,
                )
            )
    return out


def _sitemap_findings(crawl: CrawlResult, pages: list[CrawledPage]) -> list[RawFinding]:
    out = []
    if not crawl.sitemap_urls:
        out.append(
            RawFinding(
                code="NO_SITEMAP", category=Cat.TECHNICAL, severity=Sev.MEDIUM,
                affected_url=crawl.root_url, evidence="No sitemap.xml found via robots.txt or the conventional path.",
                explanation="A sitemap helps search engines discover and prioritize your pages, especially on smaller sites.",
                recommended_action="Publish an XML sitemap and reference it from robots.txt.",
                estimated_effort=2, estimated_impact=4, confidence=7,
            )
        )
    return out


def _performance_findings(pages: list[CrawledPage]) -> list[RawFinding]:
    out = []
    for p in pages:
        if p.response_time_ms and p.response_time_ms > SLOW_RESPONSE_MS:
            out.append(
                RawFinding(
                    code="SLOW_RESPONSE", category=Cat.TECHNICAL, severity=Sev.LOW,
                    affected_url=p.url, evidence=f"Server responded in {p.response_time_ms:.0f}ms.",
                    explanation="Slow server response time hurts both user experience and crawl efficiency.",
                    recommended_action="Investigate hosting, caching, or render-blocking resources for this page.",
                    estimated_effort=4, estimated_impact=3, confidence=5,
                )
            )
    return out


def _schema_presence_findings(pages: list[CrawledPage]) -> list[RawFinding]:
    out = []
    any_schema = any(p.json_ld for p in pages)
    if not any_schema and pages:
        out.append(
            RawFinding(
                code="NO_STRUCTURED_DATA", category=Cat.STRUCTURED_DATA, severity=Sev.MEDIUM,
                affected_url=pages[0].url if pages else None,
                evidence="No JSON-LD structured data found on any crawled page.",
                explanation="Structured data helps search engines and AI systems parse entities (business, services, location) reliably instead of inferring them from prose.",
                recommended_action="Add LocalBusiness/Organization schema site-wide, and Service schema on service pages, matching what's actually true.",
                estimated_effort=3, estimated_impact=6, confidence=6,
            )
        )
    return out
