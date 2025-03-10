# loginservice/api/routers/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from loginservice.model.schema import UserCreate, UserLogin
from loginservice.model.user_model import User
from loginservice.adaptor.database import get_db_connection, SessionLocal
from loginservice.service.auth_service import (
    get_user_by_username,
    create_user,
    login_user,
    view_users
)

router = APIRouter()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, added_by: str, db: Session = Depends(get_db)):
    # Validate the user who is adding the new user
    adder = get_user_by_username(db, added_by)
    if not adder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User who is adding not found")
    if adder.role == 'admin' and user.role != 'user':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins can only add users with 'user' role")
    if adder.role == 'user':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Users are not allowed to add new users")

    # Create the new user
    return create_user(db, user, added_by)


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Authenticate the user and generate an access token
    return login_user(db, user.username, user.password)


@router.get("/users")
def view_users(db: Session = Depends(get_db)):
    # Retrieve a list of all users
    return view_users(db)