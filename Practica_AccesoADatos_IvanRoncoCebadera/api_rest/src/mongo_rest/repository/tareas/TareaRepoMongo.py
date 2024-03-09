from datetime import date
from typing import List, Optional
from uuid import UUID
from IRepository.tareas.ITareaRepo import ITareaRepo
from models.tareas.ListaTareasDTO import ListaTareasDTO
from models.tareas.TareaDTO import TareaDTO
from IRepository import mongo_db

validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["id", "list_id", "text", "created", "updated", "checked", "important"],
        "properties": {
            "id": { "bsonType": "string", "description": "UUID de la tarea" },
            "list_id": { "bsonType": "string", "description": "id de la lista a la que pertenece" },
            "text": { "bsonType": "string", "description": "Texto de la tarea" },
            "created": { "bsonType": "string", "description": "Fecha de creación de la tarea" },
            "updated": { "bsonType": "string", "description": "Fecha de actualización de la tarea" },
            "checked": { "bsonType": "bool", "description": "Indica si la tarea está marcada como completada" },
            "important": { "bsonType": "bool", "description": "Indica si la tarea es importante" }
        }
    }
}

validator_lists = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["id", "user_id", "name", "created"],
        "properties": {
            "id": { "bsonType": "string", "description": "id de la lista de tareas" },
            "user_id": { "bsonType": "string", "description": "id del usuario a quien pertenece" },
            "name": { "bsonType": "string", "description": "Nombre de la lista de tareas" },
            "created": { "bsonType": "string", "description": "Fecha de creación de la lista de tareas" }
        }
    }
}

class TareaRepoMongo(ITareaRepo):

    def __init__(self):
        self.db = mongo_db.testdb

        try: 
            self.db.create_collection("lista_tareas", validator = validator)
            self.db.create_collection("coleccion_listas", validator = validator_lists)
        except: pass

    def find_all(self) -> List[TareaDTO]:
        try: return list(self.db.lista_tareas.find())
        except: return []

    def find_by_id(self, id: UUID) -> Optional[TareaDTO]:
        try: return TareaDTO(**self.db.lista_tareas.find_one({"id": id}))
        except: return None

    def find_all_of_listID(self, listID: str) -> List[TareaDTO]:
        try:  return list(self.db.lista_tareas.find({"list_id": listID}))
        except: return []

    def add(self, entity: TareaDTO) -> bool:
        try: 
            tarea = TareaDTO(
                id=entity.id,
                list_id=entity.list_id,
                text=entity.text,
                created=entity.created,
                updated=date.today().strftime("%Y-%m-%d"),
                checked=entity.checked,
                important=entity.important
            ) #Ningun método del tipo: entity.copy() o entity.model_copy() que probe funciono!! (Esto lo hago, por lo del campo 'update')

            self.db.lista_tareas.insert_one(tarea.__dict__)
        except: return False
        else: return True
    
    def update(self, entity: TareaDTO) -> bool:
        try: 
            tarea = TareaDTO(
                id=entity.id,
                list_id=entity.list_id,
                text=entity.text,
                created=entity.created,
                updated=date.today().strftime("%Y-%m-%d"),
                checked=entity.checked,
                important=entity.important
            ) #Ningun método del tipo: entity.copy() o entity.model_copy() que probe funciono!! (Esto lo hago, por lo del campo 'update')

            self.db.lista_tareas.update_one({"id":tarea.id}, {"$set":tarea.__dict__})
        except: return False
        else: return True

    def delete_by_id(self, id: UUID) -> bool:
        try: self.db.lista_tareas.delete_one({"id":id})
        except: return False
        else: return True

    def delete_all(self) -> bool:
        try: self.db.lista_tareas.delete_many({})
        except: return False
        else: return True

    def delete_all_by_listId(self, listId: str) -> bool:
        try: 
            self.db.lista_tareas.delete_many({"list_id":listId})
            print(listId)
        except: return False
        else: return True

    def find_single_list_by_id(self, id: str) -> Optional[ListaTareasDTO]:
        try: return ListaTareasDTO(**self.db.coleccion_listas.find_one({"id": id}))
        except: return None

    def find_all_list(self) -> List[ListaTareasDTO]:
        try: return list(self.db.coleccion_listas.find())
        except: return []
    
    def find_all_list_by_userId(self, userId: str) -> List[ListaTareasDTO]:
        try: return list(self.db.coleccion_listas.find({"user_id":userId}))
        except: return []

    def find_tasks_by_list_name(self, name: str) -> List[TareaDTO]:
        try: 
            list = ListaTareasDTO(**self.db.coleccion_listas.find_one({"name": name}))
            return self.find_all_of_listID(list.id)
        except: return []

    def find_list_by_id(self, id: str) -> List[TareaDTO]:
        try: 
            list = ListaTareasDTO(**self.db.coleccion_listas.find_one({"id": id}))
            return self.find_all_of_listID(list.id)
        except: return []

    def add_list(self, entity: ListaTareasDTO) -> bool:
        try: self.db.coleccion_listas.insert_one(entity.__dict__)
        except:return False
        else: return True
    
    def update_list(self, entity: ListaTareasDTO) -> bool:
        try: self.db.coleccion_listas.update_one({"id":entity.id}, {"$set":entity.__dict__})
        except: return False
        else: return True

    def delete_list_by_id(self, id: str) -> bool:
        try: self.db.coleccion_listas.delete_one({"id":id})
        except: return False
        else: return True

    def delete_all_lists(self) -> bool:
        try: self.db.coleccion_listas.delete_many({})
        except: return False
        else: return True

    def delete_all_lists_by_userId(self, userId: str) -> bool:
        try: self.db.coleccion_listas.delete_many({"user_id":userId})
        except: return False
        else: return True