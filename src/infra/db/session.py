from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

if TYPE_CHECKING:
    from typing import AsyncGenerator

from src.core.config import settings

engine = ...  # TODO: finish session.py and start working on RAG
