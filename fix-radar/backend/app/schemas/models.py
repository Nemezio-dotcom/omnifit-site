from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SiteCreate(BaseModel):
    name: str
    base_url: str


class SiteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    base_url: str
    created_at: datetime


class ScanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    site_id: int
    started_at: datetime
    finished_at: Optional[datetime]
    status: str
    source: str
    pages_crawled: int
    error: Optional[str]
    technical_score: Optional[float]
    seo_score: Optional[float]
    local_score: Optional[float]
    aio_score: Optional[float]
    authority_score: Optional[float]
    conversion_score: Optional[float]
    overall_score: Optional[float]


class ScanRequest(BaseModel):
    max_pages: Optional[int] = None
    max_depth: Optional[int] = None
    use_local_fixture: bool = Field(
        default=False,
        description="Crawl the repo's own local fixture server instead of the live base_url. "
        "Only meaningful when the environment cannot reach the live site.",
    )


class PageListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    url: str
    status_code: Optional[int]
    title: Optional[str]
    word_count: Optional[int]
    is_orphan: bool
    is_indexable: Optional[bool]
    technical_score: Optional[float]
    seo_score: Optional[float]
    aio_score: Optional[float]
    local_score: Optional[float]
    trust_score: Optional[float]
    conversion_score: Optional[float]


class PageDetail(PageListItem):
    meta_description: Optional[str]
    canonical: Optional[str]
    h1: Optional[list]
    h2: Optional[list]
    h3: Optional[list]
    internal_links: Optional[list]
    external_links: Optional[list]
    images: Optional[list]
    json_ld: Optional[list]
    open_graph: Optional[dict]
    robots_meta: Optional[str]
    in_sitemap: Optional[bool]
    inbound_internal_link_count: int
    response_time_ms: Optional[float]
    redirect_chain: Optional[list]
    final_url: Optional[str]


class FindingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str
    category: str
    severity: str
    affected_url: Optional[str]
    evidence: Optional[str]
    explanation: str
    recommended_action: str
    estimated_effort: int
    estimated_impact: float
    confidence: float


class OpportunityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    site_id: int
    title: str
    category: str
    affected_pages: Optional[list]
    severity: str
    impact_score: float
    confidence_score: float
    effort_score: float
    priority_score: float
    explanation: str
    evidence: Optional[str]
    recommended_fix: str
    expected_benefit: Optional[str]
    implementation_notes: Optional[str]
    estimated_minutes: Optional[int]
    status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime


class OpportunityPatch(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None


class DashboardOut(BaseModel):
    site: SiteOut
    latest_scan: Optional[ScanOut]
    fix_next: list[OpportunityOut]
    biggest_strength: Optional[str]
    biggest_weakness: Optional[str]
    recently_fixed: list[OpportunityOut]
    site_health: dict
    aio_opportunities: list[OpportunityOut]
    authority_opportunities: list[OpportunityOut]
    competitor_gaps: list[str]
    simulator_summary: Optional[dict]
    score_trend: list[dict]
    network_notice: Optional[str] = None


class RecommendationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    opportunity_id: int
    kind: str
    content: dict
    generated_by: str
    created_at: datetime


class TaskCreateIn(BaseModel):
    title: str
    notes: Optional[str] = None
    opportunity_id: Optional[int] = None


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    opportunity_id: Optional[int]
    title: str
    notes: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime


class CompetitorCreate(BaseModel):
    site_id: int
    name: str
    base_url: str


class CompetitorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    site_id: int
    name: str
    base_url: str
    last_crawled_at: Optional[datetime]


class CompetitorGapOut(BaseModel):
    summary: list[str]
    top_opportunities: list[dict]
    comparison_table: list[dict]


class SimulatorQueryIn(BaseModel):
    query_text: str
    compare_competitors: bool = False


class SimulatorRunOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    query_id: int
    scan_id: int
    readiness_score: float
    sub_scores: dict
    entities: dict
    evidence_map: list
    strongest_evidence: list
    weakest_evidence: list
    would_recommend: bool
    simulated_answer: str
    evidence_used: list
    page_support: list
    evidence_gaps: list
    generated_by: str
    created_at: datetime


class SavedQueryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    site_id: int
    query_text: str
    intent: Optional[str]
    cluster: Optional[str]
    created_at: datetime
    latest_run: Optional[SimulatorRunOut] = None
    previous_score: Optional[float] = None
