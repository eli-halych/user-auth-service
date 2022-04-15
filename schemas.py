from pydantic import BaseModel

class User(BaseModel):
    first_name: str
    last_name: str

class UserAuthData(BaseModel):
    username: str
    password: str

class UserCreateDB(UserAuthData, User):
    pass


class UserInDB(UserAuthData, User):
    id: int

    class Config:
        orm_mode = True