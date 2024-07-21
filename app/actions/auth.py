from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import jwt
from dependencies.hash_password import verify_password
from dependencies.jwt.configs import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import actions.user as actions_user
from schemas.auth import Token as SchemaToken
import actions.user as actions_user


def login(db: Session, email: str, password: str):

    user = actions_user.get_user_by_email(db, email)

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def login_access_token(user_email: str):

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
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
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
