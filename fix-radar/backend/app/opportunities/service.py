from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.core import Opportunity, Site
from app.models.enums import OpportunityStatus
from app.opportunities.engine import OpportunityDraft


def sync_opportunities(db: Session, site: Site, drafts: list[OpportunityDraft]) -> list[Opportunity]:
    """Reconcile freshly-generated opportunity drafts against the persisted table.

    - New issue -> new OPEN Opportunity.
    - Issue still present, previously OPEN/IN_PROGRESS -> refresh its data, keep status.
    - Issue still present, previously IGNORED -> refresh data, keep IGNORED (stays out of Fix Next).
    - Issue still present, previously FIXED -> it regressed. Reopen it and note the regression.
    - Issue no longer present, previously OPEN/IN_PROGRESS -> mark FIXED (rescan-verified).
    - Issue no longer present, previously FIXED/IGNORED -> leave as-is.

    A score should never improve just because an issue was ignored; IGNORED
    opportunities are excluded from priority ranking, not deleted, and their
    underlying findings still count against the health scores each scan.
    """
    existing = {o.fingerprint: o for o in db.query(Opportunity).filter(Opportunity.site_id == site.id).all()}
    draft_fingerprints = {d.fingerprint for d in drafts}

    for draft in drafts:
        current = existing.get(draft.fingerprint)
        if current is None:
            current = Opportunity(site_id=site.id, fingerprint=draft.fingerprint, status=OpportunityStatus.OPEN)
            db.add(current)
        elif current.status == OpportunityStatus.FIXED:
            note = f"Regressed: this issue reappeared on the latest scan after previously being marked fixed."
            current.notes = f"{current.notes}\n{note}" if current.notes else note
            current.status = OpportunityStatus.OPEN

        current.title = draft.title
        current.category = draft.category
        current.affected_pages = draft.affected_pages
        current.severity = draft.severity
        current.impact_score = draft.impact_score
        current.confidence_score = draft.confidence_score
        current.effort_score = draft.effort_score
        current.priority_score = draft.priority_score
        current.explanation = draft.explanation
        current.evidence = draft.evidence
        current.recommended_fix = draft.recommended_fix
        current.expected_benefit = draft.expected_benefit
        current.estimated_minutes = draft.estimated_minutes
        current.source_finding_codes = draft.source_finding_codes

    for fingerprint, opp in existing.items():
        if fingerprint not in draft_fingerprints and opp.status in (OpportunityStatus.OPEN, OpportunityStatus.IN_PROGRESS):
            opp.status = OpportunityStatus.FIXED

    db.commit()
    return db.query(Opportunity).filter(Opportunity.site_id == site.id).all()


def upsert_opportunities(db: Session, site: Site, drafts: list[OpportunityDraft]) -> list[Opportunity]:
    """Like sync_opportunities, but only touches the given drafts' fingerprints --
    it never marks unrelated existing opportunities as FIXED. Used for opportunities
    that come from a source other than the main scan (e.g. the AI Recommendation
    Simulator's systemic-weakness detector), which only ever sees a subset of issues
    and must not be treated as the full current-state list."""
    existing = {
        o.fingerprint: o
        for o in db.query(Opportunity)
        .filter(Opportunity.site_id == site.id, Opportunity.fingerprint.in_([d.fingerprint for d in drafts]))
        .all()
    }
    for draft in drafts:
        current = existing.get(draft.fingerprint)
        if current is None:
            current = Opportunity(site_id=site.id, fingerprint=draft.fingerprint, status=OpportunityStatus.OPEN)
            db.add(current)
        elif current.status == OpportunityStatus.FIXED:
            note = "Regressed: this issue reappeared after previously being marked fixed."
            current.notes = f"{current.notes}\n{note}" if current.notes else note
            current.status = OpportunityStatus.OPEN

        current.title = draft.title
        current.category = draft.category
        current.affected_pages = draft.affected_pages
        current.severity = draft.severity
        current.impact_score = draft.impact_score
        current.confidence_score = draft.confidence_score
        current.effort_score = draft.effort_score
        current.priority_score = draft.priority_score
        current.explanation = draft.explanation
        current.evidence = draft.evidence
        current.recommended_fix = draft.recommended_fix
        current.expected_benefit = draft.expected_benefit
        current.estimated_minutes = draft.estimated_minutes
        current.source_finding_codes = draft.source_finding_codes

    db.commit()
    return list(existing.values())


def top_fix_next(db: Session, site_id: int, limit: int = 3) -> list[Opportunity]:
    return (
        db.query(Opportunity)
        .filter(Opportunity.site_id == site_id, Opportunity.status == OpportunityStatus.OPEN)
        .order_by(Opportunity.priority_score.desc())
        .limit(limit)
        .all()
    )
