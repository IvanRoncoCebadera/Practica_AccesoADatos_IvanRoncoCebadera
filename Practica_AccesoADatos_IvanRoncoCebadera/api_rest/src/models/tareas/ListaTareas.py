from datetime import date
from pydantic import BaseModel

class ListaTareas(BaseModel):
    id: int
    user_id: str
    name: str
    created: date