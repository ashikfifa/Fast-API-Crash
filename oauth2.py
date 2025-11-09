
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from sqlalchemy.orm import Session
import auth_token
from database import get_db
from models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = auth_token.verify_token(token, credentials_exception)
    
    user = db.query(User).filter(User.email == token_data.username).first()
    
    if user is None:
        raise credentials_exception
    
    return user