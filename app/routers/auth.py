from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from typing import Annotated
from schemas.auth import Token as SchemaToken, Login as SchemaLogin
from schemas.user import User as SchemaUser
from dependencies.db import get_db
import actions.auth as actions_auth
from dependencies.jwt.get_current_user import get_current_active_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"message": "Could not validate credentials"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"message": "Internal server error."},
    },
)


@router.post("/login", response_model=SchemaToken)
async def login_for_access_token(
    creedentials: SchemaLogin, db: Session = Depends(get_db)
):
    user = actions_auth.login(db, creedentials.email, creedentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    return actions_auth.login_access_token(user.email)


@router.get("/me", response_model=SchemaUser)
async def read_auth_me(
    current_user: Annotated[SchemaUser, Depends(get_current_active_user)],
):
    return current_user
