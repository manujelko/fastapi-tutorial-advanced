"""Custom OpenAPI path operation schema.

The dictionary in `openapi_extra` will be deeply merged with the automatically generated
OpenAPI schema for the path operation.

So, you could add additional data to the automatically generated schema.

For example, you could decide to read and validate the request with your own code, without
using the automatic features of FastAPI with Pydantic, but you could still want to define the
request in the OpenAPI schema.

You could do that with `openapi_extra`.

In this example, we didn't declare any Pydantic model. In fact, the request body is not even
parsed as JSON, it is read directly as bytes, and the function `magic_data_reader()` would be
in charge of parsing it in some way.

Nevertheless, we can declare the expected schema for the request body.
"""

from fastapi import FastAPI, Request

app = FastAPI()


def magic_data_reader(raw_body: bytes):
    return {
        "size": len(raw_body),
        "content": {
            "name": "Maagic",
            "price": 42,
            "description": "Just kiddin', no magic here. ✨",
        },
    }


@app.post(
    "/items/",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "required": ["name", "price"],
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "price": {"type": "number"},
                            "description": {"type": "string"},
                        },
                    }
                }
            },
            "required": True,
        },
    },
)
async def create_item(request: Request):
    raw_body = await request.body()
    data = magic_data_reader(raw_body)
    return data
