from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class User(BaseModel):
    username: str
    email: str
    password: str

# Simple blog schema for nested display (without user to avoid circular reference)
class BlogSimple(BaseModel):
    id: int
    title: str
    content: str
    author: str
    created_at: datetime
    user_id: int
    
    class Config:
        from_attributes = True
    
class UserOut(BaseModel):
    id: int
    username: str
    email: str
    password: str
    created_at: datetime
    blogs: List[BlogSimple] = []
    
    class Config:
        from_attributes = True
        

class Blog(BaseModel):
    title: str
    content: str
    author: str
    
    
class BlogOut(BaseModel):
    id: int
    title: str
    content: str
    author: str
    created_at: datetime
    user_id: int
    users: UserOut
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None