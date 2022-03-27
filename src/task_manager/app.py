from fastapi import FastAPI

from task_manager.api import router

app = FastAPI(
    title='Task manager',
    description='Сервис для задач',
    version='1.0.0'
)
app.include_router(router)


@app.get('/')
def read_root():
    return {'Hello': 'World'}
