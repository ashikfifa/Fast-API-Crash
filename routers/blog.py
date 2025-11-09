
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import Blog as BlogSchema, BlogOut
from repository import blog as blog_repo
from oauth2 import get_current_user
from models import User

router = APIRouter(
    prefix="/blog",
    tags=["Blog"]
)

@router.post("/", response_model=BlogOut, status_code=status.HTTP_201_CREATED)
def create_blog(payload: BlogSchema, db: Session = Depends(get_db)):
    return blog_repo.create_blog(payload, db)

@router.get("/", response_model=List[BlogOut], status_code=status.HTTP_200_OK)
def get_blogs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return blog_repo.get_all(db)

@router.get("/{id}", response_model=BlogOut, status_code=status.HTTP_200_OK)
def get_blog(id: int, db: Session = Depends(get_db)):  
    return blog_repo.get_blog(id, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    return blog_repo.delete_blog(id, db)

@router.patch("/{id}", response_model=BlogOut, status_code=status.HTTP_200_OK, tags=["Blog"])
def update_blog(id: int, payload: BlogSchema, db: Session = Depends(get_db)):
    return blog_repo.update_blog(id, payload, db)