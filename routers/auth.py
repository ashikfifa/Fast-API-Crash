from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserLogin
from models import User
from utils import verify_password

router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login')
def login(request_body: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request_body.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    
    # Verify the password using hash verification
    if not verify_password(request_body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")

    return {"message": "Login successful", "user_id": user.id, "username": user.username}
