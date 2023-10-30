from sqlalchemy.ext.asyncio import AsyncSession
from api.utils import get_user_id_from_token
from database.dals import UserDAL
from fastapi import HTTPException, status
from api.v1.user.shemas import UserRead


async def _replenish_balance(
    db_session: AsyncSession, account_id: int, user_id: str
) -> UserRead:
    async with db_session as session:
        async with session.begin():
            user_dal = UserDAL(session)
            if not await user_dal.is_superuser(user_id):
                if user_id != account_id:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            user = await user_dal.replenish_balance(account_id)
            return UserRead(**user.get_user_info())
