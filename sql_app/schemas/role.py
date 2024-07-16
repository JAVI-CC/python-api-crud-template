from pydantic import BaseModel

class RoleBase(BaseModel):
    id: str
    name: str

class Role(RoleBase):

    class Config:
        orm_mode = True