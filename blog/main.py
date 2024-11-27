from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "a_random_secret_key_for_jwt")  # Default to a placeholder if not set
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta

from . import schemas, models
from .database import engine, SessionLocal
from .hashedpwd import hash_password, verify_password

# Initialize the FastAPI application
app = FastAPI(
    title="Blog Application API By Akash Khatale",
    description="A FastAPI-based blog application with user management.",
    version="1.0.0",
)

# Create all tables
models.Base.metadata.create_all(bind=engine)

# OAuth2 scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency: Get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create a new JWT token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Function to decode JWT token and get user from the token
def get_user_from_token(db: Session, token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

# Root endpoint
@app.get("/", tags=["root"])
def read_root():
    return {
        "message": "Welcome to the Blog Application API! Explore our API documentation at /docs."
    }

# Authentication Routes
@app.post("/token", response_model=schemas.Token, tags=["login"])
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if user is None or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

# Blog Routes
@app.post("/blog", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog, tags=["blogs"])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = get_user_from_token(db, token)
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        creator_id=user.id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog", response_model=list[schemas.ShowBlog], tags=["blogs"])
def get_all_blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()

@app.get("/blog/{id}", response_model=schemas.ShowBlog, tags=["blogs"])
def get_blog_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with ID {id} not found",
        )
    return blog

@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = get_user_from_token(db, token)
    blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.creator_id == user.id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with ID {id} not found or you do not have permission to edit it.",
        )
    blog.title = request.title
    blog.body = request.body
    db.commit()
    return {"detail": f"Blog {id} has been updated"}

@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def delete_blog(id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = get_user_from_token(db, token)
    blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.creator_id == user.id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with ID {id} not found or you do not have permission to delete it.",
        )
    db.delete(blog)
    db.commit()
    return {"detail": f"Blog {id} has been deleted"}

# User Routes
@app.post("/user/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=["users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(
        (models.User.username == request.username) |
        (models.User.email == request.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    hashed_password = hash_password(request.password)
    new_user = models.User(
        username=request.username,
        email=request.email,
        password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user/{id}", response_model=schemas.ShowUserWithBlogs, tags=["users"])
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} not found"
        )
    return user
