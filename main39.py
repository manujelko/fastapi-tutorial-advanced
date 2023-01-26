"""Dataclases in nested data structures.

You can also combine `dataclasses` with other type annotations to make nested data
structures.

In some cases, you might still have to use Pydantic's version of `dataclasses`. For example, if
you have errors with the automatically generated API documentation.

In that case, you can simply swap the standard `dataclasses` with `pydantic.dataclasses`,
which is a drop-in replacement.
"""

from dataclasses import field
from typing import List, Union

from fastapi import FastAPI
from pydantic.dataclasses import dataclass


@dataclass
class Item:
    name: str
    description: Union[str, None] = None


@dataclass
class Author:
    name: str
    items: List[Item] = field(default_factory=list)


app = FastAPI()


@app.post("/authors/{author_id}/items/", response_model=Author)
async def create_author_items(author_id: str, items: List[Item]):
    return {"name": author_id, "items": items}


@app.get("/authors/", response_model=List[Author])
def get_authors():
    return [
        {
            "name": "Breaters",
            "items": [
                {
                    "name": "Island In The Moon",
                    "description": "A place to bee playin' and havin' fun",
                },
                {"name": "Holy Buddies"},
            ],
        },
        {
            "name": "System of an Up",
            "items": [
                {
                    "name": "Salt",
                    "description": "The kombucha mushroom people's favorite",
                },
                {
                    "name": "Pad Thai",
                },
                {
                    "name": "Lonely Night",
                    "description": "The mostest lonliest nightiest of allest",
                },
            ],
        },
    ]
