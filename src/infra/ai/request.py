from __future__ import annotations

from typing import TYPE_CHECKING

from typing import Any, cast


from src.core.config import settings
from src.core.exceptions import OpenRouterRequestError

if TYPE_CHECKING:
    from openrouter import OpenRouter, components


# helps get value from 2 forms of object(dict or object)
def _get_value(source: Any, key: str, default: Any = None) -> Any:
    if isinstance(source, dict):
        return cast(dict[str, Any], source).get(key, default)
    return getattr(source, key, default)


def _extract_text(response: Any) -> str:
    choices = _get_value(response, "choices", [])

    if not choices:
        raise OpenRouterRequestError("OpenRouter response does not contain choices.")

    choice = choices[0]
    message = _get_value(choice, "message")
    if message is None:
        raise OpenRouterRequestError("OpenRouter response does not contain message")
    content = _get_value(message, "content")
    if content is None:
        raise OpenRouterRequestError("OpenRouter response does not contain answer")

    return content


async def create_chat_completion(
    client: OpenRouter,
    messages: list[components.ChatMessagesTypedDict],
    *,
    model: str | None = None,
    stream: bool = False,
    max_tokens: int | None = None,
    **kwargs: Any,
):
    response = await client.chat.send_async(
        messages=messages,
        model=model or settings.OPENROUTER_AI_MODEL,
        stream=stream,
        max_tokens=max_tokens,
        **kwargs,
    )

    # TODO: add message stream later

    return _extract_text(response)
