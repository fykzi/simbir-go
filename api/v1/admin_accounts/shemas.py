from typing import Optional

from pydantic import BaseModel, Field


class AdminUserCreate(BaseModel):
    username: str
    password: str
    is_superuser: bool = Field(alias="isAdmin", default=False)
    balance: float


class AdminUserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    is_superuser: bool = Field(alias="isAdmin", default=False)
    balance: float = None
