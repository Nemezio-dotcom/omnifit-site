from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.export.generator import executive_pdf, full_export_json, opportunities_to_csv
from app.models.core import Site

router = APIRouter(prefix="/api/sites/{site_id}/export", tags=["export"])


def _get_site_or_404(db: Session, site_id: int) -> Site:
    site = db.query(Site).get(site_id)
    if not site:
        raise HTTPException(404, "Site not found")
    return site


@router.get("/csv")
def export_csv(site_id: int, db: Session = Depends(get_db)):
    site = _get_site_or_404(db, site_id)
    csv_text = opportunities_to_csv(db, site)
    return Response(csv_text, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=opportunities.csv"})


@router.get("/json")
def export_json(site_id: int, db: Session = Depends(get_db)):
    site = _get_site_or_404(db, site_id)
    return full_export_json(db, site)


@router.get("/pdf")
def export_pdf(site_id: int, db: Session = Depends(get_db)):
    site = _get_site_or_404(db, site_id)
    pdf_bytes = executive_pdf(db, site)
    return Response(pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=fix-radar-report.pdf"})
