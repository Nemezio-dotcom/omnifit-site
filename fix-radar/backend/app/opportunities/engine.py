from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from app.audit.base import RawFinding, clamp, group_by_code
from app.models.enums import FindingCategory, Severity

SEVERITY_ORDER = [Severity.INFO, Severity.LOW, Severity.MEDIUM, Severity.HIGH, Severity.CRITICAL]

TITLE_TEMPLATES: dict[str, str] = {
    "SERVER_ERROR": "Fix server errors on {count} page(s)",
    "CLIENT_ERROR": "Fix broken (4xx) URLs on {count} page(s)",
    "BROKEN_INTERNAL_LINK": "Repair {count} broken internal link(s)",
    "BROKEN_EXTERNAL_LINK": "Clean up {count} broken external link(s)",
    "REDIRECT_CHAIN": "Flatten redirect chains on {count} page(s)",
    "MISSING_TITLE": "Add title tags to {count} page(s) missing one",
    "DUPLICATE_TITLE": "Differentiate duplicate titles across {count} page(s)",
    "TITLE_LENGTH": "Tighten title length on {count} page(s)",
    "MISSING_META_DESCRIPTION": "Write meta descriptions for {count} page(s)",
    "DUPLICATE_META_DESCRIPTION": "Differentiate duplicate meta descriptions on {count} page(s)",
    "META_LENGTH": "Adjust meta description length on {count} page(s)",
    "MISSING_H1": "Add a clear H1 to {count} page(s)",
    "MULTIPLE_H1": "Consolidate multiple H1s on {count} page(s)",
    "THIN_CONTENT": "Expand thin content on {count} page(s)",
    "MISSING_ALT_TEXT": "Add image alt text on {count} page(s)",
    "ORPHAN_PAGE": "Link to {count} orphaned page(s) from elsewhere on the site",
    "POOR_INTERNAL_LINKING": "Strengthen internal linking to {count} under-linked page(s)",
    "MISSING_CANONICAL": "Add canonical tags to {count} page(s)",
    "NOINDEX_PAGE": "Confirm noindex is intentional on {count} page(s)",
    "NO_SITEMAP": "Publish an XML sitemap",
    "SLOW_RESPONSE": "Improve response time on {count} slow page(s)",
    "NO_STRUCTURED_DATA": "Add core structured data (LocalBusiness/Organization) site-wide",
    "MISSING_LOCATION_SIGNAL": "Strengthen San Diego / service-area signals across the site",
    "WEAK_EXPERTISE_SIGNALS": "Make trainer expertise and methodology explicit on the site",
    "WEAK_EVIDENCE": "Publish real client evidence (case studies, testimonials, outcomes)",
    "WEAK_TRUST_SIGNALS": "Surface clear contact and trust information",
    "MISSING_LOCALBUSINESS_SCHEMA": "Add LocalBusiness/Organization schema",
    "NO_FAQ_SCHEMA": "Add FAQPage schema to existing FAQ content on {count} page(s)",
    "LOW_ANSWERABILITY": "Improve answerability (who/what/where/why/how) on {count} page(s)",
    "WEAK_CONVERSION_CTA": "Add a clear call-to-action on {count} page(s)",
}

EXPECTED_BENEFIT_BY_CATEGORY = {
    FindingCategory.TECHNICAL: "More reliable crawling and indexing of the site.",
    FindingCategory.SEO: "Clearer, more differentiated search snippets and rankings.",
    FindingCategory.LOCAL: "Stronger association between OmniFit and its actual service area in search and AI answers.",
    FindingCategory.AIO: "Higher odds an AI system can understand and confidently reference this content.",
    FindingCategory.AUTHORITY: "Stronger perceived expertise and trustworthiness to prospects, search engines, and AI systems.",
    FindingCategory.CONTENT: "More substantive pages that can actually rank and be cited.",
    FindingCategory.INTERNAL_LINKING: "Better discovery and authority flow across the site.",
    FindingCategory.CONVERSION: "More visitors who are ready to act actually converting.",
    FindingCategory.TRUST: "Higher visitor and AI-system confidence that OmniFit is a legitimate, reachable business.",
    FindingCategory.STRUCTURED_DATA: "Machine-readable clarity for search engines and AI systems about what OmniFit is and offers.",
}

# Rough effort-to-minutes mapping for a solo operator making the fix themselves.
EFFORT_MINUTES = {1: 15, 2: 30, 3: 45, 4: 75, 5: 120, 6: 180, 7: 300, 8: 480, 9: 720, 10: 960}


@dataclass
class OpportunityDraft:
    title: str
    category: FindingCategory
    affected_pages: list[str]
    severity: Severity
    impact_score: float
    confidence_score: float
    effort_score: float
    priority_score: float
    explanation: str
    evidence: str
    recommended_fix: str
    expected_benefit: str
    implementation_notes: str | None
    estimated_minutes: int
    source_finding_codes: list[str]
    fingerprint: str


def _max_severity(findings: list[RawFinding]) -> Severity:
    return max((f.severity for f in findings), key=lambda s: SEVERITY_ORDER.index(s))


def priority_score(impact: float, confidence: float, effort: float) -> float:
    """priority = impact * confidence * (11 - effort), normalized to 0-100.

    This is a HEURISTIC ranking score, not an objective measurement -- it exists
    to order opportunities, not to claim a precise ROI figure.
    """
    raw = impact * confidence * (11 - effort)
    max_raw = 10 * 10 * 10
    return round(clamp(raw / max_raw * 100), 1)


def generate_opportunity_drafts(findings: list[RawFinding]) -> list[OpportunityDraft]:
    drafts: list[OpportunityDraft] = []
    for code, group in group_by_code(findings).items():
        if group[0].severity == Severity.INFO:
            continue  # informational only, not an actionable opportunity

        affected = sorted({f.affected_url for f in group if f.affected_url})
        count = len(affected) or len(group)
        title_tmpl = TITLE_TEMPLATES.get(code, group[0].explanation[:80])
        title = title_tmpl.format(count=count)

        impact = round(sum(f.estimated_impact for f in group) / len(group), 1)
        confidence = round(sum(f.confidence for f in group) / len(group), 1)
        effort = round(sum(f.estimated_effort for f in group) / len(group), 1)
        # A systemic issue touching many pages costs more effort in aggregate than one instance.
        if count > 1:
            effort = min(10.0, effort + min(3.0, (count - 1) * 0.3))

        severity = _max_severity(group)
        priority = priority_score(impact, confidence, effort)

        explanations = list(dict.fromkeys(f.explanation for f in group))
        evidence_lines = [f"{f.affected_url or 'site-wide'}: {f.evidence}" for f in group[:5] if f.evidence]
        recommended = list(dict.fromkeys(f.recommended_action for f in group))[0]

        fingerprint = hashlib.sha256(code.encode()).hexdigest()[:32]

        drafts.append(
            OpportunityDraft(
                title=title,
                category=group[0].category,
                affected_pages=affected,
                severity=severity,
                impact_score=impact,
                confidence_score=confidence,
                effort_score=effort,
                priority_score=priority,
                explanation=" ".join(explanations[:2]),
                evidence="\n".join(evidence_lines) if evidence_lines else "See affected pages.",
                recommended_fix=recommended,
                expected_benefit=EXPECTED_BENEFIT_BY_CATEGORY.get(group[0].category, "Improved site quality."),
                implementation_notes=None,
                estimated_minutes=EFFORT_MINUTES.get(round(effort), 60),
                source_finding_codes=[code],
                fingerprint=fingerprint,
            )
        )

    drafts.sort(key=lambda d: d.priority_score, reverse=True)
    return drafts
