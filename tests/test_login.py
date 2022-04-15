from xml.dom import ValidationErr
import pytest
import copy
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from fastapi import HTTPException
import json


import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, get_db
from auth import AuthHandler
from models import User as ModelUser

auth_handler = AuthHandler()

TEST_CREDENTIALS_JSON = {
    "username": "test_username",
    "password": "test_password"
}

TEST_INVALID_CREDENTIALS_JSON = {
    "username": "bad_username",
    "password": "bad_password"
}

TEST_INVALID_AUTH_SCHEMA_JSON = {
    "username": "test_username"
}

MOCK_USER_OBJ = MagicMock(
    id=0,
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

def test_login():
    response = CLIENT.post("/login", json=TEST_CREDENTIALS_JSON)
    data = response.json()

    assert response.status_code == 200
    assert 'access_token' in data
    assert 'token_type' in data
    assert len(data['access_token']) != 0
    assert data['token_type'] == 'Bearer'


def test_login_invalid_credentials():
    response = CLIENT.post("/login", json=TEST_INVALID_CREDENTIALS_JSON)
    assert response.status_code == 401
    assert json.loads(response.content)['detail']  == 'Username or/and password is invalid.'


def test_auth_schema_validation():
    response = CLIENT.post("/login", json=TEST_INVALID_AUTH_SCHEMA_JSON)

    assert response.status_code == 422
    assert json.loads(response.content)['detail'][0]['msg']  == 'field required'
    assert json.loads(response.content)['detail'][0]['type']  == 'value_error.missing'