from datetime import date
from typing import List, Optional
from uuid import UUID
import mariadb
from IRepository.tareas.ITareaRepo import ITareaRepo
from models.tareas.TareaDTO import TareaDTO
from IRepository import mariadb_connection, cursor

class TareaRepoMariaDB(ITareaRepo):

    def __init__(self):
        self.connection = mariadb_connection
        self.cursor = cursor

    def find_all(self) -> List[TareaDTO]:
        try:
            query = "SELECT * FROM tTareas"
            self.cursor.execute(query)
            tareas = self.cursor.fetchall()
            return [TareaDTO(id=tarea[0], user_id=tarea[1], text=tarea[2], created=tarea[3], updated=tarea[4], checked=tarea[5], important=tarea[6]) for tarea in tareas]
        except: return []

    def find_by_id(self, id: UUID) -> Optional[TareaDTO]:
        try:
            query = "SELECT * FROM tTareas WHERE id = %s"
            self.cursor.execute(query, (str(id),))
            tarea = self.cursor.fetchone()
            if tarea is not None:
                return TareaDTO(id=tarea[0], user_id=tarea[1], text=tarea[2], created=tarea[3], updated=tarea[4], checked=tarea[5], important=tarea[6])
            return None
        except: return None

    def find_all_of_userID(self, userID: str) -> List[TareaDTO]:
        try:
            query = "SELECT * FROM tTareas WHERE user_id = %s"
            self.cursor.execute(query, (userID,))
            rows = self.cursor.fetchall()
            return [TareaDTO(id=row[0], user_id=row[1], text=row[2], created=row[3], updated=row[4], checked=row[5], important=row[6]) for row in rows]
        except: return []

    def add(self, entity: TareaDTO) -> bool:
        try:
            query = "INSERT INTO tTareas (id, user_id, text, created, updated, checked, important) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, (str(entity.id), entity.user_id, entity.text, entity.created, date.today(), entity.checked, entity.important))
            self.connection.commit()
            return True
        except:
            return False

    def update(self, entity: TareaDTO) -> bool:
        try:
            query = "UPDATE tTareas SET user_id = %s, text = %s, created = %s, updated = %s, checked = %s, important = %s WHERE id = %s"
            self.cursor.execute(query, (entity.user_id, entity.text, entity.created, date.today(), entity.checked, entity.important, str(entity.id)))
            self.connection.commit()
            return True
        except:
            return False

    def delete_by_id(self, id: UUID) -> bool:
        try:
            query = "DELETE FROM tTareas WHERE id = %s"
            self.cursor.execute(query, (str(id),))
            self.connection.commit()
            return True
        except:
            return False

    def delete_all(self) -> bool:
        try:
            query = "DELETE FROM tTareas"
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except:
            return False
