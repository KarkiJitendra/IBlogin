from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from loginservice.model.schema import UserCreate, UserLogin
from loginservice.api.routers.user_service import UserService
from loginservice.adaptor.database import get_db_connection as get_db

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, added_by: str, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.validate_and_create_user(user, added_by)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.validate_and_login_user(user)

@router.get("/users")
def view_users(db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.get_all_users()