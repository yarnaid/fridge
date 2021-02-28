import typing
from fastapi import FastAPI, HTTPException, Request, Security, Depends
import models  # type: ignore
from repo import MemStorage  # type: ignore
import http
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyQuery, APIKey

import time
from uuid import uuid4

app = FastAPI()
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1"])
storage = MemStorage()
origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

API_KEY = "secret"
API_KEY_NAME = "apikey"
key_security = APIKeyQuery(name=API_KEY_NAME)


async def check_api_key(key: str = Security(key_security)):
    if key == API_KEY:
        return key_security
    raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail="invalid api key")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.middleware("http")
async def add_correlation_id_header(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-Id", str(uuid4()))
    response = await call_next(request)
    response.headers["X-Correlation-Id"] = correlation_id
    return response


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


@app.delete("/item/{item.id}", status_code=http.HTTPStatus.NO_CONTENT, responses={404: {"model": models.Item}})
def delete_item(item_id: int):
    try:
        storage.delete(item_id)
    except KeyError:
        raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND, detail=f"Item with id={item_id} not found")


@app.delete("/sec/item/{item.id}", status_code=http.HTTPStatus.NO_CONTENT, responses={404: {"model": models.Item}})
def secure_delete_item(item_id: int, apikey: APIKey = Depends(check_api_key)):
    try:
        storage.delete(item_id)
    except KeyError:
        raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND, detail=f"Item with id={item_id} not found")
