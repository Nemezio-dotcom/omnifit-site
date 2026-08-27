from __future__ import annotations

import re
from dataclasses import dataclass, field

from app import business_context as biz
from app.models.enums import QueryCluster, QueryIntent

_LOCATION_KEYWORDS = [biz.PRIMARY_LOCATION] + biz.SERVICE_AREAS
_AGE_RE = re.compile(r"\b(over|above)\s?(\d{2})\b|\b(\d{2})\+\b|\bmen\b|\bwomen\b|\bseniors?\b")

_INTENT_RULES: list[tuple[QueryIntent, list[str]]] = [
    (QueryIntent.EXECUTIVE_HEALTH, ["executive health", "executive coaching", "executive wellness", "executive"]),
    (QueryIntent.CORRECTIVE_EXERCISE, ["corrective exercise", "post-rehab", "injury recovery", "rehab"]),
    (QueryIntent.NUTRITION, ["nutrition", "diet", "meal plan"]),
    (QueryIntent.TRANSFORMATION, ["transformation", "before and after", "weight loss", "lose weight", "body composition"]),
    (QueryIntent.AGE_SPECIFIC, ["over 30", "over 40", "over 50", "over 60", "men over", "women over"]),
    (QueryIntent.COMPARISON, ["vs", "versus", "compare", "better than"]),
    (QueryIntent.PERSONAL_TRAINER_RECOMMENDATION, ["best personal trainer", "personal trainer for", "who is a good"]),
    (QueryIntent.LOCATION_SPECIFIC, _LOCATION_KEYWORDS),
    (QueryIntent.SERVICE_RECOMMENDATION, ["in-home", "virtual coaching", "strength training", "private training"]),
]

_CRITERIA_KEYWORDS = {
    "expertise": ["expert", "specializ", "certified", "credential"],
    "credibility": ["credibl", "trust", "reputable"],
    "experience": ["experience", "years"],
    "results": ["result", "outcome", "success"],
    "location": _LOCATION_KEYWORDS,
    "services": ["service", "offer", "provide"],
    "reviews": ["review", "testimonial", "rating"],
    "authority": ["authority", "recognized", "featured"],
    "evidence": ["evidence", "proof", "case stud"],
    "specialization": ["specializ", "focus on", "specific to"],
}


@dataclass
class QueryEntities:
    profession: str | None
    location: str | None
    audience: str | None
    intent: QueryIntent
    cluster: QueryCluster
    decision_criteria: list[str] = field(default_factory=list)


def classify_intent(query: str) -> QueryIntent:
    q = query.lower()
    # Specific-topic intents (executive, corrective exercise, nutrition, ...) win over
    # the generic "local recommendation" bucket -- a query naming both San Diego AND
    # executives is about executive positioning first, location second.
    for intent, keywords in _INTENT_RULES:
        if any(kw.lower() in q for kw in keywords):
            return intent
    if any(loc.lower() in q for loc in _LOCATION_KEYWORDS) and ("best" in q or "recommend" in q or "who" in q):
        return QueryIntent.LOCAL_RECOMMENDATION
    if "personal trainer" in q or "trainer" in q or "coach" in q:
        return QueryIntent.PERSONAL_TRAINER_RECOMMENDATION
    if "?" in q:
        return QueryIntent.GENERAL_INFORMATION
    return QueryIntent.OTHER


def classify_cluster(intent: QueryIntent, query: str) -> QueryCluster:
    q = query.lower()
    if intent == QueryIntent.EXECUTIVE_HEALTH:
        return QueryCluster.EXECUTIVE
    if intent == QueryIntent.CORRECTIVE_EXERCISE:
        return QueryCluster.CORRECTIVE_EXERCISE
    if "in-home" in q or "in home" in q:
        return QueryCluster.IN_HOME
    if intent == QueryIntent.NUTRITION:
        return QueryCluster.NUTRITION
    if intent == QueryIntent.TRANSFORMATION:
        return QueryCluster.TRANSFORMATION
    if intent == QueryIntent.AGE_SPECIFIC or _AGE_RE.search(q):
        return QueryCluster.AGE_SPECIFIC
    if any(loc.lower() in q for loc in _LOCATION_KEYWORDS):
        return QueryCluster.LOCAL
    return QueryCluster.GENERAL


def extract_entities(query: str) -> QueryEntities:
    q = query.lower()
    intent = classify_intent(query)
    cluster = classify_cluster(intent, query)

    profession = None
    if "personal trainer" in q or "trainer" in q:
        profession = "personal trainer"
    elif "coach" in q:
        profession = "coach"

    location = next((loc for loc in _LOCATION_KEYWORDS if loc.lower() in q), None)

    audience = None
    if "executive" in q:
        audience = "executives"
    elif "professional" in q:
        audience = "professionals"
    elif _AGE_RE.search(q):
        audience = _AGE_RE.search(q).group(0)
    elif "men" in q:
        audience = "men"
    elif "women" in q:
        audience = "women"

    criteria = [name for name, kws in _CRITERIA_KEYWORDS.items() if any(kw.lower() in q for kw in kws)]
    if not criteria:
        # Recommendation-shaped queries reasonably imply these baseline criteria even
        # if not spelled out -- but only for queries that are actually asking for one.
        if intent in (
            QueryIntent.LOCAL_RECOMMENDATION, QueryIntent.PERSONAL_TRAINER_RECOMMENDATION,
            QueryIntent.SERVICE_RECOMMENDATION, QueryIntent.EXECUTIVE_HEALTH, QueryIntent.CORRECTIVE_EXERCISE,
        ):
            criteria = ["expertise", "location", "evidence"]

    return QueryEntities(
        profession=profession, location=location, audience=audience,
        intent=intent, cluster=cluster, decision_criteria=criteria,
    )
