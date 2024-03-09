from typing import List, Optional
from IRepository.IRepository import IRepository
from uuid import UUID
from models.tareas.TareaDTO import TareaDTO
from models.tareas.ListaTareasDTO import ListaTareasDTO

class ITareaRepo(IRepository[TareaDTO, UUID]):
    def find_all_of_listID(self, listID: str) -> List[TareaDTO]:
        raise NotImplementedError("Método abstracto")
    
    def delete_all_by_listId(self, listId: int) -> bool:
        raise NotImplementedError("Método abstracto")
    
    def find_single_list_by_id(self, id: str) -> Optional[ListaTareasDTO]:
        raise NotImplementedError("Método abstracto")

    def find_all_list(self) -> List[ListaTareasDTO]:
        raise NotImplementedError("Método abstracto")
    
    def find_all_list_by_userId(self, userId: str) -> List[ListaTareasDTO]:
        raise NotImplementedError("Método abstracto")
    
    def find_tasks_by_list_name(self, name: str) -> List[TareaDTO]:
        raise NotImplementedError("Método abstracto")

    def find_list_by_id(self, id: str) -> List[TareaDTO]:
        raise NotImplementedError("Método abstracto")

    def add_list(self, entity: ListaTareasDTO) -> bool:
        raise NotImplementedError("Método abstracto")
    
    def update_list(self, entity: ListaTareasDTO) -> bool:
        raise NotImplementedError("Método abstracto")

    def delete_list_by_id(self, id: str) -> bool:
        raise NotImplementedError("Método abstracto")

    def delete_all_lists(self) -> bool:
        raise NotImplementedError("Método abstracto")
    
    def delete_all_lists_by_userId(self, userId: str) -> bool:
        raise NotImplementedError("Método abstracto")