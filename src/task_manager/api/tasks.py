from typing import List

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from task_manager.models.auth import User
from task_manager.models.tasks import Task
from task_manager.services.auth import get_current_user
from task_manager.services.tasks import TasksService
from task_manager.sql_app.database import get_session

tasks_router = APIRouter(
    prefix='/tasks',
    tags=['tasks'],
)


service = TasksService()


@tasks_router.get('/', response_model=List[Task])
def get_tasks(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return service.get_list(session, user.id)


@tasks_router.post('/', response_model=int)
async def create_task(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return await service.create(session, user.id)


@tasks_router.get('/{task_id}', response_model=Task)
def get_task(
    task_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return service.get(session, task_id, user.id)