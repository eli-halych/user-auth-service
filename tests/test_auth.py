from time import sleep
import pytest
from unittest import mock
import fastapi

from datetime import datetime
from datetime import timedelta

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from main import app, get_db
import auth
auth.SECRET_KEY = 'test_secret_key'

from auth import AuthHandler

auth_handler = AuthHandler()

TEST_PASSWORD = 'test_password'
TEST_WRONG_PASSWORD = 'wring_password'
TEST_DATA = dict(sub=1, username='test_username')
TEST_EXPIRATION_DELTA = timedelta(days=1)

def test_encode_decode_jwt():
    access_token = auth_handler.create_access_token(TEST_DATA, TEST_EXPIRATION_DELTA)
    data = auth_handler.decode_access_token(access_token)

    assert type(access_token) == str
    assert len(access_token) != 0

    assert data['sub'] == TEST_DATA['sub']
    assert data['username'] == TEST_DATA['username']

def test_decode_access_token_expired():
    access_token = auth_handler.create_access_token(TEST_DATA, timedelta(milliseconds=1))
    sleep(1)
    with pytest.raises(fastapi.exceptions.HTTPException) as exc_info:
        auth_handler.decode_access_token(access_token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == 'Signature has expired.'

def test_decode_access_invalid_token():
    access_token = auth_handler.create_access_token(TEST_DATA, TEST_EXPIRATION_DELTA)

    assert type(access_token) == str
    assert len(access_token) > 2

    invalid_token = access_token[:-2]

    with pytest.raises(fastapi.exceptions.HTTPException) as exc_info:
        auth_handler.decode_access_token(invalid_token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == 'Invalid token.'

def test_hash_unhash_password():
    hashed_password = auth_handler.get_hashed_password(TEST_PASSWORD)
    match = auth_handler.check_password(TEST_PASSWORD, hashed_password)
    assert match

def test_hash_unhash_password():
    hashed_password = auth_handler.get_hashed_password(TEST_PASSWORD)
    match = auth_handler.check_password(TEST_WRONG_PASSWORD, hashed_password)
    assert not match
