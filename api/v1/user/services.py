from typing import Literal, Optional
from api.utils import get_user_id_from_token, check_access_token

import jwt
from fastapi import HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.user.shemas import UserCreate, UserRead, UserUpdate
from app import settings
from database.dals import UserDAL


async def _user_sign_up(db_session: AsyncSession, data: UserCreate) -> UserRead:
    async with db_session as session:
        async with session.begin():
            user_dal = UserDAL(session)
            data = data.model_dump()
            if await user_dal.get_user_by_username(data.get("username")):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Username taken"
                )
            new_user = await user_dal.sign_up(data)
            return UserRead(**new_user.get_user_info())


async def _user_sign_in(
    db_session: AsyncSession, data: UserCreate, response: Response
) -> Optional[dict[Literal["access_token"], str]]:
    async with db_session as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_username(
                data.model_dump().get("username")
            )
            if user:
                if data.model_dump().get("password") == user.password:
                    token_payload = {
                        "user_id": str(user.user_id),
                        "is_admin": user.is_superuser,
                    }
                    token = jwt.encode(token_payload, key=settings.JWT_SECRET_KEY)
                    response.set_cookie(key="access_token", value=token, max_age=10800)
                    return {"access_token": token}


async def _user_sign_out(
    response: Response, user_id: int
) -> dict[Literal["message"], Literal["success logout"]]:
    check_access_token(user_id)
    response.delete_cookie(key="access_token")
    return {"message": "success logout"}


async def _user_me(db_session: AsyncSession, user_id: Optional[str]) -> UserRead:
    async with db_session as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_user_id(user_id)
            if user:
                return UserRead(**user.get_user_info())
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


async def _user_update(
    db_session: AsyncSession, data: UserUpdate, user_id: int
) -> UserRead:
    async with db_session as session:
        async with session.begin():
            user_dal = UserDAL(session)
            validate_data = {
                k: v for k, v in data.model_dump().items() if v is not None
            }
            user = await user_dal.user_update(user_id, validate_data)
            return UserRead(**user.get_user_info())
