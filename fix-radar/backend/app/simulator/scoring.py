from __future__ import annotations

from app.models.enums import EvidenceStrength
from app.simulator.evidence import EvidenceItem

STRENGTH_SCORE = {
    EvidenceStrength.VERY_STRONG.value: 95.0,
    EvidenceStrength.STRONG.value: 80.0,
    EvidenceStrength.MODERATE.value: 60.0,
    EvidenceStrength.WEAK.value: 35.0,
    EvidenceStrength.MISSING.value: 10.0,
}

SUB_SCORE_WEIGHTS = {
    "entity_clarity": 0.10,
    "query_relevance": 0.15,
    "expertise": 0.12,
    "evidence": 0.15,
    "trust": 0.10,
    "local_relevance": 0.13,
    "third_party_authority": 0.10,
    "content_completeness": 0.08,
    "differentiation": 0.07,
}


def _find(items: list[EvidenceItem], prefix: str) -> EvidenceItem | None:
    return next((i for i in items if i.requirement.lower().startswith(prefix.lower())), None)


def compute_sub_scores(evidence_items: list[EvidenceItem], avg_trust_0_100: float, avg_semantic_completeness_0_10: float) -> dict[str, float]:
    location_item = _find(evidence_items, "Service area")
    service_item = _find(evidence_items, "Relevant service")
    expertise_item = _find(evidence_items, "Expertise")
    evidence_item = _find(evidence_items, "Evidence")
    results_item = _find(evidence_items, "Results")
    third_party_item = _find(evidence_items, "Independent third-party")
    methodology_item = _find(evidence_items, "Methodology")

    def score_of(item: EvidenceItem | None, default: float = 50.0) -> float:
        return STRENGTH_SCORE[item.strength] if item else default

    entity_clarity = score_of(service_item, 40.0)
    query_relevance = round((score_of(service_item, 40.0) + score_of(location_item, 40.0)) / 2, 1)
    expertise = score_of(expertise_item, 30.0)
    evidence_score = round((score_of(evidence_item, 20.0) + score_of(results_item, 20.0)) / 2, 1)
    local_relevance = score_of(location_item, 20.0)
    third_party_authority = score_of(third_party_item, 10.0)
    differentiation = score_of(methodology_item, 30.0)

    sub_scores = {
        "entity_clarity": round(entity_clarity, 1),
        "query_relevance": query_relevance,
        "expertise": round(expertise, 1),
        "evidence": evidence_score,
        "trust": round(avg_trust_0_100, 1),
        "local_relevance": round(local_relevance, 1),
        "third_party_authority": round(third_party_authority, 1),
        "content_completeness": round(avg_semantic_completeness_0_10 * 10, 1),
        "differentiation": round(differentiation, 1),
    }
    return sub_scores


def overall_readiness(sub_scores: dict[str, float]) -> float:
    total = sum(sub_scores[key] * weight for key, weight in SUB_SCORE_WEIGHTS.items())
    return round(total, 1)
