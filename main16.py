"""`UJSONResponse`

An alternative JSON response using `ujson`.
`ujson` is less careful than Python's built-in implementation in how it handles some edge-cases.
"""

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

app = FastAPI()


@app.get("/items/", response_class=UJSONResponse)
async def read_items():
    return [{"item_id": "Foo"}]
