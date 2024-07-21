from sqlalchemy.orm import Session
from database import engine
from actions.role import get_role


def role_id_exists(id: str):
    with Session(engine) as db:
        if not get_role(db, id):
            raise ValueError("role_id not exists.")
        return id
