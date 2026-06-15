from fastapi import APIRouter

from app.schemas.user import UserRegister

router = APIRouter(prefix="User", tags=["Users"])

async def register(user_data: UserRegister):
    pass