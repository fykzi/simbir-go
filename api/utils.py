from app import settings
from typing import Optional, Annotated

from fastapi import HTTPException, status, Cookie, Depends
import jwt
from database.dals import TransportDAL
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_db

DBSessionDep = Annotated[AsyncSession, Depends(get_db)]


def check_access_token(access_token: str) -> None:
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def parse_jwt_token(token: str) -> None:
    return jwt.decode(jwt=token, key=settings.JWT_SECRET_KEY, algorithms=["HS256"])


def get_user_id_from_token_payload(payload: dict) -> str:
    if not (user_id := payload.get("user_id")):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return user_id


def get_token(access_token: Annotated[bytes | None, Cookie()] = None):
    return access_token


def get_user_id_from_token(access_token: Annotated[str, Depends(get_token)]) -> int:
    check_access_token(access_token)
    token_payload = parse_jwt_token(access_token)
    user_id = get_user_id_from_token_payload(token_payload)
    return int(user_id)


UserDep = Annotated[int, Depends(get_user_id_from_token)]


async def is_transport_owner(
    transport_dal: TransportDAL, user_id: int, transport_id: int
) -> bool:
    return await transport_dal.is_owner(transport_id, user_id)


async def can_be_rented(transport_dal: TransportDAL, transport_id: int) -> bool:
    return await transport_dal.can_be_rented(transport_id)


async def check_transport(
    session: AsyncSession, user_id: int, transport_id: int
) -> None:
    transport_dal = TransportDAL(session)

    if await is_transport_owner(transport_dal, user_id, transport_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="This is your transport"
        )

    if not await can_be_rented(transport_dal, transport_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="transport is not for rent"
        )


def is_admin(access_token: Annotated[str, Depends(get_token)]) -> int:
    check_access_token(access_token)
    token_payload = parse_jwt_token(access_token)
    if not (is_admin := token_payload.get("is_admin")) or is_admin is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not admin"
        )


AdminDep = Annotated[None, Depends(is_admin)]
