from fastapi import APIRouter, Depends, Cookie
from api.v1.user.shemas import UserRead
from api.v1.payment.services import _replenish_balance
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from api.utils import UserDep, DBSessionDep
from database.session import get_db

payment_router = APIRouter()


@payment_router.post("/Hesoyam/{accountId}", response_model=UserRead)
async def replenish_balance(
    accountId: int, user_id: UserDep, db_session: DBSessionDep
) -> UserRead:
    return await _replenish_balance(db_session, accountId, user_id)
