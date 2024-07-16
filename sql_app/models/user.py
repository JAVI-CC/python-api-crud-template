from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base
from .role import Role

class User(Base):
    __tablename__ = "users"

    id = Column(String(150), primary_key=True)
    name = Column(String(50), nullable=False)
    surnames = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    email = Column(String(50), unique=True, nullable=False, index=True)
    email_verified_at = Column(DateTime, nullable=True)
    hashed_password = Column(String(150), nullable=False)
    role_id = Column(String(150), ForeignKey("roles.id"))
    avatar_name_file = Column(String(150), nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    role = relationship("Role", back_populates="users")
