from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(String(150), primary_key=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    
    users = relationship("User", back_populates="role")