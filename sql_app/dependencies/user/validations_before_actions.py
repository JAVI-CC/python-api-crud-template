from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from database import engine
from schemas.user import User as SchemaUser, UserUpdate as SchemaUserUpdate
from enums.rol_type import RolType
from dependencies.jwt.get_current_user import get_current_user
from actions.user import count_admin_users
from dependencies.http_exceptions import forbidden_exception

forbidden_update_admin_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="There must be at least 1 administrator",
)

forbidden_delete_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You cannot eliminate yourself",
)


async def is_admin_user(
    current_user: Annotated[SchemaUser, Depends(get_current_user)],
):

    if current_user.role.id != RolType.ADMIN.value:
        raise forbidden_exception

    return current_user


async def update_rol_admin(
    current_user: SchemaUser, update_user_id: str, update_user: SchemaUserUpdate
):

    count_admins = count_admin_users(Session(engine))

    if (
        count_admins == 1
        and update_user_id == current_user.id
        and (
            update_user.role_id == RolType.USER.value or update_user.is_active is False
        )
    ):
        raise forbidden_update_admin_exception

    return True


async def update_rol_admin(
    current_user: SchemaUser, update_user_id: str, update_user: SchemaUserUpdate
):

    count_admins = count_admin_users(Session(engine))

    if (
        count_admins == 1
        and update_user_id == current_user.id
        and (
            update_user.role_id == RolType.USER.value or update_user.is_active is False
        )
    ):
        raise forbidden_update_admin_exception

    return True


async def delete_user_not_also(current_user_id: str, update_user_id: str):

    if current_user_id == update_user_id:
        raise forbidden_delete_exception

    return True
