"""Custom Response

By default, FastAPI will return the responses using `JSONResponse`.

You can override it by returning a `Response` directly.
But if you return a `Response` directly, the data won't be automatically converted, and the
documentation won't be automatically generated.

But you can also declare the `Response` that you want to be used, in the path operation
decorator.

The contents that you return from your path operation function will be put inside of that
`Response`.

And if that `Response` has a JSON medial type (`application/json`), like is the case with the
`JSONResponse` and `UJSONResponse`, the data you return will be automatically converted (and
filtered) with any Pydantic `response_model` that you declared in the path operation decorator.

Use `ORJSONResponse`

For example, if you are squeezing performace, you can install and use orjson and set the
response to be `ORJSONResponse`.

For large responses, returning a `Response` directly is much faster than returning a dictionary.

This is because by default, FastAPI will inspect every item inside and make sure it is
serializable with JSON.
This is what allows you to return arbitrary objects, for example database models.

But if you are certain that the content you are returning is serializable with JSON, you can
pass it directly to the response class and avoid the extra overhead that FastAPI would have by
passing your return content through the `jsonable_encoder` before passing it to the response
class.
"""

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI()


@app.get("/items/", response_class=ORJSONResponse)
async def read_items():
    return ORJSONResponse([{"item_id": "Foo"}])
