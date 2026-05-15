from fastapi import APIRouter, Depends

from app.auth.models import UserInfo
from app.auth.router import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserInfo, summary="Get current user info")
def read_users_me(current_user: UserInfo = Depends(get_current_user)):
    """Return information about the currently authenticated user."""
    return current_user
