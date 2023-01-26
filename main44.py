"""Sub application mounts.

If you need to have two independent FastAPI applications, with their own independent OpenAPI
and their own docs UIs, you can have a main app and "mount" one (or more) sub-application(s).

"Mounting" means adding a completely "independent" application in a specific path, that then
takes care of handling everything under that path, with the path operations declared in that sub-
application.
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}


subapi = FastAPI()


@subapi.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}


app.mount("/subapi", subapi)
