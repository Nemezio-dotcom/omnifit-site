from app.audit.base import RawFinding
from app.models.core import Site
from app.models.enums import FindingCategory as Cat
from app.models.enums import OpportunityStatus, Severity as Sev
from app.opportunities.engine import generate_opportunity_drafts
from app.opportunities.service import sync_opportunities


def _finding(code, url, severity=Sev.HIGH):
    return RawFinding(
        code=code, category=Cat.SEO, severity=severity, explanation="x", recommended_action="y",
        estimated_effort=2, estimated_impact=6, confidence=7, affected_url=url,
    )


def test_generate_opportunity_drafts_groups_by_code_and_sorts_by_priority():
    findings = [
        _finding("MISSING_TITLE", "https://a.com/1"),
        _finding("MISSING_TITLE", "https://a.com/2"),
        _finding("MISSING_H1", "https://a.com/3", severity=Sev.LOW),
    ]
    drafts = generate_opportunity_drafts(findings)
    codes = {d.source_finding_codes[0] for d in drafts}
    assert codes == {"MISSING_TITLE", "MISSING_H1"}
    title_draft = next(d for d in drafts if d.source_finding_codes == ["MISSING_TITLE"])
    assert len(title_draft.affected_pages) == 2
    assert drafts == sorted(drafts, key=lambda d: d.priority_score, reverse=True)


def test_info_findings_produce_no_opportunity():
    findings = [_finding("NOINDEX_PAGE", "https://a.com/1", severity=Sev.INFO)]
    assert generate_opportunity_drafts(findings) == []


def test_sync_creates_new_opportunity(db_session):
    site = Site(name="Test", base_url="https://a.com/")
    db_session.add(site)
    db_session.commit()

    drafts = generate_opportunity_drafts([_finding("MISSING_TITLE", "https://a.com/1")])
    opps = sync_opportunities(db_session, site, drafts)
    assert len(opps) == 1
    assert opps[0].status == OpportunityStatus.OPEN


def test_sync_marks_resolved_issue_as_fixed(db_session):
    site = Site(name="Test", base_url="https://a.com/")
    db_session.add(site)
    db_session.commit()

    drafts = generate_opportunity_drafts([_finding("MISSING_TITLE", "https://a.com/1")])
    sync_opportunities(db_session, site, drafts)

    # Second scan: the finding no longer occurs.
    opps = sync_opportunities(db_session, site, [])
    assert len(opps) == 1
    assert opps[0].status == OpportunityStatus.FIXED


def test_sync_reopens_regressed_issue(db_session):
    site = Site(name="Test", base_url="https://a.com/")
    db_session.add(site)
    db_session.commit()

    drafts = generate_opportunity_drafts([_finding("MISSING_TITLE", "https://a.com/1")])
    sync_opportunities(db_session, site, drafts)
    sync_opportunities(db_session, site, [])  # now fixed

    opps = sync_opportunities(db_session, site, drafts)  # issue reappears
    assert opps[0].status == OpportunityStatus.OPEN
    assert "Regressed" in (opps[0].notes or "")


def test_sync_keeps_ignored_status(db_session):
    site = Site(name="Test", base_url="https://a.com/")
    db_session.add(site)
    db_session.commit()

    drafts = generate_opportunity_drafts([_finding("MISSING_TITLE", "https://a.com/1")])
    opps = sync_opportunities(db_session, site, drafts)
    opps[0].status = OpportunityStatus.IGNORED
    db_session.commit()

    opps_again = sync_opportunities(db_session, site, drafts)
    assert opps_again[0].status == OpportunityStatus.IGNORED
