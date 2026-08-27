from __future__ import annotations

import re
from dataclasses import dataclass, field

from app import business_context as biz
from app.audit.base import RawFinding, score_from_findings
from app.crawler.crawler import CrawledPage
from app.models.enums import FindingCategory as Cat
from app.models.enums import Severity as Sev

CREDENTIAL_KEYWORDS = [
    "certified", "certification", "cscs", "nasm", "ace ", "nsca", "credential",
    "licensed", "license", "corrective exercise specialist", "years of experience",
    "degree in", "b.s.", "m.s.", "kinesiology", "exercise science", "physiology",
]
EVIDENCE_KEYWORDS = [
    "case study", "case studies", "before and after", "results", "client results",
    "testimonial", "review", "success story", "outcome", "transformation", "lost ",
    "gained ", "improved", "reduced", "increased",
]
TRUST_KEYWORDS = ["contact", "phone", "email", "address", "privacy policy", "terms of service", "policy"]
CTA_KEYWORDS = ["book", "schedule", "call", "get started", "contact us", "free consultation", "apply", "sign up"]
WHO_KEYWORDS = [biz.BUSINESS_NAME.lower(), "trainer", "coach"]
WHAT_KEYWORDS = [s.lower() for s in biz.SERVICES] + ["personal training", "coaching"]
WHY_KEYWORDS = ["because", "why", "unlike", "different", "difference"]
HOW_KEYWORDS = [s.lower() for s in biz.METHODOLOGY_STAGES] + ["method", "approach", "process"]
AUDIENCE_KEYWORDS = ["executive", "professional", "busy", "over 30", "over 40", "over 50", "men", "women"]
DIFFERENTIATOR_KEYWORDS = [d.lower() for d in biz.DIFFERENTIATORS] + ["unlike", "difference", "what makes"]


@dataclass
class PageAioProfile:
    url: str
    entity_clarity: float
    expertise: float
    evidence: float
    geo_relevance: float
    answerability: float
    semantic_completeness: float
    trust: float
    conversion: float
    structured_data: float
    missing_dimensions: list[str] = field(default_factory=list)
    citation_candidates: list[str] = field(default_factory=list)
    location_mentions: list[str] = field(default_factory=list)


def _hit_count(text: str, keywords: list[str]) -> int:
    return sum(1 for kw in keywords if kw in text)


def _ratio_score(hits: int, target: int) -> float:
    if target <= 0:
        return 10.0
    return round(min(10.0, 10.0 * hits / target), 1)


def _extract_citation_candidates(text_content: str) -> list[str]:
    """Pull out concise, specific, factual-sounding sentences that could serve
    as an AI citation passage. Purely extractive -- never invents text."""
    sentences = re.split(r"(?<=[.!?])\s+", text_content)
    candidates = []
    for s in sentences:
        s = s.strip()
        if not (30 <= len(s) <= 220):
            continue
        has_number = bool(re.search(r"\d", s))
        has_specific_term = any(
            kw in s.lower() for kw in (WHAT_KEYWORDS + HOW_KEYWORDS + [biz.PRIMARY_LOCATION.lower()])
        )
        if has_number or has_specific_term:
            candidates.append(s)
    return candidates[:5]


def analyze_page(page: CrawledPage) -> PageAioProfile:
    text = (page.text_content or "").lower()
    all_headings = " ".join((page.h1 or []) + (page.h2 or []) + (page.h3 or [])).lower()

    entity_hits = _hit_count(text, WHO_KEYWORDS)
    entity_clarity = _ratio_score(entity_hits, 2)

    expertise = _ratio_score(_hit_count(text, CREDENTIAL_KEYWORDS), 3)
    evidence = _ratio_score(_hit_count(text, EVIDENCE_KEYWORDS), 3)

    location_mentions = [loc for loc in ([biz.PRIMARY_LOCATION] + biz.SERVICE_AREAS) if loc.lower() in text]
    geo_relevance = _ratio_score(len(location_mentions), 2)

    trust = _ratio_score(_hit_count(text, TRUST_KEYWORDS), 2)
    conversion = _ratio_score(_hit_count(text, CTA_KEYWORDS), 1)

    dims = {
        "who": _hit_count(text, WHO_KEYWORDS) > 0,
        "what": _hit_count(text, WHAT_KEYWORDS) > 0,
        "where": len(location_mentions) > 0,
        "why": _hit_count(text, WHY_KEYWORDS) > 0,
        "how": _hit_count(text, HOW_KEYWORDS) > 0,
        "who it is for": _hit_count(text, AUDIENCE_KEYWORDS) > 0,
        "what makes it different": _hit_count(text, DIFFERENTIATOR_KEYWORDS) > 0,
    }
    missing_dimensions = [k for k, present in dims.items() if not present]
    semantic_completeness = round(10.0 * sum(dims.values()) / len(dims), 1)

    question_headings = len(re.findall(r"\?", all_headings))
    has_faq_schema = any(
        "faqpage" in str(item.get("@type", "")).lower() for item in (page.json_ld or []) if isinstance(item, dict)
    )
    if question_headings > 0:
        answerability = 10.0 if has_faq_schema else _ratio_score(question_headings, 3)
    else:
        # No explicit Q&A structure: base it on whether the page's content actually
        # covers who/what/where/why/how at all.
        answerability = semantic_completeness

    schema_types = {
        str(item.get("@type", "")).lower()
        for item in (page.json_ld or [])
        if isinstance(item, dict)
    }
    structured_data = 10.0 if schema_types else 0.0

    return PageAioProfile(
        url=page.url,
        entity_clarity=entity_clarity,
        expertise=expertise,
        evidence=evidence,
        geo_relevance=geo_relevance,
        answerability=round(answerability, 1),
        semantic_completeness=semantic_completeness,
        trust=trust,
        conversion=conversion,
        structured_data=structured_data,
        missing_dimensions=missing_dimensions,
        citation_candidates=_extract_citation_candidates(page.text_content or ""),
        location_mentions=location_mentions,
    )


def run_aio_audit(pages: list[CrawledPage]) -> tuple[list[RawFinding], dict[str, PageAioProfile], dict[str, float]]:
    ok_pages = [p for p in pages if p.status_code and p.status_code < 400 and (p.text_content or "").strip()]
    profiles = {p.url: analyze_page(p) for p in ok_pages}
    findings: list[RawFinding] = []

    site_has_credentials = any(prof.expertise > 0 for prof in profiles.values())
    site_has_evidence = any(prof.evidence > 0 for prof in profiles.values())
    site_has_geo = any(prof.geo_relevance > 0 for prof in profiles.values())
    site_has_trust = any(prof.trust > 0 for prof in profiles.values())
    site_has_faq_schema = any(
        any("faqpage" in str(item.get("@type", "")).lower() for item in (p.json_ld or []) if isinstance(item, dict))
        for p in ok_pages
    )
    site_has_local_business_schema = any(
        any(
            t in str(item.get("@type", "")).lower()
            for t in ("localbusiness", "organization")
            for item in (p.json_ld or []) if isinstance(item, dict)
        )
        for p in ok_pages
    )

    if not site_has_geo:
        findings.append(
            RawFinding(
                code="MISSING_LOCATION_SIGNAL", category=Cat.LOCAL, severity=Sev.HIGH,
                affected_url=pages[0].url if pages else None,
                evidence="No crawled page mentions San Diego or a named service area.",
                explanation="An AI system answering a location-based query needs explicit, repeated geographic signals to associate OmniFit with San Diego.",
                recommended_action=f"State the service area explicitly on key pages: {biz.PRIMARY_LOCATION} and the specific neighborhoods served.",
                estimated_effort=2, estimated_impact=8, confidence=7,
            )
        )

    if not site_has_credentials:
        findings.append(
            RawFinding(
                code="WEAK_EXPERTISE_SIGNALS", category=Cat.AUTHORITY, severity=Sev.MEDIUM,
                affected_url=pages[0].url if pages else None,
                evidence="No credential, certification, or methodology-depth language found on any crawled page.",
                explanation="Without explicit expertise signals, an AI system has little basis to describe OmniFit as expert or credentialed versus a generic trainer.",
                recommended_action="Add a credentials/expertise section (only real, verifiable facts) explaining trainer qualifications and methodology depth.",
                estimated_effort=3, estimated_impact=7, confidence=6,
            )
        )

    if not site_has_evidence:
        findings.append(
            RawFinding(
                code="WEAK_EVIDENCE", category=Cat.AUTHORITY, severity=Sev.HIGH,
                affected_url=pages[0].url if pages else None,
                evidence="No case studies, testimonials, or measurable outcome language found on any crawled page.",
                explanation="Evidence (results, testimonials, case studies) is one of the strongest signals for both human trust and AI recommendation confidence.",
                recommended_action="Publish at least one detailed, real client case study with a measurable, honestly-reported outcome.",
                estimated_effort=5, estimated_impact=9, confidence=7,
            )
        )

    if not site_has_trust:
        findings.append(
            RawFinding(
                code="WEAK_TRUST_SIGNALS", category=Cat.TRUST, severity=Sev.MEDIUM,
                affected_url=pages[0].url if pages else None,
                evidence="No contact, phone, or policy language found on any crawled page.",
                explanation="Clear contact information and policies are baseline trust signals for both users and AI systems evaluating legitimacy.",
                recommended_action="Ensure a page clearly lists contact information (phone/email/address) and links to any policies.",
                estimated_effort=1, estimated_impact=5, confidence=7,
            )
        )

    if not site_has_local_business_schema:
        findings.append(
            RawFinding(
                code="MISSING_LOCALBUSINESS_SCHEMA", category=Cat.STRUCTURED_DATA, severity=Sev.MEDIUM,
                affected_url=pages[0].url if pages else None,
                evidence="No LocalBusiness or Organization JSON-LD found.",
                explanation="LocalBusiness/Organization schema gives search and AI systems an unambiguous, structured description of who OmniFit is and where it operates.",
                recommended_action="Add LocalBusiness schema with accurate name, address/service area, phone, and services -- only fields you can state as true.",
                estimated_effort=3, estimated_impact=6, confidence=6,
            )
        )

    for p in ok_pages:
        prof = profiles[p.url]
        question_headings_present = any("?" in h for h in (p.h2 or []) + (p.h3 or []))
        has_faq_schema_here = any(
            "faqpage" in str(item.get("@type", "")).lower() for item in (p.json_ld or []) if isinstance(item, dict)
        )
        if question_headings_present and not has_faq_schema_here:
            findings.append(
                RawFinding(
                    code="NO_FAQ_SCHEMA", category=Cat.STRUCTURED_DATA, severity=Sev.LOW,
                    affected_url=p.url,
                    evidence="Page has question-style headings but no FAQPage structured data.",
                    explanation="FAQPage schema helps AI systems and search engines lift Q&A content directly, only where the content genuinely is a Q&A.",
                    recommended_action="Add FAQPage schema mirroring the on-page questions and answers exactly.",
                    estimated_effort=2, estimated_impact=4, confidence=6,
                )
            )

        if len(prof.missing_dimensions) >= 4 and p.word_count > 80:
            findings.append(
                RawFinding(
                    code="LOW_ANSWERABILITY", category=Cat.AIO, severity=Sev.MEDIUM,
                    affected_url=p.url,
                    evidence=f"Page does not clearly address: {', '.join(prof.missing_dimensions)}.",
                    explanation="A page that doesn't cover who/what/where/why/how gives an AI system little to work with when deciding whether to cite or recommend it.",
                    recommended_action=f"Add a short section explicitly covering: {', '.join(prof.missing_dimensions)}.",
                    estimated_effort=3, estimated_impact=6, confidence=6,
                )
            )

        if prof.conversion == 0 and p.word_count > 80:
            findings.append(
                RawFinding(
                    code="WEAK_CONVERSION_CTA", category=Cat.CONVERSION, severity=Sev.LOW,
                    affected_url=p.url,
                    evidence="No clear call-to-action language (book/schedule/contact) found on this page.",
                    explanation="A page that doesn't tell a ready visitor what to do next loses conversions it already earned.",
                    recommended_action="Add a clear, single next-step CTA (e.g. \"Book a consultation\") near the top and bottom of the page.",
                    estimated_effort=1, estimated_impact=5, confidence=6,
                )
            )

    if not site_has_faq_schema:
        any_faq_content = any(
            any("?" in h for h in (p.h2 or []) + (p.h3 or [])) for p in ok_pages
        )
        if any_faq_content:
            findings.append(
                RawFinding(
                    code="NO_FAQ_SCHEMA", category=Cat.STRUCTURED_DATA, severity=Sev.LOW,
                    affected_url=None,
                    evidence="FAQ-style content exists on the site but no page carries FAQPage schema.",
                    explanation="This is a site-wide structured-data gap on top of any single page.",
                    recommended_action="Roll out FAQPage schema wherever a page has a genuine, on-page FAQ section.",
                    estimated_effort=3, estimated_impact=4, confidence=6,
                )
            )

    aio_findings = [f for f in findings if f.category in (Cat.AIO, Cat.STRUCTURED_DATA)]
    local_findings = [f for f in findings if f.category == Cat.LOCAL]
    authority_findings = [f for f in findings if f.category == Cat.AUTHORITY]
    conversion_findings = [f for f in findings if f.category in (Cat.CONVERSION, Cat.TRUST)]

    def avg(attr: str) -> float:
        vals = [getattr(p, attr) for p in profiles.values()]
        return (sum(vals) / len(vals)) if vals else 0.0

    # Blend two heuristics: a "does depth/coverage actually exist across pages"
    # signal (graduated, 0-10 scaled to 0-100) with a "were structural gaps found"
    # signal (severity-weighted, from score_from_findings). Using either alone is
    # misleading -- findings-only scoring can't tell "mentioned once" from
    # "thoroughly covered", and coverage-only scoring would ignore real structural
    # gaps like missing schema. Both are still heuristics, not measurements.
    graduated = {
        "aio_score": (avg("entity_clarity") + avg("semantic_completeness") + avg("answerability")) / 3 * 10,
        "local_score": avg("geo_relevance") * 10,
        "authority_score": (avg("expertise") + avg("evidence")) / 2 * 10,
        "conversion_score": avg("conversion") * 10,
    }
    finding_based = {
        "aio_score": score_from_findings(aio_findings, len(ok_pages)),
        "local_score": score_from_findings(local_findings, len(ok_pages)),
        "authority_score": score_from_findings(authority_findings, len(ok_pages)),
        "conversion_score": score_from_findings(conversion_findings, len(ok_pages)),
    }
    scores = {key: round(0.6 * graduated[key] + 0.4 * finding_based[key], 1) for key in graduated}
    return findings, profiles, scores
