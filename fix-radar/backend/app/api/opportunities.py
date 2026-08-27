from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.factory import get_ai_provider
from app.ai.provider import RecommendationInput
from app.business_context import business_context_summary
from app.database import get_db
from app.models.core import Opportunity, OFTask, Page, Recommendation
from app.models.enums import OpportunityStatus
from app.schemas.models import OpportunityOut, OpportunityPatch, RecommendationOut, TaskCreateIn, TaskOut

router = APIRouter(prefix="/api/opportunities", tags=["opportunities"])
tasks_router = APIRouter(prefix="/api/tasks", tags=["tasks"])


def _get_opportunity_or_404(db: Session, opportunity_id: int) -> Opportunity:
    opp = db.query(Opportunity).get(opportunity_id)
    if not opp:
        raise HTTPException(404, "Opportunity not found")
    return opp


@router.get("/{opportunity_id}", response_model=OpportunityOut)
def get_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    return _get_opportunity_or_404(db, opportunity_id)


@router.patch("/{opportunity_id}", response_model=OpportunityOut)
def patch_opportunity(opportunity_id: int, payload: OpportunityPatch, db: Session = Depends(get_db)):
    opp = _get_opportunity_or_404(db, opportunity_id)
    if payload.status is not None:
        if payload.status not in OpportunityStatus.__members__:
            raise HTTPException(400, f"Invalid status: {payload.status}")
        opp.status = OpportunityStatus[payload.status]
    if payload.notes is not None:
        opp.notes = payload.notes
    db.commit()
    db.refresh(opp)
    return opp


@router.get("/{opportunity_id}/recommendations", response_model=list[RecommendationOut])
def list_recommendations(opportunity_id: int, db: Session = Depends(get_db)):
    _get_opportunity_or_404(db, opportunity_id)
    return db.query(Recommendation).filter(Recommendation.opportunity_id == opportunity_id).order_by(Recommendation.created_at.desc()).all()


@router.post("/{opportunity_id}/generate-recommendation", response_model=RecommendationOut)
def generate_recommendation(opportunity_id: int, db: Session = Depends(get_db)):
    """Draft AI-assisted implementation assets for this opportunity. Never auto-published --
    this only creates a Recommendation row for a human to review and act on manually."""
    opp = _get_opportunity_or_404(db, opportunity_id)
    affected = opp.affected_pages or []
    sample_page = None
    if affected:
        sample_page = db.query(Page).filter(Page.url == affected[0]).order_by(Page.id.desc()).first()

    provider = get_ai_provider()
    rec_input = RecommendationInput(
        opportunity_title=opp.title,
        explanation=opp.explanation,
        recommended_fix=opp.recommended_fix,
        affected_pages=affected,
        page_title=sample_page.title if sample_page else None,
        page_text_excerpt=(sample_page.text_content or "") if sample_page else "",
        business_context=business_context_summary(),
    )
    assets = provider.generate_recommendation_assets(rec_input)

    rec = Recommendation(
        opportunity_id=opp.id,
        kind="implementation_draft",
        content=assets.model_dump(),
        generated_by=assets.generated_by,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


@tasks_router.post("", response_model=TaskOut)
def create_task(payload: TaskCreateIn, db: Session = Depends(get_db)):
    task = OFTask(title=payload.title, notes=payload.notes, opportunity_id=payload.opportunity_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@tasks_router.get("", response_model=list[TaskOut])
def list_tasks(opportunity_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(OFTask)
    if opportunity_id is not None:
        q = q.filter(OFTask.opportunity_id == opportunity_id)
    return q.order_by(OFTask.created_at.desc()).all()


@tasks_router.patch("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskCreateIn, db: Session = Depends(get_db)):
    task = db.query(OFTask).get(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    task.title = payload.title
    task.notes = payload.notes
    db.commit()
    db.refresh(task)
    return task
