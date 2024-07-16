from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from schemas.user import User as SchemaUser, UserCreate as SchemaUserCreate
from actions.user import get_user, get_users, get_user_by_email
from dependencies.db import get_db

router = APIRouter(
    prefix="/users",
    tags=["user"],
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {"message": "Internal server error."}},
)


@router.post("/", response_model=SchemaUser)
async def create_user(user: SchemaUserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@router.get("/", response_model=list[SchemaUser])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=SchemaUser)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
