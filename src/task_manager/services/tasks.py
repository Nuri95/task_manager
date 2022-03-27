from multiprocessing import Process, Queue
from typing import List

from fastapi import (
    HTTPException,
    Depends,
)
from sqlalchemy.orm import Session

from starlette import status

from task_manager.sql_app import tables
from task_manager.sql_app.database import (
    get_session,
)


def sum1(q, a, b):
    q.put(a+b)


class TasksService:
    count = 0

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get(self, task_id: int, user_id: int) -> tables.Task:
        task = (
            self.session
            .query(tables.Task)
            .filter_by(id=task_id, user_id=user_id)
            .first()
        )
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return task

    def get_list(self, user_id: int) -> List[tables.Task]:
        tasks = (
            self.session
            .query(tables.Task)
            .filter_by(user_id=user_id)
            .all()
        )

        return tasks

    def create(self, user_id: int) -> int:
        task = tables.Task(user_id=user_id)
        self.session.add(task)
        self.session.commit()

        q = Queue()
        p = Process(target=sum1, args=(q, 400, 600))
        p.start()
        p.join()
        sum = q.get()
        p.close()
        print(sum)

        return task.id
