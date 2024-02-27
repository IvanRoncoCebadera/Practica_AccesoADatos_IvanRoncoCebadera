from datetime import date
from uuid import UUID
from pydantic import BaseModel

class Tarea(BaseModel):
    id: UUID
    user_id: str
    text: str
    created: date
    updated: date
    checked: bool
    important: bool