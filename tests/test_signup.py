import pytest
import copy

TEST_USER_JSON = {
    "username": "test_username",
    "password": "test_password",
    "first_name": "test_first_name",
    "last_name": "test_last_name"
}

def test_signup(client_fixture):
    response = client_fixture.post("/signup", json=TEST_USER_JSON)

    assert response.status_code == 201
    assert response.json() == {"msg": f"User {TEST_USER_JSON['username']} successfully created."}


def test_signup_missing_attribute(client_fixture):
    corrupt_json = copy.deepcopy(TEST_USER_JSON)
    del corrupt_json["last_name"]

    response = client_fixture.post("/signup", json=corrupt_json)

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'field required'
    assert response.json()['detail'][0]['type'] == 'value_error.missing'

