"""Combining information.

You can also combine response information from multiple places, including the
`response_model`, `status_code`, and `responses` parameters.

You can declare a `response_model`, using the default status code 200,
and then declare additional information for that same response in responses, directly in
the OpenAPI schema.

FastAPI will keep the additional information from `responses`, and combine it with the JSON
Schema from your model.

For example, you can declare a response with a status code 404 that uses a Pydantic model
and has a custom description.

And a response with a status code 200 that uses your `response_model`, but includes a custom `example`.
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


@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item was requested by ID",
            "content": {
                "application/json": {
                    "example": {"id": "bar", "value": "The bar tenders"},
                }
            },
        },
    },
)
async def read_item(item_id: str):
    if item_id == "foo":
        return {"id": "foo", "value": "there goes my hero"}
    else:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
