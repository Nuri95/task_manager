from fastapi import APIRouter

from task_manager.api.auth import auth_router
from task_manager.api.tasks import tasks_router


router = APIRouter()
router.include_router(tasks_router)
router.include_router(auth_router)
