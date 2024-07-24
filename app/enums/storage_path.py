from enum import Enum
from dependencies.root_dir import ROOT_DIR

INIT = f"{ROOT_DIR}/storage"

class StoragePath(Enum):
    AVATARS = f"{INIT}/avatars"
    AVATAR_DEFAULT = f"{INIT}/avatar_default.png"
