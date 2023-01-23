"""Using `StreamingResponse` with file-like objects.

If you have a file-like object (e.g. the object returned by `open()`), you can create a generator
function to iterate over that file-like object.

That way, you don't have to read it all first in memory, and you can pass that generator function
to the `StreamingResponse`, and return it.

This includes many libraries to interact with cloud storage, video processing, and others.
"""

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

some_file_path = "large-video-file.mp4"
app = FastAPI()


@app.get("/")
def main():
    def iterfile():
        with open(some_file_path, mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile(), media_type="video/mp4")
