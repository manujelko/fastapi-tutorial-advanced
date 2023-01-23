"""Exclude from OpenAPI.

To exclude a path operation from the generated OpenAPI schema (and thus, from the
automatic documentation systems), use the parameter `inlude_in_schema` and set it to
False:
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/items/", include_in_schema=False)
async def read_items():
    return [{"item_id": "Foo"}]
