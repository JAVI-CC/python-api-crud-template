from fastapi import Depends, HTTPException, APIRouter, status, Request
from sqlalchemy.orm import Session
from schemas.role import Role as SchemaRole
import actions.role as actions_role
from dependencies.db import get_db
from dependencies.user.validations_before_actions import is_admin_user
from dependencies.slowapi_init import limiter, limit_value


router = APIRouter(
    prefix="/roles",
    tags=["role"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"message": "Could not validate credentials."},
        status.HTTP_404_NOT_FOUND: {"message": "Role not found."},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"message": "Internal server error."},
    },
    dependencies=[Depends(is_admin_user)],
)


@router.get("/", response_model=list[SchemaRole])
@limiter.limit(limit_value)
async def show_roles(request: Request, db: Session = Depends(get_db)):
    roles = actions_role.get_roles(db)
    return roles


@router.get("/{role_id}", response_model=SchemaRole)
@limiter.limit(limit_value)
async def show_role(request: Request, role_id: str, db: Session = Depends(get_db)):
    db_role = actions_role.get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found.")
    return db_role
