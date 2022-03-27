from typing import List

from fastapi import (
    APIRouter,
    Depends,
)

from task_manager.models.auth import User
from task_manager.models.tasks import Task
from task_manager.services.auth import get_current_user
from task_manager.services.tasks import TasksService

tasks_router = APIRouter(
    prefix='/tasks',
    tags=['tasks'],
)


@tasks_router.get('/', response_model=List[Task])
def get_tasks(
    service: TasksService = Depends(),
    user: User = Depends(get_current_user),
):
    return service.get_list(user.id)


@tasks_router.post('/', response_model=int)
def create_task(
    service: TasksService = Depends(),
    user: User = Depends(get_current_user),
):
    return service.create(user.id)


@tasks_router.get('/{task_id}', response_model=Task)
def get_task(
    task_id: int,
    service: TasksService = Depends(),
    user: User = Depends(get_current_user),
):
    return service.get(task_id, user.id)