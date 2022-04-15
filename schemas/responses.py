from pydantic import BaseModel


class ResponseMessage(BaseModel):
    msg: str


class ResponseJWT(BaseModel):
    access_token: str
    token_type: str