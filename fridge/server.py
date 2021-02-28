import typing
from fastapi import FastAPI, HTTPException, Request
import models  # type: ignore
from repo import MemStorage  # type: ignore
import http
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1"])
storage = MemStorage()


@app.get("/item", response_model=typing.List[models.Item])
def items_list() -> typing.List[models.Item]:
    return storage.get_all()


@app.get("/item/{item_id}", response_model=models.Item)
def item(item_id: int):
    try:
        return storage.get(item_id)
    except KeyError:
        raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND, detail=f"Item with id={item_id} not found")


@app.post("/item", response_model=int, status_code=http.HTTPStatus.CREATED)
def create_item(item: models.Item):
    if item.id is not None:
        raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail="Item should not have an ID")
    return storage.create(item)


@app.delete("/item/{item.id}", status_code=http.HTTPStatus.NO_CONTENT)
def delete_item(item_id: int):
    try:
        storage.delete(item_id)
    except KeyError:
        raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND, detail=f"Item with id={item_id} not found")
