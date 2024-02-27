from datetime import date
from typing import List, Optional
from uuid import UUID
from IRepository.tareas.ITareaRepo import ITareaRepo
from models.tareas.TareaDTO import TareaDTO
from IRepository import mongo_db

validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["id", "user_id", "text", "created", "updated", "checked", "important"],
        "properties": {
            "id": { "bsonType": "string", "description": "UUID de la tarea" },
            "user_id": { "bsonType": "string", "description": "id del usuario a quien pertenece" },
            "text": { "bsonType": "string", "description": "Texto de la tarea" },
            "created": { "bsonType": "string", "description": "Fecha de creación de la tarea" },
            "updated": { "bsonType": "string", "description": "Fecha de actualización de la tarea" },
            "checked": { "bsonType": "bool", "description": "Indica si la tarea está marcada como completada" },
            "important": { "bsonType": "bool", "description": "Indica si la tarea es importante" }
        }
    }
}

class TareaRepoMongo(ITareaRepo):

    def __init__(self):
        self.db = mongo_db.testdb

        try: self.db.create_collection("lista_tareas", validator = validator)
        except: pass

    def find_all(self) -> List[TareaDTO]:
        try: return list(self.db.lista_tareas.find())
        except: return []

    def find_by_id(self, id: UUID) -> Optional[TareaDTO]:
        try:
            return TareaDTO(**self.db.lista_tareas.find_one({"id": id}))
        except: return None

    def find_all_of_userID(self, userID: str) -> List[TareaDTO]:
        try:
            return list(self.db.lista_tareas.find({"user_id": userID}))
        except: return None

    def add(self, entity: TareaDTO) -> bool:
        try: 
            tarea = TareaDTO(
                id=entity.id,
                user_id=entity.user_id,
                text=entity.text,
                created=entity.created,
                updated=date.today().strftime("%Y-%m-%d"),
                checked=entity.checked,
                important=entity.important
            ) #Ningun método del tipo: entity.copy() o entity.model_copy() que probe funciono!!

            self.db.lista_tareas.insert_one(tarea.__dict__)
        except: return False
        else: return True
    
    def update(self, entity: TareaDTO) -> bool:
        try: 
            tarea = TareaDTO(
                id=entity.id,
                user_id=entity.user_id,
                text=entity.text,
                created=entity.created,
                updated=date.today().strftime("%Y-%m-%d"),
                checked=entity.checked,
                important=entity.important
            ) #Ningun método del tipo: entity.copy() o entity.model_copy() que probe funciono!!

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