"""Additional status codes.

By default, FastAPI will return the responses using a `JSONResponse`, putting the content you
return from your path operation inside of that `JSONResponse`.

It will use the default status code or the one you set in your path operation.

If you want to return additional status codes apart from the main one, you can do that by
returning a `Response` directly.

For example, let's say that you want to have a path operation that allows to update items, and
returns HTTP status codes of 200 "OK" when successful.

But you also want it to accept new items. And when the items didn't exist before, it creates
then, and returns an HTTP status code of 201 "Created".

To achieve this, import `JSONResponse`, and return your content there directly, setting the
`status_code` that you want.

If you return additional status codes and responses directly, they won't be included in the
OpenAPI schema (the API docs), because FastAPI doesn't hav a way to know beforehand
what you are going to return.
"""

from typing import Union

from fastapi import Body, FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

items = {"foo": {"name": "Fighters", "size": 6}, "bar": {"name": "Tenders", "size": 3}}


@app.put("/items/{item_id}")
async def upsert_item(
    item_id: str,
    name: Union[str, None] = Body(default=None),
    size: Union[int, None] = Body(default=None),
):
    if item_id in items:
        item = items[item_id]
        item["name"] = name
        item["size"] = size
        return item
    else:
        item = {"name": name, "size": size}
        items[item_id] = item
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)
