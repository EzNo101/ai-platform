from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.core.dependencies import ChatServiceDependency

router = APIRouter(prefix="/chat")


@router.post("/send")
async def ai_response(user_prompt: str, chat_service: ChatServiceDependency):
    return await chat_service.chat(user_prompt)


@router.websocket("/ws")
async def chat_websocket(websocket: WebSocket, chat_service: ChatServiceDependency):
    await websocket.accept()

    try:
        while True:
            user_prompt = await websocket.receive_text()
            async for chunk in chat_service.stream_chat(user_prompt):
                await websocket.send_text(chunk)

    except WebSocketDisconnect:
        pass
