from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.board import Board

class User(Base):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str | None] = mapped_column(default=None, unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    
    boards: Mapped[list["Board"]] = relationship(back_populates="creator", lazy="noload")
