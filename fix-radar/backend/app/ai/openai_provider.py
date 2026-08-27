from __future__ import annotations

import json
import logging

from app.ai.heuristic_provider import HeuristicAIProvider
from app.ai.provider import AIProvider, PageInput, RecommendationInput
from app.ai.schemas import PageAIAnalysis, RecommendationAssets

logger = logging.getLogger(__name__)

PAGE_ANALYSIS_SYSTEM_PROMPT = """You are a technical SEO and AI-search-readiness analyst reviewing ONE page \
of a small business website. You will be given the page's URL, title, meta description, \
headings, visible text, and a short factual summary of the business.

Rules, strictly enforced:
- Only report what is actually observable in the page text provided. Never invent facts, \
credentials, statistics, or claims about the business that are not in the text.
- If something is unknown, say so explicitly (e.g. in missing_information) rather than guessing.
- Do not inflate severity or manufacture problems that aren't real.
- Return ONLY valid JSON matching the exact schema you are given. No prose outside the JSON.
"""

RECOMMENDATION_SYSTEM_PROMPT = """You are a conversion copywriter and technical SEO assistant drafting \
IMPLEMENTATION SUGGESTIONS for a specific, already-identified website opportunity. You will be given the \
opportunity, why it matters, the recommended fix, the affected page's current title/content excerpt, and a \
factual business summary.

Rules, strictly enforced:
- Never invent credentials, statistics, client outcomes, awards, or affiliations not given to you.
- Every suggestion must be something a human can review and edit before publishing -- these are drafts.
- If you don't have enough information for a field, leave it null/empty rather than fabricating it.
- Return ONLY valid JSON matching the exact schema you are given.
"""


class OpenAIProvider(AIProvider):
    name = "openai"

    def __init__(self, api_key: str, model: str):
        from openai import OpenAI

        self._client = OpenAI(api_key=api_key)
        self._model = model
        self._fallback = HeuristicAIProvider()

    def _chat_json(self, system: str, user: str) -> dict | None:
        try:
            resp = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                response_format={"type": "json_object"},
                temperature=0.2,
                timeout=30,
            )
            content = resp.choices[0].message.content
            return json.loads(content) if content else None
        except Exception:
            logger.exception("OpenAI call failed; falling back to heuristic analysis")
            return None

    def analyze_page(self, page: PageInput) -> PageAIAnalysis:
        user = json.dumps(
            {
                "business_context": page.business_context,
                "url": page.url,
                "title": page.title,
                "meta_description": page.meta_description,
                "h1": page.h1,
                "h2": page.h2,
                "visible_text": (page.text_content or "")[:8000],
                "json_schema_fields": list(PageAIAnalysis.model_fields.keys()),
            }
        )
        data = self._chat_json(PAGE_ANALYSIS_SYSTEM_PROMPT, user)
        if data is None:
            return self._fallback.analyze_page(page)
        try:
            data["generated_by"] = f"openai:{self._model}"
            return PageAIAnalysis(**data)
        except Exception:
            logger.exception("OpenAI response failed schema validation; falling back to heuristic analysis")
            return self._fallback.analyze_page(page)

    def generate_recommendation_assets(self, rec_input: RecommendationInput) -> RecommendationAssets:
        user = json.dumps(
            {
                "business_context": rec_input.business_context,
                "opportunity_title": rec_input.opportunity_title,
                "explanation": rec_input.explanation,
                "recommended_fix": rec_input.recommended_fix,
                "affected_pages": rec_input.affected_pages,
                "page_title": rec_input.page_title,
                "page_text_excerpt": rec_input.page_text_excerpt[:4000],
                "json_schema_fields": list(RecommendationAssets.model_fields.keys()),
            }
        )
        data = self._chat_json(RECOMMENDATION_SYSTEM_PROMPT, user)
        if data is None:
            return self._fallback.generate_recommendation_assets(rec_input)
        try:
            data["generated_by"] = f"openai:{self._model}"
            return RecommendationAssets(**data)
        except Exception:
            logger.exception("OpenAI response failed schema validation; falling back to heuristic assets")
            return self._fallback.generate_recommendation_assets(rec_input)
