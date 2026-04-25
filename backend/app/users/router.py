from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import require_admin
from app.database import get_db
from app.models import User
from app.users.schemas import UserItem, UserListResponse
from app.users.service import delete_user, list_users

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=UserListResponse)
async def get_users(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    users = await list_users(db)
    return UserListResponse(users=users, total=len(users))


@router.delete("/{user_id}")
async def remove_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    await delete_user(db, user_id)
    return {"success": True, "message": "User deleted"}
