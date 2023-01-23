"""`FileResponse`.

Asynchronously streams a file as the response.

Takes a different set of arguments to instantiate than the other response types:

- path: The filepath to the file to stream.
- headers: Any custom headers to include, as a dictionary.
- media_type: A string giving the media type. If unset, the filename or path will be used to
infer a media type.
- filename: If set, this will be included in the response Content-Disposition.

File responses will include appropriate Content-Length, Last-Modified and ETag headers.
"""

from fastapi import FastAPI
from fastapi.responses import FileResponse

some_file_path = "large-video-file.mp4"
app = FastAPI()


@app.get("/")
async def main():
    return FileResponse(some_file_path)


# You can also use the `response_class` parameter:
# @app.get("/", response_class=FileResponse)
# async def main():
#     return some_file_path
