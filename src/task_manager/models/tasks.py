from typing import (
    Optional,
    Union,
)

from pydantic.main import BaseModel

from task_manager.sql_app.enums import Status


class CreateTask(BaseModel):
    value1: Union[int, float]
    value2: Union[int, float]


class Task(BaseModel):
    status: Status
    result: Optional[dict]
    id: int

    class Config:
        orm_mode = True


