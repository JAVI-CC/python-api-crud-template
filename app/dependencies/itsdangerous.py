from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, SignatureExpired
from fastapi import HTTPException, status
from pydantic import EmailStr
import i18n
from dependencies.jwt.configs import SECRET_KEY
from dependencies.read_env import getenv
import actions.user as actions_user
from sqlalchemy.orm import Session
from dependencies.http_exceptions import token_expiration_exception

token_algo = URLSafeTimedSerializer(
    SECRET_KEY, salt="Email_Verification_&_Forgot_password"
)


def generate_token(email: EmailStr):
    _token = token_algo.dumps(email)
    url = f"{getenv('APP_URL')}/users/confirm_email/{_token}"

    return url


def verify_token(token: str, db: Session):
    try:
        email = token_algo.loads(token, max_age=1800)
        user = actions_user.get_user_by_email(db, email)
        if not user or user.is_active is False:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{i18n.t('user_with_email_does_not_exist', email=email)}",
            )
    except SignatureExpired:
        raise token_expiration_exception
    except BadTimeSignature:
        raise token_expiration_exception
    return user
