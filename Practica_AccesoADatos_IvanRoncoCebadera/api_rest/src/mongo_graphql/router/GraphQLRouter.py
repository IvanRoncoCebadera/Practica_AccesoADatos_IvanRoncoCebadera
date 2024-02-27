from typing  import List
from fastapi import APIRouter, HTTPException
from mongo_rest.repository.usuarios.UsuarioRepoMongo import UsuarioRepoMongo
from IRepository.usuarios import IUsuarioRepo
from models.usuarios.Usuario import Usuario
import graphene
from graphene_pydantic import PydanticObjectType

class UsuarioType(PydanticObjectType):
    class Meta:
        model = Usuario

class Query(graphene.ObjectType):
    usuarios = graphene.List(UsuarioType)

    async def resolve_usuarios(self, info):
        usuarios_repo: IUsuarioRepo = UsuarioRepoMongo()
        return usuarios_repo.find_all()
    
schema = graphene.Schema(query=Query)