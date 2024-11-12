from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, models
from .database import engine, SessionLocal

app = FastAPI()

# Create all tables
models.Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def read_root():
    return {"message": "Welcome to the blog application"}

@app.post('/blog')
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    # Use request.body instead of request.content
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', response_model=list[schemas.Blog])
def all_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', response_model=schemas.Blog)
def show(id: int, db: Session = Depends(get_db)):  # Fixed the type of `id` to `int`
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog
