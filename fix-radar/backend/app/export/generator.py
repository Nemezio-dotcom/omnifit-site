from __future__ import annotations

import csv
import io
import json

from sqlalchemy.orm import Session

from app.dashboard_service import build_dashboard
from app.models.core import Finding, Opportunity, Scan, Site
from app.models.enums import OpportunityStatus, Severity


def opportunities_to_csv(db: Session, site: Site) -> str:
    opps = db.query(Opportunity).filter(Opportunity.site_id == site.id).order_by(Opportunity.priority_score.desc()).all()
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([
        "id", "title", "category", "severity", "status", "priority_score", "impact_score",
        "confidence_score", "effort_score", "estimated_minutes", "affected_pages", "recommended_fix",
    ])
    for o in opps:
        writer.writerow([
            o.id, o.title, o.category, o.severity, o.status, o.priority_score, o.impact_score,
            o.confidence_score, o.effort_score, o.estimated_minutes, "; ".join(o.affected_pages or []), o.recommended_fix,
        ])
    return buf.getvalue()


def full_export_json(db: Session, site: Site) -> dict:
    latest_scan = (
        db.query(Scan).filter(Scan.site_id == site.id, Scan.status == "COMPLETE").order_by(Scan.finished_at.desc()).first()
    )
    opportunities = db.query(Opportunity).filter(Opportunity.site_id == site.id).order_by(Opportunity.priority_score.desc()).all()
    findings = db.query(Finding).filter(Finding.scan_id == latest_scan.id).all() if latest_scan else []

    return {
        "site": {"id": site.id, "name": site.name, "base_url": site.base_url},
        "latest_scan": {
            "id": latest_scan.id, "finished_at": latest_scan.finished_at.isoformat() if latest_scan.finished_at else None,
            "source": latest_scan.source, "pages_crawled": latest_scan.pages_crawled,
            "overall_score": latest_scan.overall_score, "technical_score": latest_scan.technical_score,
            "seo_score": latest_scan.seo_score, "local_score": latest_scan.local_score,
            "aio_score": latest_scan.aio_score, "authority_score": latest_scan.authority_score,
            "conversion_score": latest_scan.conversion_score,
        } if latest_scan else None,
        "opportunities": [
            {
                "id": o.id, "title": o.title, "category": o.category, "severity": o.severity, "status": o.status,
                "priority_score": o.priority_score, "impact_score": o.impact_score, "confidence_score": o.confidence_score,
                "effort_score": o.effort_score, "affected_pages": o.affected_pages, "explanation": o.explanation,
                "recommended_fix": o.recommended_fix, "expected_benefit": o.expected_benefit,
            }
            for o in opportunities
        ],
        "findings_count": len(findings),
        "note": "All scores are heuristic 0-100 estimates produced by Fix Radar, not third-party measurements.",
    }


def executive_pdf(db: Session, site: Site) -> bytes:
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    dash = build_dashboard(db, site)
    styles = getSampleStyleSheet()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=LETTER, topMargin=0.6 * inch, bottomMargin=0.6 * inch)
    story = [
        Paragraph(f"{site.name} -- Fix Radar Executive Report", styles["Title"]),
        Spacer(1, 8),
    ]

    scan = dash["latest_scan"]
    if scan:
        story.append(Paragraph(f"Overall score: {scan.overall_score}/100 (heuristic)", styles["Heading2"]))
        rows = [["Technical", "SEO", "Local", "AIO", "Authority", "Conversion"], [
            scan.technical_score, scan.seo_score, scan.local_score, scan.aio_score, scan.authority_score, scan.conversion_score,
        ]]
        story.append(Table(rows, style=TableStyle([("GRID", (0, 0), (-1, -1), 0.5, "#999999")])))
    else:
        story.append(Paragraph("No completed scan yet.", styles["Normal"]))

    story.append(Spacer(1, 16))
    story.append(Paragraph("Top priorities", styles["Heading2"]))
    for i, opp in enumerate(dash["fix_next"], start=1):
        story.append(Paragraph(f"{i}. {opp.title} (priority {opp.priority_score}/100, ~{opp.estimated_minutes} min)", styles["Normal"]))
        story.append(Paragraph(opp.explanation, styles["Normal"]))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Critical issues", styles["Heading2"]))
    critical = [o for o in db.query(Opportunity).filter(Opportunity.site_id == site.id, Opportunity.severity == Severity.CRITICAL.value).all()]
    if critical:
        for o in critical:
            story.append(Paragraph(f"- {o.title}", styles["Normal"]))
    else:
        story.append(Paragraph("None found.", styles["Normal"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("AIO opportunities", styles["Heading2"]))
    for o in dash["aio_opportunities"]:
        story.append(Paragraph(f"- {o.title}", styles["Normal"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Authority opportunities", styles["Heading2"]))
    for o in dash["authority_opportunities"]:
        story.append(Paragraph(f"- {o.title}", styles["Normal"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Recently fixed", styles["Heading2"]))
    if dash["recently_fixed"]:
        for o in dash["recently_fixed"]:
            story.append(Paragraph(f"- {o.title}", styles["Normal"]))
    else:
        story.append(Paragraph("None yet.", styles["Normal"]))

    doc.build(story)
    return buf.getvalue()
