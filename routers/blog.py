
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import Base, engine, get_db
from models import Blog, User
from schemas import Blog as BlogSchema, BlogOut


router = APIRouter()

@router.post("/create-blog", response_model=BlogOut, status_code=status.HTTP_201_CREATED, tags=["Blog"])
def create_blog(payload: BlogSchema, db: Session = Depends(get_db)):
    new_blog = Blog(title=payload.title, content=payload.content, author=payload.author, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/get-blogs", response_model=List[BlogOut], status_code=status.HTTP_200_OK, tags=["Blog"])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs

@router.get("/get-blog/{id}", response_model=BlogOut, status_code=status.HTTP_200_OK, tags=["Blog"])
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog

@router.delete("/delete-blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Blog"])
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    db.delete(blog)
    db.commit()
    return

@router.patch("/update-blog/{id}", response_model=BlogOut, status_code=status.HTTP_200_OK, tags=["Blog"])
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