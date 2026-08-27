from app.audit.base import RawFinding, score_from_findings
from app.models.enums import FindingCategory as Cat
from app.models.enums import Severity as Sev
from app.opportunities.engine import priority_score


def _finding(code, severity, url):
    return RawFinding(
        code=code, category=Cat.SEO, severity=severity, explanation="x", recommended_action="y",
        estimated_effort=1, estimated_impact=5, confidence=5, affected_url=url,
    )


def test_empty_findings_score_100():
    assert score_from_findings([], 10) == 100.0


def test_info_findings_dont_lower_score():
    findings = [_finding("X", Sev.INFO, "https://a.com/1")]
    assert score_from_findings(findings, 10) == 100.0


def test_critical_findings_lower_score_more_than_low():
    critical = [_finding("X", Sev.CRITICAL, "https://a.com/1")]
    low = [_finding("Y", Sev.LOW, "https://a.com/1")]
    assert score_from_findings(critical, 10) < score_from_findings(low, 10)


def test_widespread_issue_costs_more_than_single_page_issue():
    single = [_finding("X", Sev.MEDIUM, "https://a.com/1")]
    widespread = [_finding("X", Sev.MEDIUM, f"https://a.com/{i}") for i in range(10)]
    assert score_from_findings(widespread, 10) < score_from_findings(single, 10)


def test_score_never_below_zero():
    findings = [_finding("X", Sev.CRITICAL, f"https://a.com/{i}") for i in range(50)]
    assert score_from_findings(findings, 50) >= 0.0


def test_priority_score_bounds():
    assert priority_score(0, 0, 10) == 0.0
    assert priority_score(10, 10, 1) == 100.0


def test_priority_score_rewards_low_effort():
    high_effort = priority_score(8, 8, 9)
    low_effort = priority_score(8, 8, 2)
    assert low_effort > high_effort
