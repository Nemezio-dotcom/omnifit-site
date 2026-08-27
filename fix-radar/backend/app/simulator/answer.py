from __future__ import annotations

from app import business_context as biz
from app.models.core import Page
from app.models.enums import EvidenceStrength
from app.simulator.evidence import EvidenceItem
from app.simulator.query_analysis import QueryEntities

CORE_REQUIREMENT_PREFIXES = ("Service area", "Relevant service")
RECOMMEND_THRESHOLD = 65.0


def would_recommend(overall_score: float, evidence_items: list[EvidenceItem]) -> bool:
    core_ok = all(
        item.strength not in (EvidenceStrength.MISSING.value,)
        for item in evidence_items
        if item.requirement.startswith(CORE_REQUIREMENT_PREFIXES)
    )
    return overall_score >= RECOMMEND_THRESHOLD and core_ok


def build_simulated_answer(query: str, entities: QueryEntities, evidence_items: list[EvidenceItem], recommend: bool) -> tuple[str, list[dict]]:
    strong_items = [i for i in evidence_items if i.strength in (EvidenceStrength.STRONG.value, EvidenceStrength.VERY_STRONG.value) and i.source_url]
    evidence_used = [{"url": i.source_url, "note": i.requirement} for i in strong_items[:6]]

    if not recommend:
        missing = [i.requirement for i in evidence_items if i.strength == EvidenceStrength.MISSING.value]
        answer = (
            f'Based on the currently indexed evidence, I would not have enough information to confidently '
            f'recommend {biz.BUSINESS_NAME} for "{query}" yet. '
            + (f"The clearest gaps are: {', '.join(missing[:3])}." if missing else "The available evidence is too thin across several requirements.")
        )
        return answer, evidence_used

    strengths_text = "; ".join(f"{i.requirement.lower()}" for i in strong_items[:4]) or "its stated service offering"
    answer = (
        f"{biz.BUSINESS_NAME} would be a reasonable candidate for \"{query}\" based on the currently indexed evidence: "
        f"{strengths_text}. Its {biz.METHODOLOGY_NAME} methodology and explicit service list "
        f"({', '.join(biz.SERVICES[:4])}, among others) provide additional supporting context. "
        "This reflects evidence strength as observed on the crawled site, not an actual ranking from any AI provider."
    )
    return answer, evidence_used


def build_page_support(pages: list[Page], entities: QueryEntities) -> list[dict]:
    keywords = []
    if entities.location:
        keywords.append(entities.location.lower())
    if entities.profession:
        keywords.append(entities.profession.lower())
    keywords += [s.lower() for s in biz.SERVICES]

    out = []
    for p in pages:
        text = (p.text_content or "").lower()
        if not text:
            continue
        hits = sum(1 for kw in keywords if kw in text)
        support_pct = round(min(100, hits / max(len(keywords), 1) * 140), 0)  # scaled so a few strong hits reads as strong support
        if support_pct > 0:
            out.append({"url": p.url, "title": p.title, "support_pct": support_pct})
    out.sort(key=lambda x: x["support_pct"], reverse=True)
    return out[:8]


def build_evidence_gaps(evidence_items: list[EvidenceItem]) -> list[dict]:
    weak_or_missing = [i for i in evidence_items if i.strength in (EvidenceStrength.WEAK.value, EvidenceStrength.MISSING.value)]

    def importance(item: EvidenceItem) -> int:
        if item.requirement.startswith(CORE_REQUIREMENT_PREFIXES):
            return 10
        if "third-party" in item.requirement.lower():
            return 9
        if "evidence" in item.requirement.lower() or "results" in item.requirement.lower():
            return 8
        return 6

    weak_or_missing.sort(key=importance, reverse=True)
    gaps = []
    for item in weak_or_missing[:5]:
        gaps.append(
            {
                "gap": item.requirement,
                "importance": importance(item),
                "current_evidence": item.strength,
                "why_it_matters": item.gap or "This weakens confidence an AI system could have in recommending the business for this query.",
                "recommended_action": _recommend_action_for(item),
                "estimated_effort": "Medium" if "third-party" in item.requirement.lower() else "Low",
            }
        )
    return gaps


def _recommend_action_for(item: EvidenceItem) -> str:
    req = item.requirement.lower()
    if "third-party" in req:
        return (
            "Seek legitimate third-party references: professional-association mentions, guest interviews, "
            "verified reviews, or coverage from a reputable local publication. Do not use fake reviews, "
            "paid link schemes, or spammy directories."
        )
    if "service area" in req:
        return f"State the service area explicitly and repeatedly on key pages (e.g. {biz.PRIMARY_LOCATION} and named neighborhoods)."
    if "relevant service" in req:
        return "Add or expand a dedicated page naming this specific service clearly in the title and H1."
    if "evidence" in req or "results" in req:
        return "Publish a real, specific, honestly-reported client outcome or case study."
    if "expertise" in req:
        return "State real credentials and methodology depth -- only verifiable facts, no invented certifications."
    return "Add explicit, specific content addressing this requirement."
