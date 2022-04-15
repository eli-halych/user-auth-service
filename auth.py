import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import bcrypt

load_dotenv(".env")

SECRET_KEY = os.environ["SECRET_KEY"]

algorithm = "HS256"

class AuthHandler():

    def create_access_token(self, data, expires_delta):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=algorithm)
        return access_token

    def decode_access_token(self, data):
        try:
            token_data = jwt.decode(data, SECRET_KEY, algorithms=algorithm)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired.')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token.')
        return token_data

    def get_hashed_password(self, plain_text_password):
        # Hash a password for the first time
        #   (Using bcrypt, the salt is saved into the hash itself)
        return bcrypt.hashpw(plain_text_password, bcrypt.gensalt(12))

    def check_password(self, plain_text_password, hashed_password):
        # Check hashed password. Using bcrypt, the salt is saved into the hash itself
        return bcrypt.checkpw(plain_text_password, hashed_password)