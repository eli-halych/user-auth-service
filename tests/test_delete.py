import pytest
import json
from datetime import timedelta

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import AuthHandler


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

TEST_DATA_JWT = dict(sub=1, username='test_username')
TEST_DATA_JWT_NO_SUB = dict(username='test_username')

TEST_EXPIRATION_DELTA = timedelta(days=1)

TEST_JWT_HEADER = auth_handler.create_access_token(TEST_DATA_JWT, TEST_EXPIRATION_DELTA)
TEST_TOKEN_NO_SUB = auth_handler.create_access_token(TEST_DATA_JWT_NO_SUB, TEST_EXPIRATION_DELTA)

def test_missing_sub_jwt(client_fixture):

    response = client_fixture.delete(
        "/delete",
        headers={
            "Authorization": f"Bearer {TEST_TOKEN_NO_SUB}"
            })

    assert response.status_code == 401
    assert json.loads(response.content)['detail']  == 'Authorization failed.'

def test_missing_user(client_fixture_none):

    response = client_fixture_none.delete(
        "/delete",
        json=TEST_DATA_JSON,
        headers={
            "Authorization": f"Bearer {TEST_JWT_HEADER}"
            })

    assert response.status_code == 403
    assert json.loads(response.content)['detail']  == 'Access forbidden.'
