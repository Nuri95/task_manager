from typing import Optional

from pydantic.main import BaseModel

from task_manager.sql_app.enums import Status


class Task(BaseModel):
    status: Status
    result: Optional[dict]
    id: int

    class Config:
        orm_mode = True
