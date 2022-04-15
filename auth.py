import logging
import os
from datetime import datetime

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException
import bcrypt

load_dotenv(".env")

SECRET_KEY = os.environ["SECRET_KEY"]

ALGORITHM = "HS256"

class AuthHandler():

    def create_access_token(self, data, expires_delta):
        logging.info('Start encoding JWT token.')

        to_encode = data.copy()

        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        logging.debug(f'Set expiration date in {expires_delta}.')

        access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logging.info('Successfully encoded JWT data.')
        return access_token

    def decode_access_token(self, data):
        try:
            token_data = jwt.decode(data, SECRET_KEY, algorithms=ALGORITHM)
            logging.info('Decoded JWT token successfully.')
        except jwt.ExpiredSignatureError:
            msg = 'Signature has expired.'
            code = 401

            logging.error(msg + ' ' + f'Status: {code}')
            raise HTTPException(status_code=code, detail=msg)
        except jwt.InvalidTokenError:
            msg = 'Invalid token.'
            code = 401

            logging.error(msg + ' ' + f'Status: {code}')
            raise HTTPException(status_code=code, detail=msg)
        return token_data

    def get_hashed_password(self, plain_text_password):
        # Hash a password for the first time
        #   (Using bcrypt, the salt is saved into the hash itself)
        logging.info('Start hashing password.')
        hash = bcrypt.hashpw(plain_text_password, bcrypt.gensalt(12))
        logging.info('Finish hashing password.')
        return hash

    def check_password(self, plain_text_password, hashed_password):
        # Check hashed password. Using bcrypt, the salt is saved into the hash itself
        valid = bcrypt.checkpw(plain_text_password, hashed_password)
        logging.debug(f'Password is valid: {valid}')
        return valid