from sqlalchemy.ext.asyncio import AsyncSession
from api.v1.admin_transports.shemas import (
    AdmintransportTypes,
    AdminTransportCreate,
    AdminTransportUpdate,
)
from typing import Optional, List
from api.v1.transport.shemas import TransportRead
from database.dals import AdminTransportDal, TransportDAL
from fastapi import HTTPException, status


async def _get_transports(
    db_session: AsyncSession,
    start: int,
    count: int,
    transport_type: AdmintransportTypes,
) -> Optional[List[TransportRead]]:
    async with db_session as session:
        async with session.begin():
            admin_transport_dal = AdminTransportDal(session)
            print(transport_type)
            if transport_type.value == AdmintransportTypes.All.value:
                res = await admin_transport_dal.get_transports(start, count)
            else:
                res = await admin_transport_dal.get_transports(
                    start, count, transport_type.value
                )
            return [TransportRead(**i[0].get_transport_info()) for i in res]


async def _add_transport(
    db_session: AsyncSession, data: AdminTransportCreate
) -> TransportRead:
    async with db_session as session:
        async with session.begin():
            transport_dal = TransportDAL(session)
            data = data.model_dump()
            new_transport = await transport_dal.add_transport(data)
            return TransportRead(**new_transport.get_transport_info())


async def _update_transport(
    db_session: AsyncSession, transport_id: int, data: AdminTransportUpdate
) -> TransportRead:
    async with db_session as session:
        async with session.begin():
            transport_dal = TransportDAL(session)
            validate_data = {k: v for k, v in data.model_dump().items() if v}
            transport = await transport_dal.update_(transport_id, validate_data)
            return TransportRead(**transport.get_transport_info())


async def _admin_delete_transport(db_session: AsyncSession, transport_id: int) -> dict:
    async with db_session as session:
        async with session.begin():
            admin_transport_dal = AdminTransportDal(session)
            await admin_transport_dal.delete_(transport_id)
            return {"message": "success"}
