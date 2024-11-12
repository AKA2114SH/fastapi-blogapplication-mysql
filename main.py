from fastapi import FastAPI
from blog import models
from blog.database import engine
from blog.main import app as blog_app  # Import the app from `blog/main.py`

# Initialize the database tables
models.Base.metadata.create_all(bind=engine)

# Mount `blog` app to the main FastAPI app
app = FastAPI()
app.mount("/blog", blog_app)
