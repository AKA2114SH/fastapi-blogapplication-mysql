from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas, models
from .database import engine, SessionLocal
from .hashedpwd import hash_password, verify_password  # Import password hashing functions

# Initialize the FastAPI application
app = FastAPI()

# Create all tables
models.Base.metadata.create_all(bind=engine)

# Dependency: get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the blog application"}

# Create a new blog post
@app.post("/blog", status_code=status.HTTP_201_CREATED, response_model=schemas.Blog)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# Get all blog posts
@app.get("/blog", response_model=list[schemas.Blog])
def get_all_blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()

# Get a blog post by ID
@app.get("/blog/{id}", response_model=schemas.Blog)
def get_blog_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with ID {id} not found",
        )
    return blog

# Update a blog post by ID
@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with ID {id} not found",
        )
    blog.title = request.title
    blog.body = request.body
    db.commit()
    return {"detail": f"Blog {id} has been updated"}

# Delete a blog post by ID
@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with ID {id} not found",
        )
    db.delete(blog)
    db.commit()
    return {"detail": f"Blog {id} has been deleted"}

# Create a new user
@app.post("/user/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    # Check if the username or email already exists
    existing_user = db.query(models.User).filter(
        (models.User.username == request.username) |
        (models.User.email == request.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    # Hash the password
    hashed_password = hash_password(request.password)

    # Create and save the new user
    new_user = models.User(
        username=request.username,
        email=request.email,
        password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
