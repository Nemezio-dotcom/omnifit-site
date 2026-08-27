from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Competitor(Base):
    __tablename__ = "competitors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"))
    name: Mapped[str] = mapped_column(String(255))
    base_url: Mapped[str] = mapped_column(String(500))
    last_crawled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    pages: Mapped[list["CompetitorPage"]] = relationship(back_populates="competitor", cascade="all, delete-orphan")


class CompetitorPage(Base):
    __tablename__ = "competitor_pages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    competitor_id: Mapped[int] = mapped_column(ForeignKey("competitors.id"))
    url: Mapped[str] = mapped_column(String(1000))
    title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    word_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    headings: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    has_schema: Mapped[bool] = mapped_column(default=False)
    schema_types: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    faq_count: Mapped[int] = mapped_column(Integer, default=0)
    testimonial_signals: Mapped[int] = mapped_column(Integer, default=0)
    credential_signals: Mapped[int] = mapped_column(Integer, default=0)
    topics: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # coarse topic tags matched by keyword
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    competitor: Mapped["Competitor"] = relationship(back_populates="pages")
