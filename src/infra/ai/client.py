from openrouter import OpenRouter

from src.core.config import settings

openrouter = OpenRouter(api_key=settings.OPENROUTER_API_KEY)


def get_openrouter_client() -> OpenRouter:
    return openrouter
