from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Blog model
class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # Foreign key pointing to User
    title = Column(String(255), nullable=False)
    body = Column(String(1000), nullable=False)

    # Relationship with the User model
    creator = relationship("User", back_populates="blogs")

# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    # Relationship with the Blog model
    blogs = relationship("Blog", back_populates="creator", cascade="all, delete-orphan")
