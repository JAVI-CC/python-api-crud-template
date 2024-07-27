from fastapi import Depends, HTTPException, APIRouter, status, Request
from sqlalchemy.orm import Session
import i18n
import actions.role as actions_role
from dependencies.db import get_db
import dependencies.user.validations_before_actions as validations_actions
from dependencies.slowapi_init import limiter, limit_value
from schemas.role import Role as SchemaRole


router = APIRouter(
    prefix="/roles",
    tags=["role"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "message": f"{i18n.t('could_not_validate_credentials')}"
        },
        status.HTTP_404_NOT_FOUND: {"message": f"{i18n.t('role_not_found')}"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "message": f"{i18n.t('internal_server_error')}"
        },
    },
    dependencies=[Depends(validations_actions.is_admin_user)],
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
        raise HTTPException(status_code=404, detail=f"{i18n.t('role_not_found')}")
    return db_role
