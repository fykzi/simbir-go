from sqlalchemy.ext.asyncio import AsyncSession
from api.v1.transport.shemas import TransportCreate, TransportRead, TransportUpdate
from database.dals import TransportDAL
from typing import Optional
from fastapi import HTTPException, status


async def _add_transport(
    db_session: AsyncSession, data: TransportCreate, user_id: Optional[str]
) -> TransportRead:
    async with db_session as session:
        async with session.begin():
            transport_dal = TransportDAL(session)
            data = data.model_dump()
            data["owner"] = user_id
            new_transport = await transport_dal.add_transport(data)
            return TransportRead(**new_transport.get_transport_info())


async def _get_transport(db_session: AsyncSession, transport_id: int) -> TransportRead:
    async with db_session as session:
        async with session.begin():
            transport_dal = TransportDAL(session)
            transport = await transport_dal.get_transport_by_id(transport_id)
            if transport:
                return TransportRead(**transport.get_transport_info())
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


async def _update_transport(
    db_session: AsyncSession,
    transport_id: int,
    data: TransportUpdate,
    user_id: Optional[str],
) -> TransportRead:
    async with db_session as session:
        async with session.begin():
            transport_dal = TransportDAL(session)
            if not await transport_dal.is_owner(transport_id, user_id):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            validate_data = {k: v for k, v in data.model_dump().items() if v}
            transport = await transport_dal.update_(transport_id, validate_data)
            return TransportRead(**transport.get_transport_info())


async def _delete_transport(
    db_session: AsyncSession, transport_id: int, user_id: Optional[str]
) -> dict:
    async with db_session as session:
        async with session.begin():
            transport_dal = TransportDAL(session)
            if not await transport_dal.is_owner(transport_id, user_id):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            await transport_dal.delete_(transport_id)
            return {"message": "success"}
