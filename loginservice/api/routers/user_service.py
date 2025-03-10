from sqlalchemy.orm import Session
from loginservice.model.schema import UserCreate, UserLogin
from loginservice.model.user_model import User
from loginservice.utils.security import pwd_context, create_access_token
from fastapi import HTTPException, status
from datetime import datetime, timedelta

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def validate_and_create_user(self, user: UserCreate, added_by: str):
        adder = self.get_user_by_username(added_by)
        if not adder:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User who is adding not found")
        if adder.role == 'admin' and user.role != 'user':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins can only add users with 'user' role")
        if adder.role == 'user':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Users are not allowed to add new users")

        hashed_password = pwd_context.hash(user.password)
        db_user = User(username=user.username, email=user.email, role=user.role, password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def validate_and_login_user(self, user: UserLogin):
        db_user = self.get_user_by_username(user.username)
        if not db_user or not pwd_context.verify(user.password, db_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        access_token = create_access_token({"sub": db_user.username}, timedelta(minutes=30))
        return {"access_token": access_token, "token_type": "bearer"}

    def get_all_users(self):
        users = self.db.query(User).all()
        return [{"username": user.username, "role": user.role} for user in users]