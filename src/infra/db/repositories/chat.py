from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.infra.db.models.chat import ChatSession, ChatMessage


class ChatRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # TODO: keep working on repo and later add chat session_id, logging, chat history etc.

    async def get_chat_by_id(self, chat_id: int) -> ChatSession | None:
        result = await self.session.execute(
            select(ChatSession).where(ChatSession.id == chat_id)
        )
        return result.scalar_one_or_none()

    async def create_chat_session(
        self, session_id: str, summary: str | None = None
    ) -> ChatSession:
        chat_session = ChatSession(session_id=session_id, summary=summary)
        self.session.add(chat_session)
        await self.session.commit()
        await self.session.refresh(chat_session)
        return chat_session

    async def add_message_to_chat(
        self, session_id: str, role: str, content: str
    ) -> ChatMessage:
        chat_message = ChatMessage(session_id=session_id, role=role, content=content)
        self.session.add(chat_message)
        await self.session.commit()
        await self.session.refresh(chat_message)
        return chat_message

    async def update_chat_summary(
        self, session_id: str, summary: str
    ) -> ChatSession | None:
        chat = await self.session.execute(
            select(ChatSession).where(ChatSession.session_id == session_id)
        )
        if chat := chat.scalar_one_or_none():
            chat.summary = summary
            self.session.add(chat)
            await self.session.commit()
            await self.session.refresh(chat)
            return chat
        return None

    async def get_messages_by_session_id(self, session_id: str) -> list[ChatMessage]:
        result = await self.session.execute(
            select(ChatMessage).where(ChatMessage.session_id == session_id)
        )
        return list(result.scalars().all())
