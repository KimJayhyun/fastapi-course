from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/")
async def get_user():
    return {"user": "authenticated"}
