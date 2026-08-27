from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.ai.schemas import PageAIAnalysis, RecommendationAssets


@dataclass
class PageInput:
    url: str
    title: str | None
    meta_description: str | None
    h1: list[str]
    h2: list[str]
    text_content: str
    business_context: str


@dataclass
class RecommendationInput:
    opportunity_title: str
    explanation: str
    recommended_fix: str
    affected_pages: list[str]
    page_title: str | None
    page_text_excerpt: str
    business_context: str


class AIProvider(ABC):
    name: str = "base"

    @abstractmethod
    def analyze_page(self, page: PageInput) -> PageAIAnalysis: ...

    @abstractmethod
    def generate_recommendation_assets(self, rec_input: RecommendationInput) -> RecommendationAssets: ...
