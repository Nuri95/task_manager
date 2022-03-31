import os

from pydantic import BaseSettings

basedir = os.path.abspath(os.path.dirname(__file__))


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    database_url: str = f'sqlite:///{basedir}/sql_app.db'

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 360000000

    class Config:
        env_file = "../../.env"


settings = Settings()
