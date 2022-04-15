import pytest
import copy
from unittest.mock import MagicMock
from fastapi.testclient import TestClient


import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, get_db

def override_get_db():
    try:
        db = MagicMock()
        db.session.add.return_value = True
        db.session.commit.return_value = True
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

CLIENT = TestClient(app)

TEST_USER_JSON = {
    "username": "test_username",
    "password": "test_password",
    "first_name": "test_first_name",
    "last_name": "test_last_name"
}

def test_signup():
    response = CLIENT.post("/signup", json=TEST_USER_JSON)

    assert response.status_code == 201
    assert response.json() == {"msg": f"User {TEST_USER_JSON['username']} successfully created."}


def test_signup_missing_attribute():
    corrupt_json = copy.deepcopy(TEST_USER_JSON)
    del corrupt_json["last_name"]

    response = CLIENT.post("/signup", json=corrupt_json)

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'field required'
    assert response.json()['detail'][0]['type'] == 'value_error.missing'

