from __future__ import annotations

import hashlib
from dataclasses import dataclass

from app.models.enums import FindingCategory, Severity

SEVERITY_WEIGHT = {
    Severity.CRITICAL: 20.0,
    Severity.HIGH: 10.0,
    Severity.MEDIUM: 5.0,
    Severity.LOW: 2.0,
    Severity.INFO: 0.0,
}


@dataclass
class RawFinding:
    code: str
    category: FindingCategory
    severity: Severity
    explanation: str
    recommended_action: str
    estimated_effort: int  # 1 (trivial) - 10 (major project)
    estimated_impact: float  # 0-10
    confidence: float  # 0-10
    affected_url: str | None = None
    evidence: str | None = None

    @property
    def fingerprint(self) -> str:
        raw = f"{self.code}:{self.affected_url or ''}"
        return hashlib.sha256(raw.encode()).hexdigest()[:32]


def clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


def group_by_code(findings: list[RawFinding]) -> dict[str, list[RawFinding]]:
    groups: dict[str, list[RawFinding]] = {}
    for f in findings:
        groups.setdefault(f.code, []).append(f)
    return groups


def score_from_findings(findings: list[RawFinding], total_pages: int) -> float:
    """Heuristic 0-100 score. NOT an objective measurement.

    Each distinct issue "code" costs its severity weight, scaled by how much
    of the site it touches (a single-page slip costs less than a site-wide
    pattern) so one thin page doesn't crater the score the way a systemic
    missing-canonical problem should.
    """
    total_pages = max(total_pages, 1)
    deduction = 0.0
    for code, group in group_by_code(findings).items():
        weight = SEVERITY_WEIGHT[group[0].severity]
        if weight == 0:
            continue
        affected_fraction = min(len(group) / total_pages, 1.0)
        code_deduction = weight * (0.4 + 0.6 * affected_fraction)
        deduction += min(code_deduction, weight * 3)
    return round(clamp(100 - deduction), 1)
