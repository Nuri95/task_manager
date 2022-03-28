from concurrent.futures.process import ProcessPoolExecutor
from multiprocessing import Process, Queue
from typing import List

import asyncio
import httpx
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
from task_manager.sql_app.enums import Status


def sum1(a, b):
    return a+b


class TasksService:
    count = 0

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, task_id: int, user_id: int):
        task = (
            self.session
            .query(tables.Task)
            .filter_by(id=task_id, user_id=user_id)
            .first()
        )
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return task

    def get(self, task_id: int, user_id: int) -> tables.Task:
        return self._get(task_id, user_id).first()

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

        self.fill_result(task.id, user_id)

        return task.id

    async def get_datetime(self):
        async with httpx.AsyncClient() as client:
            response = await client.get('http://worldtimeapi.org/api/timezone/Asia/Yekaterinburg')

        try:
            json = response.json()
            return json['datetime']
        except (ConnectionError, KeyError, ValueError) as e:
            print('Api не работает')

    def fill_result(self, task_id: int, user_id):
        with ProcessPoolExecutor(max_workers=4) as executor:
            future = executor.submit(sum1, 400, 600)
            sum = future.result(timeout=900)
            print(sum)
            task = self._get(task_id, user_id)

            date = asyncio.run(self.get_datetime())

            task.status = Status.FINISHED
            task.result = {"sum": sum, "date": date}
            self.session.commit()

