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

###############################  Usuarios  #####################################

@maria_router.get("/usuarios/", response_model=List[Usuario], tags=["MariaDB"])
async def get_all_usuarios():
    usuarios = usuariosRepo.find_all()
    return usuarios

@maria_router.get("/usuarios/{id}", response_model=Usuario, tags=["MariaDB"])
async def get_usuario_by_id(id: str):
    usuario = usuariosRepo.find_by_id(id)
    if usuario is not None:
        return usuario
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
@maria_router.post("/usuarios/", tags=["MariaDB"])
async def add_usuario(usuario: Usuario):
    salioBien = usuariosRepo.add(usuario)
    if salioBien:
        return {"message": "La información se guardo exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="No se guardo la información")
    
@maria_router.put("/usuarios/{item_id}", tags=["MariaDB"])
async def update_usuario(usuario: Usuario):
    salioBien = usuariosRepo.update(usuario)
    if salioBien:
        return {"message": "La información se actualizo exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="No se actualizo la información")

@maria_router.delete("/usuarios/{id}", tags=["MariaDB"])
async def delete_usuario_by_id(id: str):
    salioBien = usuariosRepo.delete_by_id(id)
    if salioBien:
        return {"message": "Usuario borrado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
@maria_router.delete("/usuarios/", tags=["MariaDB"])
async def delete_all_usuarios():
    salioBien = usuariosRepo.delete_all()
    if salioBien:
        return {"message": "Se han borrado todos los usuarios"}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
###############################  Tareas  #####################################
    
@maria_router.get("/tareas/", response_model=List[Tarea], tags=["MariaDB"])
async def get_all_tareas():
    tareasDTO = tareasRepo.find_all()
    tareas = []
    for tareaDto in tareasDTO:
        tareas.append(to_tarea(tareaDto))
    return tareas

@maria_router.get("/tareas/{id}", response_model=Tarea, tags=["MariaDB"])
async def get_tarea_by_id(id: str):
    tareaDto = tareasRepo.find_by_id(id)
    if tareaDto is not None:
        return to_tarea(tareaDto)
    else:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
@maria_router.get("/tareas/usuario/{userID}", response_model=List[Tarea], tags=["MariaDB"])
async def get_all_tareas_by_user_id(userID: str):
    tareasDto = tareasRepo.find_all_of_userID(userID)
    tareas = []
    for tareaDto in tareasDto:
        tareas.append(to_tarea(tareaDto))
    return tareas
    
@maria_router.post("/tareas/", tags=["MariaDB"])
async def add_tarea(tarea: Tarea):
    salioBien = tareasRepo.add(to_tareaDto(tarea))
    if salioBien:
        return {"message": "La información se guardo exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="No se guardo la información")
    
@maria_router.put("/tareas/{id}", tags=["MariaDB"])
async def update_tarea(tarea: Tarea):
    salioBien = tareasRepo.update(to_tareaDto(tarea))
    if salioBien:
        return {"message": "La información se actualizo exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="No se actualizo la información")

@maria_router.delete("/tareas/{id}", tags=["MariaDB"])
async def delete_tarea_by_id(id: str):
    salioBien = tareasRepo.delete_by_id(id)
    if salioBien:
        return {"message": "Tarea borrada exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
@maria_router.delete("/tareas/", tags=["MariaDB"])
async def delete_all_tareas():
    salioBien = tareasRepo.delete_all()
    if salioBien:
        return {"message": "Se han borrado todas las tareas"}
    else:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")