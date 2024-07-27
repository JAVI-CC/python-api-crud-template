from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
import actions.user as actions_user
from database import engine
import dependencies.jwt.configs as jwt_config
import dependencies.http_exceptions as http_except
from schemas.auth import TokenData as SchemaTokenData
from schemas.user import User as SchemaUser


async def get_current_user(token: Annotated[str, Depends(jwt_config.oauth2_scheme)]):

    try:
        payload = jwt.decode(
            token, jwt_config.SECRET_KEY, algorithms=[jwt_config.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = SchemaTokenData(username=username)
    except InvalidTokenError:
        raise http_except.credentials_exception

    user = actions_user.get_user_by_email(Session(engine), token_data.username)
    if user is None or user.is_active is False:
        raise http_except.forbidden_exception
    return user


async def get_current_verified_user(
    token: Annotated[str, Depends(jwt_config.oauth2_scheme)]
):

    try:
        payload = jwt.decode(
            token, jwt_config.SECRET_KEY, algorithms=[jwt_config.ALGORITHM]
        )
        username: str = payload.get("sub")
        token_data = SchemaTokenData(username=username)
    except InvalidTokenError:
        raise http_except.credentials_exception

    user = actions_user.get_user_by_email(Session(engine), token_data.username)
    if user is None or user.is_active is False or not user.email_verified_at:
        raise http_except.forbidden_exception
    return user


async def get_current_active_user(
    current_user: Annotated[SchemaUser, Depends(get_current_user)],
):

    return current_user


async def get_current_active_verified_user(
    current_user: Annotated[SchemaUser, Depends(get_current_verified_user)],
):

    return current_user
