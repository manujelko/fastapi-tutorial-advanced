"""Custom request and APIRoute class.

In some cases, you might want to override the logic used by the `Request` and `APIRoute` classes.
In particular, this may be a good alternative to logic in a middleware.
For example, if you want to read on manipulate the request body before it is processed by your application.

Use cases:
- Converting non-JSON request bodies to JSON
- Decompressing gzip-compressed request bodies
- Automatically logging all request bodies
"""

import gzip
from typing import Callable, List

from fastapi import Body, FastAPI, Request, Response
from fastapi.routing import APIRoute


class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body


class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler


app = FastAPI()
app.router.route_class = GzipRoute


@app.post("/sum")
async def sum_numbers(numbers: List[int] = Body()):
    return {"sum": sum(numbers)}
