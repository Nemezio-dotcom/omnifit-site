from pydantic import BaseModel, Field


class PageAIAnalysis(BaseModel):
    """Strict-JSON output for a single page's semantic AI review.

    Every list should only contain things actually grounded in the page text
    that was sent to the model (or, for the heuristic provider, in keyword
    signals detected in that text). Nothing here should be treated as fact
    about OmniFit beyond what the page itself states.
    """

    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    unsupported_claims: list[str] = Field(default_factory=list)
    unclear_positioning: list[str] = Field(default_factory=list)
    content_gaps: list[str] = Field(default_factory=list)
    entity_ambiguity: list[str] = Field(default_factory=list)
    authority_gaps: list[str] = Field(default_factory=list)
    recommended_improvements: list[str] = Field(default_factory=list)
    suggested_questions: list[str] = Field(default_factory=list)
    citation_worthy_passages: list[str] = Field(default_factory=list)
    recommended_internal_links: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1, default=0.5)
    generated_by: str = "heuristic"


class RecommendationAssets(BaseModel):
    """Draft implementation assets for an Opportunity. Always manual-approval only."""

    suggested_title: str | None = None
    suggested_meta_description: str | None = None
    suggested_h1: str | None = None
    faq_items: list[dict] = Field(default_factory=list)  # [{question, answer}]
    section_outline: list[str] = Field(default_factory=list)
    internal_link_suggestions: list[str] = Field(default_factory=list)
    schema_draft: dict | None = None
    content_brief: str | None = None
    generated_by: str = "heuristic"
    caveat: str = "Draft only. Verify every factual claim before publishing; nothing here is auto-published."
