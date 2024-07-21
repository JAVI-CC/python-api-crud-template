from fastapi.security import OAuth2PasswordBearer
from dependencies.read_env import getenv

SECRET_KEY = getenv("JWT_SECRET_KEY")
ALGORITHM = getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
