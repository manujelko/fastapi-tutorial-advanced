"""Async tests.

Being able to use asynchronous functions in your tests could be useful, for example, when you're querying your
database asynchronously. Imagine you want to test sending requests to your FastAPI application and then verify that
your backend successfully wrote the correct data in the database, while using an async database library.

`pytest.mark.anyio`
If we want to call asynchronous functions in our tests, our test functions have to be asynchronous.
AnyIO provides a neat plugin for this, that allows us to specify that some test functions are to be called
asynchronously.

`HTTPX`
Even if your FastAPI application uses normal `def` functions instead of `async def`, it is still an `async`
application underneath.
The `TestClient` does some magic inside to call the asynchronous FastAPI function in your normal `def` test functions,
using standard pytest. But that magic doesn't work anymore when we're using it inside asynchronous functions.
By running our tests asynchronously, we can no longer use the `TestClient` inside our test functions.
The `TestClient` is based on `HTTPX` and luckily, we can use it directly to test the API.
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Tomato"}
