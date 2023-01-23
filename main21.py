"""Custom response class.

You can create your own custom response class, inheriting from `Response` and using it.

For example, let's say that you want to use `orjson`, but with some custom settings not
used in the included `ORJSONResponse` class.

Let's say you want it to return indented and formatted JSON, so you want to use the orjson
option `orjson.OPT_INDENT_2`.

You could create a `CustomORJSONResponse`. The main thing you have to do is create a
`Response.render(content)` method that returns the content as `bytes`.
"""

from typing import Any

import orjson
from fastapi import FastAPI, Response

app = FastAPI()


class CustomORJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)


@app.get("/", response_class=CustomORJSONResponse)
async def main():
    return {"message": "Hello World"}
