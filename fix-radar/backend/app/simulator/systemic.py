from __future__ import annotations

import hashlib

from sqlalchemy.orm import Session

from app.models.core import Site
from app.models.enums import FindingCategory, Severity
from app.models.simulator import SimulatorQuery, SimulatorRun
from app.opportunities.engine import OpportunityDraft, priority_score

MIN_QUERIES_FOR_SYSTEMIC = 3
WEAK_THRESHOLD = 55.0

DIMENSION_META = {
    "third_party_authority": (
        "Strengthen third-party authority",
        FindingCategory.AUTHORITY,
        "Seek legitimate third-party references, professional-association mentions, interviews, or reputable coverage. Never fake reviews or buy links.",
    ),
    "evidence": (
        "Publish stronger client evidence across the site",
        FindingCategory.AUTHORITY,
        "Add real, specific, honestly-reported case studies and outcomes.",
    ),
    "expertise": (
        "Make expertise and credentials more explicit site-wide",
        FindingCategory.AUTHORITY,
        "State real credentials and methodology depth on more pages.",
    ),
    "local_relevance": (
        "Strengthen local/service-area signals site-wide",
        FindingCategory.LOCAL,
        "Repeat explicit service-area language across more pages.",
    ),
    "content_completeness": (
        "Improve semantic completeness (who/what/where/why/how) across pages",
        FindingCategory.AIO,
        "Add short sections covering the commonly-missing dimensions identified per page.",
    ),
    "differentiation": (
        "Make what makes OmniFit different clearer site-wide",
        FindingCategory.AIO,
        "State the methodology and differentiators explicitly on more pages.",
    ),
}


def detect_systemic_weaknesses(db: Session, site: Site) -> list[OpportunityDraft]:
    """Look across ALL saved queries' latest runs for a sub-score that's
    consistently weak -- not a single-query problem but a pattern. Per the
    spec, this must feed into the main Fix Next ranking with a priority that
    reflects it being a systemic issue, not a one-off keyword problem.
    """
    queries = db.query(SimulatorQuery).filter(SimulatorQuery.site_id == site.id).all()
    latest_runs = []
    for q in queries:
        run = db.query(SimulatorRun).filter(SimulatorRun.query_id == q.id).order_by(SimulatorRun.created_at.desc()).first()
        if run:
            latest_runs.append(run)

    if len(latest_runs) < MIN_QUERIES_FOR_SYSTEMIC:
        return []

    drafts = []
    for dim, (title, category, fix) in DIMENSION_META.items():
        values = [r.sub_scores.get(dim) for r in latest_runs if r.sub_scores.get(dim) is not None]
        if not values:
            continue
        avg = sum(values) / len(values)
        weak_count = sum(1 for v in values if v < WEAK_THRESHOLD)
        if avg >= WEAK_THRESHOLD or weak_count < MIN_QUERIES_FOR_SYSTEMIC:
            continue

        impact = round(min(10.0, 5 + weak_count / len(latest_runs) * 5), 1)
        confidence = round(min(10.0, 4 + len(latest_runs) * 0.5), 1)
        effort = 6.0
        priority = priority_score(impact, confidence, effort)
        fingerprint = hashlib.sha256(f"SYSTEMIC_{dim.upper()}".encode()).hexdigest()[:32]

        drafts.append(
            OpportunityDraft(
                title=title,
                category=category,
                affected_pages=[],
                severity=Severity.HIGH if avg < 40 else Severity.MEDIUM,
                impact_score=impact,
                confidence_score=confidence,
                effort_score=effort,
                priority_score=priority,
                explanation=(
                    f"Across {len(latest_runs)} tested AI-recommendation queries, '{dim.replace('_', ' ')}' "
                    f"averaged {avg:.0f}/100 and was weak in {weak_count} of them -- this is a pattern across "
                    "many different query types, not an isolated keyword gap."
                ),
                evidence=f"Weak in {weak_count}/{len(latest_runs)} saved queries (avg {avg:.0f}/100).",
                recommended_fix=fix,
                expected_benefit="Improves AI recommendation readiness across many query types at once, not just one page.",
                implementation_notes=None,
                estimated_minutes=240,
                source_finding_codes=[f"SYSTEMIC_{dim.upper()}"],
                fingerprint=fingerprint,
            )
        )
    return drafts
