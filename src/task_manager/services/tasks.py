from concurrent.futures.process import ProcessPoolExecutor
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


def sum(a, b):
    return a+b


class Profiler:
    def __init__(self):
        self.client = httpx.AsyncClient()

    def __enter__(self):
        return self

    async def _get_from_worldtimeapi(self):
        response = await self.client.get(
            'http://worldtimeapi.org/api/timezone/Asia/Yekaterinburg'
        )

        try:
            return response.json()
        except (ConnectionError, KeyError, ValueError) as e:
            print('Api не работает', repr(e))

    async def get_data(self):
        data = await self._get_from_worldtimeapi()
        await self.client.aclose()
        return data

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class TasksService:
    count = 0

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.executor = ProcessPoolExecutor(max_workers=4)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

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

        self.loop.run_until_complete(
            self.fill_result(task.id, user_id)
        )
        self.loop.close()

        return task.id

    async def fill_result(self, task_id: int, user_id):
        sum = await self.loop.run_in_executor(
            self.executor,
            sum,
            400,
            600
        )

        task = self._get(task_id, user_id)
        with Profiler() as p:
            data = await p.get_data()
            date = data['datetime']

        task.status = Status.FINISHED
        task.result = {"sum": sum, "date": date}
        self.session.commit()
