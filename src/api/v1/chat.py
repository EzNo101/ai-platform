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

            result = await chat_service.stream_chat(user_prompt)

            buffer: list[str] = []
            async for chunk in result.stream:
                buffer.append(chunk)
                await websocket.send_text(chunk)

            usage = await result.usage_future
            full_text = "".join(buffer)

            await websocket.send_json(
                {
                    "type": "done",
                    "text": full_text,
                    "usage": usage,
                }
            )

    except WebSocketDisconnect:
        pass
