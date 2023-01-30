"""GraphQL.

As FastAPI is based on the ASGI standard, it's very easy to integrate any GraphQL library also compatible with ASGI.
You can combine normal FastAPI path operations with GraphQL on the same application.

If you need or want to work with GraphQL, Strawberry is the recommended library as it has the design closest to FastAPI's
design, it's all based on type annotations.
"""

import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL


@strawberry.type
class User:
    name: str
    age: int


@strawberry.type
class Query:
    @strawberry.field
    def user(self) -> User:
        return User(name="Patrick", age=100)


schema = strawberry.Schema(query=Query)

graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)
