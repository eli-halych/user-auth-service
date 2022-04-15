import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, get_db
from auth import AuthHandler

auth_handler = AuthHandler()

TEST_CREDENTIALS_JSON = {
    "username": "test_username",
    "password": "test_password"
}

MOCK_USER_OBJ = MagicMock(
    id=1,
    username=TEST_CREDENTIALS_JSON['username'],
    password=auth_handler.get_hashed_password(TEST_CREDENTIALS_JSON['password'])
    )

@pytest.fixture
def mock_user_obj_fixture():
    return MOCK_USER_OBJ

@pytest.fixture
def client_fixture():
    def override_get_db():
        try:
            db = MagicMock()
            db.query.return_value.filter.return_value.first.return_value = MOCK_USER_OBJ
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def client_fixture_none():
    def override_get_db():
        try:
            db = MagicMock()
            db.query.return_value.filter.return_value.first.return_value = None
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)