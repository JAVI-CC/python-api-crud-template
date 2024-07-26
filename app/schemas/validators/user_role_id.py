from sqlalchemy.orm import Session
import i18n
from database import engine
from actions.role import get_role


def role_id_exists(id: str):
    with Session(engine) as db:
        if not get_role(db, id):
            raise ValueError(i18n.t("role_id_not_exists"))
        return id
