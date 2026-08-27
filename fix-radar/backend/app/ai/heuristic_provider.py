from __future__ import annotations

import re

from app import business_context as biz
from app.ai.provider import AIProvider, PageInput, RecommendationInput
from app.ai.schemas import PageAIAnalysis, RecommendationAssets


class HeuristicAIProvider(AIProvider):
    """Rule-based stand-in for an LLM. Used when no AI_PROVIDER key is configured.

    Everything it says is directly traceable to a keyword or structural signal
    in the page text that was passed in -- it never infers facts not present.
    """

    name = "heuristic"

    def analyze_page(self, page: PageInput) -> PageAIAnalysis:
        text = (page.text_content or "").lower()
        strengths, weaknesses, missing, gaps, ambiguity, authority_gaps = [], [], [], [], [], []
        improvements, questions, citations, internal_links = [], [], [], []

        if page.title and any(loc.lower() in page.title.lower() for loc in [biz.PRIMARY_LOCATION] + biz.SERVICE_AREAS):
            strengths.append("Title includes a specific location, which helps geographic query matching.")
        elif page.title:
            gaps.append("Title does not mention a specific location.")

        if biz.BUSINESS_NAME.lower() in text:
            strengths.append(f"Page explicitly names {biz.BUSINESS_NAME}, reducing entity ambiguity.")
        else:
            ambiguity.append(f"Page never mentions '{biz.BUSINESS_NAME}' by name; an AI system reading only this page may not attribute it to the business.")

        service_hits = [s for s in biz.SERVICES if s.lower() in text]
        if service_hits:
            strengths.append(f"Clearly names specific services: {', '.join(service_hits)}.")
        else:
            missing.append("No specific service names from the business's actual service list appear on this page.")

        if any(stage.lower() in text for stage in biz.METHODOLOGY_STAGES):
            strengths.append(f"References the {biz.METHODOLOGY_NAME} methodology.")

        evidence_kw = ["case study", "testimonial", "review", "result", "transformation", "before and after"]
        if not any(k in text for k in evidence_kw):
            weaknesses.append("No testimonials, reviews, or case-study language found on this page.")
            authority_gaps.append("Missing third-party or client evidence to back up claims made on this page.")

        superlative_kw = ["best ", "#1", "top-rated", "leading", "world-class", "the best"]
        unsupported = [kw.strip() for kw in superlative_kw if kw in text]
        unsupported_claims = []
        if unsupported:
            unsupported_claims.append(
                f"Uses superlative language ({', '.join(unsupported)}) without visible supporting evidence on this page."
            )

        if page.meta_description is None:
            missing.append("No meta description to summarize the page for search/AI snippets.")

        sentences = re.split(r"(?<=[.!?])\s+", page.text_content or "")
        for s in sentences:
            s = s.strip()
            if 30 <= len(s) <= 220 and (re.search(r"\d", s) or any(w in s.lower() for w in service_hits)):
                citations.append(s)
        citations = citations[:5]

        if not any("?" in h for h in page.h2):
            questions.append("What specific outcomes has OmniFit delivered for clients like me?")
            questions.append(f"Does OmniFit serve my specific area near {biz.PRIMARY_LOCATION}?")

        if "executive" in text or "professional" in text:
            strengths.append("Addresses a professional/executive audience explicitly.")
        else:
            gaps.append("Does not explicitly address the target audience (professionals 30+).")

        if not service_hits and not strengths:
            improvements.append("Add a clear statement of what OmniFit is, who it serves, and where, near the top of the page.")
        if unsupported_claims:
            improvements.append("Support superlative claims with specific evidence, or soften the language.")
        if not any(k in text for k in evidence_kw):
            improvements.append("Add at least one concrete, honestly-reported client outcome or testimonial.")

        return PageAIAnalysis(
            strengths=strengths,
            weaknesses=weaknesses,
            missing_information=missing,
            unsupported_claims=unsupported_claims,
            unclear_positioning=gaps,
            content_gaps=gaps,
            entity_ambiguity=ambiguity,
            authority_gaps=authority_gaps,
            recommended_improvements=improvements,
            suggested_questions=questions,
            citation_worthy_passages=citations,
            recommended_internal_links=internal_links,
            confidence=0.5,
            generated_by="heuristic",
        )

    def generate_recommendation_assets(self, rec_input: RecommendationInput) -> RecommendationAssets:
        return RecommendationAssets(
            suggested_title=None,
            suggested_meta_description=None,
            suggested_h1=None,
            faq_items=[],
            section_outline=[
                "What this section should cover (heuristic draft -- fill in with real facts):",
                rec_input.recommended_fix,
            ],
            internal_link_suggestions=rec_input.affected_pages[:3],
            schema_draft=None,
            content_brief=(
                f"Draft brief for: {rec_input.opportunity_title}\n\n"
                f"Why it matters: {rec_input.explanation}\n\n"
                f"What to do: {rec_input.recommended_fix}\n\n"
                "This is a heuristic (non-AI) draft. Connect an OpenAI API key in .env to get "
                "AI-drafted titles, meta descriptions, and FAQ copy grounded in your actual page content."
            ),
            generated_by="heuristic",
        )
