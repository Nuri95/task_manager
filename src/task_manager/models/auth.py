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


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    # эти поля обязательные если мы хотим следовать стандарту OAuth
    # в access_token будет лежать jwt