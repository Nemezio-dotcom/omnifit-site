from __future__ import annotations

from datetime import datetime, date
from typing import Optional

from sqlalchemy import JSON, Date, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SearchConsoleQuery(Base):
    __tablename__ = "search_console_queries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"))
    query: Mapped[str] = mapped_column(String(500))
    page_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    clicks: Mapped[int] = mapped_column(Integer, default=0)
    impressions: Mapped[int] = mapped_column(Integer, default=0)
    ctr: Mapped[float] = mapped_column(Float, default=0.0)
    avg_position: Mapped[float] = mapped_column(Float, default=0.0)
    date_range_start: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_range_end: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    imported_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class SearchConsolePage(Base):
    __tablename__ = "search_console_pages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"))
    page_url: Mapped[str] = mapped_column(String(1000))
    clicks: Mapped[int] = mapped_column(Integer, default=0)
    impressions: Mapped[int] = mapped_column(Integer, default=0)
    ctr: Mapped[float] = mapped_column(Float, default=0.0)
    avg_position: Mapped[float] = mapped_column(Float, default=0.0)
    imported_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PageSpeedResult(Base):
    __tablename__ = "pagespeed_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"))
    page_url: Mapped[str] = mapped_column(String(1000))
    strategy: Mapped[str] = mapped_column(String(20), default="mobile")  # mobile | desktop

    performance: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    accessibility: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    best_practices: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    seo: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    lcp_ms: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    cls: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    inp_ms: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    fcp_ms: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    raw: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
