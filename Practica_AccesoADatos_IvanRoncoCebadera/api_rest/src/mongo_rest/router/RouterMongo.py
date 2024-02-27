from typing  import List
from fastapi import APIRouter, HTTPException
from mongo_rest.repository.usuarios.UsuarioRepoMongo import UsuarioRepoMongo
from IRepository.usuarios import IUsuarioRepo
from models.usuarios.Usuario import Usuario
from mongo_rest.repository.tareas.TareaRepoMongo import TareaRepoMongo
from IRepository.tareas import ITareaRepo
from models.tareas.Tarea import Tarea
from models.tareas.TareaDTO import TareaDTO
from models.tareas.TareaMapper import to_tareaDto, to_tarea

tareasRepo: ITareaRepo = TareaRepoMongo()
usuariosRepo: IUsuarioRepo = UsuarioRepoMongo()

mongo_router = APIRouter()

GET_ALL_USERS_ROUTE="/usuarios/"
GET_USER_BY_ID_ROUTE="/usuarios/{id}"
POST_USER_ROUTE="/usuarios/"
PUT_USER_ROUTE="/usuarios/{id}"
DELETE_USER_BY_ID_ROUTE="/usuarios/{id}"
DELETE_ALL_USERS_ROUTE="/usuarios/"

GET_ALL_TASKS_ROUTE="/tareas/"
GET_TASK_BY_ID_ROUTE="/tareas/{id}"
GET_ALL_TASKS_BY_USER_ID="/tareas/usuario/{userID}"
POST_TASK_ROUTE="/tareas/"
PUT_TASK_ROUTE="/tareas/{id}"
DELETE_TASK_BY_ID_ROUTE="/tareas/{id}"
DELETE_ALL_TASKS_ROUTE="/tareas/"

###############################  Rutas  ###############################

@mongo_router.get("/", tags=["MongoDB"])
async def get_all_routes():
    routes = { 
        "GET_ALL_USERS_ROUTE": GET_ALL_USERS_ROUTE, 
        "GET_USER_BY_ID_ROUTE": GET_USER_BY_ID_ROUTE, 
        "POST_USER_ROUTE": POST_USER_ROUTE, 
        "PUT_USER_ROUTE": PUT_USER_ROUTE, 
        "DELETE_USER_BY_ID_ROUTE": DELETE_USER_BY_ID_ROUTE, 
        "DELETE_ALL_USERS_ROUTE": DELETE_ALL_USERS_ROUTE,

        "GET_ALL_TASKS_ROUTE": GET_ALL_TASKS_ROUTE,
        "GET_TASK_BY_ID_ROUTE": GET_TASK_BY_ID_ROUTE,
        "GET_ALL_TASKS_BY_USER_ID": GET_ALL_TASKS_BY_USER_ID,
        "POST_TASK_ROUTE": POST_TASK_ROUTE,
        "PUT_TASK_ROUTE": PUT_TASK_ROUTE,
        "DELETE_TASK_BY_ID_ROUTE": DELETE_TASK_BY_ID_ROUTE,
        "DELETE_ALL_TASKS_ROUTE": DELETE_ALL_TASKS_ROUTE  }
    return routes

###############################  Usuarios  #####################################

@mongo_router.get(GET_ALL_USERS_ROUTE, response_model=List[Usuario], tags=["MongoDB"])
async def get_all_usuarios():
    usuarios = usuariosRepo.find_all()
    return usuarios

@mongo_router.get(GET_USER_BY_ID_ROUTE, response_model=Usuario, tags=["MongoDB"])
async def get_usuario_by_id(id: str, doRaise: bool = True):
    usuario = usuariosRepo.find_by_id(id)
    if usuario is not None:
        return usuario
    else:
        if doRaise:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
@mongo_router.post(POST_USER_ROUTE, tags=["MongoDB"])
async def add_usuario(usuario: Usuario):
    user = await get_usuario_by_id(usuario.id, False)
    if user is None:
        salioBien = usuariosRepo.add(usuario)
    else:
        salioBien = False
    if salioBien:
        return {"message": "La información se guardo exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="No se guardo la información")
    
@mongo_router.put(PUT_USER_ROUTE, tags=["MongoDB"])
async def update_usuario(usuario: Usuario):
    salioBien = usuariosRepo.update(usuario)
    if salioBien:
        return {"message": "La información se actualizo exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="No se actualizo la información")

@mongo_router.delete(DELETE_USER_BY_ID_ROUTE, tags=["MongoDB"])
async def delete_usuario_by_id(id: str):
    salioBien = usuariosRepo.delete_by_id(id)
    if salioBien:
        return {"message": "Usuario borrado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
@mongo_router.delete(DELETE_ALL_USERS_ROUTE, tags=["MongoDB"])
async def delete_all_usuarios():
    salioBien = usuariosRepo.delete_all()
    if salioBien:
        return {"message": "Se han borrado todos los usuarios"}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
###############################  Tareas  #####################################
    
@mongo_router.get(GET_ALL_TASKS_ROUTE, response_model=List[Tarea], tags=["MongoDB"])
async def get_all_tareas():
    tareasDTO = tareasRepo.find_all()
    tareas = []
    for tareaDto in tareasDTO:
        tareas.append(to_tarea(TareaDTO(**tareaDto)))
    return tareas

@mongo_router.get(GET_TASK_BY_ID_ROUTE, response_model=Tarea, tags=["MongoDB"])
async def get_tarea_by_id(id: str, doRaise: bool = True):
    tareaDto = tareasRepo.find_by_id(id)
    if tareaDto is not None:
        return to_tarea(tareaDto)
    else:
        if doRaise:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
@mongo_router.get(GET_ALL_TASKS_BY_USER_ID, response_model=List[Tarea], tags=["MongoDB"])
async def get_all_tareas_by_user_id(userID: str):
    tareasDto = tareasRepo.find_all_of_userID(userID)
    tareas = []
    for tareaDto in tareasDto:
        tareas.append(to_tarea(TareaDTO(**tareaDto)))
    return tareas
    
@mongo_router.post(POST_TASK_ROUTE, tags=["MongoDB"])
async def add_tarea(tarea: Tarea):
    task = await get_tarea_by_id(str(tarea.id), False)
    if task is None:
        salioBien = tareasRepo.add(to_tareaDto(tarea))
    else:
        salioBien = False
    if salioBien:
        return {"message": "La información se guardo exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="No se guardo la información")
    
@mongo_router.put(PUT_TASK_ROUTE, tags=["MongoDB"])
async def update_tarea(tarea: Tarea):
    salioBien = tareasRepo.update(to_tareaDto(tarea))
    if salioBien:
        return {"message": "La información se actualizo exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="No se actualizo la información")

@mongo_router.delete(DELETE_TASK_BY_ID_ROUTE, tags=["MongoDB"])
async def delete_tarea_by_id(id: str):
    salioBien = tareasRepo.delete_by_id(id)
    if salioBien:
        return {"message": "Tarea borrada exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
@mongo_router.delete(DELETE_ALL_TASKS_ROUTE, tags=["MongoDB"])
async def delete_all_tareas():
    salioBien = tareasRepo.delete_all()
    if salioBien:
        return {"message": "Se han borrado todas las tareas"}
    else:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")