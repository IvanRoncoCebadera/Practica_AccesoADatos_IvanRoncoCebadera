from datetime import datetime
import uuid
from models.tareas.ListaTareas import ListaTareas
from models.tareas.ListaTareasDTO import ListaTareasDTO
from models.tareas.Tarea import Tarea
from models.tareas.TareaDTO import TareaDTO

def to_tareaDto(tarea: Tarea) -> 'TareaDTO':
    return TareaDTO(
        id=str(tarea.id),
        list_id=str(tarea.list_id),
        text=tarea.text,
        created=tarea.created.strftime("%Y-%m-%d"),
        updated=tarea.updated.strftime("%Y-%m-%d"),
        checked=tarea.checked,
        important=tarea.important
    )

def to_tarea(tarea_dto: TareaDTO) -> Tarea:
    return Tarea(
        id=uuid.UUID(tarea_dto.id),
        list_id=int(tarea_dto.list_id),
        text=tarea_dto.text,
        created=datetime.strptime(tarea_dto.created, "%Y-%m-%d").date(),
        updated=datetime.strptime(tarea_dto.updated, "%Y-%m-%d").date(),
        checked=tarea_dto.checked,
        important=tarea_dto.important
    )

def to_listatareasDto(listaTarea: ListaTareas) -> ListaTareasDTO:
    return ListaTareasDTO(
        id=str(listaTarea.id),
        user_id=listaTarea.user_id,
        name=listaTarea.name,
        created=listaTarea.created.strftime("%Y-%m-%d")
    )

def to_listatareas(listaTareas_dto: ListaTareasDTO) -> ListaTareas:
    return ListaTareas(
        id=int(listaTareas_dto.id),
        user_id=listaTareas_dto.user_id,
        name=listaTareas_dto.name,
        created=datetime.strptime(listaTareas_dto.created, "%Y-%m-%d").date()
    )