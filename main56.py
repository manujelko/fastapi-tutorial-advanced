"""Testing dependencies with overrides.

There are some scenarios where you might want to override a dependency during testing.
You don't want the original dependency to run (nor any of the sub-dependencies it might have).
Instead, you want to provide a different dependency that will be used only during tests (possibly only some
specific tests), and will provide a value that can be used where the value of the original dependency was used.

An example could be that you have an external authentication provider that you need to call.
You send it a token, and it returns an authenticated user.
In this case, you override the dependency that calls that provider, and use a custom dependency that returns
a mock user, only for your tests.

For these cases, your FastAPI application has an attribute `app.dependency_overrides`, it is a simple `dict`.
To override a dependency for testing, you put as a key the original dependency (a function), and as the value,
your dependency override (another function).
"""

from typing import Union

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


async def common_parameters(
    q: Union[str, None] = None,
    skip: int = 0,
    limit: int = 100,
):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return {"message": "Hello Items!", "params": commons}


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return {"message": "Hello Users!", "params": commons}


client = TestClient(app)


async def override_dependency(q: Union[str, None] = None):
    return {"q": q, "skip": 5, "limit": 10}


app.dependency_overrides[common_parameters] = override_dependency


def test_override_in_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": None, "skip": 5, "limit": 10},
    }


def test_override_in_items_with_q():
    response = client.get("/items/?q=foo")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }


def test_override_in_items_with_params():
    response = client.get("/items/?q=foo&skip=100&limit=200")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }
