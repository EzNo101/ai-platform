from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, cast

from src.core.config import settings
from src.core.exceptions import OpenRouterRequestError
from src.infra.ai.types import ChatCompletionResult, StreamChatResult

if TYPE_CHECKING:
    from openrouter import OpenRouter, components
    from collections.abc import AsyncGenerator


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


def _extract_usage(response: Any) -> dict[str, int]:
    usage = _get_value(response, "usage")
    if not usage:
        return {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}

    completion = _get_value(usage, "completion_tokens", 0) or 0
    prompt = _get_value(usage, "prompt_tokens", 0) or 0
    total = _get_value(usage, "total_tokens", 0) or 0

    return {
        "completion_tokens": int(completion),
        "prompt_tokens": int(prompt),
        "total_tokens": int(total),
    }


async def create_chat_completion(
    client: OpenRouter,
    messages: list[components.ChatMessagesTypedDict],
    *,
    model: str | None = None,
    max_tokens: int | None = None,
    **kwargs: Any,
):
    response = await client.chat.send_async(
        messages=messages,
        model=model or settings.OPENROUTER_AI_MODEL,
        stream=False,
        max_tokens=max_tokens,
        **kwargs,
    )

    return ChatCompletionResult(
        text=_extract_text(response),
        usage=_extract_usage(response),
    )


async def stream_chat_completion(
    client: OpenRouter,
    messages: list[components.ChatMessagesTypedDict],
    *,
    model: str | None = None,
    max_tokens: int | None = None,
    **kwargs: Any,
) -> StreamChatResult:
    loop = asyncio.get_running_loop()
    usage_future: asyncio.Future[dict[str, int]] = loop.create_future()

    async def _stream() -> AsyncGenerator[str, None]:
        response = await client.chat.send_async(
            messages=messages,
            model=model or settings.OPENROUTER_AI_MODEL,
            stream=True,
            max_tokens=max_tokens,
            **kwargs,
        )

        final_usage = {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}

        async for event in response:
            usage = _get_value(event, "usage")
            if usage:
                final_usage = _extract_usage(event)
                continue

            if not event.choices:
                continue

            delta = event.choices[0].delta
            chunk = getattr(delta, "content", None)

            if chunk:
                yield chunk

        if not usage_future.done():
            usage_future.set_result(final_usage)

    return StreamChatResult(stream=_stream(), usage_future=usage_future)
