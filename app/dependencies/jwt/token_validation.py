# token_validation.py
from fastapi import HTTPException
import jwt
import i18n
import dependencies.jwt.configs as jwt_config


# Function to verify the access token extracted from the request
def verify_access_token(request):
    # Extract the token from the request
    token = get_token_from_request(request)

    try:
        # Decode and verify the token using the secret key and algorithm
        payload = jwt.decode(token, jwt_config.SECRET_KEY, algorithms=[jwt_config.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # Raise an HTTPException with status code 401 if the token has expired
        raise HTTPException(status_code=401, detail=f"{i18n.t('token_expired')}")
    except jwt.InvalidTokenError:
        # Raise an HTTPException with status code 401 if the token is invalid
        raise HTTPException(status_code=401, detail=f"{i18n.t('invalid_token')}")


def get_token_from_request(request):
    return request.headers.get("Authorization")
