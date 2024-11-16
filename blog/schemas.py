from pydantic import BaseModel

# Blog Schema
class Blog(BaseModel):
    title: str
    body: str

    class Config:
        from_attributes = True  # Changed from orm_mode to from_attributes

# User Schema
class User(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True  # Changed from orm_mode to from_attributes
