from sqlalchemy import Column, Integer, String
from .database import Base

class Blog(Base):
    __tablename__ = "blogs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)  # Specifying a length for the title column and setting it as not nullable
    body = Column(String(1000), nullable=False)   # Specifying a length for the body column and setting it as not nullable
