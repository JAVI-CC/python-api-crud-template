from fastapi import HTTPException, status
import i18n

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"{i18n.t('could_not_validate_credentials')}",
)

forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail=f"{i18n.t('you_do_not_have_permissions_to_access')}",
)

user_not_verified_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail=f"{i18n.t('user_not_verified')}",
)

login_incorrect_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"{i18n.t('email_or_password_incorrect')}",
)

email_not_exists_exception = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail=f"{i18n.t('the_email_is_not_registered')}",
)

token_expiration_exception = HTTPException(
    status_code=406, detail=f"{i18n.t('token_for_email_verification_has_expired')}"
)
