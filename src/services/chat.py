from typing import TYPE_CHECKING


from src.infra.ai.request import create_chat_completion

if TYPE_CHECKING:
    from openrouter import OpenRouter, components


class ChatService:
    def __init__(self, client: OpenRouter) -> None:
        self.client = client

    async def chat(self, prompt: str) -> str:
        messages: list[components.ChatMessagesTypedDict] = [
            {"role": "user", "content": prompt},
        ]
        return await create_chat_completion(client=self.client, messages=messages)
