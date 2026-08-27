from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.factory import get_ai_provider
from app.ai.provider import PageInput
from app.ai.schemas import PageAIAnalysis
from app.business_context import business_context_summary
from app.crawler.normalize import normalize_url
from app.dashboard_service import build_dashboard
from app.database import get_db
from app.fixture_server import LOCAL_FIXTURE_URL, ensure_fixture_server_running
from app.models.core import Finding, Opportunity, Page, Scan, Site
from app.scan_service import run_scan, run_scan_for_local_fixture
from app.schemas.models import (
    DashboardOut, FindingOut, OpportunityOut, PageDetail, PageListItem, ScanOut, ScanRequest, SiteCreate, SiteOut,
)

router = APIRouter(prefix="/api/sites", tags=["sites"])


@router.post("", response_model=SiteOut)
def create_site(payload: SiteCreate, db: Session = Depends(get_db)):
    site = Site(name=payload.name, base_url=normalize_url(payload.base_url))
    db.add(site)
    db.commit()
    db.refresh(site)
    return site


@router.get("", response_model=list[SiteOut])
def list_sites(db: Session = Depends(get_db)):
    return db.query(Site).order_by(Site.id).all()


def _get_site_or_404(db: Session, site_id: int) -> Site:
    site = db.query(Site).get(site_id)
    if not site:
        raise HTTPException(404, "Site not found")
    return site


@router.post("/{site_id}/scan", response_model=ScanOut)
def trigger_scan(site_id: int, payload: ScanRequest = ScanRequest(), db: Session = Depends(get_db)):
    site = _get_site_or_404(db, site_id)
    if payload.use_local_fixture:
        ensure_fixture_server_running()
        scan = run_scan_for_local_fixture(
            db, site, LOCAL_FIXTURE_URL, max_pages=payload.max_pages, max_depth=payload.max_depth
        )
    else:
        try:
            scan = run_scan(db, site, max_pages=payload.max_pages, max_depth=payload.max_depth)
        except Exception as exc:
            raise HTTPException(502, f"Scan failed: {exc}") from exc
    return scan


@router.get("/{site_id}/scans", response_model=list[ScanOut])
def list_scans(site_id: int, db: Session = Depends(get_db)):
    _get_site_or_404(db, site_id)
    return db.query(Scan).filter(Scan.site_id == site_id).order_by(Scan.started_at.desc()).all()


@router.get("/{site_id}/dashboard", response_model=DashboardOut)
def dashboard(site_id: int, db: Session = Depends(get_db)):
    site = _get_site_or_404(db, site_id)
    return build_dashboard(db, site)


def _latest_scan_id(db: Session, site_id: int) -> int | None:
    scan = (
        db.query(Scan)
        .filter(Scan.site_id == site_id, Scan.status == "COMPLETE")
        .order_by(Scan.finished_at.desc())
        .first()
    )
    return scan.id if scan else None


@router.get("/{site_id}/pages", response_model=list[PageListItem])
def list_pages(site_id: int, scan_id: int | None = None, db: Session = Depends(get_db)):
    _get_site_or_404(db, site_id)
    sid = scan_id or _latest_scan_id(db, site_id)
    if not sid:
        return []
    return db.query(Page).filter(Page.scan_id == sid).order_by(Page.url).all()


@router.get("/{site_id}/pages/{page_id}", response_model=PageDetail)
def get_page(site_id: int, page_id: int, db: Session = Depends(get_db)):
    _get_site_or_404(db, site_id)
    page = db.query(Page).get(page_id)
    if not page:
        raise HTTPException(404, "Page not found")
    return page


@router.post("/{site_id}/pages/{page_id}/analyze", response_model=PageAIAnalysis)
def analyze_page(site_id: int, page_id: int, db: Session = Depends(get_db)):
    """Ephemeral, on-demand AI semantic review for one page (not persisted --
    re-run any time). Uses the configured AI provider, or the heuristic
    fallback when no OpenAI key is set."""
    _get_site_or_404(db, site_id)
    page = db.query(Page).get(page_id)
    if not page:
        raise HTTPException(404, "Page not found")
    provider = get_ai_provider()
    return provider.analyze_page(
        PageInput(
            url=page.url,
            title=page.title,
            meta_description=page.meta_description,
            h1=page.h1 or [],
            h2=page.h2 or [],
            text_content=page.text_content or "",
            business_context=business_context_summary(),
        )
    )


@router.get("/{site_id}/findings", response_model=list[FindingOut])
def list_findings(site_id: int, scan_id: int | None = None, db: Session = Depends(get_db)):
    _get_site_or_404(db, site_id)
    sid = scan_id or _latest_scan_id(db, site_id)
    if not sid:
        return []
    return db.query(Finding).filter(Finding.scan_id == sid).order_by(Finding.severity).all()


@router.get("/{site_id}/opportunities", response_model=list[OpportunityOut])
def list_opportunities(site_id: int, status: str | None = None, db: Session = Depends(get_db)):
    _get_site_or_404(db, site_id)
    q = db.query(Opportunity).filter(Opportunity.site_id == site_id)
    if status:
        q = q.filter(Opportunity.status == status)
    return q.order_by(Opportunity.priority_score.desc()).all()


@router.get("/{site_id}/opportunities/top", response_model=list[OpportunityOut])
def top_opportunities(site_id: int, limit: int = 3, db: Session = Depends(get_db)):
    _get_site_or_404(db, site_id)
    from app.opportunities.service import top_fix_next

    return top_fix_next(db, site_id, limit=limit)
