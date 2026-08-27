from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.core import Site
from app.models.simulator import SimulatorQuery, SimulatorRun
from app.opportunities.service import upsert_opportunities
from app.schemas.models import SavedQueryOut, SimulatorQueryIn, SimulatorRunOut
from app.simulator.clusters import cluster_readiness
from app.simulator.engine import run_all_saved_queries, run_saved_query, run_simulation
from app.simulator.systemic import detect_systemic_weaknesses

router = APIRouter(prefix="/api/sites/{site_id}/simulator", tags=["simulator"])

EXAMPLE_QUERIES = [
    "Who is the best personal trainer for executives in San Diego?",
    "What is the best personal trainer in Rancho Santa Fe?",
    "Who specializes in corrective exercise in San Diego?",
    "Who is a good personal trainer for men over 50 in San Diego?",
    "Who provides premium in-home personal training in La Jolla?",
    "Who provides executive health coaching in San Diego?",
    "What personal trainer combines strength training and nutrition coaching in San Diego?",
]


def _get_site_or_404(db: Session, site_id: int) -> Site:
    site = db.query(Site).get(site_id)
    if not site:
        raise HTTPException(404, "Site not found")
    return site


@router.get("/example-queries")
def example_queries():
    return EXAMPLE_QUERIES


@router.post("/run", response_model=SimulatorRunOut)
def run(site_id: int, payload: SimulatorQueryIn, db: Session = Depends(get_db)):
    site = _get_site_or_404(db, site_id)
    try:
        run_result = run_simulation(db, site, payload.query_text)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    _refresh_systemic_opportunities(db, site)
    return run_result


@router.get("/queries", response_model=list[SavedQueryOut])
def list_saved_queries(site_id: int, db: Session = Depends(get_db)):
    _get_site_or_404(db, site_id)
    queries = db.query(SimulatorQuery).filter(SimulatorQuery.site_id == site_id).order_by(SimulatorQuery.created_at.desc()).all()
    out = []
    for q in queries:
        runs = db.query(SimulatorRun).filter(SimulatorRun.query_id == q.id).order_by(SimulatorRun.created_at.desc()).limit(2).all()
        item = SavedQueryOut.model_validate(q)
        if runs:
            item.latest_run = SimulatorRunOut.model_validate(runs[0])
        if len(runs) > 1:
            item.previous_score = runs[1].readiness_score
        out.append(item)
    return out


@router.post("/run-all", response_model=list[SimulatorRunOut])
def run_all(site_id: int, db: Session = Depends(get_db)):
    site = _get_site_or_404(db, site_id)
    try:
        runs = run_all_saved_queries(db, site)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    _refresh_systemic_opportunities(db, site)
    return runs


@router.post("/queries/{query_id}/run", response_model=SimulatorRunOut)
def rerun_query(site_id: int, query_id: int, db: Session = Depends(get_db)):
    site = _get_site_or_404(db, site_id)
    q = db.query(SimulatorQuery).get(query_id)
    if not q or q.site_id != site_id:
        raise HTTPException(404, "Saved query not found")
    run_result = run_saved_query(db, site, q)
    _refresh_systemic_opportunities(db, site)
    return run_result


@router.delete("/queries/{query_id}")
def delete_saved_query(site_id: int, query_id: int, db: Session = Depends(get_db)):
    q = db.query(SimulatorQuery).get(query_id)
    if not q or q.site_id != site_id:
        raise HTTPException(404, "Saved query not found")
    db.delete(q)
    db.commit()
    return {"ok": True}


@router.get("/clusters")
def clusters(site_id: int, db: Session = Depends(get_db)):
    _get_site_or_404(db, site_id)
    return cluster_readiness(db, site_id)


def _refresh_systemic_opportunities(db: Session, site: Site) -> None:
    drafts = detect_systemic_weaknesses(db, site)
    if drafts:
        upsert_opportunities(db, site, drafts)
