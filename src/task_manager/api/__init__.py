from fastapi import APIRouter

from task_manager.api.tasks import tasks_router


router = APIRouter()
router.include_router(tasks_router)
