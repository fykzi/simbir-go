from fastapi import APIRouter, Path
from typing import List
from api.v1.rent.shemas import RentCreate, RentRead, Coordinates, RentTransportRead
from api.v1.rent.services import (
    _new_rent,
    _my_history,
    _end_rent,
    _get_transport,
    _transport_history,
    _get_rent_info,
)
from api.utils import UserDep, DBSessionDep


rent_router = APIRouter()


@rent_router.get("/Transport")
async def get_transport(db_session: DBSessionDep) -> List[RentTransportRead]:
    return await _get_transport(db_session)


@rent_router.get("/MyHistory")
async def my_history(user_id: UserDep, db_session: DBSessionDep) -> List[RentRead]:
    return await _my_history(db_session, user_id)


@rent_router.get("/{rentId}")
async def get_rent_info(
    db_session: DBSessionDep, user_id: UserDep, rent_id: int = Path(alias="rentId")
) -> RentRead:
    return await _get_rent_info(db_session, user_id, rent_id)


@rent_router.get("/TransportHistory/{transportId}")
async def transport_history(
    db_session: DBSessionDep,
    user_id: UserDep,
    transport_id: int = Path(alias="transportId"),
) -> List[RentRead]:
    return await _transport_history(db_session, user_id, transport_id)


@rent_router.post("/New/{transportId}")
async def new_rent(
    data: RentCreate,
    user_id: UserDep,
    db_session: DBSessionDep,
    transport_id: int = Path(alias="transportId"),
) -> RentRead:
    return await _new_rent(db_session, user_id, transport_id, data)


@rent_router.post("/End/{rentId}")
async def end_rent(
    user_id: UserDep, rentId: int, data: Coordinates, db_session: DBSessionDep
) -> None:
    return await _end_rent(db_session, user_id, rentId, data)
