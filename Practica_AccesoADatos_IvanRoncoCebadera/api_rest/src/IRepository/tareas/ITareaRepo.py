from typing import List
from IRepository.IRepository import IRepository
from uuid import UUID
from models.tareas.TareaDTO import TareaDTO

class ITareaRepo(IRepository[TareaDTO, UUID]):
    def find_all_of_userID(self, userID: str) -> List[TareaDTO]:
        raise NotImplementedError("Método abstracto")