from sqlalchemy.orm import Session
import i18n
from database import engine
from actions.user import get_user_by_email


def user_email_exists(email: str):
    with Session(engine) as db:
        if get_user_by_email(db, email):
            raise ValueError(i18n.t("the_email_is_already_registered"))
        return email
