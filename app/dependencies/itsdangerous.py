from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, SignatureExpired
from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session
import i18n
import actions.user as actions_user
from dependencies.read_env import getenv
import dependencies.jwt.configs as jwt_config
import dependencies.http_exceptions as http_except

token_algo = URLSafeTimedSerializer(
    jwt_config.SECRET_KEY, salt="Email_Verification_&_Forgot_password"
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
        raise http_except.token_expiration_exception
    except BadTimeSignature:
        raise http_except.token_expiration_exception
    return user
