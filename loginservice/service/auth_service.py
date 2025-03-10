from typing import Optional

from sqlalchemy.orm import Session
from loginservice.model.schema import UserCreate
from loginservice.model.user_model import User
from loginservice.utils.security import pwd_context, create_access_token
from fastapi import HTTPException
from datetime import timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# def get_user_by_username(db: Session, username: str):
#     return db.query(User).filter(User.username == username).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    # Ensure username is a string
    if not isinstance(username, str):
        raise TypeError("username must be a string")

    # Query the database for the user
    return db.query(User).filter(User.username == username).first()

# Function to create a new user
def create_user(db: Session, user: UserCreate, added_by: str):
    # Fetch the role of the user who is adding
    adder = get_user_by_username(db, added_by)

    if not adder or (adder.role == 'admin' and user.role != 'user') or (adder.role == 'user'):
        raise HTTPException(status_code=403, detail="Not authorized to add this role")

    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email, role=user.role, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Function to authenticate a user and generate an access token
def login_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)

    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}


# Function to retrieve a list of all users
def view_users(db: Session):
    return db.query(User).all()