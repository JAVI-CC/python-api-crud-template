from sqlalchemy.orm import Session
from models.user import User as ModelUser
from schemas.user import (
    User as SchemaUser,
    UserCreate as SchemaUserCreate,
    UserUpdate as SchemaUserUpdate,
    UserUpdatePassword as SchemaUserUpdatePassword,
)
from datetime import datetime
from dependencies.hash_password import hash_password
import uuid
from enums.rol_type import RolType


def get_user(db: Session, user_id: str):
    return db.query(ModelUser).filter(ModelUser.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(ModelUser).filter(ModelUser.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ModelUser).offset(skip).limit(limit).all()


def create_user(db: Session, user: SchemaUserCreate):
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db_user = ModelUser(
        **user.model_dump(exclude={"password", "password_confirmation"}),
        id=uuid.uuid4(),
        hashed_password=hash_password(user.password),
        created_at=date_now,
        updated_at=date_now
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(db: Session, user_id: str, user: SchemaUserUpdate):

    db_user = db.query(ModelUser).filter(ModelUser.id == user_id).first()

    if db_user is None:
        return None

    for key, value in vars(user).items():
        setattr(db_user, key, value) if value or value == False else None

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: str):
    db_user = db.query(ModelUser).filter(ModelUser.id == user_id).first()

    if db_user is None:
        return None

    db.delete(db_user)
    db.commit()

    return db.query(ModelUser).filter(ModelUser.id == user_id).delete()


def update_password_user(
    db: Session, user_auth: SchemaUser, user: SchemaUserUpdatePassword
):

    db_user = db.query(ModelUser).filter(ModelUser.id == user_auth.id).first()

    if db_user is None:
        return False

    db_user.hashed_password = hash_password(user.password)

    db.commit()

    return True


def count_admin_users(db: Session):
    return db.query(ModelUser).filter(ModelUser.role_id == RolType.ADMIN.value).count()