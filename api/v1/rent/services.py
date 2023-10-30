from fastapi import HTTPException, status
from api.v1.rent.shemas import RentCreate, RentRead, Coordinates, RentTransportRead
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database.dals import RentDAL, TransportDAL
from api.utils import check_transport, is_transport_owner
from datetime import datetime


async def _new_rent(
    db_session: AsyncSession, user_id: int, transport_id: int, data: RentCreate
) -> RentRead:
    async with db_session as session:
        async with session.begin():
            await check_transport(session, user_id, transport_id)
            rent_dal = RentDAL(session)
            data = data.model_dump()
            data["renter_id"] = user_id
            data["transport_id"] = transport_id
            data["time_start"] = datetime.now()
            new_rent = await rent_dal.create_(data)
            return RentRead(**new_rent.get_rent_info())


async def _my_history(db_session: AsyncSession, user_id: int) -> List[RentRead]:
    async with db_session as session:
        async with session.begin():
            rent_dal = RentDAL(session)
            user_history = await rent_dal.get_user_rents(user_id)
            result = [RentRead(**rent[0].get_rent_info()) for rent in user_history]
            return result


async def _end_rent(
    db_session: AsyncSession, user_id: int, rent_id: int, data: Coordinates
) -> dict:
    async with db_session as session:
        async with session.begin():
            rent_dal = RentDAL(session)
            if not await rent_dal.is_renter(rent_id, user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You are not a renter",
                )
            await rent_dal.end_rent(rent_id, data.model_dump())


async def _get_transport(db_session: AsyncSession) -> List[RentTransportRead]:
    async with db_session as session:
        async with session.begin():
            transport_dal = TransportDAL(session)
            result = await transport_dal.get_transports()
            return [
                RentTransportRead(**i[0].get_transport_info_for_rent_search())
                for i in result
            ]


async def _transport_history(
    db_session: AsyncSession, user_id: int, transport_id: int
) -> List[RentRead]:
    async with db_session as session:
        async with session.begin():
            transport_dal = TransportDAL(session)
            if not await is_transport_owner(transport_dal, user_id, transport_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This is not your transport",
                )
            rent_dal = RentDAL(session)
            result = await rent_dal.get_transport_rents(transport_id)
            try:
                return [RentRead(**i[0].get_rent_info()) for i in result]
            except AttributeError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to obtain rental vehicle",
                )


async def _get_rent_info(
    db_session: AsyncSession, user_id: int, rent_id: int
) -> RentRead:
    async with db_session as session:
        async with session.begin():
            rent_dal = RentDAL(session)
            if not (rent := await rent_dal.is_renter_or_owner(rent_id, user_id)):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You are not renter or owner",
                )
            return RentRead(**rent.get_rent_info())
