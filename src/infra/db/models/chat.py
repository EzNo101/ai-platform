from __future__ import annotations

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.db.base import Base
from src.infra.db.models.mixins import IdMixin, CreatedAtMixin, UpdatedAtMixin


class ChatSession(Base, IdMixin, CreatedAtMixin, UpdatedAtMixin):
    messages: Mapped[list[ChatMessage]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)


class ChatMessage(Base, IdMixin, CreatedAtMixin, UpdatedAtMixin):
    session_id: Mapped[str] = mapped_column(
        ForeignKey("chat_sessions.id"),
        index=True,
        nullable=False,
    )
    role: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    session: Mapped[ChatSession] = relationship(back_populates="messages")
