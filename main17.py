"""`RedirectResponse`.

Returns an HTTP redirect. Uses a 307 status code (Temporary Redirect) by default.
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


# You can return a `RedirectResponse` directly:
@app.get("/typer")
async def redirect_typer():
    return RedirectResponse("https://typer.tiangolo.com")


# Or you can use it in the `response_class` parameter:
@app.get("/fastapi", response_class=RedirectResponse)
async def redirect_fastapi():
    return "https://fastapi.tiangolo.com"
