from fastapi import HTTPException
import logging
from sqlalchemy.orm import Session
from models import User as ModelUser
from schemas import UserAuthData as UserAuthSchema, UserCreateDB as UserCreateSchema
from auth import AuthHandler
from sqlalchemy.exc import IntegrityError
from datetime import timedelta

auth_handler = AuthHandler()


def create_user(db: Session, user: UserCreateSchema) -> dict:
    """Create a user entry in the database.

    Args:
        db (Session): database session.
        user (UserCreateSchema): user schema object with registration attributes.

    Raises:
        HTTPException: 409 when kdatabase experienced an error.

    Returns:
        dict: successul operation message.
    """
    logging.info("Start creation.")

    hashed_password = auth_handler.get_hashed_password(user.password)
    logging.info("Hashed password.")
    try:
        db_user = ModelUser(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            password=hashed_password,
        )
        db.add(db_user)
        db.commit()
        logging.info("Created a entry in the database.")
    except IntegrityError as exc:
        code = 409
        msg = str(exc)
        logging.error("Operation was not successful.")
        logging.debug(msg)
        raise HTTPException(status_code=code, detail=msg)

    response = dict(msg=f"User {user.username} successfully created.")

    return response


def remove_user(db: Session, authorization: str) -> dict:
    """Remove user entry from the database.

    Args:
        db (Session): database session.
        authorization (str): JWT token.

    Raises:
        HTTPException: 409 when database experienced an error.

    Returns:
        dict: successul operation message.
    """
    logging.info("Start removal.")

    access_token = authorization

    payload = auth_handler.decode_access_token(access_token)

    user_id = get_user_id(payload)

    user = db.query(ModelUser).filter(ModelUser.id == user_id).first()

    try:
        user_exists(user)

        db.delete(user)
        db.commit()
        logging.info("Removal successful")
        logging.debug(f"User `{user.username}` deleted.")
    except IntegrityError as exc:
        code = 409
        msg = str(exc)
        logging.error("Operation was not successful.")
        logging.debug(msg)
        raise HTTPException(status_code=code, detail=msg)

    response = dict(msg=f"User {user.username} was successfully deleted.")

    return response


def update_user(db: Session, authorization: str, data: dict) -> dict:
    """Update user entry in the database with provided attribute values.

    Args:
        db (Session): database session.
        authorization (str): JWT token.
        data (dict): user attribute values to be applied to an entry in the database.

    Raises:
        HTTPException: 422 when a provided attrinute doesn't exist in the database table.
        HTTPException: 409 when database experienced an error.

    Returns:
        dict: successul operation message.
    """
    logging.info("Start updating.")

    access_token = authorization

    logging.info("Extracted JWT token type and encoded data.")

    payload = auth_handler.decode_access_token(access_token)

    user_id = get_user_id(payload)

    user = db.query(ModelUser).filter(ModelUser.id == user_id).first()

    user_exists(user)

    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)
        else:
            code = 422
            msg = "Error while updating user's data."
            logging.error("An attribute name to be updated doesn't exist.")
            logging.debug(f"`{key}` attribute doesn't exist in the database.")
            raise HTTPException(status_code=code, detail=msg)

    try:
        db.commit()
        logging.info("User updated.")
    except IntegrityError as exc:
        code = 409
        msg = str(exc)
        logging.error("Operation was not successful.")
        logging.debug(msg)
        raise HTTPException(status_code=code, detail=msg)

    response = dict(msg=f"User {user.username} was successfully updated.")

    return response


def login(db: Session, auth_data: UserAuthSchema) -> dict:
    """Login using username nad password.

    Args:
        db (Session): database session.
        auth_data (UserAuthSchema): login and password.

    Raises:
        HTTPException: 401 when user password is incorrect.

    Returns:
        dict: successul operation message.
    """
    logging.info("Start logging in.")

    user = db.query(ModelUser).filter(ModelUser.username == auth_data.username).first()

    user_exists(user)

    if not auth_handler.check_password(auth_data.password, user.password):
        code = 401
        msg = "Username or/and password is invalid."
        logging.error(msg)
        logging.debug("Password is invalid.")
        raise HTTPException(status_code=code, detail=msg)

    payload = dict(sub=user.id, username=user.username)

    token = auth_handler.create_access_token(
        data=payload, expires_delta=timedelta(days=1)
    )

    logging.info("Logging successful.")

    response = dict(access_token=token, token_type="Bearer")

    return response


def user_exists(user: ModelUser) -> None:
    """Checks whether exists.

    Args:
        user (ModelUser): user ORM object.

    Raises:
        HTTPException: 403 when user doesn't exist.
    """
    if not user:
        code = 403
        msg = "Access forbidden."
        logging.error("Invalid Authorization token.")
        raise HTTPException(status_code=code, detail=msg)


def get_user_id(payload: dict) -> int:
    """Extracts user ID from JWT payload.

    Args:
        payload (dict): JWT payload.

    Raises:
        HTTPException: 401 when there's no user ID in the payload.

    Returns:
        int: user ID.
    """
    if "sub" in payload:
        user_id = payload["sub"]
    else:
        code = 401
        msg = "Authorization failed."
        logging.error("JWT token has invalid payload.")
        logging.debug("`sub` attribute is missing in JWT payload.")
        raise HTTPException(status_code=code, detail=msg)
    return user_id
