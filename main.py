import logging
import crud

import uvicorn
from fastapi import FastAPI
from fastapi import Depends, Header
import os
# from fastapi_sqlalchemy import DBSessionMiddleware
from dotenv import load_dotenv
from schemas import (
    User as SchemaUser,
    UserAuthData as UserAuthSchema,
    UserCreateDB as UserCreateSchema)

from datetime import timedelta
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import SessionLocal
from sqlalchemy.orm import Session


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()

# app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login")
def login(auth_data: UserAuthSchema, db: Session = Depends(get_db)):
    return crud.login(db=db, auth_data=auth_data)

@app.put("/update")
def update(data: dict, Authorization: str = Header(None), db: Session = Depends(get_db)):
    return crud.update_user(db=db, Authorization=Authorization, data=data)

@app.delete("/delete")
def delete(Authorization: str = Header(None), db: Session = Depends(get_db)):
    return crud.remove_user(db=db, Authorization=Authorization)

@app.post("/signup", status_code=201)
def signup(user: UserCreateSchema, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)