from fastapi import APIRouter

router = APIRouter(prefix="User", tags=["Users"])

@router.get("/get_users")
def get_users():
    return None