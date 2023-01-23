"""Response cookies.

You can declare a parameter of type `Response` in your path opeartion function.
And then you can set cookies in that temporal response object.
And then you can return any object you need, as you normally would.
And if you declared a `response_model`, it will still be used to filter and convert the object you
returned.

FastAPI will use that temporal response to extract the cookies (also headers and status code),
and will put them in the final response that contains the value you returned, filtered by an
`response_model`.

You can also declare the `Response` parameter in dependencies, and set cookies (and headers)
in them.
"""

from fastapi import FastAPI, Response

app = FastAPI()


@app.post("/cookie-and-object")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}
