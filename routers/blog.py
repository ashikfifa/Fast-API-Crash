
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import Base, engine, get_db
from models import Blog, User
from schemas import Blog as BlogSchema, BlogOut


router = APIRouter(
    prefix="/blog",
    tags=["Blog"]
)

@router.post("/", response_model=BlogOut, status_code=status.HTTP_201_CREATED)
def create_blog(payload: BlogSchema, db: Session = Depends(get_db)):
    new_blog = Blog(title=payload.title, content=payload.content, author=payload.author, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/", response_model=List[BlogOut], status_code=status.HTTP_200_OK)
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs

@router.get("/{id}", response_model=BlogOut, status_code=status.HTTP_200_OK)
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    db.delete(blog)
    db.commit()
    return

@router.patch("/{id}", response_model=BlogOut, status_code=status.HTTP_200_OK, tags=["Blog"])
def update_blog(id: int, payload: BlogSchema, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    blog.title = payload.title
    blog.content = payload.content
    blog.author = payload.author
    db.commit()
    db.refresh(blog)
    return blog