from fastapi import FastAPI
from database import Base, engine
from routers import blog, user

app= FastAPI()

# Include routers
app.include_router(blog.router)
app.include_router(user.router)


# Create tables on startup (simple dev approach)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine) 
