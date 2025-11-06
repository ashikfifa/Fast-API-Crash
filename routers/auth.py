from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserLogin,Token
from models import User
from utils import verify_password
from auth_token import create_access_token

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

    access_token = create_access_token(
        data={"sub": user.email}
    )
    return Token(access_token=access_token, token_type="bearer")
