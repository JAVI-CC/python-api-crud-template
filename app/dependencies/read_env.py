import os
from dotenv import load_dotenv

load_dotenv()
env = os.getenv("APP_ENV", "dev")
load_dotenv(f".env.{env}")


def getenv(key: str, default="") -> str:
    return os.getenv(key, default)
