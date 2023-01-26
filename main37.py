"""Using Dataclasses.

FastAPI also supports using dataclasses.
This is supported thanks to Pydantic, as it has internal support for dataclasses.
"""

from dataclasses import dataclass
from typing import Union

from fastapi import FastAPI


@dataclass
class Item:
    name: str
    price: float
    description: Union[str, None] = None
    tax: Union[float, None] = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item
