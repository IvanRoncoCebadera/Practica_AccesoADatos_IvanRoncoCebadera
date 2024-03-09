from typing  import List
from fastapi import APIRouter, HTTPException
from mariaDB_rest.repository.usuarios.UsuarioRepoMariaDB import UsuarioRepoMariaDB
from IRepository.usuarios import IUsuarioRepo
from models.usuarios.Usuario import Usuario
from mariaDB_rest.repository.tareas.TareaRepoMariaDB import TareaRepoMariaDB
from IRepository.tareas import ITareaRepo
from models.tareas.Tarea import Tarea
from models.tareas.ListaTareas import ListaTareas
from models.tareas.TareaMapper import to_tareaDto, to_tarea, to_listatareas, to_listatareasDto
import random
import string

usuariosRepo: IUsuarioRepo = UsuarioRepoMariaDB()
tareasRepo: ITareaRepo = TareaRepoMariaDB()

def generate_validation_code(length: int = 6) -> str: #Esta funcion genera un codigo de validación para simular cuando se creé un usuario
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

maria_router = APIRouter()

GET_ALL_USERS_ROUTE="/usuarios/"
GET_USER_BY_ID_ROUTE="/usuarios/{id}"
POST_USER_ROUTE="/usuarios/"
PUT_USER_ROUTE="/usuarios/"
DELETE_USER_BY_ID_ROUTE="/usuarios/{id}"
DELETE_ALL_USERS_ROUTE="/usuarios/"

GET_ALL_LISTS_ROUTE="/listas/"
GET_LIST_BY_ID_ROUTE="/listas/{id}"
GET_ALL_LISTS_OF_USER_ROUTE="/listas/usuario/{userID}"
GET_ALL_TASKS_BY_LIST_NAME_ROUTE="/listas/nombre/{name}"
GET_ALL_TASKS_BY_LIST_ROUTE="/tareas/{listID}"
POST_LISTS_ROUTE="/listas/"
POST_TASKS_INTO_LIST_ROUTE="/tareas/"
PUT_LISTS_ROUTE="/listas/"
PUT_TASKS_ROUTE="/tareas/"
DELETE_ALL_LISTS_ROUTES="/listas/"
DELETE_LISTS_BY_USER="/listas/usuario/{userID}"
DELETE_LISTS_BY_ID="/listas/{id}"
DELETE_LISTS_BY_NAME="/listas/nombre/{name}"
DELETE_TASKS_BY_ID="/tareas/{id}"

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

        "GET_ALL_LISTS_ROUTE": GET_ALL_LISTS_ROUTE,
        "GET_LIST_BY_ID_ROUTE": GET_LIST_BY_ID_ROUTE,
        "GET_ALL_TASKS_BY_LIST_NAME_ROUTE": GET_ALL_TASKS_BY_LIST_NAME_ROUTE,
        "GET_ALL_LISTS_OF_USER_ROUTE": GET_ALL_LISTS_OF_USER_ROUTE,
        "GET_ALL_TASKS_BY_LIST_ROUTE": GET_ALL_TASKS_BY_LIST_ROUTE,
        "POST_LISTS_ROUTE": POST_LISTS_ROUTE,
        "POST_TASKS_INTO_LIST_ROUTE": POST_TASKS_INTO_LIST_ROUTE,
        "PUT_LISTS_ROUTE": PUT_LISTS_ROUTE,
        "PUT_TASKS_ROUTE": PUT_TASKS_ROUTE,
        "DELETE_ALL_LISTS_ROUTES": DELETE_ALL_LISTS_ROUTES,
        "DELETE_LISTS_BY_USER": DELETE_LISTS_BY_USER,
        "DELETE_LISTS_BY_ID": DELETE_LISTS_BY_ID,
        "DELETE_LISTS_BY_NAME": DELETE_LISTS_BY_NAME,
        "DELETE_TASKS_BY_ID": DELETE_TASKS_BY_ID }
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
        validation_code = generate_validation_code() #Cojo el codigo de validación y lo muestro.
        return {"message": "La información se guardo exitosamente. Se ha enviado un código de validación al usuario.", "validation_code": validation_code}
    else:
        raise HTTPException(status_code=406, detail="No se guardo la información")
    
@maria_router.put(PUT_USER_ROUTE, tags=["MariaDB"])
async def update_usuario(usuario: Usuario):
    salioBien = usuariosRepo.update(usuario)
    if salioBien:
        return {"message": "La información se actualizo exitosamente"}
    else:
        raise HTTPException(status_code=406, detail="No se actualizo la información")

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
    
@maria_router.get(GET_ALL_LISTS_ROUTE, response_model=List[ListaTareas], tags=["MariaDB"])
async def get_all_lists():
    listasDTO = tareasRepo.find_all_list()
    listas = []
    for listaDTO in listasDTO:
        listas.append(to_listatareas(listaDTO))
    return listas

@maria_router.get(GET_LIST_BY_ID_ROUTE, response_model=ListaTareas, tags=["MariaDB"])
async def get_single_list_by_id(id: str):
    lista = tareasRepo.find_single_list_by_id(id)
    if lista is not None:
        return lista
    else:
        raise HTTPException(status_code=404, detail="Lista no encontrada")

@maria_router.get(GET_ALL_LISTS_OF_USER_ROUTE, response_model=List[ListaTareas], tags=["MariaDB"])
async def get_all_lists_of_user(userID: str):
    listasDTO = tareasRepo.find_all_list_by_userId(userID)
    listas = []
    for listaDTO in listasDTO:
        listas.append(to_listatareas(listaDTO))
    return listas

@maria_router.get(GET_ALL_TASKS_BY_LIST_NAME_ROUTE, response_model=List[Tarea], tags=["MariaDB"])
async def get_all_tasks_by_list_name(name: str):
    tareasDTO = tareasRepo.find_tasks_by_list_name(name)
    tareas = []
    for tareaDto in tareasDTO:
        tareas.append(to_tarea(tareaDto))
    return tareas

@maria_router.get(GET_ALL_TASKS_BY_LIST_ROUTE, response_model=List[Tarea], tags=["MariaDB"])
async def get_all_tareas(listID: str):
    tareasDTO = tareasRepo.find_all_of_listID(listID)
    tareas = []
    for tareaDto in tareasDTO:
        tareas.append(to_tarea(tareaDto))
    return tareas

@maria_router.post(POST_LISTS_ROUTE, tags=["MariaDB"])
async def add_list(list: ListaTareas):
    salioBien = tareasRepo.add_list(to_listatareasDto(list))
    if salioBien:
        return {"message": "La información se guardo exitosamente"}
    else:
        raise HTTPException(status_code=406, detail="No se guardo la información")
    
@maria_router.post(POST_TASKS_INTO_LIST_ROUTE, tags=["MariaDB"])
async def add_tarea(tarea: Tarea, userID: str, pwd: str):
    usuario = usuariosRepo.find_by_id(userID)
    if usuario is not None:
        if usuario.password == pwd:
            lista = tareasRepo.find_single_list_by_id(str(tarea.list_id))
            if lista is not None:
                if lista.user_id.lower() == userID.lower():
                    salioBien = tareasRepo.add(to_tareaDto(tarea))
                    if salioBien:
                        return {"message": "La información se guardo exitosamente"}
                    else:
                        raise HTTPException(status_code=406, detail="No se guardo la información")
                else:
                    raise HTTPException(status_code=401, detail="Esa lista no pertenece a tu usuario")
            else:
                raise HTTPException(status_code=404, detail="No existe la lista sobre la que se desea guardar")
        else:
            raise HTTPException(status_code=401, detail="La contraseña es incorrecta")
    else:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    
@maria_router.put(PUT_LISTS_ROUTE, tags=["MariaDB"])
async def update_list(list: ListaTareas):
    salioBien = tareasRepo.update_list(to_listatareasDto(list))
    if salioBien:
        return {"message": "La información se actualizo exitosamente"}
    else:
        raise HTTPException(status_code=406, detail="No se actualizo la información")

@maria_router.put(PUT_TASKS_ROUTE, tags=["MariaDB"])
async def update_tarea(tarea: Tarea):
    salioBien = tareasRepo.update(to_tareaDto(tarea))
    if salioBien:
        return {"message": "La información se actualizo exitosamente"}
    else:
        raise HTTPException(status_code=406, detail="No se actualizo la información")

    
@maria_router.delete(DELETE_ALL_LISTS_ROUTES, tags=["MariaDB"])
async def delete_all_lists():
    salioBien = tareasRepo.delete_all_lists()
    if salioBien:
        return {"message": "Se han borrado todas los datos"}
    else:
        raise HTTPException(status_code=404, detail="Listas no encontradas")
    
@maria_router.delete(DELETE_LISTS_BY_USER, tags=["MariaDB"])
async def delete_all_lists_by_user(userID: str):
    salioBien = tareasRepo.delete_all_lists_by_userId(userID)
    if salioBien:
        return {"message": "Se han borrado todas los datos solicitados"}
    else:
        raise HTTPException(status_code=404, detail="Listas no encontradas")
    
@maria_router.delete(DELETE_LISTS_BY_ID, tags=["MariaDB"])
async def delete_list_by_id(id: str):
    salioBien = tareasRepo.delete_list_by_id(id)
    if salioBien:
        return {"message": "Se han borrado todas los datos solicitados"}
    else:
        raise HTTPException(status_code=404, detail="Listas no encontradas")
    
@maria_router.delete(DELETE_LISTS_BY_NAME, tags=["MariaDB"])
async def delete_list_by_name(name: str):
    lists = tareasRepo.find_all_list()
    namedList = None
    for list in lists:
        if list.name.lower() == name.lower():
            namedList = list
            break
    if namedList is None:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    else:
        return await delete_list_by_id(namedList.id)

@maria_router.delete(DELETE_TASKS_BY_ID, tags=["MariaDB"])
async def delete_tarea_by_id(id: str):
    salioBien = tareasRepo.delete_by_id(id)
    if salioBien:
        return {"message": "Tarea borrada exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")