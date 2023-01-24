"""Using the Request directly.

Up to now, you have been declaring the parts of the request that you need with their types.
Taking data from:
- The path as parameters.
- Headers
- Cookies

And by doing so, FastAPI is validating that data, converting it and generating documentation
for your API automatically.

But there are situations where you might need to access the `Request` object directly.
"""

from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/items/{item_id}")
def read_root(item_id: str, request: Request):
    client_host = request.client.host
    return {"client_host": client_host, "item_id": item_id}
