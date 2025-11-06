from schemas import User as UserSchema, UserOut
from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from repository import user as user_repo

router= APIRouter(
    prefix="/user",
    tags=["User"]
)
@router.post('/', response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserSchema, db: Session = Depends(get_db)):
    return user_repo.create_user(payload, db)

@router.get('/', response_model=UserOut, status_code=status.HTTP_200_OK)
def get_user(id: int,db: Session = Depends(get_db)):
    return user_repo.get_user(id, db)