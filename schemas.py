from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str

    class Config:
        orm_mode = True