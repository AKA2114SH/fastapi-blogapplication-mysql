from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use environment variables for sensitive information
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "root")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "PASSWORD")  #replace your sql password here
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "3306")
DATABASE_NAME = os.getenv("DATABASE_NAME", "blog_db")

# Connection URL for MySQL
SQLALCHEMY_DATABASE_URL = (
    f"mysql+mysqlconnector://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()
