from fastapi import FastAPI
from dotenv import dotenv_values
from mongo_rest.router.RouterMongo import mongo_router
from mariaDB_rest.router.RouterMariaDB import maria_router
from mongo_graphql.router.GraphQLMongo import users_schema, lists_schema, tasks_schema
from strawberry.fastapi import GraphQLRouter

# Carga de variables de entorno
env = dotenv_values(".env")

MONGO_ROUTE = "/api/v1"
MARIA_ROUTE = "/api/v2"
GRAPHQL_ROUTE = "/graphql"
GRAPHQL_USERS_ROUTE = GRAPHQL_ROUTE+"/usuarios"
GRAPHQL_LISTS_ROUTE = GRAPHQL_ROUTE+"/listas"
GRAPHQL_TASKS_ROUTE = GRAPHQL_ROUTE+"/tareas"

FT_MariaDB = bool(env.get("FT_MariaDB"))
FT_GraphQL = bool(env.get("FT_GraphQL"))
FT_MongoDB = bool(env.get("FT_MongoDB"))

app = FastAPI()

if FT_MariaDB:
    app.include_router(maria_router, prefix=MARIA_ROUTE, tags=["MariaDB"])

if FT_MongoDB:
    app.include_router(mongo_router, prefix=MONGO_ROUTE, tags=["MongoDB"])

if FT_GraphQL:
    graphql_users = GraphQLRouter(users_schema)
    app.include_router(graphql_users, prefix = GRAPHQL_USERS_ROUTE)
    graphql_lists = GraphQLRouter(lists_schema)
    app.include_router(graphql_lists, prefix = GRAPHQL_LISTS_ROUTE)
    graphql_tasks = GraphQLRouter(tasks_schema)
    app.include_router(graphql_tasks, prefix = GRAPHQL_TASKS_ROUTE)

@app.get("/")
def loadRoutes():
    routes = {"maria_db": MARIA_ROUTE}
    if FT_MongoDB:
        routes["mongo_db"] = MONGO_ROUTE
    if FT_GraphQL:
        routes["graphql"] = GRAPHQL_ROUTE
    return routes

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
