"""WebSockets.

You can use WebSockets with FastAPI.

In your production system you probably have a frontend created with a modern framework like React, Vue.js or Angular.
And to communicate using WebSockets with your backend you would probably use your frontend's utilities.
Or you might have a native mobile application that communicates with your WebSocket backend directly, in native code.
Or you might have any other way to communicate with the WebSocket endpoint.

But for this example, we'll use a very simple HTML document with some JavaScript, all inside a long string.
This, of course, is not optimal and you wouldn't use it for production.
In production you would have one of the options above.
But it's the simplest way to focus on the server-side of WebSockets and have a working example.
"""

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id="messages">
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var content = document.createTextNode(event.data);
                message.appendChild(content);
                messages.appendChild(message);
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText");
                ws.send(input.value);
                input.value = ''
                event.preventDefault();
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
