from pydantic import BaseModel, EmailStr
from typing import List, Optional

# Blog Schema
class Blog(BaseModel):
    title: str
    body: str
    creator_id: int

    class Config:
        from_attributes = True  # For SQLAlchemy 2.x compatibility

# ShowUser Schema for Responses
class ShowUser(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # For SQLAlchemy 2.x compatibility

# ShowBlog Schema for Responses
class ShowBlog(BaseModel):
    title: str
    body: str
    creator: Optional[ShowUser] = None  # Blog creator's details, allowing None

    class Config:
        from_attributes = True  # For SQLAlchemy 2.x compatibility

# User Schema for Requests
class User(BaseModel):
    username: str
    email: EmailStr
    password: str  # Include password for user creation requests

    class Config:
        from_attributes = True  # For SQLAlchemy 2.x compatibility

# Token Schema for Authentication Responses
class Token(BaseModel):
    access_token: str
    token_type: str

# Example for including a list of blogs with a user
class ShowUserWithBlogs(BaseModel):
    username: str
    email: EmailStr
    blogs: List[ShowBlog] = []  # List of blogs created by the user

    class Config:
        from_attributes = True  # For SQLAlchemy 2.x compatibility
