from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User

class Board(Base):
    __tablename__ = "boards"

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(length=150))
    description: Mapped[str] = mapped_column(String(length=600))

    creator_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    creator: Mapped["User"] = relationship(back_populates="boards")
