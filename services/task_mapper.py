from core.task import Task, generate_object_id, current_datetime
from dto.task_create_dto import TaskCreateDTO
from dto.task_dto import TaskDTO

def convert_from_dto_to_task(dto: TaskCreateDTO) -> Task:
    return Task(
        id=generate_object_id(),
        title=dto.title,
        created_by=dto.created_by,
        date=current_datetime()
    )

def convert_task_to_dto(task: Task) -> TaskDTO:
    return TaskDTO(
        id=task.id,
        title=task.title,
        created_by=task.created_by,
        date=task.date
    )
