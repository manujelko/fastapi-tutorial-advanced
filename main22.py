"""Default response class.

When creating a FastAPI class instance or an `APIRouter` you can specify which response
class to use by default.

The parameter that defines this is `default_response_class`.
"""

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(default_response_class=ORJSONResponse)


@app.get("/items/")
async def read_items():
    return [{"item_id": "Foo"}]
