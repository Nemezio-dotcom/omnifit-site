from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.competitors.engine import compute_gap_analysis, crawl_competitor
from app.database import get_db
from app.models.competitors import Competitor
from app.models.core import Site
from app.schemas.models import CompetitorCreate, CompetitorGapOut, CompetitorOut

router = APIRouter(prefix="/api/competitors", tags=["competitors"])


@router.post("", response_model=CompetitorOut)
def create_competitor(payload: CompetitorCreate, db: Session = Depends(get_db)):
    if not db.query(Site).get(payload.site_id):
        raise HTTPException(404, "Site not found")
    competitor = Competitor(site_id=payload.site_id, name=payload.name, base_url=payload.base_url)
    db.add(competitor)
    db.commit()
    db.refresh(competitor)
    return competitor


@router.get("", response_model=list[CompetitorOut])
def list_competitors(site_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(Competitor)
    if site_id is not None:
        q = q.filter(Competitor.site_id == site_id)
    return q.order_by(Competitor.id).all()


@router.post("/{competitor_id}/crawl", response_model=CompetitorOut)
def crawl(competitor_id: int, db: Session = Depends(get_db)):
    competitor = db.query(Competitor).get(competitor_id)
    if not competitor:
        raise HTTPException(404, "Competitor not found")
    try:
        crawl_competitor(db, competitor)
    except ValueError as exc:
        raise HTTPException(502, str(exc)) from exc
    db.refresh(competitor)
    return competitor


@router.delete("/{competitor_id}")
def delete_competitor(competitor_id: int, db: Session = Depends(get_db)):
    competitor = db.query(Competitor).get(competitor_id)
    if not competitor:
        raise HTTPException(404, "Competitor not found")
    db.delete(competitor)
    db.commit()
    return {"ok": True}


@router.get("/gap-analysis/{site_id}", response_model=CompetitorGapOut)
def gap_analysis(site_id: int, db: Session = Depends(get_db)):
    site = db.query(Site).get(site_id)
    if not site:
        raise HTTPException(404, "Site not found")
    return compute_gap_analysis(db, site)
