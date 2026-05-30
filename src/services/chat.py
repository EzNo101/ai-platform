from __future__ import annotations
from typing import TYPE_CHECKING


from src.infra.ai.request import create_chat_completion, stream_chat_completion

if TYPE_CHECKING:
    from openrouter import OpenRouter, components
    from src.infra.ai.types import ChatCompletionResult, StreamChatResult


class ChatService:
    def __init__(self, client: OpenRouter) -> None:
        self.client = client

    async def chat(self, prompt: str) -> ChatCompletionResult:
        messages: list[components.ChatMessagesTypedDict] = [
            {"role": "user", "content": prompt},
        ]

        return await create_chat_completion(client=self.client, messages=messages)

    async def stream_chat(self, prompt: str) -> StreamChatResult:
        messages: list[components.ChatMessagesTypedDict] = [
            {"role": "user", "content": prompt},
        ]
        return await stream_chat_completion(
            client=self.client,
            messages=messages,
        )
