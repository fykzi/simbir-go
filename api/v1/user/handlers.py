from typing import Annotated, Literal

from fastapi import APIRouter, Cookie, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.user.services import (
    _user_me,
    _user_sign_in,
    _user_sign_out,
    _user_sign_up,
    _user_update,
)
from api.v1.user.shemas import UserCreate, UserRead, UserUpdate
from database.session import get_db
from api.utils import UserDep

account_router = APIRouter()


@account_router.get("/Me", response_model=UserRead)
async def user_me(
    user_id: UserDep,
    db_session: AsyncSession = Depends(get_db),
) -> UserRead:
    return await _user_me(db_session, user_id)


@account_router.post("/SignIn")
async def user_sign_in(
    data: UserCreate, response: Response, db_session: AsyncSession = Depends(get_db)
):
    return await _user_sign_in(db_session, data, response)


@account_router.post("/SignUp", response_model=UserRead)
async def user_sign_up(
    data: UserCreate, db_session: AsyncSession = Depends(get_db)
) -> UserRead:
    return await _user_sign_up(db_session, data)


@account_router.post("/SignOut")
async def user_sign_out(
    response: Response,
    access_token: Annotated[str | None, Cookie()] = None,
) -> dict[Literal["message"], Literal["success logout"]]:
    return await _user_sign_out(response, access_token)


@account_router.put("/Update")
async def user_update(
    data: UserUpdate,
    user_id: UserDep,
    db_session: AsyncSession = Depends(get_db),
) -> UserRead:
    return await _user_update(db_session, data, user_id)
