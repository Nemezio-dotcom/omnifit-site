from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.simulator import SimulatorQuery, SimulatorRun


def _latest_run(db: Session, query_id: int) -> SimulatorRun | None:
    return db.query(SimulatorRun).filter(SimulatorRun.query_id == query_id).order_by(SimulatorRun.created_at.desc()).first()


def cluster_readiness(db: Session, site_id: int) -> dict:
    queries = db.query(SimulatorQuery).filter(SimulatorQuery.site_id == site_id).all()
    by_cluster: dict[str, list[float]] = {}
    gap_counter: dict[str, dict[str, int]] = {}

    for q in queries:
        run = _latest_run(db, q.id)
        if not run:
            continue
        cluster = q.cluster or "GENERAL"
        by_cluster.setdefault(cluster, []).append(run.readiness_score)
        for gap in run.evidence_gaps or []:
            gap_counter.setdefault(cluster, {})
            key = gap.get("gap", "unknown")
            gap_counter[cluster][key] = gap_counter[cluster].get(key, 0) + 1

    cluster_scores = {c: round(sum(scores) / len(scores), 1) for c, scores in by_cluster.items() if scores}
    if not cluster_scores:
        return {"clusters": {}, "strongest_cluster": None, "weakest_cluster": None, "biggest_opportunity": None, "queries_tested": 0}

    strongest = max(cluster_scores, key=cluster_scores.get)
    weakest = min(cluster_scores, key=cluster_scores.get)

    biggest_opportunity = None
    if gap_counter.get(weakest):
        top_gap = max(gap_counter[weakest], key=gap_counter[weakest].get)
        biggest_opportunity = f"{weakest}: {top_gap} (appears across {gap_counter[weakest][top_gap]} quer{'y' if gap_counter[weakest][top_gap]==1 else 'ies'})"

    return {
        "clusters": cluster_scores,
        "strongest_cluster": strongest,
        "weakest_cluster": weakest,
        "biggest_opportunity": biggest_opportunity,
        "queries_tested": len(queries),
    }
