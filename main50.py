"""Events: startup - shutdown.

You can define event handlers (functions) that need o be executed before the application starts up, or when the
application is shutting down.
"""

from fastapi import FastAPI

app = FastAPI()

items = {}


@app.on_event("startup")
async def startup_event():
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}


@app.on_event("shutdown")
def shutdown_event():
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")


@app.get("/items/{item_id}")
async def read_items(item_id: str):
    return items[item_id]
