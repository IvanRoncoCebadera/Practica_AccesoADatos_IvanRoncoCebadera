from datetime import date
from typing import List, Optional
from uuid import UUID
from IRepository.tareas.ITareaRepo import ITareaRepo
from models.tareas.ListaTareasDTO import ListaTareasDTO
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
            return [TareaDTO(id=tarea[0], list_id=str(tarea[1]), text=tarea[2], created=tarea[3], updated=tarea[4], checked=tarea[5], important=tarea[6]) for tarea in tareas]
        except: return []

    def find_by_id(self, id: UUID) -> Optional[TareaDTO]:
        try:
            query = "SELECT * FROM tTareas WHERE id = %s"
            self.cursor.execute(query, (str(id),))
            tarea = self.cursor.fetchone()
            if tarea is not None:
                return TareaDTO(id=tarea[0], list_id=str(tarea[1]), text=tarea[2], created=tarea[3], updated=tarea[4], checked=tarea[5], important=tarea[6])
            return None
        except: return None

    def find_all_of_listID(self, listID: str) -> List[TareaDTO]:
        try:
            query = "SELECT * FROM tTareas WHERE list_id = %s"
            self.cursor.execute(query, (listID,))
            rows = self.cursor.fetchall()
            return [TareaDTO(id=row[0], list_id=str(row[1]), text=row[2], created=row[3], updated=row[4], checked=row[5], important=row[6]) for row in rows]
        except Exception as e:
            print(e)
            return []

    def add(self, entity: TareaDTO) -> bool:
        try:
            query = "INSERT INTO tTareas (id, list_id, text, created, updated, checked, important) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, (str(entity.id), entity.list_id, entity.text, entity.created, date.today(), entity.checked, entity.important))
            self.connection.commit()
            return True
        except: return False

    def update(self, entity: TareaDTO) -> bool:
        try:
            query = "UPDATE tTareas SET list_id = %s, text = %s, created = %s, updated = %s, checked = %s, important = %s WHERE id = %s"
            self.cursor.execute(query, (entity.list_id, entity.text, entity.created, date.today(), entity.checked, entity.important, str(entity.id)))
            self.connection.commit()
            return True
        except: return False

    def delete_by_id(self, id: UUID) -> bool:
        try:
            query = "DELETE FROM tTareas WHERE id = %s"
            self.cursor.execute(query, (str(id),))
            self.connection.commit()
            return True
        except: return False

    def delete_all(self) -> bool:
        try:
            query = "DELETE FROM tTareas"
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except: return False
        
    def delete_all_by_listId(self, listId: int) -> bool:
        try:
            query = "DELETE FROM tTareas WHERE list_id = %s"
            self.cursor.execute(query, (str(listId),))
            self.connection.commit()
            return True
        except: return False

    def find_single_list_by_id(self, id: str) ->  Optional[ListaTareasDTO]:
        try:
            self.cursor.execute("SELECT * FROM tListas WHERE id = %s", (str(id),))
            lista = self.cursor.fetchone()
            return ListaTareasDTO(
                    id=str(lista[0]),
                    user_id=lista[1],
                    name=lista[2],
                    created=lista[3]
                )
        except: return None
        
    def find_all_list(self) -> List[ListaTareasDTO]:
        try:
            self.cursor.execute("SELECT * FROM tListas")
            results = self.cursor.fetchall()
            lista_tareas = []
            for row in results:
                lista_tareas.append(ListaTareasDTO(
                    id=str(row[0]),
                    user_id=row[1],
                    name=row[2],
                    created=row[3]
                ))
            return lista_tareas
        except: return []


    def find_all_list_by_userId(self, userId: str) -> List[ListaTareasDTO]:
        try:
            self.cursor.execute("SELECT * FROM tListas WHERE user_id = %s", (userId,))
            results = self.cursor.fetchall()
            lista_tareas = []
            for row in results:
                lista_tareas.append(ListaTareasDTO(
                    id=str(row[0]),
                    user_id=row[1],
                    name=row[2],
                    created=row[3]
                ))
            return lista_tareas
        except: return []

    def find_tasks_by_list_name(self, name: str) -> List[TareaDTO]:
        try:
            self.cursor.execute("SELECT * FROM tListas WHERE name = %s", (name,))
            result = self.cursor.fetchone()
            lista = ListaTareasDTO(
                    id=str(result[0]),
                    user_id=result[1],
                    name=result[2],
                    created=result[3]
                )
            tareas = self.find_all_of_listID(lista.id)
            print(tareas)
            return tareas
        except: return []

    def find_list_by_id(self, id: str) -> ListaTareasDTO:
        try:
            self.cursor.execute("SELECT * FROM tListas WHERE id = %s", (id,))
            result = self.cursor.fetchone()
            if result:
                return ListaTareasDTO(**result)
            else:
                return None
        except: return None

    def add_list(self, entity: ListaTareasDTO) -> bool:
        try:
            insert_query = """
                INSERT INTO tListas (user_id, name, created)
                VALUES (%s, %s, %s)
            """
            data = (entity.user_id, entity.name, entity.created)
            self.cursor.execute(insert_query, data)
            self.connection.commit()
            return True
        except: return False

    def update_list(self, entity: ListaTareasDTO) -> bool:
        try:
            update_query = """
                UPDATE tListas
                SET user_id = %s, name = %s, created = %s
                WHERE id = %s
            """
            data = (entity.user_id, entity.name, entity.created, entity.id)
            self.cursor.execute(update_query, data)
            self.connection.commit()
            return True
        except: return False

    def delete_list_by_id(self, id: str) -> bool:
        try:
            delete_query = "DELETE FROM tListas WHERE id = %s"
            self.cursor.execute(delete_query, (id,))
            self.connection.commit()
            return True
        except: return False

    def delete_all_lists(self) -> bool:
        try:
            delete_query = "DELETE FROM tListas"
            self.cursor.execute(delete_query)
            self.connection.commit()
            return True
        except: return False

    def delete_all_lists_by_userId(self, userId: str) -> bool:
        try:
            delete_query = "DELETE FROM tListas WHERE user_id = %s"
            self.cursor.execute(delete_query, (userId,))
            self.connection.commit()
            return True
        except: return False