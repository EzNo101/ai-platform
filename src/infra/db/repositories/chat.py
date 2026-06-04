from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.infra.db.models.chat import ChatSession, ChatMessage


class ChatRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

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

    async def delete_chat_session(self, session_id: str) -> None:
        result = await self.session.execute(
            select(ChatSession).where(ChatSession.session_id == session_id)
        )
        if chat_session := result.scalar_one_or_none():
            await self.session.delete(chat_session)
            await self.session.commit()

    async def add_message_to_chat(
        self, session_id: str, role: str, content: str
    ) -> ChatMessage:
        chat_message = ChatMessage(session_id=session_id, role=role, content=content)
        self.session.add(chat_message)
        await self.session.commit()
        await self.session.refresh(chat_message)
        return chat_message

    async def get_messages_by_session_id(self, session_id: str) -> list[ChatMessage]:
        result = await self.session.execute(
            select(ChatMessage).where(ChatMessage.session_id == session_id)
        )
        return list(result.scalars().all())

    async def get_chat_message_by_id(
        self, session_id: str, message_id: int
    ) -> ChatMessage | None:
        result = await self.session.execute(
            select(ChatMessage).where(
                ChatMessage.session_id == session_id, ChatMessage.id == message_id
            )
        )
        return result.scalar_one_or_none()

    async def delete_chat_message(self, session_id: str, message_id: int) -> None:
        result = await self.session.execute(
            select(ChatMessage).where(
                ChatMessage.session_id == session_id, ChatMessage.id == message_id
            )
        )
        if chat_message := result.scalar_one_or_none():
            await self.session.delete(chat_message)
            await self.session.commit()
