from typing import Optional

from pydantic.main import BaseModel
from pydantic.types import Json

from task_manager.sql_app.enums import Status


class Task(BaseModel):
    status: Status
    result: Optional[Json]
    id: int

    class Config:
        orm_mode = True
