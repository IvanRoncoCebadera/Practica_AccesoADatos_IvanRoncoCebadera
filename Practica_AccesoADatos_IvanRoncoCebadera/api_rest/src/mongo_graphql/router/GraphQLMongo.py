from fastapi import HTTPException
from typing import List
from models.usuarios.Usuario import Usuario
from IRepository.usuarios.IUsuarioRepo import IUsuarioRepo
from mongo_rest.repository.usuarios.UsuarioRepoMongo import UsuarioRepoMongo
from models.tareas.TareaDTO import TareaDTO
from mongo_rest.repository.tareas.TareaRepoMongo import TareaRepoMongo
from IRepository.tareas import ITareaRepo
from models.tareas.ListaTareasDTO import ListaTareasDTO
import strawberry
import random
import string

tareasRepo: ITareaRepo = TareaRepoMongo()
usuariosRepo: IUsuarioRepo = UsuarioRepoMongo()

def generate_validation_code(length: int = 6) -> str: #Esta funcion genera un codigo de validación para simular cuando se creé un usuario
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

########################################### Usuarios #####################################

@strawberry.experimental.pydantic.type(model=Usuario, all_fields=True)
class UserType:
    pass

@strawberry.experimental.pydantic.input(model=Usuario, all_fields=True)
class UsuarioInput:
    pass

@strawberry.type
class UsuarioQuery:
    @strawberry.field
    def obtener_usuarios() -> List[UserType]:
        users = usuariosRepo.find_all()
        return [UserType.from_pydantic(user) for user in users]
    
    @strawberry.field
    def obtener_por_id(id: str) -> UserType:
        user = usuariosRepo.find_by_id(id)
        if user is not None:
            return UserType.from_pydantic(user)
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

@strawberry.type
class UsuarioMutation:
    @strawberry.mutation
    def crear(usuario_input: UsuarioInput) -> str:
        if usuariosRepo.add(usuario_input.to_pydantic()):
            return "Validation code: "+generate_validation_code()
        else:
            raise HTTPException(status_code=406, detail="La informacion no se ha guardado")
        
    @strawberry.mutation
    def actualizar(usuario_input: UsuarioInput) -> str:
        if usuariosRepo.update(usuario_input.to_pydantic()):
            return "OK: El usuario se actualizo correctamente"
        else:
            raise HTTPException(status_code=406, detail="La informacion no se ha guardado")
        
    @strawberry.mutation
    def eliminar_por_id(id: str) -> str:
        if usuariosRepo.delete_by_id(id):
            return "OK: El usuario se borro correctamente"
        else:
            raise HTTPException(status_code=404, detail="El usuario no se ha encontrado")
        
    @strawberry.mutation
    def eliminar_usuarios() -> str:
        if usuariosRepo.delete_all():
            return "OK: La infromación se borro correctamente"
        else:
            raise HTTPException(status_code=406, detail="La información no se a podido guardar")
        

users_schema = strawberry.Schema(query=UsuarioQuery, mutation=UsuarioMutation)

############################################ Listas #####################################
        
@strawberry.experimental.pydantic.type(model=ListaTareasDTO, all_fields=True)
class ListaType:
    pass

@strawberry.experimental.pydantic.input(model=ListaTareasDTO, all_fields=True)
class ListaInput:
    pass

@strawberry.type
class ListaQuery:
    @strawberry.field
    def obtener_listas() -> List[ListaType]:
        listasDTO = tareasRepo.find_all_list()
        return [ListaType.from_pydantic(ListaTareasDTO(**listaDTO)) for listaDTO in listasDTO]
    
    @strawberry.field
    def obtener_por_id(id: str) -> ListaType:
        listaDTO = tareasRepo.find_single_list_by_id(id)
        if listaDTO is not None:
            return ListaType.from_pydantic(listaDTO)
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    @strawberry.field
    def obtener_por_user_id(user_id: str) -> List[ListaType]:
        listasDTO = tareasRepo.find_all_list_by_userId(user_id)
        return [ListaType.from_pydantic(ListaTareasDTO(**listaDTO)) for listaDTO in listasDTO]

@strawberry.type
class ListaMutation:
    # def __init__(self): # El constructor no ayuda con el problema del self
    #     pass

    @strawberry.mutation
    def crear(lista_input: ListaInput) -> str:
        if tareasRepo.find_single_list_by_id(lista_input.id) is not None:
            print("Hola!!!")
            salioBien = False
        else:
            if usuariosRepo.find_by_id(lista_input.user_id) is not None:
                salioBien = tareasRepo.add_list(lista_input.to_pydantic())
            else:
                raise HTTPException(status_code=404, detail="No existe usuario al que asignar la lista")
        if salioBien:
            return "OK: La información se guardo exitosamente"
        else:
            raise HTTPException(status_code=406, detail="La informacion no se ha guardado")

    @strawberry.mutation
    def actualizar(lista_input: ListaInput) -> str:
        if tareasRepo.update_list(lista_input.to_pydantic()):
            return "OK: La lista se actualizo correctamente"
        else:
            raise HTTPException(status_code=406, detail="La informacion no se ha guardado")
        
    @strawberry.mutation
    def eliminar_por_id(id: str) -> str:
        salioBien = tareasRepo.delete_list_by_id(id)
        if salioBien:
            salioBien = tareasRepo.delete_all_by_listId(id)
            if salioBien:
                return "OK: Se han borrado todas los datos"
            else:
                raise HTTPException(status_code=404, detail="Tareas no encontrada")
        else:
            raise HTTPException(status_code=404, detail="Listas no encontrada")
        
    @strawberry.mutation
    def eliminar_por_nombre(self, name: str) -> str:
        lists = tareasRepo.find_all_list()
        namedList = None
        for list in lists:
            listDTO = ListaTareasDTO(**list)
            if listDTO.name.lower() == name.lower():
                namedList = listDTO
                break
        if namedList is None:
            raise HTTPException(status_code=404, detail="Lista no encontrada")
        else:
            # self -> None (Strawberry tiene problemas con esto!!)
            # return self.eliminar_lista_por_id(namedList.id)
            # No me queda otra que repetir el código:
            salioBien = tareasRepo.delete_list_by_id(namedList.id)
            if salioBien:
                salioBien = tareasRepo.delete_all_by_listId(namedList.id)
                if salioBien:
                    return "OK: Se han borrado todas los datos"
                else:
                    raise HTTPException(status_code=404, detail="Tareas no encontradas")
            else:
                raise HTTPException(status_code=404, detail="Listas no encontradas")
        
    @strawberry.mutation
    def eliminar_listas() -> str:
        salioBien = tareasRepo.delete_all_lists()
        if salioBien:
            salioBien = tareasRepo.delete_all()
            if salioBien:
                return "OK: Se han borrado todas los datos"
            else:
                raise HTTPException(status_code=404, detail="Tareas no encontradas")
        else:
            raise HTTPException(status_code=404, detail="Listas no encontradas")

lists_schema = strawberry.Schema(query=ListaQuery, mutation=ListaMutation)

############################################ Listas #####################################
        
@strawberry.experimental.pydantic.type(model=TareaDTO, all_fields=True)
class TareaType:
    pass

@strawberry.experimental.pydantic.input(model=TareaDTO, all_fields=True)
class TareaInput:
    pass

@strawberry.type
class TareaQuery:
    @strawberry.field
    def obtener_tareas_por_nombre_lista(name: str) -> List[TareaType]:
        tareasDTO = tareasRepo.find_tasks_by_list_name(name)
        return [TareaType.from_pydantic(TareaDTO(**tareaDTO)) for tareaDTO in tareasDTO]
    
    @strawberry.field
    def obtener_tareas_por_id_lista(list_id: str) -> List[TareaType]:
        tareasDTO = tareasRepo.find_all_of_listID(list_id)
        return [TareaType.from_pydantic(TareaDTO(**tareaDTO)) for tareaDTO in tareasDTO]

@strawberry.type
class TareaMutation:
    def __init__(self):
        pass

    @strawberry.mutation
    def crear(self, tarea_input: TareaInput, user_id: str, pwd: str) -> str:
        usuario = usuariosRepo.find_by_id(user_id)
        if usuario is not None:
            if usuario.password == pwd:
                lista = tareasRepo.find_single_list_by_id(tarea_input.list_id)
                if lista is not None:
                    if lista.user_id.lower() == user_id.lower():
                        # tareas = self.obtener_tareas_por_id_lista(tarea_input.listId) # Otra vez más, el self no funciona (es None)
                        tareasDTO = tareasRepo.find_all_of_listID(tarea_input.list_id)
                        tareas = [TareaType.from_pydantic(TareaDTO(**tareaDTO)) for tareaDTO in tareasDTO]
                    
                        salioBien = True
                        for task in tareas:
                            if task.id == tarea_input.id:
                                salioBien = False
                                break

                        if salioBien:
                            salioBien = tareasRepo.add(tarea_input.to_pydantic())
                            if salioBien:
                                return "OK: La información se guardo exitosamente"
                            else:
                                raise HTTPException(status_code=406, detail="No se guardo la información")
                        else:
                            raise HTTPException(status_code=400, detail="La tarea ya existe")
                    else:
                        raise HTTPException(status_code=401, detail="Esa lista no pertenece a tu usuario")
                else:
                    raise HTTPException(status_code=404, detail="No existe la lista sobre la que se desea guardar")
            else:
                raise HTTPException(status_code=401, detail="La contraseña es incorrecta")
        else:
            raise HTTPException(status_code=404, detail="El usuario no existe")

    @strawberry.mutation
    def actualizar(tarea_input: TareaInput) -> str:
        if tareasRepo.update(tarea_input.to_pydantic()):
            return "OK: La tarea se actualizo correctamente"
        else:
            raise HTTPException(status_code=406, detail="La informacion no se ha guardado")
        
    @strawberry.mutation
    def eliminar_por_id(id: str) -> str:
        salioBien = tareasRepo.delete_by_id(id)
        if salioBien:
            return "OK: Tarea borrada exitosamente"
        else:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")

tasks_schema = strawberry.Schema(query=TareaQuery, mutation=TareaMutation)