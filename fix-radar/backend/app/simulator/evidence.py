from __future__ import annotations

from dataclasses import asdict, dataclass

from app import business_context as biz
from app.models.core import Page
from app.models.enums import EvidenceStrength
from app.simulator.query_analysis import QueryEntities

REQUIREMENT_KEYWORDS: dict[str, list[str]] = {
    "expertise": ["certified", "certification", "cscs", "nasm", "nsca", "credential", "licensed", "expert", "specializ"],
    "credibility": ["credible", "trusted", "reputable", "professional"],
    "results": ["result", "outcome", "measurable", "transformation", "improved", "reduced", "increased", "lost "],
    "reviews": ["review", "testimonial", "rating", "client says"],
    "authority": ["recognized", "featured in", "as seen on", "partnered with", "association", "press"],
    "evidence": ["case study", "case studies", "testimonial", "before and after", "outcome", "result"],
    "specialization": [],  # filled dynamically from intent
}
THIRD_PARTY_KEYWORDS = ["featured in", "as seen on", "partnered with", "press", "media coverage", "association member", "affiliate of"]
METHODOLOGY_KEYWORDS = [s.lower() for s in biz.METHODOLOGY_STAGES]


@dataclass
class EvidenceItem:
    requirement: str
    evidence: str
    source_url: str | None
    strength: str
    gap: str | None


def _pages_matching(pages: list[Page], keywords: list[str]) -> list[Page]:
    if not keywords:
        return []
    out = []
    for p in pages:
        text = (p.text_content or "").lower()
        if any(kw in text for kw in keywords):
            out.append(p)
    return out


def _strength_from_hits(matching_pages: list[Page], strong_threshold: int = 3, moderate_threshold: int = 1) -> EvidenceStrength:
    if len(matching_pages) == 0:
        return EvidenceStrength.MISSING
    if len(matching_pages) >= strong_threshold:
        return EvidenceStrength.STRONG
    if len(matching_pages) >= moderate_threshold:
        return EvidenceStrength.MODERATE
    return EvidenceStrength.WEAK


def _requirement_from_keywords(name: str, keywords: list[str], pages: list[Page], gap_text: str) -> EvidenceItem:
    matches = _pages_matching(pages, keywords)
    strength = _strength_from_hits(matches)
    if not matches:
        return EvidenceItem(requirement=name, evidence="Not found on any crawled page.", source_url=None, strength=strength.value, gap=gap_text)
    best = matches[0]
    evidence = f"Found on {len(matches)} page(s), e.g. {best.title or best.url}."
    return EvidenceItem(requirement=name, evidence=evidence, source_url=best.url, strength=strength.value, gap=None)


def build_evidence_map(entities: QueryEntities, pages: list[Page]) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []

    location_term = entities.location or biz.PRIMARY_LOCATION
    loc_pages = _pages_matching(pages, [location_term.lower()])
    loc_strength = _strength_from_hits(loc_pages, strong_threshold=3, moderate_threshold=1)
    items.append(
        EvidenceItem(
            requirement=f"Service area: {location_term}",
            evidence=(f"Mentioned on {len(loc_pages)} page(s)." if loc_pages else "Not mentioned on any crawled page."),
            source_url=loc_pages[0].url if loc_pages else None,
            strength=loc_strength.value,
            gap=None if loc_pages else f"No crawled page explicitly names {location_term}.",
        )
    )

    if entities.audience:
        aud_kw = [entities.audience.lower(), "professional", "executive"]
        items.append(_requirement_from_keywords(
            f"Audience fit: {entities.audience}", aud_kw, pages,
            f"No crawled page explicitly addresses '{entities.audience}' as the target audience.",
        ))

    service_kw = [s.lower() for s in biz.SERVICES]
    if entities.intent.value == "EXECUTIVE_HEALTH":
        service_kw = ["executive health", "executive coaching"]
    elif entities.intent.value == "CORRECTIVE_EXERCISE":
        service_kw = ["corrective exercise"]
    elif entities.profession:
        service_kw = [entities.profession] + service_kw
    items.append(_requirement_from_keywords(
        "Relevant service offering", service_kw, pages,
        "No crawled page explicitly names a matching service.",
    ))

    for criterion in entities.decision_criteria:
        if criterion in ("location", "services", "specialization"):
            continue  # already covered above
        keywords = REQUIREMENT_KEYWORDS.get(criterion, [])
        if not keywords:
            continue
        items.append(_requirement_from_keywords(
            criterion.capitalize(), keywords, pages,
            f"No crawled page provides clear {criterion} signals.",
        ))

    items.append(_requirement_from_keywords(
        f"Methodology ({biz.METHODOLOGY_NAME})", METHODOLOGY_KEYWORDS, pages,
        "No crawled page explains the methodology.",
    ))

    # Third-party authority is deliberately always evaluated this strictly: we have
    # no backlink/press API connected, so first-party mentions of "featured in"
    # etc. are the ONLY evidence we can honestly claim, and even those are weak
    # relative to genuine independent corroboration.
    tp_matches = _pages_matching(pages, THIRD_PARTY_KEYWORDS)
    items.append(
        EvidenceItem(
            requirement="Independent third-party authority",
            evidence=(
                f"{len(tp_matches)} page(s) reference third-party recognition, but this tool has no connected "
                "backlink/press/review API -- treat this as weak at best until independently verified."
                if tp_matches else
                "No third-party recognition language found, and no backlink/press/review API is connected."
            ),
            source_url=tp_matches[0].url if tp_matches else None,
            strength=(EvidenceStrength.WEAK.value if tp_matches else EvidenceStrength.MISSING.value),
            gap="No independent corroboration is currently indexed by this tool.",
        )
    )

    return items
