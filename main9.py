"""Return a response directly.

When you create a FastAPI path operation you can normally return any data from it: a `dict`, a
`list`, a Pydantic model, a database model, etc.

By default, FastAPI would automatically convert that return value to JSON using the
`jsonable_encoder`.

Then, behind the scenes, it would put that JSON-compatible data (e.g. `dict`) inside a
`JSONResponse` that would be used to send the response to the client.

But you can return a `JSONResponse` directly from your path operations.

It might be useful, for example, to return custom headers or cookies.

In fact, you can return any `Response` or any subclass of it.
And when you return a `Response`, FastAPI will pass it directly.
It won't do any data conversion with Pydantic models, it won't convert contents to any type,
etc.
This gives you a lot of flexibility. You can return any data type, override any data declaration or
validation, etc.

Because FastAPI doesn't do any change to a `Response` you return, you have to make sure its
contents are ready for it.

For example, you cannot put a Pydantic model in a `JSONResponse` without first converting it to
a `dict` with all the data types (like `datetime`, `UUID`, etc) converted to JSON-compatible types.

For those cases, you can use the `jsonable_encoder` to convert your data before passing it to a response.
"""

from datetime import datetime
from typing import Union

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Union[str, None] = None


app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    return JSONResponse(content=json_compatible_item_data)
