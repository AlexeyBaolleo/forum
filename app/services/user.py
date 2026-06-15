from app.schemas.user import UserRegister
from app.repo.user import UserRepo

from app.core.config.logging import configure_logging

logger = configure_logging("INFO")

class UserService():
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo

    async def register(self, user_data: UserRegister):
        await self.repo.register(**user_data.model_dump())
