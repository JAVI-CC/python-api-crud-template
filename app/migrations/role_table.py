import sys
from os import path

ROOT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from models import role as Role
from database import engine

Role.Base.metadata.create_all(bind=engine)
