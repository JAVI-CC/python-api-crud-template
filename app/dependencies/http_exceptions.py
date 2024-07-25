from fastapi import HTTPException, status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)

forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You do not have permissions to access",
)

user_not_verified_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User not verified",
)

login_incorrect_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Email or password incorrect",
)

email_not_exists_exception = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="The email is not registered",
)

token_expiration_exception = HTTPException(
    status_code=406, detail="Token for Email Verification has expired."
)
