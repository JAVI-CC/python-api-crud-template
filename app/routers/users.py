from fastapi import Depends, HTTPException, APIRouter, status, UploadFile
from sqlalchemy.orm import Session
from typing import Annotated
from schemas.auth import Token as SchemaToken
from schemas.user import (
    User as SchemaUser,
    UserCreate as SchemaUserCreate,
    UserUpdate as SchemaUserUpdate,
    UserUpdatePassword as SchemaUserUpdatePassword,
)
import actions.user as actions_user
import actions.auth as actions_auth
from dependencies.db import get_db
from dependencies.jwt.get_current_user import get_current_active_user
from dependencies.user.validations_before_actions import (
    is_admin_user,
    update_rol_admin,
    delete_user_not_also,
    validate_user_image_avatar,
)


router = APIRouter(
    prefix="/users",
    tags=["user"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"message": "Could not validate credentials."},
        status.HTTP_404_NOT_FOUND: {"message": "User not found."},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"message": "Internal server error."},
    },
)


@router.get(
    "/",
    response_model=list[SchemaUser],
    dependencies=[Depends(get_current_active_user)],
)
async def show_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = actions_user.get_users(db, skip, limit)
    return users


@router.get(
    "/{user_id}",
    response_model=SchemaUser,
    dependencies=[Depends(get_current_active_user)],
)
async def show_user(user_id: str, db: Session = Depends(get_db)):
    db_user = actions_user.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post(
    "/",
    response_model=SchemaUser,
    dependencies=[Depends(is_admin_user)],
)
async def add_user(user: SchemaUserCreate, db: Session = Depends(get_db)):
    return actions_user.create_user(db, user)


@router.put(
    "/{user_id}",
    response_model=SchemaUser,
    dependencies=[Depends(is_admin_user)],
)
async def update_values_user(
    current_user: Annotated[SchemaUser, Depends(get_current_active_user)],
    user_id: str,
    user: SchemaUserUpdate,
    db: Session = Depends(get_db),
):

    update_rol_admin(current_user, user_id, user)  # Validation

    db_user = actions_user.update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete(
    "/{user_id}",
    response_model=None,
    status_code=204,
    dependencies=[Depends(is_admin_user)],
)
async def drop_user(
    current_user: Annotated[SchemaUser, Depends(get_current_active_user)],
    user_id: str,
    db: Session = Depends(get_db),
):

    delete_user_not_also(current_user.id, user_id)  # Validation

    is_drop_user = await actions_user.delete_user(db, user_id)

    if is_drop_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {}


@router.patch(
    "/update_password",
    response_model=SchemaToken,
    dependencies=[Depends(get_current_active_user)],
)
async def update_password_current_user(
    current_user: Annotated[SchemaUser, Depends(get_current_active_user)],
    user: SchemaUserUpdatePassword,
    db: Session = Depends(get_db),
):
    is_update_password = actions_user.update_password_user(db, current_user, user)

    if is_update_password is False:
        raise HTTPException(status_code=404, detail="User not found")

    access_token = actions_auth.generate_access_token(data={"sub": current_user.email})

    return SchemaToken(access_token=access_token, token_type="bearer")


@router.post(
    "/upload_avatar",
    response_model=SchemaUser,
    dependencies=[Depends(get_current_active_user)],
)
async def upload_avatar(
    current_user: Annotated[SchemaUser, Depends(get_current_active_user)],
    file: UploadFile,
    db: Session = Depends(get_db),
):

    validate_user_image_avatar(file)  # Validation

    user = await actions_user.add_avatar_user(db, current_user, file)

    return user
