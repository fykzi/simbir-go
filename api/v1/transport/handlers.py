from fastapi import APIRouter
from api.v1.transport.shemas import TransportRead, TransportCreate, TransportUpdate
from api.v1.transport.services import (
    _add_transport,
    _get_transport,
    _update_transport,
    _delete_transport,
)

from api.utils import UserDep, DBSessionDep

transport_router = APIRouter()


@transport_router.get("/{id}", response_model=TransportRead)
async def get_transport(id: int, db_session: DBSessionDep) -> TransportRead:
    return await _get_transport(db_session, id)


@transport_router.post("/", response_model=TransportRead)
async def add_transport(
    data: TransportCreate, user_id: UserDep, db_session: DBSessionDep
) -> TransportRead:
    return await _add_transport(db_session, data, user_id)


@transport_router.put("/{id}", response_model=TransportRead)
async def update_transport(
    id: int, data: TransportUpdate, user_id: UserDep, db_session: DBSessionDep
) -> TransportRead:
    return await _update_transport(db_session, id, data, user_id)


@transport_router.delete("/{id}")
async def delete_transport(id: int, user_id: UserDep, db_session: DBSessionDep) -> dict:
    return await _delete_transport(db_session, id, user_id)
