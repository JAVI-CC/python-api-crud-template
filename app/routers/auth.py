from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter, status, Request
from sqlalchemy.orm import Session
import i18n
import actions.auth as actions_auth
from dependencies.db import get_db
import dependencies.jwt.get_current_user as jwt_user
from dependencies.slowapi_init import limiter, limit_value
from schemas.auth import Token as SchemaToken, Login as SchemaLogin
from schemas.user import User as SchemaUser

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "message": f"{i18n.t('could_not_validate_credentials')}"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "message": f"{i18n.t('internal_server_error')}"
        },
    },
)


@router.post("/login", response_model=SchemaToken)
@limiter.limit(limit_value)
async def login_for_access_token(
    request: Request, creedentials: SchemaLogin, db: Session = Depends(get_db)
):
    user = actions_auth.login(db, creedentials.email, creedentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{i18n.t('could_not_validate_credentials')}",
        )

    return actions_auth.login_access_token(user.email)


@router.get("/me", response_model=SchemaUser)
@limiter.limit(limit_value)
async def read_auth_me(
    request: Request,
    current_user: Annotated[SchemaUser, Depends(jwt_user.get_current_active_user)],
):

    return current_user
