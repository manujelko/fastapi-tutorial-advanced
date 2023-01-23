"""Response Headers.

You can declare a parameter of type `Response` in your path operation function.
And then you can set headers in that temporal response object.
And then you can return any object you need, as you normally would.
And if you declared a `response_model`, it will still be used to filter and convert the object you
returned.
FastAPI will use that temporal response to extract the headers (also cookies and status code),
and will put them in the final response that contains the value you returned, filtered by any
`response_model`.
"""

from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/headers-and-object")
def get_headers(response: Response):
    response.headers["X-Cat-Dog"] = "alone in the world"
    return {"message": "Hello World"}
