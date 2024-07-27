from typing import Annotated
from datetime import datetime
from fastapi import (
    Depends,
    HTTPException,
    APIRouter,
    status,
    UploadFile,
    BackgroundTasks,
    Request,
)
from sqlalchemy.orm import Session
import i18n
import actions.user as actions_user
import actions.auth as actions_auth
from schemas.auth import Token as SchemaToken
from schemas.user import (
    User as SchemaUser,
    UserCreate as SchemaUserCreate,
    UserUpdate as SchemaUserUpdate,
    UserUpdatePassword as SchemaUserUpdatePassword,
)
from dependencies.db import get_db
import dependencies.jwt.get_current_user as jwt_user
import dependencies.user.validations_before_actions as validations_actions
import dependencies.itsdangerous as token_utils
from dependencies.slowapi_init import limiter, limit_value
from exports.excel.users import export_excel_list_users
from exports.pdf.users import export_pdf_list_users
import mail.user as mail_user

router = APIRouter(
    prefix="/users",
    tags=["user"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "message": f"{i18n.t('could_not_validate_credentials')}"
        },
        status.HTTP_404_NOT_FOUND: {"message": f"{i18n.t('user_not_found')}"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "message": f"{i18n.t('internal_server_error')}"
        },
    },
)


@router.get(
    "/",
    response_model=list[SchemaUser],
    dependencies=[Depends(jwt_user.get_current_active_verified_user)],
)
@limiter.limit(limit_value)
async def show_users(
    request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    users = actions_user.get_users(db, skip, limit)
    return users


@router.get(
    "/{user_id}",
    response_model=SchemaUser,
    dependencies=[Depends(jwt_user.get_current_active_verified_user)],
)
@limiter.limit(limit_value)
async def show_user(request: Request, user_id: str, db: Session = Depends(get_db)):
    db_user = actions_user.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"{i18n.t('user_not_found')}")
    return db_user


@router.post(
    "/",
    response_model=SchemaUser,
    dependencies=[Depends(validations_actions.is_admin_user)],
)
@limiter.limit(limit_value)
async def add_user(
    request: Request,
    background_tasks: BackgroundTasks,
    user: SchemaUserCreate,
    db: Session = Depends(get_db),
):
    new_user = actions_user.create_user(db, user)

    url_verify = token_utils.generate_token(new_user.email)

    try:
        mail_user.send_email_verify_user_background(
            background_tasks, new_user.email, url_verify
        )
    except:
        pass

    return new_user


@router.put(
    "/{user_id}",
    response_model=SchemaUser,
    dependencies=[Depends(validations_actions.is_admin_user)],
)
@limiter.limit(limit_value)
async def update_values_user(
    request: Request,
    current_user: Annotated[
        SchemaUser, Depends(jwt_user.get_current_active_verified_user)
    ],
    user_id: str,
    user: SchemaUserUpdate,
    db: Session = Depends(get_db),
):

    validations_actions.update_rol_admin(current_user, user_id, user)  # Validation

    db_user = actions_user.update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"{i18n.t('user_not_found')}")
    return db_user


@router.delete(
    "/{user_id}",
    response_model=None,
    status_code=204,
    dependencies=[Depends(validations_actions.is_admin_user)],
)
@limiter.limit(limit_value)
async def drop_user(
    request: Request,
    current_user: Annotated[
        SchemaUser, Depends(jwt_user.get_current_active_verified_user)
    ],
    user_id: str,
    db: Session = Depends(get_db),
):

    validations_actions.delete_user_not_also(current_user.id, user_id)  # Validation

    is_drop_user = await actions_user.delete_user(db, user_id)

    if is_drop_user is None:
        raise HTTPException(status_code=404, detail=f"{i18n.t('user_not_found')}")

    return {}


@router.patch(
    "/update_password",
    response_model=SchemaToken,
    dependencies=[Depends(jwt_user.get_current_active_verified_user)],
)
@limiter.limit(limit_value)
async def update_password_current_user(
    request: Request,
    current_user: Annotated[
        SchemaUser, Depends(jwt_user.get_current_active_verified_user)
    ],
    user: SchemaUserUpdatePassword,
    db: Session = Depends(get_db),
):
    is_update_password = actions_user.update_password_user(db, current_user, user)

    if is_update_password is False:
        raise HTTPException(status_code=404, detail=f"{i18n.t('user_not_found')}")

    access_token = actions_auth.generate_access_token(data={"sub": current_user.email})

    return SchemaToken(access_token=access_token, token_type="bearer")


@router.post(
    "/upload_avatar",
    response_model=SchemaUser,
    dependencies=[Depends(jwt_user.get_current_active_verified_user)],
)
@limiter.limit(limit_value)
async def upload_avatar(
    request: Request,
    current_user: Annotated[
        SchemaUser, Depends(jwt_user.get_current_active_verified_user)
    ],
    file: UploadFile,
    db: Session = Depends(get_db),
):

    validations_actions.validate_user_image_avatar(file)  # Validation

    user = await actions_user.add_avatar_user(db, current_user, file)

    return user


@router.get(
    "/export/excel",
    response_description="xlsx",
    dependencies=[Depends(validations_actions.is_admin_user)],
)
@limiter.limit(limit_value)
def export_excel_users(request: Request, db: Session = Depends(get_db)):
    users = actions_user.get_users(db)

    return export_excel_list_users(users)


@router.get(
    "/export/pdf",
    response_description="pdf",
    dependencies=[Depends(validations_actions.is_admin_user)],
)
@limiter.limit(limit_value)
def export_excel_users(request: Request, db: Session = Depends(get_db)):
    users = actions_user.get_users(db)

    return export_pdf_list_users(users)


@router.get(
    "/confirm_email/{token}",
    status_code=202,
)
@limiter.limit(limit_value)
async def verified_user_email(
    request: Request, token: str, db: Session = Depends(get_db)
):
    user_verify = token_utils.verify_token(token, db)

    if user_verify.email_verified_at:
        return {"message": f"{i18n.t('email_is_already_verified')}"}

    user_verify.email_verified_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db.add(user_verify)
    db.commit()

    return {"message": f"{i18n.t('email_forwarded_successful')}"}


@router.get(
    "/resend/confirm_email",
    status_code=200,
    dependencies=[Depends(jwt_user.get_current_active_user)],
)
@limiter.limit(limit_value)
async def resend_verify_user_email(
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: Annotated[SchemaUser, Depends(jwt_user.get_current_active_user)],
):

    if current_user.email_verified_at:
        return {"message": f"{i18n.t('email_is_already_verified')}"}

    url_verify = token_utils.generate_token(current_user.email)

    try:
        mail_user.send_email_verify_user_background(
            background_tasks, current_user.email, url_verify
        )
    except:
        raise HTTPException(
            status_code=500,
            detail=f"{i18n.t('verification_email_not_send_try_again')}",
        )

    return {"message": f"{i18n.t('email_forwarded_successful')}"}
