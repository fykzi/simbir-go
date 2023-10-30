from sqlalchemy.ext.asyncio import AsyncSession
from api.v1.rent.shemas import RentRead
from database.dals import AdminRentDAL
from typing import List, Optional
from fastapi import HTTPException, status
from api.v1.rent.shemas import Coordinates
from api.v1.admin_rents.shemas import AdminRentCreate, AdminUpdateRent


async def _get_rent_info(db_session: AsyncSession, rent_id: int) -> RentRead | List:
    async with db_session as session:
        async with session.begin():
            admin_rent_dal = AdminRentDAL(session)
            rent = await admin_rent_dal.get_rent_by_id(rent_id)
            # print(rent.get_rent_info())
            if rent:
                return RentRead(**rent.get_rent_info())
            return []


async def _admin_transport_history(
    db_session: AsyncSession, transport_id: int
) -> List[RentRead]:
    async with db_session as session:
        async with session.begin():
            rent_dal = AdminRentDAL(session)
            result = await rent_dal.get_transport_rents(transport_id)
            try:
                return [RentRead(**i[0].get_rent_info()) for i in result]
            except AttributeError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to obtain rental vehicle",
                )


async def _admin_end_rent(
    db_session: AsyncSession, rent_id: int, data: Coordinates
) -> dict:
    async with db_session as session:
        async with session.begin():
            rent_dal = AdminRentDAL(session)
            await rent_dal.end_rent(rent_id, data.model_dump())


async def _admin_create_rent(
    db_session: AsyncSession, data: AdminRentCreate
) -> RentRead:
    async with db_session as session:
        async with session.begin():
            data = data.model_dump()
            if data.get("final_price") is None:
                del data["final_price"]
            if data.get("time_end") is None:
                del data["time_end"]
            admin_rent_dal = AdminRentDAL(session)
            rent = await admin_rent_dal.create_(data)
            return RentRead(**rent.get_rent_info())


async def _admin_update_rent(
    db_session: AsyncSession, rent_id: int, data: AdminUpdateRent
) -> Optional[RentRead]:
    async with db_session as session:
        async with session.begin():
            validate_data = {
                k: v for k, v in data.model_dump().items() if v is not None
            }
            admin_rent_dal = AdminRentDAL(session)
            res = await admin_rent_dal.update_(rent_id, validate_data)
            if res:
                return RentRead(**res.get_rent_info())


async def _admin_delete_rent(db_session: AsyncSession, rent_id: int) -> dict:
    async with db_session as session:
        async with session.begin():
            admin_rent_dal = AdminRentDAL(session)
            await admin_rent_dal.delete_(rent_id)
            return {"message": "success"}
