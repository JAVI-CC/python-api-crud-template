from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from schemas.role import Role as SchemaRole
from actions.role import get_role, get_roles
from dependencies.db import get_db

router = APIRouter(
    prefix="/roles",
    tags=["role"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"message": "Internal server error."}
    },
)


@router.get("/", response_model=list[SchemaRole])
async def get_roles(db: Session = Depends(get_db)):
    roles = get_roles(db)
    return roles


@router.get("/{role_id}", response_model=SchemaRole)
async def get_role(role_id: int, db: Session = Depends(get_db)):
    db_role = get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role
