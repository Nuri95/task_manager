from concurrent.futures.process import ProcessPoolExecutor
from datetime import datetime
from typing import List

import asyncio
import httpx
from fastapi import (
    HTTPException,
    Depends,
)
from httpx import (
    ConnectError,
    TimeoutException,
)
from sqlalchemy.orm import Session

from starlette import status

from task_manager.sql_app import tables
from task_manager.sql_app.database import (
    get_session,
)
from task_manager.sql_app.enums import Status


def calculation(a, b):
    return a + b


class WorldTimeService:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.url = 'http://worldtimeapi.org/api/timezone/Asia/Yekaterinburg'

    async def get_date(self):
        try:
            response = await self.client.get(self.url)
            json = response.json()

            if 'datetime' in json:
                date = json['datetime']
            else:
                unixtime = int(json['unixtime'])
                date = datetime.fromtimestamp(unixtime).isoformat()

            return date
        except (TimeoutException, ConnectError, KeyError, ValueError) as e:
            print('Api не работает', repr(e))
            await self.client.aclose()
            return datetime.now().isoformat()


class TasksService:
    count = 0

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.executor = ProcessPoolExecutor(max_workers=4)
        self.time_service = WorldTimeService()

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
        return self._get(task_id, user_id)

    def get_list(self, user_id: int) -> List[tables.Task]:
        tasks = (
            self.session
            .query(tables.Task)
            .filter_by(user_id=user_id)
            .all()
        )

        return tasks

    async def create(self, user_id: int) -> int:
        task = tables.Task(user_id=user_id)
        self.session.add(task)
        self.session.commit()

        asyncio.create_task(self.fill_result(task.id, user_id))

        return task.id

    async def fill_result(self, task_id: int, user_id):
        loop = asyncio.get_event_loop()

        sum = await loop.run_in_executor(
            self.executor,
            calculation,
            400,
            600
        )
        task = self._get(task_id, user_id)

        date = await self.time_service.get_date()

        task.status = Status.FINISHED
        task.result = {"sum": sum, "date": date}
        self.session.commit()
