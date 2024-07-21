from sqlalchemy.orm import Session
from database import engine
from actions.user import get_user_by_email


def user_email_exists(email: str):
    with Session(engine) as db:
        if get_user_by_email(db, email):
            raise ValueError("The email is already registered.")
        return email
