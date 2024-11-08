from fastapi import FastAPI

app = FastAPI()

@app.get("/", summary="Index")
def index():
    return {'data': 'blog list'}

@app.get("/blog/unpublished", summary="Unpublished")
def unpublish():
    return {'data': 'all unpublished blogs'}

@app.get("/blog/{id}", summary="Show")
def show(id: int):
    # Fetch blog with id = id
    return {'data': id}

@app.get("/blog/{id}/comments", summary="Comments")
def comments(id: int):
    # Fetch comments of blog with id = id
    return {'data': ['1', '2']}  # Example response
