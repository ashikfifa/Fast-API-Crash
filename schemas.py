from pydantic import BaseModel
from datetime import datetime



class User(BaseModel):
    username: str
    email: str
    password: str
    
class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    
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
