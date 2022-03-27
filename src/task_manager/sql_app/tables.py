import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from task_manager.sql_app.enums import Status

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.Text)
    email = sqlalchemy.Column(sqlalchemy.Text, unique=True)
    password_hash = sqlalchemy.Column(sqlalchemy.Text)

    tasks = relationship('Task')


class Task(Base):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    status = sqlalchemy.Column(
        sqlalchemy.Enum(Status),
        nullable=False,
        default=Status.IN_PROGRESS,
        server_default=Status.IN_PROGRESS,
    )
    result = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)