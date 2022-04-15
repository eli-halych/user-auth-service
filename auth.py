import logging
import os
import datetime

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException
import bcrypt

load_dotenv(".env")

SECRET_KEY = os.environ["SECRET_KEY"]

ALGORITHM = "HS256"


class AuthHandler:
    """Handler of JWT and password hashing logic."""

    def create_access_token(self, data: dict, expires_delta: datetime.timedelta) -> str:
        """Encode data into a JWT token.

        Args:
            data (dict): Data containing sub as user ID and username.
            expires_delta (datetime.timedelta): time in which the token should expire.

        Returns:
            str: JWT token.
        """
        logging.info("Start encoding JWT token.")

        to_encode = data.copy()

        expire = datetime.datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        logging.debug(f"Set expiration date in {expires_delta}.")

        access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logging.info("Successfully encoded JWT data.")
        return access_token

    def decode_access_token(self, token: str) -> dict:
        """Decodes JWT into data.

        Args:
            token (str): JWT token.

        Raises:
            HTTPException: 401 when signature of JWT is expired.
            HTTPException: 401 when JWT is invalid.

        Returns:
            dict: decoded payload.
        """
        try:
            token_data = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            logging.info("Decoded JWT token successfully.")
        except jwt.ExpiredSignatureError:
            msg = "Signature has expired."
            code = 401

            logging.error(msg + " " + f"Status: {code}")
            raise HTTPException(status_code=code, detail=msg)
        except jwt.InvalidTokenError:
            msg = "Invalid token."
            code = 401

            logging.error(msg + " " + f"Status: {code}")
            raise HTTPException(status_code=code, detail=msg)
        return token_data

    def get_hashed_password(self, plain_text_password: str) -> str:
        """Hash a password string. The salt is saved into the hash itself.

        Args:
            plain_text_password (str): plaintext password.

        Returns:
            str: hashed password.
        """
        logging.info("Start hashing password.")
        hash = bcrypt.hashpw(plain_text_password, bcrypt.gensalt(12))
        logging.info("Finish hashing password.")
        return hash

    def check_password(self, plain_text_password: str, hashed_password: str) -> bool:
        """Verify whether plaintext password matches hashed password.

        Args:
            plain_text_password (str): plaintext password.
            hashed_password (str): hashed password.

        Returns:
            bool: whether passwords match.
        """
        valid = bcrypt.checkpw(plain_text_password, hashed_password)
        logging.debug(f"Password is valid: {valid}")
        return valid
