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

###############################  Usuarios  #####################################

@mongo_router.get("/usuarios/", response_model=List[Usuario], tags=["MongoDB"])
async def get_all_usuarios():
    usuarios = usuariosRepo.find_all()
    return usuarios

@mongo_router.get("/usuarios/{id}", response_model=Usuario, tags=["MongoDB"])
async def get_usuario_by_id(id: str):
    usuario = usuariosRepo.find_by_id(id)
    if usuario is not None:
        return usuario
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
@mongo_router.post("/usuarios/", tags=["MongoDB"])
async def add_usuario(usuario: Usuario):
    salioBien = usuariosRepo.add(usuario)
    if salioBien:
        return {"message": "La información se guardo exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="No se guardo la información")
    
@mongo_router.put("/usuarios/{item_id}", tags=["MongoDB"])
async def update_usuario(usuario: Usuario):
    salioBien = usuariosRepo.update(usuario)
    if salioBien:
        return {"message": "La información se actualizo exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="No se actualizo la información")

@mongo_router.delete("/usuarios/{id}", tags=["MongoDB"])
async def delete_usuario_by_id(id: str):
    salioBien = usuariosRepo.delete_by_id(id)
    if salioBien:
        return {"message": "Usuario borrado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
@mongo_router.delete("/usuarios/", tags=["MongoDB"])
async def delete_all_usuarios():
    salioBien = usuariosRepo.delete_all()
    if salioBien:
        return {"message": "Se han borrado todos los usuarios"}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
###############################  Tareas  #####################################
    
@mongo_router.get("/tareas/", response_model=List[Tarea], tags=["MongoDB"])
async def get_all_tareas():
    tareasDTO = tareasRepo.find_all()
    tareas = []
    for tareaDto in tareasDTO:
        tareas.append(to_tarea(TareaDTO(**tareaDto)))
    return tareas

@mongo_router.get("/tareas/{id}", response_model=Tarea, tags=["MongoDB"])
async def get_tarea_by_id(id: str):
    tareaDto = tareasRepo.find_by_id(id)
    if tareaDto is not None:
        return to_tarea(tareaDto)
    else:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
@mongo_router.get("/tareas/usuario/{userID}", response_model=List[Tarea], tags=["MongoDB"])
async def get_all_tareas_by_user_id(userID: str):
    tareasDto = tareasRepo.find_all_of_userID(userID)
    tareas = []
    for tareaDto in tareasDto:
        tareas.append(to_tarea(TareaDTO(**tareaDto)))
    return tareas
    
@mongo_router.post("/tareas/", tags=["MongoDB"])
async def add_tarea(tarea: Tarea):
    salioBien = tareasRepo.add(to_tareaDto(tarea))
    if salioBien:
        return {"message": "La información se guardo exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="No se guardo la información")
    
@mongo_router.put("/tareas/{id}", tags=["MongoDB"])
async def update_tarea(tarea: Tarea):
    salioBien = tareasRepo.update(to_tareaDto(tarea))
    if salioBien:
        return {"message": "La información se actualizo exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="No se actualizo la información")

@mongo_router.delete("/tareas/{id}", tags=["MongoDB"])
async def delete_tarea_by_id(id: str):
    salioBien = tareasRepo.delete_by_id(id)
    if salioBien:
        return {"message": "Tarea borrada exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
@mongo_router.delete("/tareas/", tags=["MongoDB"])
async def delete_all_tareas():
    salioBien = tareasRepo.delete_all()
    if salioBien:
        return {"message": "Se han borrado todas las tareas"}
    else:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")