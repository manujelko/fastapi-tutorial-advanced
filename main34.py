"""HTTP basic auth.

For the simplest cases, you can use HTTP basic auth.
In HTTP basic auth, the application expects a header that contains a username and a
password.
If it doesn't receive it, it returns an HTTP 401 "Unauthorized" error.
And returns a header `WWW-Authenticate` with a value of `Basic`, and an optional `realm`
parameter.
That tells the browser to show the integrated prompt for a username and password.
Then, when you type that username and password, the browser sends them in the header
automatically.
"""

from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()


@app.get("/users/me")
def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username, "password": credentials.password}
