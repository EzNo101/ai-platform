from fastapi import APIRouter

from src.core.dependencies import ChatServiceDependency

router = APIRouter(prefix="/chat")


@router.post("/send")
async def ai_response(user_prompt: str, chat_service: ChatServiceDependency):
    return await chat_service.chat(user_prompt)
