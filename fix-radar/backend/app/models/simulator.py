from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SimulatorQuery(Base):
    """A saved query in the AI Recommendation Simulator's Query Library."""

    __tablename__ = "simulator_queries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"))
    query_text: Mapped[str] = mapped_column(Text)
    intent: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    cluster: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    runs: Mapped[list["SimulatorRun"]] = relationship(back_populates="query", cascade="all, delete-orphan")


class SimulatorRun(Base):
    """One execution of a query against a scan's evidence base."""

    __tablename__ = "simulator_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    query_id: Mapped[int] = mapped_column(ForeignKey("simulator_queries.id"))
    scan_id: Mapped[int] = mapped_column(ForeignKey("scans.id"))

    readiness_score: Mapped[float] = mapped_column(Float)
    sub_scores: Mapped[dict] = mapped_column(JSON)  # entity_clarity, query_relevance, expertise, evidence, trust, local_relevance, third_party_authority, content_completeness, differentiation
    entities: Mapped[dict] = mapped_column(JSON)  # extracted profession/location/audience/intent/criteria
    evidence_map: Mapped[list] = mapped_column(JSON)  # list of {requirement, evidence, source_url, strength, gap}
    strongest_evidence: Mapped[list] = mapped_column(JSON)
    weakest_evidence: Mapped[list] = mapped_column(JSON)
    would_recommend: Mapped[bool] = mapped_column(default=False)
    simulated_answer: Mapped[str] = mapped_column(Text)
    evidence_used: Mapped[list] = mapped_column(JSON)  # list of {url, note}
    page_support: Mapped[list] = mapped_column(JSON)  # [{url, title, support_pct}]
    evidence_gaps: Mapped[list] = mapped_column(JSON)  # top 5 gaps
    generated_by: Mapped[str] = mapped_column(String(50))  # "heuristic" | "openai:..."
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    query: Mapped["SimulatorQuery"] = relationship(back_populates="runs")
