from sqlalchemy.orm import Session
from models.role import Role as ModelRole


def get_role(db: Session, role_id: str):
    return db.query(ModelRole.Role).filter(ModelRole.id == role_id).first()


def get_roles(db: Session):
    return db.query(ModelRole.Role).all()
