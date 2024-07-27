from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
import jwt
import actions.user as actions_user
import dependencies.jwt.configs as jwt_config
import dependencies.http_exceptions as http_except
from dependencies.hash_password import verify_password
from schemas.auth import Token as SchemaToken


def login(db: Session, email: str, password: str):

    user = actions_user.get_user_by_email(db, email)

    if not user:
        raise http_except.email_not_exists_exception
    elif not user.is_active:
        raise http_except.forbidden_exception
    elif not verify_password(password, user.hashed_password):
        raise http_except.login_incorrect_exception

    return user


def login_access_token(user_email: str):

    access_token_expires = timedelta(minutes=jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_access_token(
        data={"sub": user_email}, expires_delta=access_token_expires
    )

    return SchemaToken(access_token=access_token, token_type="bearer")


def generate_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, jwt_config.SECRET_KEY, algorithm=jwt_config.ALGORITHM
    )

    return encoded_jwt
