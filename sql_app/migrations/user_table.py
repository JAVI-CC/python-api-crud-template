import sys
from os import path

ROOT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from models import user as User
from database import engine
import sql_app.migrations.init as init

User.Base.metadata.create_all(bind=engine)
