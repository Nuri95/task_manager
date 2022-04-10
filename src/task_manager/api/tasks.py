from typing import List

from fastapi import (
    APIRouter,
    Depends,
)

from task_manager.models.auth import User
from task_manager.models.tasks import (
    Task,
    CreateTask,
)
from task_manager.services.auth import get_current_user
from task_manager.services.tasks import TasksService
from task_manager.sql_app.database import get_db_session

tasks_router = APIRouter(
    prefix='/tasks',
    tags=['tasks'],
)

db_session = get_db_session().__next__()
service = TasksService(db_session)


@tasks_router.on_event("shutdown")
async def shutdown_event():
    await service.time_service.aclose()


@tasks_router.get('/', response_model=List[Task])
def get_tasks(
    user: User = Depends(get_current_user),
):
    return service.get_list(user.id)


@tasks_router.post('/', response_model=int)
async def create_task(
    task_data: CreateTask,
    user: User = Depends(get_current_user),
):
    return await service.create(user.id, task_data.dict())


@tasks_router.get('/{task_id}', response_model=Task)
def get_task(
    task_id: int,
    user: User = Depends(get_current_user),
):
    return service.get(task_id, user.id)