from pydantic import BaseModel

class ListaTareasDTO(BaseModel):
    id: str
    user_id: str
    name: str
    created: str