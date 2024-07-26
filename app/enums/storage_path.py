from enum import Enum
from dependencies.root_dir import ROOT_DIR
from dependencies.read_env import getenv

INIT = f"{ROOT_DIR}/storage"

class StoragePath(Enum):
    AVATARS = f"{INIT}/avatars"
    AVATARS_URL = f"{getenv("APP_URL")}/avatars"
    AVATAR_DEFAULT = f"{INIT}/avatar_default.png"
    TEMPLATES_PDF = f"{ROOT_DIR}/exports/pdf/templates"
    TEMPLATES_HTML = f"{ROOT_DIR}/mail/templates"
    STATIC_IMAGES = f"{ROOT_DIR}/static/images"
    
    STATIC_IMAGES_URL = f"{getenv("APP_URL")}/static"

