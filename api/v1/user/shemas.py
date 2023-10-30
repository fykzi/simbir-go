from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    user_id: int
    username: str
    balance: float
    is_superuser: bool


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
