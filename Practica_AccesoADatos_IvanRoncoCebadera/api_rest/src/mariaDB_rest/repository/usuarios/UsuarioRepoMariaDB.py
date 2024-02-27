from typing import List, Optional
from models.usuarios.Usuario import Usuario
from IRepository.usuarios.IUsuarioRepo import IUsuarioRepo
from IRepository import mariadb_connection

class UsuarioRepoMariaDB(IUsuarioRepo):

    def __init__(self):
        self.connection = mariadb_connection

    def find_all(self) -> List[Usuario]:
        try:
            query = "SELECT * FROM tUsuarios"
            self.cursor.execute(query)
            usuarios = self.cursor.fetchall()
            return [Usuario(id=usuario[0], password=usuario[1]) for usuario in usuarios]
        except: return []

    def find_by_id(self, id: str) -> Optional[Usuario]:
        try:
            query = "SELECT * FROM tUsuarios WHERE id = %s"
            self.cursor.execute(query, (id,))
            usuario = self.cursor.fetchone()
            if usuario is not None:
                return Usuario(id=usuario[0], password=usuario[1])
            return None
        except: None

    def add(self, entity: Usuario) -> bool:
        try:
            query = "INSERT INTO tUsuarios (id, password) VALUES (%s, %s)"
            self.cursor.execute(query, (entity.id, entity.password))
            self.connection.commit()
            return True
        except: return False

    def update(self, entity: Usuario) -> bool:
        try:
            query = "UPDATE tUsuarios SET password = %s WHERE id = %s"
            self.cursor.execute(query, (entity.password, entity.id))
            self.connection.commit()
            return True
        except: return False

    def delete_by_id(self, id: str) -> bool:
        try:
            query = "DELETE FROM tUsuarios WHERE id = %s"
            self.cursor.execute(query, (id,))
            self.connection.commit()
            return True
        except: return False

    def delete_all(self) -> bool:
        try:
            query = "DELETE FROM tUsuarios"
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except: return False
