"""`GZipMiddleware`

Handles GZip responses for any request that includes a `"gzip"` in the Accept-Encoding header.
The middleware will handle both standard and streaming responses.
"""

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.get("/")
async def main():
    return "somebigcontent"
