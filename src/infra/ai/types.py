import asyncio
from dataclasses import dataclass
from collections.abc import AsyncIterator


@dataclass(slots=True)
class ChatCompletionResult:
    text: str
    usage: dict[str, int]


@dataclass(slots=True)
class StreamChatResult:
    stream: AsyncIterator[str]
    usage_future: asyncio.Future[dict[str, int]]
