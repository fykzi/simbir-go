from fastapi import APIRouter, Path
from typing import List, Optional
from api.v1.rent.shemas import RentCreate, RentRead, Coordinates, RentTransportRead
from api.v1.admin_rents.services import (
    _get_rent_info,
    _admin_transport_history,
    _admin_end_rent,
    _admin_create_rent,
    _admin_update_rent,
    _admin_delete_rent,
)
from api.utils import AdminDep, DBSessionDep
from api.v1.rent.services import _my_history
from api.v1.admin_rents.shemas import AdminRentCreate, AdminUpdateRent


admin_rent_router = APIRouter()


@admin_rent_router.get("/{rentId}")
async def get_transport(
    db_session: DBSessionDep, is_admin: AdminDep, rent_id: int = Path(alias="rentId")
) -> RentRead | List:
    return await _get_rent_info(db_session, rent_id)


@admin_rent_router.get("/UserHistory/{userId}")
async def get_user_history(
    db_session: DBSessionDep, is_admin: AdminDep, user_id: int = Path(alias="userId")
) -> Optional[List[RentRead]]:
    return await _my_history(db_session, user_id)


@admin_rent_router.get("/TransportHistory/{transportId}")
async def get_transport_history(
    db_session: DBSessionDep,
    is_admin: AdminDep,
    transport_id: int = Path(alias="transportId"),
) -> Optional[List[RentRead]]:
    return await _admin_transport_history(db_session, transport_id)


@admin_rent_router.post("/Rent/End/{rentId}")
async def end_rent(
    db_session: DBSessionDep,
    is_admin: AdminDep,
    data: Coordinates,
    rent_id: int = Path(alias="rentId"),
) -> None:
    return await _admin_end_rent(db_session, rent_id, data)


@admin_rent_router.post("/Rent")
async def create(db_session: DBSessionDep, is_admin: AdminDep, data: AdminRentCreate):
    return await _admin_create_rent(db_session, data)


@admin_rent_router.put("/Rent/{id}")
async def admin_update_rent(
    db_session: DBSessionDep, is_admin: AdminDep, data: AdminUpdateRent, id: int
) -> Optional[RentRead]:
    return await _admin_update_rent(db_session, id, data)


@admin_rent_router.delete("/Rent/{rentId}")
async def delete_rent(
    db_session: DBSessionDep, is_admin: AdminDep, rent_id: int = Path(alias="rentId")
) -> dict:
    return await _admin_delete_rent(db_session, rent_id)
