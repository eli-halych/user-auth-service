from email import header
from xml.dom import ValidationErr
import pytest
import copy
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from fastapi import HTTPException
import json
import dotenv



import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, get_db
from auth import AuthHandler
from models import User as ModelUser
# from auth import load_dotenv
# load_dotenv = dotenv.load_dotenv('.env_test')

auth_handler = AuthHandler()

TEST_CREDENTIALS_JSON = {
    "username": "test_username",
    "password": "test_password"
}

TEST_DATA_JSON = {
    "first_name": "test_name",
    "last_name": "test_name"
}

TEST_INVALID_DATA_JSON = {
    "wrong_field": "test_value"
}

TEST_JWT_HEADER = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsInVzZXJuYW1lIjoidGVzdF91c2VybmFtZSIsImV4cCI6MTY1MDExMjU2Mn0.KsEMSh974zYzeHVB0EBzByelPTmid0mFQkTMWSV_w7s"
TEST_TOKEN_NO_SUB = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3RfdXNlcm5hbWUiLCJleHAiOjE2NTAxMTIzNjl9.h91T4OqjMsrEZRgH3cyZacgF3lYjmzIcSTsqoeUOCFo"

MOCK_USER_OBJ = MagicMock(
    id=1,
    username=TEST_CREDENTIALS_JSON['username'],
    password=auth_handler.get_hashed_password(TEST_CREDENTIALS_JSON['password'])
    )

def override_get_db():
    try:
        db = MagicMock()
        db.query.return_value.filter.return_value.first.return_value = MOCK_USER_OBJ
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

CLIENT = TestClient(app)

def test_invalid_token_type():
    token_type = 'WrongType'

    response = CLIENT.delete(
        "/delete",
        headers={
            "Authorization": f"{token_type} {TEST_JWT_HEADER}"
            })

    assert response.status_code == 401
    assert json.loads(response.content)['detail']  == 'Authorization failed.'

def test_missing_sub_jwt():

    response = CLIENT.delete(
        "/delete",
        headers={
            "Authorization": f"Bearer {TEST_TOKEN_NO_SUB}"
            })

    assert response.status_code == 401
    assert json.loads(response.content)['detail']  == 'Authorization failed.'

def test_missing_user():

    def override_get_db():
        try:
            db = MagicMock()
            db.query.return_value.filter.return_value.first.return_value = None
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    response = client.delete(
        "/delete",
        json=TEST_DATA_JSON,
        headers={
            "Authorization": f"Bearer {TEST_JWT_HEADER}"
            })

    assert response.status_code == 403
    assert json.loads(response.content)['detail']  == 'Access forbidden.'
