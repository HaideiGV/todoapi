from fastapi import FastAPI

from api import items, todos


app = FastAPI()

app.include_router(
    items.router, prefix="/todos",
)
app.include_router(
    todos.router, prefix="/todos",
)


@app.get("/")
def index():
    return {"Hello": "World"}
