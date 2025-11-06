from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import User as UserSchema, UserOut
from models import User
from utils import hash_password

def create_user(payload: UserSchema, db: Session = Depends(get_db)):
    # Hash the password before storing
    hashed_password = hash_password(payload.password)
    new_user = User(username=payload.username, email=payload.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user