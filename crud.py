from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import User as ModelUser
from schemas import (
    UserAuthData as UserAuthSchema,
    UserCreateDB as UserCreateSchema)
from auth import AuthHandler
from sqlalchemy.exc import IntegrityError
from datetime import timedelta

auth_handler = AuthHandler()

def create_user(db: Session, user: UserCreateSchema):
    hashed_password = auth_handler.get_hashed_password(user.password)
    try:
        db_user = ModelUser(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            password=hashed_password
        )
        db.add(db_user)
        db.commit()
    except IntegrityError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

    response = dict(msg=f"User {user.username} successfully created.")

    return response

def remove_user(db: Session, Authorization: str):

    auth_header_split = Authorization.split(" ")

    token_type = auth_header_split[0]
    access_token = auth_header_split[1]

    payload = auth_handler.decode_access_token(access_token)

    if token_type != 'Bearer':
        raise HTTPException(status_code=401, detail='Authorization failed.')
    elif 'sub' in payload:
        user_id = payload['sub']
    else:
        raise HTTPException(
            status_code=401,
            detail=f'Authorization failed.')

    user = db.query(ModelUser).filter(ModelUser.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=403,
            detail=f'Access forbidden.')
    else:
        db.delete(user)
        db.commit()

    response = dict(msg=f'User {user.username} was successfully deleted.')

    return response

def update_user(db: Session, Authorization: str, data: dict):

    auth_header_split = Authorization.split(" ")

    token_type = auth_header_split[0]
    access_token = auth_header_split[1]

    payload = auth_handler.decode_access_token(access_token)


    if token_type != 'Bearer':
        raise HTTPException(status_code=401, detail='Authorization failed.')
    elif 'sub' in payload:
        user_id = payload['sub']
    else:
        raise HTTPException(status_code=401, detail='Authorization failed.')

    user = db.query(ModelUser).filter(ModelUser.id == user_id).first()

    if not user:
        raise HTTPException(status_code=403, detail='Access forbidden.')

    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)
        else:
            raise HTTPException(
                status_code=422,
                detail=f'Error while updating user\'s data.')

    db.commit()

    response = dict(msg=f'User {user.username} was successfully updated.')

    return response

def login(db: Session, auth_data: UserAuthSchema):
    user = db.query(ModelUser).filter(ModelUser.username == auth_data.username).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail='Username or/and password is invalid.')

    if not auth_handler.check_password(auth_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail='Username or/and password is invalid.')

    payload = dict(sub=user.id, username=user.username)

    token = auth_handler.create_access_token(
        data=payload, expires_delta=timedelta(days=1))

    response = dict(access_token=token, token_type='Bearer')

    return response
