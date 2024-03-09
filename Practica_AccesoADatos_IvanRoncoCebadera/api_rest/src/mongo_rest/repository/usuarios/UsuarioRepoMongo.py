from typing import List, Optional
from IRepository.usuarios.IUsuarioRepo import IUsuarioRepo
from models.usuarios.Usuario import Usuario
from IRepository import mongo_db

validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["id", "password"],
            "properties": {
                "id": { "bsonType": "string", "description": "Gmail del usuario, no se puede repetir" },
                "password": { "bsonType": "string" }
            }
        }
    }

class UsuarioRepoMongo(IUsuarioRepo):

    def __init__(self):
        self.db = mongo_db.testdb

        try: self.db.create_collection("lista_usuarios", validator = validator)
        except: pass

    def find_all(self) -> List[Usuario]:
        try: 
            users = self.db.lista_usuarios.find()
            return [Usuario(**user) for user in users]
        except: return []

    def find_by_id(self, id: str) -> Optional[Usuario]:
        try: return Usuario(**self.db.lista_usuarios.find_one({"id": id}))
        except: return None

    def add(self, entity: Usuario) -> bool:
        try: self.db.lista_usuarios.insert_one(entity.__dict__)
        except: return False
        else: return True
    
    def update(self, entity: Usuario) -> bool:
        try: self.db.lista_usuarios.update_one({"id":entity.id}, {"$set":entity.__dict__})
        except: return False
        else: return True

    def delete_by_id(self, id: str) -> bool:
        try: self.db.lista_usuarios.delete_one({"id":id})
        except: return False
        else: return True

    def delete_all(self) -> bool:
        try: self.db.lista_usuarios.delete_many({})
        except: return False
        else: return True