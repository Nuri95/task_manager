import uvicorn

from task_manager.settings import settings

uvicorn.run(
    'task_manager.app:app',
    host=settings.server_host,
    port=settings.server_port,
    reload=True,
)
