from typing  import List
from fastapi import APIRouter, HTTPException
from mariaDB_rest.repository.usuarios.UsuarioRepoMariaDB import UsuarioRepoMariaDB
from IRepository.usuarios import IUsuarioRepo
from models.usuarios.Usuario import Usuario
from mariaDB_rest.repository.tareas.TareaRepoMariaDB import TareaRepoMariaDB
from IRepository.tareas import ITareaRepo
from models.tareas.Tarea import Tarea
from models.tareas.TareaDTO import TareaDTO
from models.tareas.TareaMapper import to_tareaDto, to_tarea

usuariosRepo: IUsuarioRepo = UsuarioRepoMariaDB() #Primero creo la tabal de Usuario

tareasRepo: ITareaRepo = TareaRepoMariaDB() #Luego la de Tarea, esto se debe la clave foranea

maria_router = APIRouter()

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

@maria_router.get("/", tags=["MariaDB"])
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

@maria_router.get(GET_ALL_USERS_ROUTE, response_model=List[Usuario], tags=["MariaDB"])
async def get_all_usuarios():
    usuarios = usuariosRepo.find_all()
    return usuarios

@maria_router.get(GET_USER_BY_ID_ROUTE, response_model=Usuario, tags=["MariaDB"])
async def get_usuario_by_id(id: str):
    usuario = usuariosRepo.find_by_id(id)
    if usuario is not None:
        return usuario
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
@maria_router.post(POST_USER_ROUTE, tags=["MariaDB"])
async def add_usuario(usuario: Usuario):
    salioBien = usuariosRepo.add(usuario)
    if salioBien:
        return {"message": "La información se guardo exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="No se guardo la información")
    
@maria_router.put(PUT_USER_ROUTE, tags=["MariaDB"])
async def update_usuario(usuario: Usuario):
    salioBien = usuariosRepo.update(usuario)
    if salioBien:
        return {"message": "La información se actualizo exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="No se actualizo la información")

@maria_router.delete(DELETE_USER_BY_ID_ROUTE, tags=["MariaDB"])
async def delete_usuario_by_id(id: str):
    salioBien = usuariosRepo.delete_by_id(id)
    if salioBien:
        return {"message": "Usuario borrado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
@maria_router.delete(DELETE_ALL_USERS_ROUTE, tags=["MariaDB"])
async def delete_all_usuarios():
    salioBien = usuariosRepo.delete_all()
    if salioBien:
        return {"message": "Se han borrado todos los usuarios"}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
###############################  Tareas  #####################################
    
@maria_router.get(GET_ALL_TASKS_ROUTE, response_model=List[Tarea], tags=["MariaDB"])
async def get_all_tareas():
    tareasDTO = tareasRepo.find_all()
    tareas = []
    for tareaDto in tareasDTO:
        tareas.append(to_tarea(tareaDto))
    return tareas

@maria_router.get(GET_TASK_BY_ID_ROUTE, response_model=Tarea, tags=["MariaDB"])
async def get_tarea_by_id(id: str):
    tareaDto = tareasRepo.find_by_id(id)
    if tareaDto is not None:
        return to_tarea(tareaDto)
    else:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
@maria_router.get(GET_ALL_TASKS_BY_USER_ID, response_model=List[Tarea], tags=["MariaDB"])
async def get_all_tareas_by_user_id(userID: str):
    tareasDto = tareasRepo.find_all_of_userID(userID)
    tareas = []
    for tareaDto in tareasDto:
        tareas.append(to_tarea(tareaDto))
    return tareas
    
@maria_router.post(POST_TASK_ROUTE, tags=["MariaDB"])
async def add_tarea(tarea: Tarea):
    salioBien = tareasRepo.add(to_tareaDto(tarea))
    if salioBien:
        return {"message": "La información se guardo exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="No se guardo la información")
    
@maria_router.put(PUT_TASK_ROUTE, tags=["MariaDB"])
async def update_tarea(tarea: Tarea):
    salioBien = tareasRepo.update(to_tareaDto(tarea))
    if salioBien:
        return {"message": "La información se actualizo exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="No se actualizo la información")

@maria_router.delete(DELETE_TASK_BY_ID_ROUTE, tags=["MariaDB"])
async def delete_tarea_by_id(id: str):
    salioBien = tareasRepo.delete_by_id(id)
    if salioBien:
        return {"message": "Tarea borrada exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
@maria_router.delete(DELETE_ALL_TASKS_ROUTE, tags=["MariaDB"])
async def delete_all_tareas():
    salioBien = tareasRepo.delete_all()
    if salioBien:
        return {"message": "Se han borrado todas las tareas"}
    else:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")