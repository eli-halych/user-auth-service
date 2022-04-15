import pytest
import json

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import AuthHandler

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

def test_login(client_fixture):

    response = client_fixture.post("/login", json=TEST_CREDENTIALS_JSON)
    data = response.json()

    assert response.status_code == 200
    assert 'access_token' in data
    assert 'token_type' in data
    assert len(data['access_token']) != 0
    assert data['token_type'] == 'Bearer'


def test_login_invalid_credentials(client_fixture):
    response = client_fixture.post("/login", json=TEST_INVALID_CREDENTIALS_JSON)
    assert response.status_code == 401
    assert json.loads(response.content)['detail']  == 'Username or/and password is invalid.'


def test_auth_schema_validation(client_fixture):
    response = client_fixture.post("/login", json=TEST_INVALID_AUTH_SCHEMA_JSON)

    assert response.status_code == 422
    assert json.loads(response.content)['detail'][0]['msg']  == 'field required'
    assert json.loads(response.content)['detail'][0]['type']  == 'value_error.missing'