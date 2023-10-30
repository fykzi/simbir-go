from fastapi import APIRouter, Depends
from api.utils import DBSessionDep, AdminDep
from typing import Optional, List, Literal
from api.v1.user.shemas import UserRead
from api.v1.admin_accounts.services import _get_user_accounts, _delete_account
from api.v1.user.services import _user_me, _user_sign_up, _user_update
from api.v1.admin_accounts.shemas import AdminUserCreate, AdminUserUpdate

admin_account_router = APIRouter()


@admin_account_router.get("/")
async def get_user_accounts(
    db_session: DBSessionDep, is_admin: AdminDep, start: int, count: int
) -> Optional[List[UserRead]]:
    return await _get_user_accounts(db_session, start, count)


@admin_account_router.get("/{id}")
async def get_user_by_id(
    db_session: DBSessionDep, is_admin: AdminDep, id: int
) -> UserRead:
    return await _user_me(db_session, id)


@admin_account_router.post("/")
async def user_sign_up(
    db_session: DBSessionDep, is_admin: AdminDep, data: AdminUserCreate
) -> UserRead:
    return await _user_sign_up(db_session, data)


@admin_account_router.put("/{id}")
async def update_account(
    db_session: DBSessionDep, is_admin: AdminDep, id: int, data: AdminUserUpdate
) -> UserRead:
    return await _user_update(db_session, data, id)


# TODO
@admin_account_router.delete("/{id}")
async def delete_account(
    db_session: DBSessionDep, is_admin: AdminDep, id: int
) -> dict[Literal["message"], str]:
    return await _delete_account(db_session, id)
