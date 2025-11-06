
from schemas import User as UserSchema, UserOut
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from models import User

router= APIRouter()
@router.post('/create-user', response_model=UserOut, status_code=status.HTTP_201_CREATED, tags=["User"])
def create_user(payload: UserSchema, db: Session = Depends(get_db)):
    new_user = User(username=payload.username, email=payload.email, password=payload.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/get-user', response_model=UserOut, status_code=status.HTTP_200_OK, tags=["User"])
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user