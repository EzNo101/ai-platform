from datetime import datetime

from sqlalchemy import func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, declarative_mixin


@declarative_mixin
class IdMixin:
    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )


@declarative_mixin
class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


@declarative_mixin
class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
