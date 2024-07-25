from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from database import engine
import actions.user as actions_user
from schemas.auth import TokenData as SchemaTokenData
from schemas.user import User as SchemaUser
import actions.user as actions_user
from dependencies.jwt.configs import SECRET_KEY, ALGORITHM, oauth2_scheme
from dependencies.http_exceptions import credentials_exception, forbidden_exception


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = SchemaTokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = actions_user.get_user_by_email(Session(engine), token_data.username)
    if user is None or user.is_active is False:
        raise forbidden_exception
    return user

async def get_current_verified_user(token: Annotated[str, Depends(oauth2_scheme)]):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_data = SchemaTokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = actions_user.get_user_by_email(Session(engine), token_data.username)
    if user is None or user.is_active is False or not user.email_verified_at:
        raise forbidden_exception
    return user


async def get_current_active_user(
    current_user: Annotated[SchemaUser, Depends(get_current_user)],
):

    return current_user

async def get_current_active_verified_user(
    current_user: Annotated[SchemaUser, Depends(get_current_verified_user)],
):

    return current_user