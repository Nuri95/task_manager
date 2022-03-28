from pydantic.main import BaseModel


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
#  orm_mode сообщит модели Pydantic о необходимости чтения данных,
#  даже если это не dict, а модель ORM


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'