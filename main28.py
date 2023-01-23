"""Return a `Response` directly.

You can also create cookies when returning a `Response` directly in your code.
To do that, you can create a response then set cookies in it, and then return it.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/cookie/")
def create_cookie():
    content = {"message": "Come to the dark side, we have cookies"}
    response = JSONResponse(content=content)
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return response
