import os
from dependencies.read_env import getenv

os.environ["TZ"] = getenv("TIMEZONE", "Europe/London")
