from functools import lru_cache

from app.ai.heuristic_provider import HeuristicAIProvider
from app.ai.provider import AIProvider
from app.core.config import get_settings


@lru_cache
def get_ai_provider() -> AIProvider:
    settings = get_settings()
    if settings.ai_provider == "openai" and settings.openai_api_key:
        try:
            from app.ai.openai_provider import OpenAIProvider

            return OpenAIProvider(api_key=settings.openai_api_key, model=settings.openai_model)
        except Exception:
            return HeuristicAIProvider()
    return HeuristicAIProvider()
