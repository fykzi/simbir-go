from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Literal
from api.v1.user.shemas import UserRead
from database.dals import AdminAccountDAL


async def _get_user_accounts(
    db_session: AsyncSession, start: int, count: int
) -> Optional[List[UserRead]]:
    async with db_session as session:
        async with session.begin():
            admin_account_dal = AdminAccountDAL(session)
            result = await admin_account_dal.get_accounts(start, count)
            return [UserRead(**account[0].get_user_info()) for account in result]


# TODO this
async def _delete_account(
    db_session: AsyncSession, account_id: int
) -> dict[Literal["message"], str]:
    async with db_session as session:
        async with session.begin():
            admin_account_dal = AdminAccountDAL(session)
            await admin_account_dal.delete_(account_id)
            return {"message": "success"}
