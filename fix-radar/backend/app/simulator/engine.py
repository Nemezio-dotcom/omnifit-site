from __future__ import annotations

from sqlalchemy.orm import Session

from app.audit.aio import analyze_page
from app.models.core import Page, Scan, Site
from app.models.simulator import SimulatorQuery, SimulatorRun
from app.simulator.answer import build_evidence_gaps, build_page_support, build_simulated_answer, would_recommend
from app.simulator.evidence import build_evidence_map
from app.simulator.query_analysis import extract_entities
from app.simulator.scoring import compute_sub_scores, overall_readiness


def _latest_scan(db: Session, site_id: int) -> Scan | None:
    return (
        db.query(Scan)
        .filter(Scan.site_id == site_id, Scan.status == "COMPLETE")
        .order_by(Scan.finished_at.desc())
        .first()
    )


def run_simulation(db: Session, site: Site, query_text: str, *, query_id: int | None = None) -> SimulatorRun:
    scan = _latest_scan(db, site.id)
    if not scan:
        raise ValueError("Run a scan before using the AI Recommendation Simulator.")

    pages = db.query(Page).filter(Page.scan_id == scan.id, Page.status_code < 400).all()
    entities = extract_entities(query_text)
    evidence_items = build_evidence_map(entities, pages)

    trust_scores = [p.trust_score for p in pages if p.trust_score is not None]
    avg_trust = sum(trust_scores) / len(trust_scores) if trust_scores else 30.0

    completeness_vals = []
    for p in pages[:60]:  # cap re-analysis cost; page-level profiles aren't persisted separately
        if not p.text_content:
            continue
        from app.crawler.crawler import CrawledPage

        proxy = CrawledPage(
            url=p.url, normalized_url=p.normalized_url, status_code=p.status_code or 200,
            response_time_ms=0, content_type="text/html", final_url=p.url, redirect_chain=[], depth=0,
            title=p.title, h1=p.h1 or [], h2=p.h2 or [], h3=p.h3 or [], word_count=p.word_count or 0,
            text_content=p.text_content, json_ld=p.json_ld or [],
        )
        completeness_vals.append(analyze_page(proxy).semantic_completeness)
    avg_completeness = sum(completeness_vals) / len(completeness_vals) if completeness_vals else 4.0

    sub_scores = compute_sub_scores(evidence_items, avg_trust, avg_completeness)
    readiness = overall_readiness(sub_scores)
    recommend = would_recommend(readiness, evidence_items)
    answer_text, evidence_used = build_simulated_answer(query_text, entities, evidence_items, recommend)
    page_support = build_page_support(pages, entities)
    gaps = build_evidence_gaps(evidence_items)

    from app.models.enums import EvidenceStrength

    strongest = [
        f"{i.requirement}: {i.strength}" for i in evidence_items
        if i.strength in (EvidenceStrength.STRONG.value, EvidenceStrength.VERY_STRONG.value)
    ][:5]
    weakest = [
        f"{i.requirement}: {i.strength}" for i in evidence_items
        if i.strength in (EvidenceStrength.WEAK.value, EvidenceStrength.MISSING.value)
    ][:5]

    if query_id is None:
        saved = SimulatorQuery(site_id=site.id, query_text=query_text, intent=entities.intent.value, cluster=entities.cluster.value)
        db.add(saved)
        db.commit()
        db.refresh(saved)
        query_id = saved.id

    run = SimulatorRun(
        query_id=query_id,
        scan_id=scan.id,
        readiness_score=readiness,
        sub_scores=sub_scores,
        entities={
            "profession": entities.profession, "location": entities.location, "audience": entities.audience,
            "intent": entities.intent.value, "cluster": entities.cluster.value, "decision_criteria": entities.decision_criteria,
        },
        evidence_map=[i.__dict__ for i in evidence_items],
        strongest_evidence=strongest,
        weakest_evidence=weakest,
        would_recommend=recommend,
        simulated_answer=answer_text,
        evidence_used=evidence_used,
        page_support=page_support,
        evidence_gaps=gaps,
        generated_by="heuristic",
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def run_saved_query(db: Session, site: Site, saved_query: SimulatorQuery) -> SimulatorRun:
    return run_simulation(db, site, saved_query.query_text, query_id=saved_query.id)


def run_all_saved_queries(db: Session, site: Site) -> list[SimulatorRun]:
    queries = db.query(SimulatorQuery).filter(SimulatorQuery.site_id == site.id).all()
    return [run_saved_query(db, site, q) for q in queries]
