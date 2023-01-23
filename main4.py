"""Advanced description from docstring.

You can limit the lines used from the docstring of a path operation function for OpenAPI.
Adding an `\f` (an escaped "form feed" character) causes FastAPI to truncate the output used
for OpenAPI at this point.

It won't show up in the documentation, but other tools (such as Sphinx) will be able to use the
rest.
"""

from typing import Set, Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


@app.post("/items/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    \f
    :param item: User input.
    """
    return item
