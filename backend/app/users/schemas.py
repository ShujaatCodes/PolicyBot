from pydantic import BaseModel

from app.models import UserRole


class UserItem(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    users: list[UserItem]
    total: int
