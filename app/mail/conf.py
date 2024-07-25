from fastapi_mail import ConnectionConfig
from dependencies.read_env import getenv
from enums.storage_path import StoragePath


conf_mail = ConnectionConfig(
    MAIL_USERNAME=getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=getenv("MAIL_PASSWORD"),
    MAIL_FROM=getenv("MAIL_FROM_ADDRESS"),
    MAIL_PORT=getenv("MAIL_PORT"),
    MAIL_SERVER=getenv("MAIL_SERVER"),
    MAIL_FROM_NAME=getenv("MAIL_FROM_NAME"),
    MAIL_STARTTLS=(
        True if getenv("MAIL_STARTTLS", "True").lower() in ("true", "1", "t") else False
    ),
    MAIL_SSL_TLS=(
        True if getenv("MAIL_SSL_TLS", "False").lower() in ("true", "1", "t") else False
    ),
    USE_CREDENTIALS=(
        True
        if getenv("MAIL_USE_CREDENTIALS", "True").lower() in ("true", "1", "t")
        else False
    ),
    TEMPLATE_FOLDER=f"{StoragePath.TEMPLATES_HTML.value}/",
)
