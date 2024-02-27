from pydantic import BaseModel

class Usuario(BaseModel):
    id: str #Gmail, no se puede repetir
    password: str