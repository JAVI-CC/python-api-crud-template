from pydantic import BaseModel

class RoleBase(BaseModel):
    id: str
    name: str

class RoleCreate(RoleBase):
    pass # para crear la clase

class RoleCreateSeeder(RoleBase):
    pass # para crear la clase

class Role(RoleBase):
    
    class Config:
        from_attributes = True