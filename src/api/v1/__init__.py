from fastapi import APIRouter

from src.api.v1.chat import router as chat_router

router = APIRouter(prefix="/v1")
router.include_router(chat_router)
