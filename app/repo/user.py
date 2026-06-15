from sqlalchemy.ext.asyncio import AsyncSession

from typing import Any

from app.models.user import User

class UserRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def register(self, **kwargs: Any) -> User:
        user = User(**kwargs)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user