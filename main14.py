"""Document in OpenAPI and override `Response`.

If you want to override the response from inside the function but at the same time document
the "media type" in OpenAPI, you can use the `response_class` parameter AND return a
`Response` object.

The `response_class` will then be used only to document the OpenAPI path operation, but your
`Response` will be used as is.
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/items/", response_class=HTMLResponse)
async def read_items():
    return generate_html_response()
