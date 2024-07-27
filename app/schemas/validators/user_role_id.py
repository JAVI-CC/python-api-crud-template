from sqlalchemy.orm import Session
import i18n
from database import engine
import actions.role as actions_role


def role_id_exists(id: str):
    with Session(engine) as db:
        if not actions_role.get_role(db, id):
            raise ValueError(i18n.t("role_id_not_exists"))
        return id
