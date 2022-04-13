from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str

class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True

class User(UserInDBBase):
    pass
