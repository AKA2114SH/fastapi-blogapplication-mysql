from fastapi import FastAPI

app = FastAPI()

@app.get("/", summary="Index")
def index():
    return {'data': 'blog list'}

# Only get limited number of published or all blogs
@app.get("/blog", summary="Blog List")
def get_blogs(limit: int=10 , published: bool=True,sort:str=None):
    if published:
        return {'data': f'{limit} published blogs from the db'}
    else:
        return {'data': f'{limit} blogs from the db'}

@app.get("/blog/unpublished", summary="Unpublished Blogs")
def unpublish():
    return {'data': 'all unpublished blogs'}

@app.get("/blog/{id}", summary="Show Blog")
def show(id: int):
    # Fetch blog with id = id
    return {'data': id}

@app.get("/blog/{id}/comments", summary="Blog Comments")
def comments(id: int,limit=10):
    # Fetch comments of blog with id = id
    return {'data': ['1', '2']}  # Example response
