from fastapi import FastAPI
from dotenv import load_dotenv, dotenv_values
from models.usuarios.Usuario import Usuario
from mongo_rest.repository.usuarios.UsuarioRepoMongo import UsuarioRepoMongo
from IRepository.usuarios import IUsuarioRepo
from mongo_rest.router.RouterMongo import mongo_router
from mariaDB_rest.router.RouterMariaDB import maria_router
from mongo_graphql.router.GraphQLRouter import schema as graphql_schema
from strawberry.fastapi import GraphQLRouter

################# PROBANDO LA MONGO_DB
# db: IUsuarioRepoMongo = UsuarioRepoMongo()

# db.update(Usuario(id="ivanrc@gmail.com", password="wiwi"))
# db.delete_by_id("ivanrc@gmail.com")

# print(db.find_all())
# print(db.find_by_id("Jorge"))
#print("Holaaaaaaaaaaal")


################# ESTO ES LO QUE DESPUES DEBO DESCOMENTAR!!!!

env = dotenv_values("enviroment.env")

MONGO_ROUTE = "/api/v1"
MARIA_ROUTE = "/api/v2"
GRAPHQL_ROUTE = "/graphql"

FT_GraphQL = bool(env.get("FT_GraphQL"))
FT_MongoDB = bool(env.get("FT_MongoDB"))

app = FastAPI()

from graphene import ObjectType, String, Schema
import fastapi

class Query(ObjectType):
    hello = String(name=String(default_value="ESPAÑA")) #El 'name' aquí, debe coincidir con

    def resolve_hello(self, info, name): #El 'name' aquí!!!
        return 'Hello ' + name
    
schema = Schema(query=Query)


app.include_router(maria_router, prefix=MARIA_ROUTE, tags=["MariaDB"])

if FT_MongoDB:
    app.include_router(mongo_router, prefix=MONGO_ROUTE, tags=["MongoDB"])

if FT_GraphQL:
    app.include_router(GraphQLRouter(schema), prefix=GRAPHQL_ROUTE)

@app.get("/")
def loadRoutes():
    routes = { "maria_db": MARIA_ROUTE }
    if FT_MongoDB: routes["mongo_db"] = MONGO_ROUTE
    if FT_GraphQL: routes["graphql"] = GRAPHQL_ROUTE
    return routes

if __name__ == "__main__":
    #app.run()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)