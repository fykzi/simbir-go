from fastapi import APIRouter, Depends, Query
from api.utils import DBSessionDep, AdminDep
from typing import Optional, List, Literal
from api.v1.admin_transports.shemas import (
    AdmintransportTypes,
    AdminTransportCreate,
    AdminTransportUpdate,
)
from api.v1.transport.shemas import TransportRead
from api.v1.admin_transports.services import (
    _get_transports,
    _add_transport,
    _update_transport,
    _admin_delete_transport,
)
from api.v1.transport.services import _get_transport

admin_transport_router = APIRouter()


@admin_transport_router.delete("/{id}")
async def delete_transport(
    db_session: DBSessionDep, is_admin: AdminDep, id: int
) -> dict:
    return await _admin_delete_transport(db_session, id)


@admin_transport_router.get("/{id}")
async def get_transport(db_session: DBSessionDep, is_admin: AdminDep, id: int):
    return await _get_transport(db_session, id)


@admin_transport_router.post("/")
async def add_transport(
    db_session: DBSessionDep, is_admin: AdminDep, data: AdminTransportCreate
) -> TransportRead:
    return await _add_transport(db_session, data)


@admin_transport_router.put("/{id}")
async def update_transport(
    db_session: DBSessionDep, is_admin: AdminDep, id: int, data: AdminTransportUpdate
) -> TransportRead:
    return await _update_transport(db_session, id, data)


@admin_transport_router.get("/")
async def get_transports(
    db_session: DBSessionDep,
    is_admin: AdminDep,
    start: int,
    count: int,
    transport_type: AdmintransportTypes = Query(alias="transportTypes"),
) -> Optional[List[TransportRead]]:
    return await _get_transports(db_session, start, count, transport_type)
