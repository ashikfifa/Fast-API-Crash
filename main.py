from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import Base, engine, get_db
from models import Blog, User
from schemas import Blog as BlogSchema, BlogOut
from schemas import User as UserSchema, UserOut

app= FastAPI()


# Create tables on startup (simple dev approach)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.post("/create-blog", response_model=BlogOut, status_code=status.HTTP_201_CREATED, tags=["Blog"])
def create_blog(payload: BlogSchema, db: Session = Depends(get_db)):
    new_blog = Blog(title=payload.title, content=payload.content, author=payload.author, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/get-blogs", response_model=List[BlogOut], status_code=status.HTTP_200_OK, tags=["Blog"])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs

@app.get("/get-blog/{id}", response_model=BlogOut, status_code=status.HTTP_200_OK, tags=["Blog"])
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog

@app.delete("/delete-blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Blog"])
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    db.delete(blog)
    db.commit()
    return

@app.patch("/update-blog/{id}", response_model=BlogOut, status_code=status.HTTP_200_OK, tags=["Blog"])
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

@app.post('/create-user', response_model=UserOut, status_code=status.HTTP_201_CREATED, tags=["User"])
def create_user(payload: UserSchema, db: Session = Depends(get_db)):
    new_user = User(username=payload.username, email=payload.email, password=payload.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/get-user', response_model=UserOut, status_code=status.HTTP_200_OK, tags=["User"])
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user