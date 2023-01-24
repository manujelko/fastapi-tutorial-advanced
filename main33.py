"""OAuth2 scopes.

OAuth2 with scopes is the mechanism used by many big authentication providers, like
Facebook, Google, GitHub, Microsoft, Twitter, etc. They use it to provide specific permissions to
users and applications.

Every time you "log in with" Facebook, Google, GitHub, Microsoft, Twitter, that application is
using OAuth2 with scopes.

The OAuth2 specification defines "scopes" as a list of strings separated by spaces.
The content of each of these strings can have any format, but should not contain spaces.
These scopes represent "permissions".
In OpenAPI (e.g. the API docs), you can define "security schemes".
When one of these security schemes uses OAuth2, you can also declare and use scopes.
Each "scope" is just a string (without spaces).
They are normally used to declare specific security permissions, for example:
- `users:read` or `users:write` are common examples.
- `instagram_basic` is used by Facebook / Instagram.
- `https://www.googleapis.com/auth/drive` is used by Google.

In OAuth2 a "scope" is just a string that declares a specific permission required.
It doesn't matter if it has other characters like `:` or if it is a URL.
Those details are implementation specific.

Let's see the parts that change from OAuth2 with password, bearer with JWT tokens.

The first change is that now we are declaring the OAuth2 security scheme with two available
scopes, `me` and `items`.
The `scopes` parameter receives a dict with each scope as a key and the description as the
value.

Because we are not declaring those scopes, they will show up in the API docs when you log-in/authorize.
And you will be able to select which scopes you want to give to: `me` and `items`.
This is the same mechanism used when you give permissions while logging in with Facebook,
Google, GitHub etc.

We modify the token path operation to return the scopes requested.
We are still using the same `OAuth2PasswordRequestForm`. It includes a property `scopes` with a
`list` of `str`, with each scope it received in the request.
And we return the scopes as part of the JWT token.
For simplicity, here we are just adding the scopes received directly to the token.
But in your application, for security, you should make sure you only add the scopes that the user is actually able to
have, or the ones you have predefined.

We declare that the path operation for `/users/me/items` requires the scope `items`.
You can use `Security` to declare dependencies (just like `Depends`), but `Security` also
receives a parameter `scopes` with a list of scopes.
We don't have to use `Security` when we don't need to specify security scopes.

The parameter `security_scopes` will be of type `SecurityScopes`.

It will have a property `scopes` with a list containing all the scopes required by itself and all the
dependencies that use this as a sub-dependency.
The `security_scopes` object also provides a `scope_str` attribute
with a single string, containing those scopes separated by spaces.

We verify that we get a `username`, and extract the scopes.
Then we validate the data with the Pydantic model.

We verify that all the scopes required are included in the scopes provided in the token received.
For this, we use `security_scopes.scopes`, that contains a `list` with all these scopes as `str`.

You can use `SecurityScopes` at any point, and in multiple places, it doesn't have to be at the
"root" dependency.
It will always have the security scopes declared in the current `Security` dependencies and all
the dependants for that specific path operation and that specific dependency tree.

Because the `SecurityScopes` will have all the scopes declared by dependants, you can use it
to verify that a token has the required scopes in a central dependency function, and then
declare different scope requirements in different path operations.
"""

from datetime import datetime, timedelta
from typing import List, Union

from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "aliechains@example.com",
        "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
        "disabled": True,
    },
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: List[str] = []


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "item": "Read items."}
)

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme),
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
        current_user: User = Security(get_current_user, scopes=["me"])
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "tokey_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
        current_user: User = Security(get_current_active_user, scopes=["items"])
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/status/")
async def read_system_status(current_user: User = Depends(get_current_user)):
    return {"status": "ok"}
