from sqlalchemy.orm import Session
from models import Blog
from schemas import Blog as BlogSchema
from fastapi import Depends
from database import get_db
from fastapi import HTTPException, status

def create_blog(payload: BlogSchema, db: Session = Depends(get_db)):
    new_blog = Blog(title=payload.title, content=payload.content, author=payload.author, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def get_all(db: Session):
    blog= db.query(Blog).all() 
    return blog

def delete_blog(    id: int, db: Session= Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    db.delete(blog)
    db.commit()
    
    return blog

def get_blog(id: int, db: Session= Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog

def update_blog(id: int, payload: BlogSchema, db: Session= Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    blog.title = payload.title
    blog.content = payload.content
    blog.author = payload.author
    db.commit()
    db.refresh(blog)
    return blog