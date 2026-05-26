from __future__ import annotations
from typing import Any, cast

from src.core.config import settings
from src.core.exceptions import OpenRouterRequestError
from src.infra.ai.client import get_openrouter_client


# helps get value from 2 forms of object(dict or object)
def _get_value(source: Any, key: str, default: Any = None) -> Any:
    if isinstance(source, dict):
        return cast(dict[str, Any], source).get(key, default)
    return getattr(source, key, default)


def _extract_text(response: Any) -> str:
    choices = _get_value(response, "choices", [])

    if not choices:
        raise OpenRouterRequestError("OpenRouter response does not contain choices.")

    # TODO: complete text extraction tomorrow


async def create_chat_completion(
    messages: list[dict[str, Any]],
    *,
    model: str | None = None,
    stream: bool = False,
    max_tokens: int | None = None,
    **kwargs: Any,
): ...
