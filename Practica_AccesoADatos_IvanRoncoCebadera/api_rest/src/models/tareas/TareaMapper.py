from datetime import datetime
import uuid
from models.tareas.Tarea import Tarea
from models.tareas.TareaDTO import TareaDTO

def to_tareaDto(tarea: Tarea) -> 'TareaDTO':
    return TareaDTO(
        id=str(tarea.id),
        user_id=tarea.user_id,
        text=tarea.text,
        created=tarea.created.strftime("%Y-%m-%d"),
        updated=tarea.updated.strftime("%Y-%m-%d"),
        checked=tarea.checked,
        important=tarea.important
    )

def to_tarea(tarea_dto: TareaDTO) -> Tarea:
    return Tarea(
        id=uuid.UUID(tarea_dto.id),
        user_id=tarea_dto.user_id,
        text=tarea_dto.text,
        created=datetime.strptime(tarea_dto.created, "%Y-%m-%d").date(),
        updated=datetime.strptime(tarea_dto.updated, "%Y-%m-%d").date(),
        checked=tarea_dto.checked,
        important=tarea_dto.important
    )