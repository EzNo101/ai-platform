from __future__ import annotations
from typing import TYPE_CHECKING, Annotated
from fastapi import Depends

from src.infra.ai.client import get_openrouter_client
from src.services.chat import ChatService

if TYPE_CHECKING:
    from openrouter import OpenRouter


def chat_service(client: OpenRouter = Depends(get_openrouter_client)) -> ChatService:
    return ChatService(client=client)


ChatServiceDependency = Annotated[ChatService, Depends(chat_service)]
