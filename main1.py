"""
You can set the OpenAPI operationId to be used in your path operation
with the parameter `operation_id`.
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/items/", operation_id="some_specific_id_you_define")
async def read_item():
    return [{"item_id": "Foo"}]
