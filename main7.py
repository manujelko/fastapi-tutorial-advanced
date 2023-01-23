"""Custom OpenAPI content type.

Using the same trick, you could use a Pydantic model to define the JSON Schema that is then
included in the custom OpenAPI schema section for the path operation.

And you could do this even if the data type in the request is not JSON.

For example, in this application we don't use FastAPI's integrated functionality to extract the
JSON Schema from Pydantic models nor the automatic validation for JSON. In fact, we are
declaring the request content type as YAML, not JSON.

Nevertheless, although we are not using the default integrated functionality, we are still using a
Pydantic model to manually generate the JSON Schema for the data that we want to receive in
YAML.

Then we use the request directly, and extract the body as `bytes`. This means that FastAPI
won't even try to parse the request payload as JSON.

And then in our code, we parse that YAML content directly, adn then we are again using the
same Pydantic model to validate the YAML content.
"""

from typing import List

import yaml
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ValidationError

app = FastAPI()


class Item(BaseModel):
    name: str
    tags: List[str]


@app.post(
    "/items/",
    openapi_extra={
        "requestBody": {
            "content": {"application/x-yaml": {"schema": Item.schema()}},
            "required": True,
        },
    },
)
async def create_item(request: Request):
    raw_body = await request.body()
    try:
        data = yaml.safe_load(raw_body)
    except yaml.YAMLError:
        raise HTTPException(status_code=422, detail="Invalid YAML")
    try:
        item = Item.parse_obj(data)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    return item
