from fastapi import Depends, HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from typing import Annotated
import i18n
from database import engine
from schemas.user import User as SchemaUser, UserUpdate as SchemaUserUpdate
from enums.rol_type import RolType
from dependencies.jwt.get_current_user import get_current_active_verified_user
from actions.user import count_admin_users
from dependencies.http_exceptions import forbidden_exception


def is_admin_user(
    current_user: Annotated[SchemaUser, Depends(get_current_active_verified_user)],
):

    if current_user.role.id != RolType.ADMIN.value:
        raise forbidden_exception

    return current_user


def update_rol_admin(
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
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{i18n.t('there_must_be_at_least_1_administrator')}",
        )

    return True


def delete_user_not_also(current_user_id: str, update_user_id: str):

    if current_user_id == update_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{i18n.t('you_cannot_eliminate_yourself')}",
        )

    return True


def validate_user_image_avatar(file: UploadFile):
    FILE_SIZE = 4194304  # 4MB

    accepted_file_types = ["image/png", "image/jpeg", "image/jpg", "png", "jpeg", "jpg"]

    if file.content_type not in accepted_file_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"{i18n.t('unsupported_file_type')}",
        )

    if file.size > FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=f"{i18n.t('too_large')}"
        )
    
    return True
