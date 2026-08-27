from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enums import FindingCategory, OpportunityStatus, Severity, TaskStatus


class Site(Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    base_url: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    scans: Mapped[list["Scan"]] = relationship(back_populates="site", cascade="all, delete-orphan")
    opportunities: Mapped[list["Opportunity"]] = relationship(back_populates="site", cascade="all, delete-orphan")


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="RUNNING")  # RUNNING | COMPLETE | FAILED
    source: Mapped[str] = mapped_column(String(50), default="live")  # live | local_fixture
    pages_crawled: Mapped[int] = mapped_column(Integer, default=0)
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Rolled-up scores (0-100), heuristic
    technical_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    seo_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    local_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    aio_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    authority_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    conversion_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    overall_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    site: Mapped["Site"] = relationship(back_populates="scans")
    pages: Mapped[list["Page"]] = relationship(back_populates="scan", cascade="all, delete-orphan")
    findings: Mapped[list["Finding"]] = relationship(back_populates="scan", cascade="all, delete-orphan")


class Page(Base):
    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scans.id"))
    url: Mapped[str] = mapped_column(String(1000), index=True)
    normalized_url: Mapped[str] = mapped_column(String(1000), index=True)

    status_code: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    response_time_ms: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    content_type: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    final_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    redirect_chain: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)

    title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    meta_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    canonical: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    h1: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # list[str]
    h2: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    h3: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    word_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    internal_links: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    external_links: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    images: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # [{src, alt}]

    json_ld: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    open_graph: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    robots_meta: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    is_indexable: Mapped[Optional[bool]] = mapped_column(nullable=True)
    in_sitemap: Mapped[Optional[bool]] = mapped_column(nullable=True)
    inbound_internal_link_count: Mapped[int] = mapped_column(Integer, default=0)
    is_orphan: Mapped[bool] = mapped_column(default=False)

    depth: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    text_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # extracted visible text, for AI/audit use

    # Page-level scores, computed post-crawl
    technical_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    seo_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    aio_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    local_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    trust_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    conversion_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    scan: Mapped["Scan"] = relationship(back_populates="pages")
    findings: Mapped[list["Finding"]] = relationship(back_populates="page", cascade="all, delete-orphan")


class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scans.id"))
    page_id: Mapped[Optional[int]] = mapped_column(ForeignKey("pages.id"), nullable=True)

    code: Mapped[str] = mapped_column(String(100))  # stable rule id, e.g. "MISSING_TITLE"
    category: Mapped[FindingCategory] = mapped_column(String(50))
    severity: Mapped[Severity] = mapped_column(String(20))
    affected_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    evidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    explanation: Mapped[str] = mapped_column(Text)
    recommended_action: Mapped[str] = mapped_column(Text)

    estimated_effort: Mapped[int] = mapped_column(Integer)  # 1-10
    estimated_impact: Mapped[float] = mapped_column(Float)  # 0-10
    confidence: Mapped[float] = mapped_column(Float)  # 0-10

    fingerprint: Mapped[str] = mapped_column(String(300), index=True)  # for cross-scan resolution tracking
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    scan: Mapped["Scan"] = relationship(back_populates="findings")
    page: Mapped[Optional["Page"]] = relationship(back_populates="findings")


class Opportunity(Base):
    __tablename__ = "opportunities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"))

    title: Mapped[str] = mapped_column(String(300))
    category: Mapped[FindingCategory] = mapped_column(String(50))
    affected_pages: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # list[str] urls
    severity: Mapped[Severity] = mapped_column(String(20))

    impact_score: Mapped[float] = mapped_column(Float)  # 0-10
    confidence_score: Mapped[float] = mapped_column(Float)  # 0-10
    effort_score: Mapped[float] = mapped_column(Float)  # 1-10 (10 = hardest)
    priority_score: Mapped[float] = mapped_column(Float)  # 0-100 normalized

    explanation: Mapped[str] = mapped_column(Text)
    evidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommended_fix: Mapped[str] = mapped_column(Text)
    expected_benefit: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    implementation_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    estimated_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    source_finding_codes: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    fingerprint: Mapped[str] = mapped_column(String(300), index=True)

    status: Mapped[OpportunityStatus] = mapped_column(String(20), default=OpportunityStatus.OPEN)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    site: Mapped["Site"] = relationship(back_populates="opportunities")
    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="opportunity", cascade="all, delete-orphan")
    tasks: Mapped[list["OFTask"]] = relationship(back_populates="opportunity", cascade="all, delete-orphan")


class Recommendation(Base):
    """AI-drafted implementation assets for an Opportunity. Never auto-published."""

    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    opportunity_id: Mapped[int] = mapped_column(ForeignKey("opportunities.id"))

    kind: Mapped[str] = mapped_column(String(50))  # title | meta_description | h1 | faq | schema | content_brief | internal_links
    content: Mapped[dict] = mapped_column(JSON)
    generated_by: Mapped[str] = mapped_column(String(50))  # "heuristic" | "openai:gpt-4o-mini"
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    opportunity: Mapped["Opportunity"] = relationship(back_populates="recommendations")


class OFTask(Base):
    """User-created follow-up task. Named OFTask to avoid clashing with the harness TaskCreate concept."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    opportunity_id: Mapped[Optional[int]] = mapped_column(ForeignKey("opportunities.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(300))
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(String(20), default=TaskStatus.OPEN)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    opportunity: Mapped[Optional["Opportunity"]] = relationship(back_populates="tasks")
