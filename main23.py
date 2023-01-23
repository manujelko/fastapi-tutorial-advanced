"""Additional response with `model`.

You can pass to your path operation decorators a parameter `responses`.

It receives a `dict`, the keys are status codes for each response, like 200, and the values are
other `dict`s with the information for each of them.

Each of those response `dict`s can have a key `model`, containing a Pydantic model, just like
`response_model`.

FastAPI will take that model, generate its JSON Schema and include it in the correct place in
OpenAPI.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Item(BaseModel):
    id: str
    value: str


class Message(BaseModel):
    message: str


app = FastAPI()


@app.get("/items/{item_id}", response_model=Item, responses={404: {"model": Message}})
async def read_item(item_id: str):
    if item_id == "foo":
        return {"id": "foo", "value": "there goes my hero"}
    return JSONResponse(status_code=404, content={"message": "Item not found"})
