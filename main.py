import logging
import crud

import uvicorn
from fastapi import FastAPI, Response
from fastapi import Depends
from fastapi.responses import JSONResponse
import os

from fastapi.security import HTTPBearer
from dotenv import load_dotenv
from schemas.users import (
    UserAuthData as UserAuthSchema,
    UserCreateDB as UserCreateSchema,
)
from schemas.responses import (
    ResponseMessage as ResponseMessageSchema,
    ResponseJWT as ResponseJWTSchema,
)

from database import SessionLocal
from sqlalchemy.orm import Session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

token_auth_scheme = HTTPBearer()

app = FastAPI()


def get_db() -> SessionLocal:
    """Database session generator.

    Yields:
        SessionLocal: database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/login", status_code=200, response_model=ResponseJWTSchema)
def login(auth_data: UserAuthSchema, db: Session = Depends(get_db)) -> JSONResponse:
    logging.info("Requested /login with authentiation data.")
    return crud.login(db=db, auth_data=auth_data)


@app.put("/update", status_code=200, response_model=ResponseMessageSchema)
def update(
    data: dict,
    authorization: str = Depends(token_auth_scheme),
    db: Session = Depends(get_db),
) -> JSONResponse:
    logging.info("Requested /update with data of the fields to update.")
    token = authorization.credentials
    return crud.update_user(db=db, authorization=token, data=data)


@app.delete("/delete", status_code=200, response_model=ResponseMessageSchema)
def delete(
    authorization: str = Depends(token_auth_scheme), db: Session = Depends(get_db)
) -> JSONResponse:
    logging.info("Requested /delete with an Authorization token in header.")
    token = authorization.credentials
    return crud.remove_user(db=db, authorization=token)


@app.post("/signup", status_code=201, response_model=ResponseMessageSchema)
def signup(user: UserCreateSchema, db: Session = Depends(get_db)) -> JSONResponse:
    logging.info("Requested /signup with user data to create an account with.")
    return crud.create_user(db=db, user=user)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
