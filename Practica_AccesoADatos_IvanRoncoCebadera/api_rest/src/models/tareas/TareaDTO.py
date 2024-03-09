from pydantic import BaseModel

class TareaDTO(BaseModel):
    id: str
    list_id: str
    text: str
    created: str
    updated: str
    checked: bool
    important: bool