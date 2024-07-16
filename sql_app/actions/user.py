from sqlalchemy.orm import Session
from models.user import User as ModelUser
from schemas.user import UserCreate as SchemaUserCreate
from datetime import datetime
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: str):
    return db.query(ModelUser.User).filter(ModelUser.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(ModelUser.User).filter(ModelUser.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ModelUser.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: SchemaUserCreate, role_id: str):
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # db_user = ModelUser.User(
    #     name=user.name,
    #     surnames=user.surnames,
    #     age=user.age,
    #     is_active=user.is_active,
    #     email=user.email,
    #     hashed_password=user.password,
    #     created_at=date_now,
    #     updated_at=date_now,
    # )

    db_user = ModelUser.User(
        # **user.model_dump(exclude={"created_at", "updated_at"}),
        **user.model_dump(),
        id=uuid.uuid4(),
        hashed_password=pwd_context.hash(user.password),
        role_id=role_id,
        created_at=date_now,
        updated_at=date_now
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
